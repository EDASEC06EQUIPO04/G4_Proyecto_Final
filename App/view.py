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
recursionLimit = 200000


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
    servicefile = 'taxi-trips-wrvz-psew-subset-small.csv'
    #elif (tFile=="M"):
    #    servicefile = 'taxi-trips-wrvz-psew-subset-medium.csv'
    #else:
    #    servicefile = 'taxi-trips-wrvz-psew-subset-large.csv'
    #cont1=controller.loadServices(cont,servicefile,graph)

    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print (gr.vertices(cont['connections']))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


    
def optionThree():
    #this thing should define origin
    controller.minimumCostPaths(cont, initialStation)

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
        #cont = controller.init()



        cont= controller.init_graph()
        #print (graph)

    elif int(inputs) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: ",  round (executiontime,2))

    elif int(inputs) == 3:
        msg = "Punto de partida: (ej 8) "
        initialStation = input(msg)
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