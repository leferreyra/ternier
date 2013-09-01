from django.db import models

# Aca van los modelos para el ORM de django


class Client(models.Model):


	name = models.CharField(max_length=60)
	dni_cuil = models.CharField(max_length=11)


	class Meta:

		verbose_name=u'cliente'
		verbose_name_plural=u'clientes'


	def __unicode__(self):

		return self.name