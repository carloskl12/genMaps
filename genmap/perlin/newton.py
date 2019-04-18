'''
funciones para estimar la serie geométrica para utilizarse
en la generación del ruido de perlin
'''
import math
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def newton(f,Df,x0,epsilon,max_iter):
  '''Approximate solution of f(x)=0 by Newton's method.

  Parameters
  ----------
  f : function
      Function for which we are searching for a solution f(x)=0.
  Df : function
      Derivative of f(x).
  x0 : number
      Initial guess for a solution f(x)=0.
  epsilon : number
      Stopping criteria is abs(f(x)) < epsilon.
  max_iter : integer
      Maximum number of iterations of Newton's method.

  Returns
  -------
  xn : number
      Implement Newton's method: compute the linear approximation
      of f(x) at xn and find x intercept by the formula
          x = xn - f(xn)/Df(xn)
      Continue until abs(f(xn)) < epsilon and return xn.
      If Df(xn) == 0, return None. If the number of iterations
      exceeds max_iter, then return None.

  Examples
  --------
  >>> f = lambda x: x**2 - x - 1
  >>> Df = lambda x: 2*x - 1
  >>> newton(f,Df,1,1e-8,10)
  Found solution after 5 iterations.
  1.618033988749989
  '''
  xn = x0
  for n in range(0,max_iter):
      fxn = f(xn)
      if abs(fxn) < epsilon:
          print('Solución hallada luego de ',n,'iteraciones.')
          return xn
      Dfxn = Df(xn)
      if Dfxn == 0:
          print('Derivada cero. No se halló una solución.')
          return None
      xn = xn - fxn/Dfxn
  print('Se excede la máxima cantidad de iteraciones. No se encontró solución.')
  return None


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def obtenerSerie(n):
  '''
  Obtiene la serie que suma 255 y tiene n terminos
  
  n: número de términos de la serie
  '''
  f = lambda x: 255 - (math.pow(x,n) - 1)/(x-1)
  Df= lambda x: (math.pow(x,n)-1)/((x-1)*(x-1)) - n*math.pow(x,n-1)/(x-1)
  x0=math.pow(255,1/(n-1))
  r= newton(f,Df,x0,1e-8,10)
  serie=[]
  ai=1
  for i in range(n):
    serie.append(round(ai))
    ai*=r
  suma= sum(serie)
  print ('** suma:', suma)
  if suma != 255:
    print('** diferencia:', 255-suma)
    serie[-1]+= 255-suma
    suma= sum(serie)
    print ('** suma corregida:', suma)
  serie.reverse()
  return serie

