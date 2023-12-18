import random
from itertools import permutations
#Cudrados mágicos usando algoritmos genéticos

#n es el tamaño del cuadrado
def inicializar_poblacion(n, tam_poblacion):
    poblacion = []
    for i in range(tam_poblacion):
      cuadrado = []#representamos al cuadrado en una linea [1,2,3,4,5,6,7,8,9]
      #generamos n*n numeros aleatorios no repetidos
      cuadrado = random.sample(range(1, n*n+1), n*n)
      poblacion.append(cuadrado)
    return poblacion

#función fitness, recibe el cuadro y la constante magica (cm)
def evaluar_aptitud(poblacion, n, cm):
  for i in range(len(poblacion)):
    cuadrado = poblacion[i]
    #calculamos la suma de las filas
    suma_filas = 0
    for j in range(n):
      suma = 0
      for k in range(n):
        suma += cuadrado[j*n+k]
      suma_filas += abs(suma-cm)
    #calculamos la suma de las columnas
    suma_columnas = 0
    for j in range(n):
      suma = 0
      for k in range(n):
        suma += cuadrado[k*n+j]
      suma_columnas += abs(suma-cm)
    #calculamos la suma de las diagonales
    suma_diagonal1 = 0
    suma_diagonal2 = 0
    for j in range(n):
      suma_diagonal1 += cuadrado[j*n+j]
      suma_diagonal2 += cuadrado[j*n+(n-1-j)]
    suma_diagonal1 = abs(suma_diagonal1-cm)
    suma_diagonal2 = abs(suma_diagonal2-cm)
    #agregamos el aptitud a la poblacion
    aptitud = suma_filas + suma_columnas + suma_diagonal1 + suma_diagonal2
    poblacion[i] = [cuadrado, aptitud]
  return poblacion

# sleccion por torneo probabilistico
def defineParejas(tamPop, padres):
  #ordenamos padres de forma aleatoria
  parejas1 = random.sample(padres, len(padres))
  #generamos a la segunda pareja
  parejas2 = random.sample(padres, len(padres))
  #eliminamos al menos apto de las parejas
  parejas1 = torneoProbabilistico(tamPop, parejas1)
  parejas2 = torneoProbabilistico(tamPop, parejas2)
  #ahora generamos los padres, que son los indices de los padres
  indices = []
  for i in range(0, len(parejas1)):
    indices.append(padres.index(parejas1[i]))
    indices.append(padres.index(parejas2[i]))
  return indices


def torneoProbabilistico(tamTorneo, parejas):
  pseleccion = 0.8 #probabilidad de seleccion
  indices_eliminar = []
  for i in range(0, tamTorneo, 2):
    #generamos un numero aleatorio entre 0 y 1 que es la probabilidad de seleccion
    seleccion = random.uniform(0,1)
    if i+1 >= len(parejas):
      break
    elif seleccion <= pseleccion:
      #selecciona el mejor individuo
      if parejas[i][1] > parejas[i+1][1]:
        #elimina al individuo de menor aptitud
        indices_eliminar.append(i+1)
      else:
        indices_eliminar.append(i)
    else:
      #selecciona el peor individuo
      if parejas[i][1] < parejas[i+1][1]:
        #elimina al individuo de menor aptitud
        indices_eliminar.append(i+1)
      else:
        indices_eliminar.append(i)
  #eliminamos los individuos marcados
  indices_eliminar.sort(reverse=True)
  for i in indices_eliminar:
    parejas.pop(i)
  return parejas


#funcion de cruce
def orderBasedCrossover(padres, n, tam_poblacion):
  #generamos los indices de los padres
  indices = defineParejas(tam_poblacion, padres)
  #generamos los hijos
  hijos = []
  for i in range(0, len(indices), 2):
    #Obtenemos n*n/2 numeros aleatorios no repetidos
    puntos1 = random.sample(range(0, (n*n)-1), int(n*n/2))
    puntos2 = random.sample(range(0, (n*n)-1), int(n*n/2))
    #generamos los hijos que son las cadenas de los padres menos los puntos
    # Hacer copias de las cadenas de los padres
    padre1 = padres[indices[i]][0]
    padre2 = padres[indices[i+1]][0]

    hijo1 = list(padre1)
    hijo2 = list(padre2)
    #iteramos sobre los hijos y remplanzamos los puntos por -1
    for j in range(n*n):
      if hijo1[j] in puntos1:
        hijo1[j] = -1
      if hijo2[j] in puntos2:
        hijo2[j] = -1
    #ahora reemplazamos los -1 por los valores del otro padre
    for j in range(n*n):
      if hijo1[j] == -1:
        hijo1[j] = reemplazarValor(hijo1, padres[indices[i+1]][0])
      if hijo2[j] == -1:
        hijo2[j] = reemplazarValor(hijo2, padres[indices[i]][0])
    #agregamos los hijos a la lista de hijos
    hijos.append(hijo1)
    hijos.append(hijo2)
    
  return hijos

