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
recursionLimit = 20000000000000000000000000000000000000000

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
    
    #servicio=lt.getElement(cont1['servicioIndex'],0)
    #print (servicio['taxi_id'])

    
def optionThree():
    print (" ")
    #mapaServicios=cont['servicioIndex']
    
    #print ("Cantidad de companias que prestan servicios: ", om.size(mapaServicios))
    print ("Cantidad de servicios prestados: ", lt.size(cont['servicioIndex']))
    print ("  ") 
    print ("Cantidad de companias: ", om.size(cont['companias']))  
    print ("  ")
    print ("Cantidad de taxis: ", om.size(cont['taxiIndex'])) 
    print ("")

    numM = int(input ("Cuantas Companias a consultar con sus Taxis: " ))
    ordenar=model.compOrdTaxis (cont)
    print ("")
    print ("*********************************************************")
    print ("**    Companias con su respectiva cantidad de Taxis    **")
    print ("*********************************************************")
    for i in range(1,numM+1):
        print(i, " : ", lt.getElement(ordenar,i)[1], ": [ ", lt.getElement(ordenar,i)[0], " ]")
    print ("")
    print ("*********************************************************")
    print ("")
    input("Clic para continuar.....")
    print ("")

    numN = int(input ("Cuantas Companias a consultar con sus Servicios: " ))
    ordenarS=model.compOrdServicios (cont)
    print ("")
    print ("*********************************************************")
    print ("**    Companias con su respectiva cantidad de Taxis    **")
    print ("*********************************************************")
    for i in range(1,numN+1):
        print(i, ": ", lt.getElement(ordenarS,i)[1], ": [ ", lt.getElement(ordenarS,i)[0], " ]")
    print ("")
    print ("*********************************************************")
    print ("")
    input("Clic para continuar.....")
    print ("")


def optionFour():
     pass
    

def optionFive():

    inicio="7:30"                 #input("Digite la hora en la que quiere iniciar el viaje: ")
    final="11:30"                  #input("Digite la hora en la que quiere termina el viaje: ")

    x=inicio.split(":")
    y=final.split(':')


    print("\nCargando información ....")
    tFile=input ("Digite S (Small), M (Medium) o L (Large), para cargar archivo [S, M o L]: " )
    tFile=tFile.upper()
    if (tFile=="S"): 
        servicefile = 'taxi-trips-wrvz-psew-subset-small.csv'
    elif (tFile=="M"):
        servicefile = 'taxi-trips-wrvz-psew-subset-medium.csv'
    else:
        servicefile = 'taxi-trips-wrvz-psew-subset-large.csv'

    controller.loadGraph(graph,servicefile, x, y)


    x=controller.minimumCostPaths(graph, 32.0)
    y=controller.minimumCostPath(x, 42.0)
    z=controller.pathto(x, 42.0)


    print(y)
    print('******************************')
    print(z)
    
    #print(gr.vertices(graph["grafo"]))
    #print(gr.numVertices(graph["grafo"]))
    #print(gr.numEdges(graph["grafo"]))

    

    """
    arcos=gr.edges(graph["grafo"])
    i=0
    while i <= lt.size(arcos):
        print(lt.getElement(arcos,i))
        i+=1
    print(lt.size(arcos))

    #print(graph["grafo"])
    """
    

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
        graph= controller.init_graph()

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