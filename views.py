
import wx

""" Archivo que contiene las clases de la GUI """


class MainFrame(wx.Frame):
	""" Ventana Principal """


	def __init__(self, parent=None, ID=-1):

		wx.Frame.__init__(self, parent, ID, size=(900, 600), 
			pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)