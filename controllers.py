
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
		pub.subscribe(self.clientAdded, 'clients.added')
		pub.subscribe(self.clientDeleted, 'clients.deleted')

		self.frame.Bind(wx.EVT_BUTTON, self.OnModify, self.frame.button_modify)
		self.frame.Bind(wx.EVT_BUTTON, self.OnNew, self.frame.button_add)
		self.frame.Bind(wx.EVT_BUTTON, self.OnDelete, self.frame.button_delete)


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
				client_dialog.getControl(field).SetValue(str(value))

		# Setting name in dialog title
		client_dialog.SetTitle("Cliente: %s" % model.getFieldValue('name'))

		client_dialog.setUnmodified()


	def saveModel(self, client_dialog, model=None):

		controls = client_dialog.getControls()
		field_names = self.model.getFieldNames()

		fields_to_save = {}

		for field in controls:
			if field in field_names:

				value = client_dialog.getControl(field).GetValue()
				# model.setFieldValue(field, value)
				fields_to_save[field] = value

		if model is not None:
			model.setFieldsValues(fields_to_save)
		else:
			self.model.createObject(fields_to_save)


	def clientChanged(self, object):

		# print "el cliente %d cambio" % object_id
		item_idx = self.frame.list_objects.FindItemData(-1, object.getId())

		code = object.getFieldValue('code')
		name = object.getFieldValue('name')
		dni_cuil = object.getFieldValue('dni_cuil')

		self.frame.setRow(item_idx,
			(str(code), name, dni_cuil)
		)


	def clientAdded(self, object):

		self.frame.insertRow((
			object.getId(), 
			(object.model.code, object.model.name, object.model.dni_cuil)
		))


	def clientDeleted(self, object_id):

		item_idx = self.frame.list_objects.FindItemData(-1, object_id)
		self.frame.deleteRow(item_idx)


	def showClientDialog(self, client_model=None):

		# Show the Client Frame
		client_dialog = ClientDialog(self.frame)

		if client_model is not None:

			# Existent Client
			self.setModel(client_dialog, client_model)

			# Save Model Data
			if client_dialog.ShowModal() == wx.ID_OK:
				self.saveModel(client_dialog, client_model)

		else:

			# Create New Client
			client_dialog.SetTitle("Nuevo Cliente")
			if client_dialog.ShowModal() == wx.ID_OK:
				self.saveModel(client_dialog)

		client_dialog.Destroy()


	def getFocusedClientId(self):

		selected_item_idx = self.frame.list_objects.GetFocusedItem()

		if selected_item_idx != -1:

			item = self.frame.list_objects.GetItem(selected_item_idx)
			cid = int(item.GetData())

		else:

			cid = -1

			info_dlg = wx.MessageDialog(
				self.frame,
				"Debe seleccionar un cliente primero",
				caption="Error",
				style=wx.OK | wx.CENTRE | wx.ICON_ERROR
			)

			info_dlg.ShowModal()
			info_dlg.Destroy()

		return cid


	def OnListItemActivated(self, event):

		client_id = int(event.GetData())
		client_model = self.model.getObjectById(client_id)

		self.showClientDialog(client_model)

		event.Skip()


	def OnModify(self, event):

		client_id = self.getFocusedClientId()

		if client_id != -1:
			client_model = self.model.getObjectById(client_id)			
			self.showClientDialog(client_model)


	def OnNew(self, event):

		self.showClientDialog()
		event.Skip()


	def OnDelete(self, event):

		client_id = self.getFocusedClientId()

		if client_id != -1:

			client_model = self.model.getObjectById(client_id)

			confirm_dlg = wx.MessageDialog(
				self.frame,
				"Esta seguro que desea eliiminar el cliente %s?" % 
					client_model.getFieldValue('name'),
				caption="Confirmar",
				style=wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION
			)

			if confirm_dlg.ShowModal() == wx.ID_OK:
				self.model.deleteObjectById(client_model.getId())



