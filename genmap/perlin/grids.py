'''
Conjunto de funciones para generar grillas o mallas 2d
'''
import random

def randomGrid(width,height, vmax):
  '''
  Genera una grilla con las dimensiones dadas y valores aleatorios
  de 0 a vmax
  
  width: cantidad de columnas
  height: cantidad de filas
  vmax: valór máximo de un nodo
  '''
  grid=[]
  for i in range(height):
    grid.append(list(map(lambda x: random.randint(0,vmax), range(width))))
  return grid

def periodicGrid(width,height,vmax):
  '''
  Genera una grilla con las dimensiones dadas y valores aleatorios
  de 0 a vmax, coincidiendo sus valores en sus extremos de forma que 
  se puede generar un azulejo continuo al unir sus partes
  
  width: cantidad de columnas
  height: cantidad de filas
  vmax: valór máximo de un nodo
  '''
  if width <2 or height <2:
    raise Exception('Las dimensiones de la grilla no pueden ser tan pequeñas')
  # Genera los valores reducidos
  gridBase=randomGrid(width-1,height-1,vmax)
  grid=[]
  for row in gridBase:
    grid.append(row+[row[0]])
  grid.append(grid[0])
  return grid

'''
A futuro se pueden crear otras funciones para generar grillas segun
diferentes distribuciones de probabilidad
'''
