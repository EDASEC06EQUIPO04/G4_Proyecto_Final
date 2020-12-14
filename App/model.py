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
from DISClib.ADT import minpq as mp
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Algorithms.Sorting import insertionsort as inSort

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
    analyzer={  'servicioIndex':None, 
                'companias':None,
                'taxiIndex':None,
                'CompaniasConServicios':None,
                'CompaniasConTaxis':None
            }
    analyzer['servicioIndex']=lt.newList('SINGLE_LINKED',compareIds)

    analyzer['companias']=om.newMap(omaptype='RBT',comparefunction=compareServicio)
    analyzer['taxiIndex']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)
    analyzer['CompaniasConTaxis']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)
    analyzer['CompaniasConServicios']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)     

    return analyzer
 

# ---------------------------------------------------------------
#                       Requerimiento Uno (1)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
#                Requerimiento Uno (1) Funciones de Consulta
# ---------------------------------------------------------------

def compOrdTaxis (analyzer):
    # Funcion para recorrer las llaves del mapa analyzer["CompaniasConTaxis"]
    # usando una lista temporal, y realiazando un ordenamiento InsertionSort
    
    ordenados = lt.newList('ARRAY_LIST',compareIds)
    recorrer = om.keySet(analyzer["CompaniasConTaxis"])

    for i in range(lt.size(recorrer)):
        lt.addLast(ordenados,(om.size(om.get(analyzer["CompaniasConTaxis"],lt.getElement(recorrer,i))['value']),lt.getElement(recorrer,i)))
    #ordenados=qs.quickSort(ordenados,lessfunction) 
    size = lt.size(ordenados)
    pos1 = 1
    while pos1 <= size:
        pos2 = pos1
        while (pos2 > 1) and (lt.getElement(ordenados, pos2)[0]> lt.getElement(ordenados, pos2-1)[0]):
            lt.exchange(ordenados, pos2, pos2-1)
            pos2 -= 1
        pos1 += 1
    
    return ordenados

def compOrdServicios (analyzer):
    # Funcion para recorrer las llaves del mapa analyzer["CompaniasConServicios"]
    # usando una lista temporal, y realiazando un ordenamiento InsertionSort
    ordenados = lt.newList('ARRAY_LIST',compareIds)
    recorrer = om.keySet(analyzer["CompaniasConServicios"])

    for i in range(lt.size(recorrer)):
        lt.addLast(ordenados,(om.size(om.get(analyzer["CompaniasConServicios"],lt.getElement(recorrer,i))['value']),lt.getElement(recorrer,i)))
    #ordenados=qs.quickSort(ordenados,lessfunction)
       
    size = lt.size(ordenados)
    pos1 = 1
    while pos1 <= size:
        pos2 = pos1
        while (pos2 > 1) and (lt.getElement(ordenados, pos2)[0]> lt.getElement(ordenados, pos2-1)[0]):
            lt.exchange(ordenados, pos2, pos2-1)
            pos2 -= 1
        pos1 += 1
    
    return ordenados


def lessfunction (elemento1, elemento2):
    if elemento1<elemento2:
      return True
    return False

# ---------------------------------------------------------------
#   Requerimiento Uno (1) Funciones de Carga de Listas y Maps
# ---------------------------------------------------------------

def addService(analyzer, service): 
    addCompaniaTaxi(analyzer,service['company'],service['taxi_id'])
    addCompaniaServicio(analyzer,service['company'], service['trip_id'])
    lt.addLast(analyzer['servicioIndex'],service)
    addServiceCompany(analyzer, service)
    om.put(analyzer['taxiIndex'],service['taxi_id'],0)

    return analyzer

def addCompaniaTaxi(analyzer, compania, idTaxi):
    """
    Esta funcion carga la companias y mapa con los IdTaxis, permite contabilizar los  taxis 
    que estan inscritos en una Compania X de taxis.
    """
    if om.contains(analyzer['CompaniasConTaxis'],compania):
        temp = om.get(analyzer['CompaniasConTaxis'],compania)['value']
        om.put(temp,idTaxi,0)
    else:
        temp = om.newMap(omaptype='RBT',comparefunction=compareTaxi)
        om.put(temp,idTaxi,0)
        om.put(analyzer['CompaniasConTaxis'],compania,temp)
    return analyzer


