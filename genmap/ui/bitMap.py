# -*- coding: utf-8 -*-
import wx

from struct import pack, unpack
from ..perlin import lineal
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
               (190,'#aa5500'), (230,'#babdb6'),(255,'#ffffff'))
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
    i=0
    cp=''
    icp=0
    rgb=None
    colors=[(0,0,0)]*256
    for ic, c in stopsColors:
      rgbP=rgb
       #unpack('BBB',c[1:].decode('hex'))
      rgb=tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
      if ic == i :
        colors[i]= rgb
        cp=c
        icp= ic
        i+=1
        continue
      #print ('** i=',i,' ic=', ic, ' icp=',icp, 'cp',cp)
      if cp== '' and i< ic:
        colors[icp:ic]= rgb
        i=ic
        cp=c
        icp=ic 
        continue
      if cp!= '' and i< ic:
        #print ('ok')
        n=ic-icp+1
        R= lineal(rgbP[0],rgb[0],n-2)
        G= self.linear(rgbP[1],rgb[1],n)
        B= self.linear(rgbP[2],rgb[2],n)
        j=0
        cp=c
        
        #print('  n=',n,'  icp=',icp,'  ic=',ic)
        for k in range(icp,ic+1):
          #print('  k=',k, '  j=',j)
          colors[k]=(R[j],G[j],B[j])
          j+=1
        icp=ic
    return colors
  def linear(self, y0,y1,n):
    '''
    Genera una vector con valores interpolados con incrementos lineales
    '''
    r=[y0]*n
    inc=(y1-y0)/(n-1)
    r[-1]=y1
    
    if n>2:
      v=y0
      for i in range(1,n-1):
        v+=inc
        r[i]=round(v)
    return r
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

  def GetBitMap( self, colors=None):
    '''Escala un array'''
    if colors == None:
      colors= self._colors
    else:
      colors= self.GenPalette(colors)
    #print(colors)
    tileEscalado=bytearray([0]*(3*self._w*self._h))
    ior=0

    for y in range(self._h):
      for x in range(self._w):
        i= (x+y*self._w)
        it= i*3
        tileEscalado[it:it+3]= colors[self._data[i]]

    wxBmp= wx.Bitmap.FromBuffer(self._w,self._h,tileEscalado)
    return wxBmp


