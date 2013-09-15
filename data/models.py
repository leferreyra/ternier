from django.db import models

# Aca van los modelos para el ORM de django


class Client(models.Model):


	code = models.IntegerField()
	name = models.CharField(max_length=60)
	dni_cuil = models.CharField(max_length=11)
	cp = models.CharField(max_length=10)
	address = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=30)
	rsocial = models.CharField(max_length=50, blank=True)


	class Meta:

		verbose_name=u'client'
		verbose_name_plural=u'clients'


	def __unicode__(self):

		return self.name