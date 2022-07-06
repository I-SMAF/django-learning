from django.db import models
from django.db.models import Count


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def have_pets(self, flag):
        return self.get_queryset().filter(pets__isnull=flag)


class Person(models.Model):
    objects = PersonManager()
    first_name = models.CharField(max_length=64, verbose_name='имя',
                                  help_text='сюда имя писать надо, максимум 64 символа')
    last_name = models.CharField(max_length=64, verbose_name='фамилия')

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.full_name()

    def __repr__(self):
        return self.full_name()

    class Meta:
        ordering = ['id']
        unique_together = ['first_name', 'last_name']
        verbose_name = 'человек'
        verbose_name_plural = 'люди'


class PetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def have_friends(self, flag):
        if flag:
            return self.get_queryset().annotate(pets_count=Count('owner__pets')).filter(pets_count__gte=2)
        else:
            return self.get_queryset().annotate(pets_count=Count('owner__pets')).filter(pets_count__lte=2)


class Pet(models.Model):
    objects = PetManager()
    name = models.CharField(verbose_name='имя', max_length=64)
    owner = models.ForeignKey(Person, verbose_name='хозяин', on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return self.name + " " + str(self.owner.id) + " " + self.owner.full_name()

    def __repr__(self):
        return self.name + " " + str(self.owner.id) + " " + self.owner.full_name()

    class Meta:
        ordering = ['owner_id', 'name']
        unique_together = ['name', 'owner']
        verbose_name = 'петомец'
        verbose_name_plural = 'петомцы'
