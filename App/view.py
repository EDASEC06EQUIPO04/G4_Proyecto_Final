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
#servicefile = '201801-1-citibike-tripdata.csv'
#servicefile2 = '201801-2-citibike-tripdata.csv'
#servicefile3 = '201801-3-citibike-tripdata.csv'
#servicefile4 = '201801-4-citibike-tripdata.csv'

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
    
    compania=lt.getElement(cont1['companias'],0)
    print (compania['taxi_id'])
    print ("Cantidad de servicios prestados: ", lt.size(cont['companias']))
    print ("")

    
    


def optionThree():
    sccA=controller.connectedComponents(cont)
    #print('El número de componentes conectados es: ' + str(controller.connectedComponents(cont)))
    print('El número de componentes conectados es: ' + str(sccA))
    input ("El argorimo de Kosaraju esta funcionando, esto es el scc.py")
    
    id1=input("Inserte Station ID_1: " )
    id2=input("Inserte Station ID_2: ")
    #TESTED WITH 
    #72 y 127, True
    #72 y 270
    scc2=(controller.connectedwithID(cont,id1,id2))
    print ("Estan ", id1, " y " , id2 , "fuertemente conectados: " , scc2) 
    input ("clic para continuar")

def stationRecursive (analyzer,stationc,time):
    print (stationc)
    input ("clic vertice que llegar parar a buscar adjacentes.......")
    station=str(stationc)
    time_u=time
    values=gr.adjacentEdges (analyzer,station)
    print (values)
    input ("estoy imprimiendo los adyacentes del vertice")

    return time_u

def optionFour():
    tiempoDisponible=int(input(" Cuanto minutos tienes disponible para la visita? " ))
    initialStation=input("Inserte el punto de partida Station ID, Ejemplo 72, 79, 82, 83, 119, 120: " )
    #controller.minimumCostPaths(cont, initialStation)
    scc3=controller.connectedwithID_1(cont,initialStation)
    contador=0
    listaReverse= lt.newList()
    listaReverse=scc3['reversePost']
    print (listaReverse)
    input ("&&&&&&&&&&&&&&&&&& Clic para correr DFS   sobre modos del Stack Reverse    &&&&&&&&&&&&&&&&&&")
    dfsAns=dfs.DepthFirstSearch(cont['connections'], initialStation)
    
    #print (dfsAns)

    j=0
    listaDSF= lt.newList()
    """
    for i in element:
        if element['value']['marked']==True:
            listaDSF[j]=element['value']['edgeTo']
            j=j+1
    for i in listaDSF:
        print (listaDSF[i])
    """
   
    print ("********************************** Voy a imprimir el Path uno ****************************************")
    print ("")
    #tam=lt.size(listaReverse)
    tam=len(listaReverse)
    verX=listaReverse[tam-6]
    verY=listaReverse[0]
    #print ("tamano del stack:" , tam, " verx a buscar: ", verX)
    dfsAnsPathVerX=dfs.pathTo(dfsAns, verX)
    print (dfsAnsPathVerX)    
    print (" ")
    print ("Acabo de imprimir el path desde ", verX, " a ",  initialStation)
    print (" ")
    print ("********************************** Voy a imprimir el Path dos ****************************************")
    print (" ")
    dfsAnsPathVerY=dfs.pathTo(dfsAns, verY)
    print (dfsAnsPathVerY)    
    print (" ")
    print ("Acabo de imprimir el path desde ", verY, " a ",  initialStation)
   
    input ("Clic para encontrar las rutas circuales")
    stackTam=stack.size(dfsAnsPathVerX)
    #print ("Tamano dle stack: ", stackTam)
    #input("clic para cotinuar")
    ruta1=lt.newList()
 
    for i in range (0,stackTam):
        punto=stack.pop(dfsAnsPathVerX)
       # print (punto)
        ruta1[i]=punto
    
    tiempoRuta1=0   
    #print ("Punto 1: ", ruta1[0], " y Punto 2: ", ruta1[1])
    #print (stackTam)
    print("")
    print ("Ruta lineal")
    print("")
    for i in range (0,stackTam-1):
        nodo = gr.getEdge(cont['connections'], ruta1[i], ruta1[i+1])
        tiempoRuta1= tiempoRuta1+ nodo['weight'] +10
        print ("Sale de: ", ruta1[i], " a ", ruta1[i+1], " tiempo de recorrido incluye visita: ", round(tiempoRuta1,0))

    print("")
    print ("Ruta Circular")
    print("")
    tiempoRuta1=0
    pos=0
    peso=0
    i=0
    j=0
    for i in range (0,stackTam-1):
        if  (tiempoRuta1<=(tiempoDisponible/3)):
            nodo = gr.getEdge(cont['connections'], ruta1[i], ruta1[i+1])
            tiempoRuta1= tiempoRuta1+ nodo['weight'] +10
            peso=nodo['weight']
            print ("Sale de: ", ruta1[i], " a ", ruta1[i+1], " tiempo de recorrido incluye visita: ", round(tiempoRuta1,0))
            pos=i
            #print ("i: ",i, " pos: ", pos)
        else:    
            i=stackTam-1

    #print ("Posicion: ", pos)
    #nodo = gr.getEdge(cont['connections'], ruta1[pos+1], ruta1[pos])
    tiempoRuta1= tiempoRuta1+ peso +10
    print ("Sale de: ", ruta1[pos+1], " a ", ruta1[pos], " tiempo de recorrido incluye visita: ", tiempoRuta1)
    for k in range (pos,1,-1):
            nodo = gr.getEdge(cont['connections'], ruta1[k], ruta1[k-1])
            peso=nodo['weight']
            tiempoRuta1= tiempoRuta1+ peso +10
            print ("Sale de: ", ruta1[k], " a ", ruta1[k-1], " tiempo de recorrido incluye visita: ", round(tiempoRuta1,0))
  
    nodo = gr.getEdge(cont['connections'], ruta1[1], ruta1[0])
    peso=nodo['weight']
    tiempoRuta1= tiempoRuta1+ peso +10
    print ("Sale de: ", ruta1[1], " a ", ruta1[0], " tiempo de recorrido incluye visita: ", round(tiempoRuta1,0))

    

def optionFive():
    pass

def optionSix():
    pass


def optionSeven():
    pass

def optionEight():
      
    
    pass

def optionNine():
    pass

def optionTen():
    IdBicicleta=int(input(" Digite el ID de la Bike que quiere consultar, Ejeplo: 32536, 14884, 14919, 14556 ? " ))
    paradas=cont['stops']
    idBicisValues=m.valueSet(paradas)
    #print (idBicisValues)
    idBicisKeys=m.keySet(paradas)
    #print (idBicisKeys)
    tam=m.size(paradas)
    listaBici=lt.newList('ARRAY_LIST')
    print ("Voy a buscar", IdBicicleta )
    #print (paradas)
    #input("")
    i=0
    for k,v in paradas.items():
        print (k,v)
        if v==IdBicicleta:
           listaBici[i]= k
           i=i+1
    print ("Esta bicicleta visito las siguientes estaciones")
     
    print (listaBici)
    #input("")



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

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
        #msg = "Estación Base (Ej: 72): "
        #initialStation = input(msg)
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 5:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 6:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
