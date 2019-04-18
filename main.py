'''
Genera mapas
'''

import wx
import random, math,os
from  genmap.perlin import BitMap, lineal, vector
from genmap.ui import CampoCtrl

print('Versiones:')
print( '  wxPython:',wx.__version__)

class MyApp(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, wx.ID_ANY, title='Genera Mapas')

    # Add a panel so it looks correct on all platforms
    self.panel = wx.Panel(self, wx.ID_ANY)
    lado=256
    self.lado=lado
    self.bmp = BitMap(self.lado,self.lado)
    self.bmpScala=2
    self.mapa=wx.StaticBitmap(self.panel, wx.ID_ANY,self.bmp.GetBitMap(scale=self.bmpScala) )
    
    self.SetPosition((600-lado//2,300-lado//2))
    #Crea barra de estado
    self.CreateMenuBar()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Panel izquierdo
    pBtWidth=170 #ancho del panel de botones
    self.pBotones=wx.Panel(self, wx.ID_ANY)
    self.btRefrescar = wx.Button(self.pBotones, label='Refrescar')
    self.semillaInput= CampoCtrl(self.pBotones, label='Semilla:',sizeInput=(pBtWidth-16,-1))
    self.octavasInput= CampoCtrl(self.pBotones, label='Octavas:',sizeInput=(pBtWidth-16,-1))
    self.periodicInput= wx.CheckBox(self.pBotones,label='Mapa periodico')
    
    vSizer= wx.BoxSizer(wx.VERTICAL)
    self.pBotones.SetSizer(vSizer)
    vSizer.Add(self.semillaInput)
    vSizer.Add((pBtWidth,5),0)
    vSizer.Add(self.octavasInput)
    vSizer.Add((pBtWidth,8),0)
    vSizer.Add(self.periodicInput)
    vSizer.Add((pBtWidth,8),0)
    vSizer.Add(self.btRefrescar,flag=wx.ALIGN_CENTER)
    
    #Valores defecto
    self.semillaInput.SetValue('21')
    self.octavasInput.SetValue('8')
    self.periodicInput.SetValue(True)
    # Sizer general
    hSizerC=wx.BoxSizer(wx.HORIZONTAL)
    hSizerC.Add((8,1),0)
    hSizerC.Add(self.pBotones,flag=wx.ALIGN_CENTER)
    hSizerC.Add((8,1),0)
    hSizerC.Add(self.panel,flag=wx.ALIGN_CENTER)
    self.Msg('Iniciado')
    self.SetSizer(hSizerC)
    self.SetSize(lado*2+pBtWidth,lado*2)
    # Accion de dibujar el mapa
    self.btRefrescar.Bind(wx.EVT_BUTTON,self.OnRefrescar)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def CreateMenuBar(self):
    filemenu= wx.Menu()
    menuExit = filemenu.Append(-1,"&Salir"," Terminate the program")
    menuSave = filemenu.Append(-1,"&Guardar Mapa","")
    
    # menu Ayuda
    helpmenu= wx.Menu()
    menuAbout= helpmenu.Append(-1, "&Acerca de ..."," Information about this program")
    
    # Creating the menubar.
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu,"Archivo") # Adding the "filemenu" to the MenuBar
    menuBar.Append(helpmenu, "Ayuda")
    self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
    #Crea barra de estado
    self.sb = self.CreateStatusBar()
    self.sb.SetBackgroundColour('#babdb6')

    #self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    self.Bind(wx.EVT_MENU,self.OnSaveImage, menuSave)
    self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnSaveImage(self, evt):
    '''
    Guarda la imagen del mapa
    '''
    extensiones={ 
      '.tif':wx.BITMAP_TYPE_TIF,
      '.png':wx.BITMAP_TYPE_PNG, 
      '.jpg':wx.BITMAP_TYPE_JPEG}
    with wx.FileDialog(self, "Guardar imagen del mapa", 
    wildcard="Formato (*.png)|*.png|Formato (*.jpg)|*.jpg|Formato (*.tif)|*.tif",
                       defaultFile="semilla"+self.semillaInput.GetValue(),
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
      if fileDialog.ShowModal() == wx.ID_CANCEL:
        return     # the user changed their mind
      # save the current contents in the file
      pathname = fileDialog.GetPath()
      try:
        bmp=self.mapa.GetBitmap()
        filename, file_extension = os.path.splitext(pathname)
        ext=file_extension.lower()
        if ext == '':
          pathname+='.png'
          ext='.png'
        bmp.SaveFile(pathname, extensiones[ext])
      except IOError:
        wx.LogError("Cannot save current data in file '%s'." % pathname)
      

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnRefrescar(self, evt):
    '''
    Genera el dibujo del mapa
    '''
    self.Msg('Se está dibujando un nuevo mapa...')
    try:
      semilla= int( self.semillaInput.GetValue())
    except:
      self.Msg('Semilla no válida, debe ser un entero')
      return
    
    try:
      octavas= int(  self.octavasInput.GetValue() )
    except:
      self.Msg('Cantidad de octavas no válida, debe ser un entero')
      return
    periodica= self.periodicInput.GetValue()
    self.bmp.GenMapa(seedValue=semilla,periodic=periodica,
          octavas=octavas, initialGrid=2)
    self.mapa=wx.StaticBitmap(self.panel, wx.ID_ANY,self.bmp.GetBitMap(scale=self.bmpScala) )
    self.Msg('Se ha dibujado un nuevo mapa')
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def Msg(self,texto):
    self.sb.SetStatusText('>>  '+ texto)
    print (texto)

  def scale_bitmap(bitmap, width, height):
    
    image = wx.ImageFromBitmap(bitmap)
    image = image.Scale(width, height, )
    result = wx.BitmapFromImage(image)
    return result

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnAbout(self,e):
    dlg = wx.MessageDialog(self, 
    """
    Una herramienta para generar mapas 
    utilizando el concepto de ruido de perlin.
    version 1.0 (Alpha)
    Carlos Jacanamejoy (2019)""",
     "Acerca de Genera Mapas", wx.OK)
    dlg.ShowModal() # Shows it
    dlg.Destroy() # finally destroy it when finished.
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnExit(self,e):
    self.Close(True)  # Close the frame.
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__ == '__main__':
  app = wx.App()
  frame = MyApp().Show()
  app.MainLoop()

