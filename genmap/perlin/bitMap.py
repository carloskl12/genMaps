# -*- coding: utf-8 -*-
import wx
import math
import random 
from struct import pack, unpack
from . import lineal, bilineal, obtenerSerie, randomGrid, periodicGrid

"""
Clase para generar un bitmap a partir de una matriz de relieves
"""

class BitMap(object):
  def __init__(self,width, height, palette=None):
    self._w= width
    self._h= height
    self._data=bytearray([0]*(width*height))
    self._size=width*height
    self._p=palette
    if palette== None:
      self._p=((0,'#000088'),(127,'#00aaff'),(128,'#00aa00'),
               (160,'#aa5500'), (200,'#babdb6'),(255,'#ffffff'))
      self._colors=self.GenPalette()

  def __setitem__(self, index, itemValue):
    self._data[index]=itemValue
  
  def __iter__(self):
    for item in self._data:
      yield item
  
  def __len__(self):
    return len(self._data)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GenPalette(self, stopsColors=None):
    '''
    Genera la lista de los 256 colores a asignar a los niveles del 
    relieve.
    Esto es a partir de interpolar los colores dados en una tupla
    '''
    if stopsColors ==None:
      stopsColors=self._p
    ns= len(stopsColors)
    # Verifica si hay color para el inicio
    # en caso contrario se define como el primer color 
    # de la lista.
    if ns <2:
      raise Exception('Se requieren al menos dos colores para generar la paleta.')
    if stopsColors[0][0]>0:
      stopsColors=(stopsColors[0],)+stopsColors
    # De forma similar para el último color
    if stopsColors[-1][0]<255:
      stopsColors=stopsColors+(stopsColors[-1],)
    # Una vez garantizados los colores para todo
    # el rango de 0 a 256 se procede a generar
    # sus valores rgb
    ns= len(stopsColors)
    
    # El primer color
    rgbP=tuple(int(stopsColors[0][1][i:i+2], 16) for i in (1, 3, 5))
    icp=0 #Acumula el indice sobre la paleta de 0 a 255
    colors=[(0,0,0)]*256
    for ic, c in stopsColors[1:]:
      #unpack('BBB',c[1:].decode('hex'))
      rgb=tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
      n=ic-icp+1
      R= lineal(rgbP[0],rgb[0],n)
      G= lineal(rgbP[1],rgb[1],n)
      B= lineal(rgbP[2],rgb[2],n)
      j=0 #Inicia de cero para agregar el rango completo
      #print('  n=',n,'  icp=',icp,'  ic=',ic)
      for k in range(icp,ic+1):
        #print('  k=',k, '  j=',j, ' dim R:',len(R))
        colors[k]=(R[j],G[j],B[j])
        j+=1
      #Guarda los valores pasados
      icp=ic
      rgbP=rgb
    return colors
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetZero(self):
    '''
    Vuelve cero todo los datos
    '''
    for i in range(self._size):
      self._data[i]=0
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetValue(self,value, x,y):
    """
    Dibuja un pixel en las coordenas especificas en pixeles virtuales
    """
    i=x+y*self._w
    self._data[i]=value

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetWidth(self):
    """Ancho en pixeles"""
    return self._w
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetHeight(self):
    """Alto en pixeles"""
    return self._h

  def GetBitMap( self, colors=None,scale=1):
    '''Escala un array'''
    if colors == None:
      colors= self._colors
    else:
      colors= self.GenPalette(colors)
    #print(colors)
    w=round( scale*self._w)
    h=round( scale*self._h)
    bufferBmp=bytearray([0]*(3*w*h))
    data=self._data
    if scale>1:
      grid=[]
      for y in range(self._h):
        offset=y*self._w
        grid.append(self._data[offset:offset+self._w])
      grid=bilineal(grid,w,h)
      data=bytearray([0]*w*h)
      for i in range(w*h):
        data[i]=grid[i//w][i%w]
    #Genera el buffer con los colores
    it=0
    for i in range(w*h):
      it= i*3
      bufferBmp[it:it+3]= colors[data[i]]

    wxBmp= wx.Bitmap.FromBuffer(w,h,bufferBmp)
    return wxBmp
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GenMapa(self,seedValue=None, periodic=False, octavas=-1 , initialGrid=2):
    '''Genera un mapa
    '''
    width=self._w
    height=self._h
    self.SetZero()
    #Calcula el número máximo de octavas posibles
    if width < height:
      octavasMax= math.floor(math.log(width)/math.log(2))
    else:
      octavasMax= math.floor(math.log(width)/math.log(2))
    if octavasMax < octavas:
      print('No se pueden tomar todas las octavas, se ha reducido a', octavasMax)
      octavas=octavasMax
    if octavas == -1:
      octavas=octavasMax
    # Ahora se requiere calcular la progresión de las
    # amplitudes entre las diferentes octavas
    #mapa=[[0]*width for i in range(height)]
    a=1
    amplitudes=[1<<i for i in range(octavas)]
    amplitudes.reverse()
    #Factor de amplitudes
    fam=255/sum(amplitudes)
    #amplitudes=obtenerSerie(octavas)
    # 0.5 interesante
    # 0.992
    random.seed(seedValue)
    #print('Semilla:',random.getstate())

    funGrid=randomGrid
    if periodic:
      funGrid=periodicGrid
    #Se debe empezar desde la escala mayor para
    #que los seeds generen un mapa a diferentes
    #escalas según se desee
    #porque si se empieza por la escala mas
    #pequeña 
    vw=[]
    vh=[]
    w=initialGrid
    h=initialGrid
    for o in range(octavas):
      vw.append(w)
      vh.append(h)
      w*=2
      h*=2
    print('  ** escalas:',vw)
    print('  ** amplitudes:', amplitudes)
    for o in range(octavas):
      grid=funGrid(vw[o],vh[o],round(amplitudes[o]*fam))
      grid=bilineal(grid,width,height)
      for x in range(width):
        for y in range(height):
          i=x+y*self._w
          self._data[i]=0xff & (self._data[i]+grid[y][x])


