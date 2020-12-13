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


# ---------------------------------------------------------------
#                       Requerimiento dos (2)
# ---------------------------------------------------------------

# ---------------------------------------------------------------
#                       Requerimiento tres (3)
# ---------------------------------------------------------------


def newGraph():
        graph = {
                    'area': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        graph['area'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        graph['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)

        return graph
   



def addStopConnection(analyzer, lastservice, service):

    try:
        origin = formatVertex(lastservice)
        destination = formatVertex(service)
        cleanServiceDistance(lastservice, service)
        distance = float(service['trip_miles']) - float(lastservice['trip_miles'])
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def formatVertex(service):

    name = service['pickup_community_area']
    return name

def cleanServiceDistance(lastservice, service):

    if service['trip_miles'] == '':
        service['trip_miles'] = 0
    if lastservice['trip_miles'] == '':
        lastservice['trip_miles'] = 0

def addStop(analyzer, stopid):
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    else: 
        if origin == destination:
            pass
        else:
            e.updateAverageWeight (edge,distance)
    return analyzer

def addRouteStop(analyzer, service):

    entry = m.get(analyzer['area'], service['pickup_community_area'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        m.put(analyzer['area'], service['pickup_community_area'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer









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



















        
def add_community_area(graph, community_area):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(graph["grafo"], community_area):
        gr.insertVertex(graph["grafo"], community_area)
    return graph


def add_CA_Connection(graph, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(graph['grafo'], origin, destination)
    if edge is None:
        gr.addEdge(graph['grafo'], origin, destination, duration)
    else:
        prev_duration = float(e.weight(edge))
        duration += prev_duration
        e.updateAverageWeight(edge, duration)


def compare_community_areas(stop, keyvaluestop):
    stopcode = float(keyvaluestop['key'])
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1




        
# ==============================
# Funciones de adicion
# ==============================


# ==============================
# Funciones de Comparacion
# ==============================


# ==============================
# Funciones de consulta
# ==============================

    
def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer




# ==============================
# Funciones Helper
# ==============================




def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['area'])
    stopsiterator = it.newIterator(lststops)
    while it.hasNext(stopsiterator):
        key = it.next(stopsiterator)
        lstroutes = m.get(analyzer['area'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route



def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

