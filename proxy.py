import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings

from data.models import *

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub



class ObjectListModel:


	def __init__(self, queryset, name):

		self.queryset = queryset
		self.name = name


	def getObjects(self):

		objs = []

		for obj in self.queryset.objects.all():
			new_obj = ObjectModel(obj)
			objs.append(new_obj)

		pub.sendMessage('%s.listed' % self.name, objects=objs)

		return objs



class ObjectModel:


	def __init__(self, django_model):

		self.django_model = django_model


	def __repr__(self):

		return repr(self.django_model)



clients_list = ObjectListModel(Client, "clients")
print clients_list.getObjects()