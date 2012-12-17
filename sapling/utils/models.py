from django.db import models


class M30CustomAttribute(models.Model):
    a = models.CharField(max_length=100)
    b = 'magic b'

    def _get_c(self):
        return 'magic c'
    c = property(_get_c)

    def d(self):
        return 'magic d'


class M30CustomAttributeSubclass(M30CustomAttribute):
    e = models.CharField(max_length=100)


class VersionedModelAbstract(M30CustomAttributeSubclass):
    class Meta:
        abstract = True


class VersionedModel(VersionedModelAbstract):
    e = models.CharField(max_length=90)
