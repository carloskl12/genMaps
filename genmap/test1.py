'''
test 1
'''
from  perlin import lineal, vector , bilineal
from perlin import obtenerSerie
import random

def testVector(v,ntotales):
  v1=vector(v,ntotales)
  print(' vector:\n  ',v1)
  if len(v1) != ntotales:
    raise Exception('Error: se esperaba una dimensión de %i, y se tiene %i.'%(ntotales,len(v1)))
  for value in v:
    if value not in v1:
      raise Exception('Error: no se halla el punto %i en el resultado'%value)

def testBilineal(grid, width,height):
  g2=bilineal(grid,width,height)
  w=len(g2[0])
  h=len(g2)
  print('De (w,h)=',(len(grid[0]),len(grid)), ' a (w,h)=',(w,h))
  print (g2)
  if w!= width or h!=height:
    raise Exception('Error: no se generó una grilla con las dimensiones requeridas')

if __name__ == '__main__':
  print('Corriendo test:')
  print('inicia en 1 y termina en 5 con dimension 4',lineal(1,5,4))
  for i in range(3,9):
    testVector([1,10,30],i)
  for i in range(5,11):
    testVector([1,10,30,1,1],i)
  vec=[10, 30, 50]
  for i in range(10):
    testVector(vec,256)
    vec+=[random.randint(0,100)]
  #Bilineal
  grid=[[1, 50],[40, 10]]
  testBilineal(grid, 10,10)
  testBilineal(grid, 10,12)
  print('\n')
  serie= obtenerSerie(10)
  print( ' serie:',serie)
  if sum(serie) != 255:
    raise Exception('Error: la suma debe ser 255')
  print('\n Test terminado cocrrectamente.')







