import random
#Cudrados mágicos usando algoritmos genéticos

#n es el tamaño del cuadrado
def inicializar_poblacion(n, tam_poblacion):
    poblacion = []
    for i in range(tam_poblacion):
      cuadrado = []#representamos al cuadrado en una linea [1,2,3,4,5,6,7,8,9]
      for j in range(n*n):
        cuadrado.append(j+1)
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
  pseleccion = 0.75#probabilidad de seleccion
  for i in range(0, tamTorneo, 2):
    #generamos un numero aleatorio entre 0 y 1 que es la probabilidad de seleccion
    seleccion = random.uniform(0,1)
    if seleccion <= pseleccion:
      #selecciona el mejor individuo
      if parejas[i][1] > parejas[i+1][1]:
        #lo marcamos para eliminarlo
        parejas[i+1].append(True)
      else:
        parejas[i].append(True)
    else:
      #selecciona el peor individuo
      if parejas[i][1] < parejas[i+1][1]:
        #elimina al individuo de mayor aptitud
        parejas[i+1].append(True)
      else:
        parejas[i].append(True)
  #eliminamos los individuos marcados
  for i in range(len(parejas)-1, -1, -1):
    if len(parejas[i]) == 3:
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

def reemplazarValor(hijo, padre):
  for i in range(len(padre)):
    if padre[i] not in hijo:
      return padre[i]

#probamos orden based crossover
padres = [[1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1], [1,2,3,4,5,6,7,8,9], [8,2,3,1,6,5,4,7,9]]
aptitud = evaluar_aptitud(padres, 3, 15)
print('aptitud ',aptitud)
hijos = orderBasedCrossover(padres, 3, 4)
print('hijos ',hijos)
aptitud = evaluar_aptitud(hijos, 3, 15)
print('aptitud hijos ',aptitud)