def addCompaniaServicio(analyzer, compania, trip_id):
    """
    Esta funcion carga la companias y mapa con los IdTRip, permite contabilizar los servicios 
    prestados por una Compania X.
    """
    if om.contains(analyzer['CompaniasConServicios'],compania):
        temp = om.get(analyzer['CompaniasConServicios'],compania)['value']
        om.put(temp,trip_id,0)
    else:
        temp = om.newMap(omaptype='RBT',comparefunction=compareTaxi)
        om.put(temp,trip_id,0)
        om.put(analyzer['CompaniasConServicios'],compania,temp)

    return analyzer


def addServiceCompany(analyzer,service):
    if(om.contains(analyzer["companias"],service['company'])):
        lt.addLast(om.get(analyzer['companias'],service['company'])['value'],service)
    else:
        add = lt.newList('SINGLE_LINKED')
        lt.addLast(add,service)
        om.put(analyzer["companias"],service["company"],add)



def compareprodComs(keyname, company):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    authentry = me.getKey(company)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


# ---------------------------------------------------------------
#   Requerimiento Uno (1) Funciones de Comparacion
# ---------------------------------------------------------------

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

def compareCustom(val1,val2):
    if(val1[0] > val2[0]):
        return -1
    elif(val1[0] < val2[0]):
        return 0
    return compareIds(val1[1],val2[1])

# ---------------------------------------------------------------
#                       Requerimiento dos (2)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
#                       Requerimiento tres (3)
# ---------------------------------------------------------------


def newGraph():
        graph = {
                    'comunity_area': None,
                    'grafo': None,
                    'paths':None
                    }

        graph['comunity_area'] = m.newMap(numelements=1400,
                                     maptype='PROBING',
                                     comparefunction=compare_community_areas)

        graph['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1200,
                                              comparefunction=compare_community_areas)
        return graph
   


def addTrip(graph, service, inicio, final):

    if service["pickup_community_area"] == '':
        service["pickup_community_area"] = "-1.0"

    if service["dropoff_community_area"] == '':
        service["dropoff_community_area"] = "-1.0"

    if service["trip_seconds"] == '':
        service["trip_seconds"] = "-1.0"


    if service["trip_start_timestamp"] == '':
        service["trip_start_timestamp"] = "00:00:00.000"


    if service["trip_end_timestamp"] == '':
        service["trip_end_timestamp"] = "00:00:00.000"


    origin_community_area= float(service["pickup_community_area"])
    destination_community_area=float(service["dropoff_community_area"])
    duration=float(service["trip_seconds"])

    start= service["trip_start_timestamp"]
    end= service["trip_end_timestamp"]

    start_time = start[11:]
    end_time= end[11:]

    z=start_time.split(":")
    w=end_time.split(":")


    if (int(inicio[0]) <= int(z[0]) <= int(final[0])) and (int(inicio[0]) <= int(w[0]) <= int(final[0])):
        add_community_area(graph,origin_community_area)
        add_community_area(graph,destination_community_area)
        addConnection(graph, origin_community_area, destination_community_area, duration)
    

        
def add_community_area(graph, community_area):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(graph["grafo"], community_area):
        gr.insertVertex(graph["grafo"], community_area)
    return graph


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['grafo'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['grafo'], origin, destination, distance)

    else: 
        if origin == destination:
            pass
        else:
            e.updateAverageWeight (edge,distance)
    return analyzer


def compare_community_areas(stop, keyvaluestop):
    stopcode = float(keyvaluestop['key'])
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def disTo (search, vertex):
    answer = djk.distTo(search, vertex)
    print(answer)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['grafo'], initialStation)
    return analyzer


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def pathTo (analyzer, destination):

    pila=djk.pathTo(analyzer["paths"], destination)

    return pila