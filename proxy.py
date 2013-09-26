import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings

from data.models import *

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub



class ObjectListModel:


	def __init__(self, queryset):

		self.queryset = queryset


	def getObjects(self):

		objs = []

		for obj in self.queryset.objects.all():
			new_obj = ObjectModel(obj)
			objs.append(new_obj)

		pub.sendMessage(
			'%s.listed' % str(self.queryset._meta.verbose_name_plural), 
			objects=objs
		)

		return objs


	def getObjectById(self, id):

		return ObjectModel(self.queryset.objects.get(pk=id))


	def deleteObjectById(self, id):

		obj = self.queryset.objects.get(pk=id)

		pub.sendMessage(
			'%s.deleted' % str(self.queryset._meta.verbose_name_plural), 
			object_id=id
		)

		obj.delete()


	def createObject(self, fields):

		new_model = self.queryset()

		for k, v in fields.iteritems():
			setattr(new_model, k, v)

		new_model.save()

		new = ObjectModel(new_model)

		pub.sendMessage(
			'%s.added' % str(self.queryset._meta.verbose_name_plural), 
			object=new
		)

		return new



	def getFieldNames(self):

		return self.queryset._meta.get_all_field_names()


	def getFieldType(self, field):

		return self.model._meta.get_field(field).get_internal_type()






class ObjectModel:


	def __init__(self, django_model):

		self.model = django_model


	def getFieldNames(self):

		return self.model._meta.get_all_field_names()


	def getFieldValue(self, field_name):

		return getattr(self.model, field_name);


	def setFieldValue(self, field_name, value):

		setattr(self.model, field_name, value)

		self.model.save()
		self.objectChanged()


	def setFieldsValues(self, fields):

		for k, v in fields.iteritems():
			setattr(self.model, k, v)

		self.model.save()
		self.objectChanged()


	def getFieldType(self, field):

		return self.model._meta.get_field(field).get_internal_type()


	def getId(self):

		return self.model.pk


	def objectChanged(self):

		pub.sendMessage(
			'%s.changed' % str(self.model._meta.verbose_name), 
			object=self
		)


	def __repr__(self):

		return repr(self.model)

