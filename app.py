# -*- coding: utf-8 -*-

import wx
from views import MainFrame

""" App main file """



class MainController:


	def __init__(self, app, main_frame):

		self.app = app
		self.main_frame = main_frame

		# setting menubar and toolbar data
		self.main_frame.createMenuBar(self.getMenuData())
		self.main_frame.createToolBar(self.getToolbarData())


	def getMenuData(self):

		# defining menus and it's callbacks methods
		return (
			("&Archivo", 
				("&Hacer Backup", "Hacer archivo de backup", self.OnBackup),
				("&Restaurar Backup", "Restaurar datos desde un backup", self.OnRestoreBackup),
				("", "", ""), # Add separator
				("&Configuración...", "Opciones varias de configuración", self.OnConfig),
				("", "", ""), # Add separator
				("Salir", "Salir de la aplicación", self.OnExit),
			),
			("&Clientes", 
				("&Nuevo Cliente...", "Crear nuevo cliente", self.OnNewClient),
				("", "", ""), # Add separator
				("&Administrar clientes...", "Administración de clientes", self.OnClients),
			),
			("&Gestión", 
				("&Comprar/Vender...", "Realizar transacción", self.OnNewTransaction),
				("", "", ""), # Add separator
				("&Administrar Stock...", "Stock de Divisas", self.OnAdminStock),
				("C&heques...", "Salir de la aplicación", self.OnChecks),
			),
		)


	def getToolbarData(self):

		return (
			("Nuevo cliente", "Crear nuevo cliente", "images/silver/test.png", self.OnNewClient),
			("Administrar clientes", "Administrar clientes", "images/silver/test.png", self.OnClients),
			("", "", "", None)
		)


	def OnBackup(self, event):
		pass


	def OnRestoreBackup(self, event):
		pass

		
	def OnConfig(self, event):
		pass


	def OnExit(self, event):
		pass


	def OnNewClient(self, event):
		pass


	def OnClients(self, event):
		pass


	def OnNewTransaction(self, event):
		pass


	def OnAdminStock(self, event):
		pass


	def OnChecks(self, event):
		pass



class App(wx.App):


	def OnInit(self):

		self.main_frame = MainFrame()
		self.main_frame.Show()

		self.main_controller = MainController(self, self.main_frame)

		self.SetTopWindow(self.main_frame)

		return True




if __name__=="__main__":

	app = App()
	app.MainLoop()
