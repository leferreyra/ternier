# -*- coding: utf-8 -*-

import wx

""" Archivo que contiene las clases de la GUI """


class MainFrame(wx.Frame):
	""" Ventana Principal """


	def __init__(self, parent=None, ID=-1):

		wx.Frame.__init__(self, parent, ID, size=(900, 600), 
			pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE )

		self.panel = BackgroundPanel(self, -1)
		self.panel.SetBackgroundColour("black")

		self.SetTitle("Gestión")
		self.Center()

		self.initUi()
		self.makeLayout()


	def makeLayout(self):
		pass


	def initUi(self):
		pass


	def createToolBar(self, toolBarData):

		toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_NODIVIDER )
		toolbar.SetBackgroundColour("#333333")

		for eachToolData in toolBarData:
			self.createTool(toolbar, *eachToolData)

		toolbar.Realize()


	def createTool(self, toolbar, label, help, filename, handler):

		if not label:
			toolbar.AddSeparator()
			return

		tool = toolbar.AddSimpleTool(-1, wx.Bitmap(filename), label, help)
		self.Bind(wx.EVT_MENU, handler, tool)


	def createMenuBar(self, menuBarData):

		menuBar = wx.MenuBar()

		for eachMenuData in menuBarData:
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1:]
			menuBar.Append(self.createMenu(menuItems), menuLabel)

		self.SetMenuBar(menuBar)


	def createMenu(self, menuData):

		menu = wx.Menu()

		for label, status, handler in menuData:
			if not label:
				menu.AppendSeparator()
				continue
			menuItem = menu.Append(-1, label, status)
			self.Bind(wx.EVT_MENU, handler, menuItem)

		return menu




# =====================
# Some Custom wxWindows
# =====================

class BackgroundPanel(wx.Panel):


	def __init__(self, parent=None, ID=-1):

		wx.Panel.__init__(self, parent, ID)

		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def OnPaint(self, event):

		dc = wx.BufferedPaintDC(self, self.buffer)


	def OnSize(self, event):

		w, h = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(w, h)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)

		self.Draw(dc)

		self.Refresh()


	def OnEraseBackground(self, event):

		# Vacio intencionalemente
		pass


	def Draw(self, dc):

		w, h = self.GetClientSize()
		dc.Clear()

		bmp = wx.Bitmap("images/wood.png")
		bmp_logo = wx.Bitmap("images/w3bex-logo.png")

		lw, lh = bmp_logo.GetSize()
		bw, bh = bmp.GetSize()

		# Centrar la imagen
		xpos = (w - bw) / 2
		ypos = (h - bh) / 2

		logox = w - lw
		logoy = h - lh

		dc.DrawBitmap(bmp, xpos, ypos)
		dc.DrawBitmap(bmp_logo, logox, logoy)
