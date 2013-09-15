
from views import ObjectListFrame, ClientDialog
from proxy import ObjectListModel
from data.models import Client

import wx
from wx.lib.pubsub import pub


class ClientsController:


	def __init__(self, parent):

		self.main_controller = parent
		self.main_frame = parent.getFrame()

		self.frame = ObjectListFrame(self.main_frame)
		self.model = ObjectListModel(Client)

		self.setupListColumns()
		self.setupSearchBy()
		self.loadAllClients()
		self.setTitle()
		self.bindEvents()

		pub.subscribe(self.clientChanged, 'client.changed')


	def setupListColumns(self):

		self.frame.setColumns((
			("ID", 100),
			("Nombre", 200),
			("DNI/CUIL", 150),
		))

		self.frame.setResizableColumn(2)


	def setupSearchBy(self):

		self.frame.setSearchBy(['Nombre', 'ID'])


	def setTitle(self):

		self.frame.SetTitle("Lista de Clientes")


	def loadAllClients(self):

		for client in self.model.getObjects():
			self.frame.insertRow((
				client.getId(), 
				(str(client.model.code), client.model.name, client.model.dni_cuil)
			))


	def bindEvents(self):

		# Bind event to DClick on ListItem
		self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)


	def show(self):

		self.frame.Show()


	def setModel(self, client_dialog, model):

		controls = client_dialog.getControls()
		field_names = model.getFieldNames()

		for field in controls:
			if field in field_names:

				value = model.getFieldValue(field)
				client_dialog.data_form.getControl(field).SetValue(str(value))

		# Setting name in dialog title
		client_dialog.SetTitle("Cliente: %s" % model.getFieldValue('name'))

		client_dialog.setUnmodified()


	def saveModel(self, client_dialog, model):

		controls = client_dialog.getControls()
		field_names = model.getFieldNames()

		fields_to_save = {}

		for field in controls:
			if field in field_names:

				value = client_dialog.data_form.getControl(field).GetValue()
				# model.setFieldValue(field, value)
				fields_to_save[field] = value

		model.setFieldsValues(fields_to_save)


	def clientChanged(self, object):

		# print "el cliente %d cambio" % object_id
		item_idx = self.frame.list_objects.FindItemData(-1, object.getFieldValue('pk'))

		code = object.getFieldValue('code')
		name = object.getFieldValue('name')
		dni_cuil = object.getFieldValue('dni_cuil')

		self.frame.setRow(item_idx,
			(str(code), name, dni_cuil)
		)


	def OnListItemActivated(self, event):

		client_id = int(event.GetData())
		client_model = self.model.getObjectById(client_id)

		# Show the Client Frame
		client_dialog = ClientDialog(self.frame)
		self.setModel(client_dialog, client_model)

		if client_dialog.ShowModal() == wx.ID_OK:
			self.saveModel(client_dialog, client_model)

		client_dialog.Destroy()

		event.Skip()
