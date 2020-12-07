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
    analyzer={  'servicioIndex':None, 
                'companias':None,
                'taxiIndex':None
            }
    analyzer['servicioIndex']=lt.newList('SINGLE_LINKED',compareIds)

    analyzer['companias']=om.newMap(omaptype='RBT',comparefunction=compareServicio)
    analyzer['taxiIndex']=om.newMap(omaptype='RBT',comparefunction=compareTaxi)
         
    return analyzer
 

# Funciones para agregar informacion al grafo

def addService(analyzer, service):

    try:
        lt.addLast(analyzer['servicioIndex'],service)
        #updateServiceIndex(analyzer['servicioIndex'], service)
        companies = service['company'].split(";")  # Se obtienen las companias
        for compania in companies:
            addSerCompany(analyzer, compania.strip(), service)
            
        taxiss = service['taxi_id'].split(";")  # Se obtienen las companias
        for taxi in taxiss:
            addSerTaxi(analyzer, taxi.strip(), service)


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

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

def addMovie(catalogo,movie):
    """
    Esta funcion adiciona un pelicula a la lista de movie,
    adicionalmente lo guarda en un Map usando como llave su production_companies_I.
    """
    lt.addLast(catalogo['movies'], movie)



def newPelicula(name):
    """
    Crea una nueva estructura para modelar los pelicuales de un productora
    y su promedio de ratings
    """
    productora = {'production_companies': "", "movies": None,  "average_rating": 0}
    productora['production_companies'] = name
    productora['movies'] = lt.newList('SINGLE_LINKED', comparePeliculasByName)
    return productora


def newProd(name):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings
    """
    company= {'production_companies': "", "movies": None,  "average_rating": 0}
    company['production_companies'] = name
    company['movies'] = lt.newList('SINGLE_LINKED', compareprodComs)    
    return company


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



#pretty sure this one is referenced by nothing and can be deleted
#dont delete without validating it is in fact useless


def addProductionCompany(catalog, companyName, movie):

    nombrePelicula = catalog['original_title']
    print ("")
    print ("\n", nombrePelicula)
    input (" Clic para continuar despues de nombre pelicula...")

    #existePelicula = mp.contains(nombrePelicula, companyName)
    existePelicula = mp.contains(catalog['production_companies_ID'], companyName)

    if existePelicula:
        entry = mp.get(catalog['production_companies_ID'], companyName)
        nombrePelicula = me.getValue(entry)
    else:
        mp.put(catalog['production_companies_ID'], companyName, nombrePelicula)

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





def addDirector(catalog, director):
#each row builds a catal;ogue entry from csv2

#this row corresponds to the rows in the CSV
    newdic = newDirector(director['director_name'], director['actor1_name'], director['id'])

#these rows are the names assigned in the catalogue. note first item in brackest is the assigned name of the new catalogue, second one is the reference matching CSV and first line
    mp.put(catalog['directors'], director['director_name'], newdic)
    mp.put(catalog['actors1'], director['actor1_name'], newdic)
    mp.put(catalog['movieIds'], director['id'], newdic)




def newDirector(director, actor1, id):

    casting= {'director': '',
            'actor1': '',
            'movieId': '',
            'total_movies': 0,
            'movies': None,
            'count': 0.0}
    casting['director'] = director
    casting['actor1'] = actor1
    casting['movieIds'] = id
    casting['movies'] = lt.newList()
    return casting





# ==============================
# Funciones de adicion
# ==============================


def addId(catalogo1,id):

    lt.addLast(catalogo1['id'], id)



def addProdCompany(catalog, prodcom, movie):

    companies = catalog['production_companies']
    existincompany = mp.contains(companies, prodcom)
    if existincompany:
        entry = mp.get(companies, prodcom)
        companyadd = me.getValue(entry)
    else:
        companyadd = newProd(prodcom)
        mp.put(companies, prodcom, companyadd)
    lt.addLast(companyadd['movies'], movie)


def addGenre(catalog, genre, movie):

    newgenre = catalog['genres']
    existgenre = mp.contains(newgenre, genre)
    if existgenre:
        entry = mp.get(newgenre, genre)
        genreToAdd = me.getValue(entry)
    else:
        genreToAdd = newProd(genre)
        mp.put(newgenre, genre, genreToAdd)
    lt.addLast(genreToAdd['movies'], movie)



def addDirectorId(catalog1, director, id):

    moviesID = catalog1['directors']
    existinID = mp.contains(moviesID, director)
    if existinID:
        entry = mp.get(moviesID, director)
        movieAdd = me.getValue(entry)
    else:
        movieAdd= newMoviedirect(director)
        mp.put(moviesID, director, movieAdd)
    lt.addLast(movieAdd['id'], id)




def newMoviedirect(nameDirector):
    """
    Crea una nueva estructura para modelar los libros de un autor
    y su promedio de ratings
    """
    directorCast= {'director': "","id":None, "movies": None,  "average_rating": 0}
    directorCast['director'] = nameDirector
    directorCast['id'] = lt.newList('SINGLE_LINKED', compareprodComsCast)    
    directorCast['movies'] = lt.newList('SINGLE_LINKED', compareprodComsCast)    
    return directorCast


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

