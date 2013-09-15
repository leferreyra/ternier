# -*- coding: utf-8 -*-

import wx
from custom import ListCtrl, BackgroundPanel, FormGrid

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

		self.list_idx = 0

		self.initUi()
		self.makeLayout()

		self.Center()
		self.Show()

		# Bind event to close on ESC press
		self.Bind(wx.EVT_CHAR_HOOK, self.OnCharHook)



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

		self.choice_search = wx.Choice(self.panel, -1, choices=[], size=(140, -1))
		self.text_search = wx.TextCtrl(self.panel, -1, size=(200, -1))
		self.label_search = wx.StaticText(self.panel, -1, label="Buscar:")

		self.list_objects = ListCtrl(self.panel, -1, style=wx.LC_REPORT)

		self.SetTitle("Object List")


	def setColumns(self, column_data):

		for column in column_data:


			self.list_objects.InsertColumn(
				column_data.index(column),
				column[0],
				width=column[1]
			)


	def setResizableColumn(self, col):

		self.list_objects.setResizeColumn(col)


	def setSearchBy(self, choices):

		self.choice_search.SetItems(choices)

		if len(choices):
			self.choice_search.SetSelection(0)


	def insertRow(self, row_data):

		column_count = self.list_objects.GetColumnCount()

		row = row_data[1]

		if len(row) == column_count:

			itemid = self.list_objects.InsertStringItem(self.list_idx, row[0])
			self.list_objects.SetItemData(itemid, row_data[0])

			for i in range(1, column_count):
				self.list_objects.SetStringItem(self.list_idx, i, row[i])

			self.list_idx += 1
		else:
			raise NameError("Row columns should be %d" % column_count)


	def setRow(self, idx, row_data):

		for i in range(self.list_objects.GetColumnCount()):
			self.list_objects.SetStringItem(idx, i, row_data[i])


	def OnCharHook(self, event):

		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()

		event.Skip()





class ClientDialog(wx.Dialog):


	def __init__(self, parent=None, ID=-1):

		wx.Dialog.__init__(self, parent, -1, "Cliente", size=(600, 400))

		self.dataFields = []
		self.billingFields = []
		self.extraFields = []

		self.modified = False

		self.initUi()
		self.makeLayout()

		self.Bind(wx.EVT_TEXT, self.OnText)


	def makeLayout(self):

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		main_sizer.Add(self.notebook, 1, wx.EXPAND)

		buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
		buttons_sizer.Add(self.button_save, 0)
		buttons_sizer.Add(self.button_close, 0)

		main_sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

		self.SetSizer(main_sizer)


	def initUi(self):

		self.notebook = wx.Notebook(self)
		self.createNotebookPages(self.notebook)

		self.button_save = wx.Button(self, wx.ID_OK, "Guardar")

		self.button_close = wx.Button(self, wx.ID_CANCEL, "Cerrar")
		self.button_close.SetDefault()


	def createNotebookPages(self, notebook):

		self.panel1 = wx.Panel(notebook)
		self.panel2 = wx.Panel(notebook)
		self.panel3 = wx.Panel(notebook)

		self.notebook.AddPage(self.panel1, "Datos")
		self.notebook.AddPage(self.panel2, u"Facturación")
		self.notebook.AddPage(self.panel3, "Observaciones")

		self.createPagesForms(self.panel1, self.dataFormFields())


	def dataFormFields(self):

		# Fields will layout 2 by line, the number is the proportion
		# of the field in the line.
		return (
			(("code", u'Código', FormGrid.TEXT_FIELD, 2), 
				("name", u'Nombre', FormGrid.TEXT_FIELD, 3)),

			(("cp", u'CP', FormGrid.TEXT_FIELD, 1), 
				("address", u'Dirección', FormGrid.TEXT_FIELD, 4)),

			(("city", u'Localidad', FormGrid.TEXT_FIELD, 1),
				("rsocial", u'Razón Social', FormGrid.TEXT_FIELD, 1),),

			(("state", u'Provincia', FormGrid.TEXT_FIELD, 2),
				("tel", u'Teléfono', FormGrid.TEXT_FIELD, 2)),

			(("cel", u'Celular', FormGrid.TEXT_FIELD, 1),
				("dni_cuil", u'DNI/CUIT', FormGrid.TEXT_FIELD, 1)),

			(("email", u'E-Mail', FormGrid.TEXT_FIELD, 1),),
		)


	def createPagesForms(self, panel, fields):

		self.data_form = FormGrid(panel, fields)


	def getControls(self):

		return self.data_form.getControls()


	def setModified(self):

		self.modified = True
		self.button_save.Enable()


	def setUnmodified(self):

		self.modified = False
		self.button_save.Disable()


	def OnText(self, event):

		self.setModified()
		event.Skip()


if __name__=='__main__':

	app = wx.PySimpleApp()

	dialog = ClientDialog()
	dialog.ShowModal()

	app.MainLoop()

