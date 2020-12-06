"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
from os import X_OK
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as e
from DISClib.DataStructures import mapentry as me

assert config
"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzer():

    # creo la lista para almacenar todos los companias, esto es cada fila del excel con sus 23 campos
    # crea un Cataolo de Analyzer, una lista para los Companias y una Mapa Ordenado los servicios y taxis
    analyzer={ 'companias':None,
               'servicioIndex':None,
               'taxiIndex':None
            }
    analyzer['companias']=lt.newList('SINGLE_LINKED',compareIds)

    analyzer['servicioIndex']=om.newMap(omaptype='RBT',comparefunction=compareServicio)
    analyzer['taxiIndex']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)
         
    return analyzer
 

# Funciones para agregar informacion al grafo

def addCompany(analyzer, company):

    try:
        lt.addLast(analyzer['companias'],company)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
            
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, los IdBikes que estuvieron los visitaron
    """
    entry = m.get(analyzer['stops'], service['end station id'])
    lstroutes = lt.newList(cmpfunction=compareroutes)
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['bikeid'])
        m.put(analyzer['stops'], service['end station id'], lstroutes)
    else:
        #lstroutes = entry['value']
        info = service['bikeid']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
            m.put(analyzer['stops'], service['end station id'], lstroutes)

    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['stops'])
    stopsiterator = it.newIterator(lststops)
    while it.hasNext(stopsiterator):
        key = it.next(stopsiterator)
        lstroutes = m.get(analyzer['stops'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    else: #actualizacion del peso de los arcos
        # Quiero poner el condicional siguiente para  que me cargue solo los que nos sean iguales..
        if origin == destination:
            #print("-------- " ,origin, " --> " , destination, ", Nodos iguales")
            pass
        else:
            #print("@@@@@@@@ " , origin, " --> " , destination, ", cargando info..")
            e.updateAverageWeight (edge,distance)
        #Aqui imprimo la imforacion de los arcos y el contador
        #print ("Arco update " + str(origin) + "-->" + str(destination) + "   count: " + str(edge['count']))
    return analyzer

# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])

    
    return scc.connectedComponents(analyzer['components'])


#def connectedwithID(analyzer, id1,id2):
#    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
# #    return scc.stronglyConnected(analyzer['components'], id1, id2)




def numSCC(analyzer):
    sc = scc.KosarajuSCC(analyzer['connections'])
    """
    print (sc['idscc'])
    input ("Clic para continuar .....")
    """
    print ("Reverse: ", sc['marked']) 
    input ("Clic para continuar .....")
    print ("Componentes conectados: ", sc['components'])
    input ("Clic para continuar .....")
    """
    print ("Reverse: ", scc.sccCount(sc))

    input ("Clic para continuar .....")
    """
    return scc.connectedComponents(sc)

def connectedwithID(analyzer, id1,id2):
    sc = scc.KosarajuSCC(analyzer['connections'])
    #print (scc.stronglyConnected  (sc,id1,id2))
    #print (sc['idscc'])
    #print (m.get(sc['idscc'],id1))
    #print (m.get(sc['idscc'],id2))
    #input ("idscc impreso")
    #print (scc.stronglyConnected  (analyzer,id1,id2))


    return scc.stronglyConnected  (sc,id1,id2)
    

def connectedwithID_1(analyzer, id1):
    sc = scc.KosarajuSCC(analyzer['connections'])
    #print (sc['idscc'])
    #print (sc)
    #input ("clic este es SCC.....")
    return sc
    


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['tripduration'] == '':
        service['tripduration'] = 0
    if lastservice['tripduration'] == '':
        lastservice['tripduration'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    #name = service['end station id'] + '-'
    #name = name + service['start station id']
    name = service['start station id']
    return name

def formatVertey(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    #name = service['end station id'] + '-'
    #name = name + service['start station id']
    name = service['end station id']
    return name


# ==============================
# Funciones de Comparacion
# ==============================

def compareServicio (servicioID1,servicioID2):
    
    # compara los crimenes
    if (servicioID1==servicioID2):
        return 0
    elif (servicioID1>servicioID2):
        return 1
    else:
        return -1

def compareTaxi (taxiID1,taxiID2):
    
    # compara los crimenes
    if (taxiID1==taxiID2):
        return 0
    elif (taxiID1>taxiID2):
        return 1
    else:
        return -1

def compareIds (id1,id2):
    
    # compara los crimenes
    if (id1==id2):
        return 0
    elif (id1>id2):
        return 1
    else:
        return -1

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