#funcion alternativa de mutacion heuristica
def mutacionHeuristica(cuadro,n,cm):
  #generamos n*n/2 numeros aleatorios no repetidos
  puntos = random.sample(range(0, len(cuadro)-1), int(len(cuadro)/2))
  #obtenemos todas las posibles permutaciones
  permutaciones = list(permutations(puntos))
  #generamos los nuevos cuadrados por cada permutacion
  cuadrados = []
  for i in range(len(permutaciones)):
    nuevoCuadrado = list(cuadro)
    for j in range(len(permutaciones[i])):
      nuevoCuadrado[puntos[j]] = cuadro[permutaciones[i][j]]
    cuadrados.append(nuevoCuadrado)
  #calculamos la aptitud de cada cuadrado
  aptitudes = evaluar_aptitud(cuadrados, n, cm)
  #ordenamos los cuadrados de menor a mayor aptitud
  aptitudes.sort(key=lambda x: x[1])
  #retornamos el mejor cuadrado
  return aptitudes[0][0]

#funcion para reemplazar los -1 por los valores del otro padre
def reemplazarValor(hijo, padre):
  for i in range(len(padre)):
    if padre[i] not in hijo:
      return padre[i]
    
#funcion de mutacion
def mutacionIntercambioReciproco(cuadro):
  #generamos dos numeros aleatorios no repetidos
  puntos = random.sample(range(0, len(cuadro)-1), 2)
  #intercambiamos los valores
  aux = cuadro[puntos[0]]
  cuadro[puntos[0]] = cuadro[puntos[1]]
  cuadro[puntos[1]] = aux
  return cuadro

#itera sobre la poblacion y aplica la mutacion si cumple con la probabilidad
def mutaciones(poblacion, coeficienteDeMutacion, n, cm):
  for i in range(len(poblacion)):
    #generamos un numero aleatorio entre 0 y 1 que es la probabilidad de mutacion
    mutacion = random.uniform(0,1)
    if mutacion <= coeficienteDeMutacion:
      poblacion[i][0] = mutacionHeuristica(poblacion[i][0],n,cm)
      #calculamos la aptitud del individuo mutado
      poblacion[i][1] = evaluar_aptitud([poblacion[i][0]], n, cm)[0][1]
  return poblacion

def algoritmoGenetico(n, coeficienteDeMutacion, generaciones, tam_poblacion):
  #inicializamos la poblacion
  poblacion = inicializar_poblacion(n, tam_poblacion)
  #calculamos la constante magica
  cm = int((n*(n*n+1))/2)
  #evaluamos la aptitud de la poblacion
  poblacion = evaluar_aptitud(poblacion, n, cm)
  #iteramos por el numero de generaciones
  for i in range(generaciones):
    #seleccionamos los padres
    padres = poblacion
    #generamos los hijos
    hijos = orderBasedCrossover(padres, n, len(poblacion))
    #evaluamos la aptitud de los hijos
    hijos = evaluar_aptitud(hijos, n, cm)
    #unimos los hijos con los padres
    poblacion = padres + hijos
    #ordenamos la poblacion de menor a mayor aptitud
    poblacion.sort(key=lambda x: x[1])
    #aplicamos las mutaciones
    poblacion = mutaciones(poblacion, coeficienteDeMutacion, n, cm)
    #ordenamos la poblacion de menor a mayor aptitud
    poblacion.sort(key=lambda x: x[1])
    #eliminamos los individuos menos aptos
    poblacion = poblacion[:tam_poblacion]
    #imprimimos la mejor aptitud
    print("Generacion: ", i+1, " Mejor aptitud: ", poblacion[0][1])
    #si la aptitud es 0, terminamos el algoritmo
    if poblacion[0][1] == 0:
      break
  #imprimimos el mejor cuadrado
  print("Mejor cuadrado: ", poblacion[0][0])

algoritmoGenetico(3, 0.1, 100, 100)