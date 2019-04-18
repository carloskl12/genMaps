'''
Conjunto de funciones para realizar interpolaciones
'''
import math

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def lineal(y0,y1,n):
  '''
  Interpolacion lineal
  
  Agrega n puntos en medio de los 
  dos valores y0 y y1 y retorna una lista 
  con n+2 puntos que corresponde a los 
  valores y0...y1 con la inserción de los 
  n puntos.
  '''
  if n<2:
    raise Exception('Error: el mínimo de n es 2, y se ingresó %i'%n)
  r=[y0]*n
  inc=(y1-y0)/(n-1)
  r[-1]=y1
  if n>0:
    v=y0
    for i in range(1,n-1):
      v+=inc
      r[i]=round(v)
  return r

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def vector(y, npuntos):
  '''
  Genera un vector con n puntos intermedios 
  interpolados de forma lineal entre
  cada par de puntos originales.
  
  y: vector de puntos a interpolar
  npuntos: total de puntos finales
  '''
  ny=len(y)
  if npuntos == ny:
    return y
  if npuntos < ny:
    raise Exception('Error: la cantidad de puntos debe ser'
    +' mayor o igual a la cantidad de puntos originales.')
  # npuntos= n*(ny-1)-ny+2
  # Se interpreta como n puntos por cada par de puntos
  # contiguos, pero como se cuenta doble cada punto intermedio 
  # se debe restar ny, excepto los dos extremos
  #
  # Despejando n se tiene
  # n = (npuntos+ny-2)/(ny-1)
  # Se redondea el cociente n 
  # a el entero inferior o igual
  n=math.floor((npuntos+ny-2)/(ny-1))
  # Calcula el número de puntos totales segun n,
  # n puede ser igual o menor a npuntos
  npt=n*(ny-1)-ny+2
  # Vector con los puntos a insertar en medio
  # de cada par de puntos
  nv=[n]*(ny-1)
  if npt < npuntos:
    faltan= npuntos-npt
    for i in range(faltan):
      nv[i]+=1
  # Inicaliza el vector del resultado
  r=[0]*npuntos
  k=0#indice sobre r
  for i in range(1,len(y)):
    y0=y[i-1]
    y1=y[i]
    yi=lineal(y0,y1,nv[i-1])
    r[k:k+nv[i-1]-1]=yi[0:-1]
    k+=nv[i-1]-1
  r[-1]=y[-1]
  return r

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def bilineal( grid, width,height):
  '''
  Interpolacion bilineal para una grilla
  
  grid: grilla
  width: nuevo ancho de la grilla
  height: nuevo alto de la grilla
  '''
  if len(grid)==height and len(grid[0])==width:
    return grid
  dimXgrid=len(grid[0])
  dimYgrid=len(grid)
  #Calcula los dos extremos en y
  Y=list(map(lambda V: vector(V,width),grid))
#  for Yi in grid:
#    Y.append(vector(Yi,n))
  #print(' ** len Y0:',len(Y[0]))
  #Transpone la matriz
  Y=list(map(list,zip(*Y)))
  #Se generan las interpolaciones verticales
  X=list(map(lambda V: vector(V,height),Y))
  newGrid= list(map(list,zip(*X)))
  return newGrid






