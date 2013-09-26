from django.db import models

# Aca van los modelos para el ORM de django


class Client(models.Model):


	# Data
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=60)
	dni_cuil = models.CharField(max_length=11)
	cp = models.CharField(max_length=10, blank=True)
	address = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=30, blank=True)
	state = models.CharField(max_length=30, blank=True)
	rsocial = models.CharField(max_length=50, blank=True)
	tel = models.CharField(max_length=20, blank=True)
	cel = models.CharField(max_length=20, blank=True)

	# Billing
	limit = models.FloatField()
	discount = models.IntegerField()

	# Notes
	notes = models.TextField()


	class Meta:

		verbose_name=u'client'
		verbose_name_plural=u'clients'


	def __unicode__(self):

		return self.name