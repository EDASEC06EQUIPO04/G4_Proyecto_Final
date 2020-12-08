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



import sys
import config
from App import controller
from App import model
from DISClib.ADT import stack
import timeit
assert config
from DISClib.Algorithms.Graphs import scc
from DISClib.ADT.graph import gr
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.Algorithms.Graphs import dfs
from DISClib.DataStructures import edge as e
from DISClib.ADT import orderedmap as om

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


initialStation = None
recursionLimit = 20000


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("****************************************************************************************")
    print("****************************  RETO FINAL  TAXIS EN CHICHAGO      ***********************")
    print("****************************************************************************************")
    print(" ")
    print("[ 1 ] Inicializar Analizador")
    print("[ 2 ] Cargar información taxis de chicago")
    print("[ 3 ] Req 1. Requerimientos de informacion de companias y taxis")
    print("[ 4 ] Req 2. Sistemas de puntos y permios a Taxis")
    print("[ 5 ] Req 3. Consulta del mejor horario en Taxi entre  && Community areas && ")
    print("[ 0 ] Salir")
    print ("")
    print("****************************************************************************************")


def optionTwo():
    print("\nCargando información ....")
    tFile=input ("Digite S (Small), M (Medium) o L (Large), para cargar archivo [S, M o L]: " )
    tFile=tFile.upper()
    if (tFile=="S"): 
        servicefile = 'taxi-trips-wrvz-psew-subset-small.csv'
    elif (tFile=="M"):
        servicefile = 'taxi-trips-wrvz-psew-subset-medium.csv'
    else:
        servicefile = 'taxi-trips-wrvz-psew-subset-large.csv'
    cont1=controller.loadServices(cont,servicefile)
    
    servicio=lt.getElement(cont1['servicioIndex'],0)
    print (servicio['taxi_id'])




    
def optionThree():
    print (" ")
    #mapaServicios=cont['servicioIndex']
    
    #print ("Cantidad de companias que prestan servicios: ", om.size(mapaServicios))
    print ("Cantidad de servicios prestados: ", lt.size(cont['servicioIndex']))
    print ("  ") 
    print ("Cantidad de companias: ", om.size(cont['companias']))  
    print ("  ")
    print ("Cantidad de taxis: ", om.size(cont['taxiIndex'])) 

    numM = int(input ("Digite el numero de companias a consultar: " ))
    ordenar=model.compOrdTaxis (cont)
    print ("")
    print ("*********************************************************")
    print ("**    Companias con su respectiva cantidad de Taxis    **")
    print ("*********************************************************")
    for i in range(0,numM):
        print(lt.getElement(ordenar,i))
    print ("")
    print ("*********************************************************")
    input("Clic para continuar")


    """
    print ("  ")   
    input ("" )
    print ("++++++++++++++++++++++++++Nombre de las companias ++++++++++++++++++++++++++++++++++++++++++") 
    print ("  ")
    print (om.keySet(cont['companias']))
    print ("  ")
    print ("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
    print ("   ")
    input ("")
    print ("++++++++++++++++++++++++++ Cantidad de serviios prestados +++++++++++++++++++++++++++++++++++++") 
    print ("  ")
    print (om.get(cont['companias'],'2733 - 74600 Benny Jona'))
    print ("  ")
    tam =(om.get(cont['companias'],'2733 - 74600 Benny Jona'))
    print ("La cantidad de servicios prestados por @@ 2733 - 74600 Benny Jona: ", tam.values())
    print ("  ")
    input (" Clic para ver a  continuacion servicios prestdos por el taxi")
    """        
    """
    print ("++++++++++++++++++++++++++ Cantidad de servicios prestados por el Taxi +++++++++++++++++++++++++++++++++++++") 
    print ("  ")
    print (om.get(cont['taxiIndex'],'47afa2ad8334a794871c5a7e9785925599304a77c3d9cc49dd7362dce26e0c44b5a262c342084cb82c1a61b3f46f06b7083b0e737f6655ec09ec8f44ff9c3cb8'))
    print ("  ")
    tam1 =(om.get(cont['taxiIndex'],'47afa2ad8334a794871c5a7e9785925599304a77c3d9cc49dd7362dce26e0c44b5a262c342084cb82c1a61b3f46f06b7083b0e737f6655ec09ec8f44ff9c3cb8'))
    print ("La cantidad de servicios prestados por el taxi @@ ", tam1.values())
    lista=lt.newList()
    lista=om.valueSet(cont['taxiIndex'])

    print ("+++++++++++++++++++++++")
    print (lt.getElement (lista,0))
    print ("+++++++++++++++++++++++")
    print ("La cantidad de taxis: " , lt.size (lista))
    
    #print ("Cantidad de companias que prestan servicios: ", om.keySet(mapaServicios))
   
    print ("")
    input ("Clic para conitnuar")
    """

def optionFour():
     pass
    

def optionFive():
    pass





"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar> ')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
        print (cont)

    elif int(inputs) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: ",  round (executiontime,2))

    elif int(inputs) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 4:
        
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 5:
        
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
