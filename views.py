# -*- coding: utf-8 -*-

import wx
import wx.lib.mixins.listctrl as listmix

""" Archivo que contiene las clases de la GUI """


class MainFrame(wx.Frame):
	""" Ventana Principal """


	def __init__(self, parent=None, ID=-1):

		wx.Frame.__init__(self, parent, ID, size=(900, 600), 
			pos=wx.DefaultPosition, style=wx.DEFAULT_FRAME_STYLE )

		self.panel = BackgroundPanel(self, -1)
		self.panel.SetBackgroundColour("black")

		self.SetTitle(u"Gestión")
		self.Center()
		self.Maximize()

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



class ObjectListFrame(wx.Frame):


	def __init__(self, parent=None, ID=-1):

		wx.Frame.__init__(self, parent, ID, size=(900, 500))

		self.panel = wx.Panel(self, -1)

		self.title = "Object List"

		self.initUi()
		self.makeLayout()

		self.Center()
		self.Show()


	def makeLayout(self):

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		top_sizer = wx.BoxSizer(wx.HORIZONTAL)

		top_sizer.Add(self.button_add, 0)
		top_sizer.Add(self.button_modify, 0)
		top_sizer.Add(self.button_delete, 0)
		top_sizer.Add(self.ruler, 0)
		top_sizer.Add(self.label_search, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 50)
		top_sizer.Add(self.choice_search, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
		top_sizer.Add(self.text_search, 0, wx.ALIGN_CENTER_VERTICAL)

		main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.ALL, 10)
		main_sizer.Add(self.list_objects, 1, wx.EXPAND)

		self.panel.SetSizer(main_sizer)


	def initUi(self):

		self.button_add = wx.Button(self.panel, -1, label="Nuevo")
		self.button_modify = wx.Button(self.panel, -1, label="Modificar")
		self.button_delete = wx.Button(self.panel, -1, label="Eliminar")

		self.ruler = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL)

		self.choice_search = wx.Choice(self.panel, -1, choices=["por Nombre"], size=(140, -1))
		self.text_search = wx.TextCtrl(self.panel, -1, size=(200, -1))
		self.label_search = wx.StaticText(self.panel, -1, label="Buscar:")

		self.list_objects = ListCtrl(self.panel, -1, style=wx.LC_REPORT)
		self.list_objects.setResizeColumn(0)

		self.SetTitle(self.title)


	def setColumns(self, column_data):

		for column in column_data:


			self.list_objects.InsertColumn(
				column_data.index(column),
				column[0],
				width=column[1]
			)




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



class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):


	def __init__(self, *args, **kwargs):

		wx.ListCtrl.__init__(self, *args, **kwargs)
		listmix.ListCtrlAutoWidthMixin.__init__(self)