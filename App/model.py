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
                'CompaniasConTaxis':None
            }
    analyzer['servicioIndex']=lt.newList('SINGLE_LINKED',compareIds)

    analyzer['companias']=om.newMap(omaptype='RBT',comparefunction=compareServicio)
    analyzer['taxiIndex']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)
    analyzer['CompaniasConTaxis']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)    

    return analyzer
 

# Funciones otras

def compOrdTaxis (analyzer):
    ordenados = lt.newList('ARRAY_LIST')
    recorrer = om.keySet(analyzer["CompaniasConTaxis"])

    for i in range(lt.size(recorrer)):
        lt.addLast(ordenados,(om.size(om.get(analyzer["CompaniasConTaxis"],lt.getElement(recorrer,i))['value']),lt.getElement(recorrer,i)))

    #qs.quickSort(ordenados,compareCustom)
    #inSort.insertionSort(ordenados,lessfunction)
    """
    size = lt.size(ordenados)
    pos1 = 1
    while pos1 <= size:
        pos2 = pos1
        while (pos2 > 1) and (lt.getElement(ordenados, pos2)< lt.getElement(ordenados, pos2-1)):
            lt.exchange(ordenados, pos2, pos2-1)
            pos2 -= 1
        pos1 += 1
    """
    return ordenados


def lessfunction (elemento1, elemento2):
    if elemento1<elemento2:
      return True
    return False

# Funcion para la camtidad de companias 

def addCompaniaTaxi(analyzer, compania, idTaxi):
    
    if om.contains(analyzer['CompaniasConTaxis'],compania):
        temp = om.get(analyzer['CompaniasConTaxis'],compania)['value']
        om.put(temp,idTaxi,0)
    else:
        temp = om.newMap(omaptype='RBT',comparefunction=compareTaxi)
        om.put(temp,idTaxi,0)
        om.put(analyzer['CompaniasConTaxis'],compania,temp)

    return analyzer


def addServiceCompany(analyzer,service):
    if(om.contains(analyzer["companias"],service['company'])):
        lt.addLast(om.get(analyzer['companias'],service['company'])['value'],service)
    else:
        add = lt.newList('SINGLE_LINKED')
        lt.addLast(add,service)
        om.put(analyzer["companias"],service["company"],add)


def addService(analyzer, service):

    
    addCompaniaTaxi(analyzer,service['company'],service['taxi_id'])

    lt.addLast(analyzer['servicioIndex'],service)
    
    addServiceCompany(analyzer, service)
        
    om.put(analyzer['taxiIndex'],service['taxi_id'],0)

    return analyzer
    
def updateServiceIndex(map, servicio):
    """
    Se toma cada companiay se busca si ya existe en el arbol. Si es asi, se adiciona a su lista de servicios
    y se actualiza el indice de servicios.
    Si no se encuentra creado un nodo para la compania en el arbol
    se crea y se actualiza el indice de tipos de servicios
    """
    companyName= servicio['company']
    ocurreService = servicio['trip_id']
    ocurreTaxi = servicio['taxi_id']
    
    entry = om.get(map, ocurreService)

    if entry is None:
        #datentry = newDataEntry(servicio)
        om.put(map, companyName, ocurreService)
    else:
        datentry = me.getValue(entry)
    addServiceIndex(datentry, servicio)
    return map






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






#################################################    
#### Adiciona una servicios a una compania   #### 
#################################################  

def addSerCompany(catalog, compania, service):
    
    companias = catalog['companias']
    existincompany = om.contains(companias, compania)
    if existincompany:
        entry = om.get(companias , compania)
        serviceAdd = me.getValue(entry)
    else:
        serviceAdd = newServicio(compania)
        om.put(companias , compania, serviceAdd)
    lt.addLast(serviceAdd['trip_id'], service)
    #print (lt.size (serviceAdd['trip_id']))
    
def newServicio(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings
    """
    servicio= {'company': "", "trip_id": None,  "taxi_id": None}
    servicio['company'] = name
    servicio['trip_id'] = lt.newList('SINGLE_LINKED', compareprodComs)      
    return servicio

def addSerTaxi(catalog, taxi_id, service):
    taxis = catalog['taxiIndex']
    existincompany = om.contains(taxis, taxi_id)
    if existincompany:
        entry = om.get(taxis , taxi_id)
        serviceAdd = me.getValue(entry)
    else:
        serviceAdd = newServicioT(taxi_id)
        om.put(taxis , taxi_id, serviceAdd)
    lt.addLast(serviceAdd['trip_id'], service)
    #print (lt.size (serviceAdd['trip_id']))
    

def newServicioT(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings
    """
    servicio= {'company': "", "trip_id": None,  "taxi_id": None}
    servicio['taxi_id'] = name
    servicio['trip_id'] = lt.newList('SINGLE_LINKED', compareprodComs)    
     
    return servicio











# ==============================
# Funciones de adicion
# ==============================




# ==============================
# Funciones de Comparacion
# ==============================
def compareMovieIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
        

def comparePeliculasByName(keyname, pelicula):
    """
    Compara dos nombres de pelicula. El primero es una cadena
    y el segundo un entry de un map
    """
    pelhentry = me.getKey(pelicula)
    if (keyname == pelhentry):
        return 0
    elif (keyname > pelhentry):
        return 1
    else:
        return -1


def compareproductionCompanies(keyname, company):
    authentry = me.getKey(company)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1

def compareActors(keyname, actor):
    authentry = me.getKey(actor)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1


def compareprodComsCast(keyname, directorCat):

    authentry = me.getKey(directorCat)
    if (keyname == authentry):
        return 0
    elif (keyname > authentry):
        return 1
    else:
        return -1



def compareDirectorIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1



def moviesSize(catalog):
    return lt.size(catalog['movies'])


def getMoviesProdCompany (cat, company):
    compania = mp.get(cat['production_companies'], company)
    if compania:
        return me.getValue(compania)
    return None



def getMoviesByDirector(catalog, nameInput):
    #this function searches with the name defined in the catalogue, not the name in the CS

    directorsearched = mp.get(catalog['directors'], nameInput)
    if directorsearched:
        return me.getValue(directorsearched)
    return None



def getMoviesGenre(cat, genre):
    genreresult = mp.get(cat['genres'], genre)
    if genreresult:
        return me.getValue(genreresult)
    return None







# ==============================
# Funciones de consulta
# ==============================



    

# ==============================
# Funciones Helper
# ==============================




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

def compareCustom(val1,val2):
    if(val1[0] > val2[0]):
        return -1
    elif(val1[0] < val2[0]):
        return 0
    return compareIds(val1[1],val2[1])

