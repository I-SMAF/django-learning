from django.db import models
from django.db.models import Count


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def have_pets(self):
        print(self.get_queryset().exclude(pets__isnull=True))
        return self.get_queryset().exclude(pets__isnull=True)


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


class PetTypeManager(models.Manager):
    pass


class PetType(models.Model):
    objects = PetTypeManager()
    title = models.CharField(verbose_name='название', max_length=64, unique=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'тип петомца'
        verbose_name_plural = 'типы петомцев'


class PetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def have_friends(self, flag):
        if flag:
            return self.get_queryset().annotate(pets_count=Count('owner__pets')).filter(pets_count__gte=2)
        else:
            return self.get_queryset().annotate(pets_count=Count('owner__pets')).filter(pets_count__lte=2)

    def cat(self):
        return self.get_queryset().filter(type__title__in=['КОТ', 'кот', 'Кот', 'кошка'])


class Pet(models.Model):
    objects = PetManager()
    name = models.CharField(verbose_name='имя', max_length=64)
    owner = models.ForeignKey(Person, verbose_name='хозяин', on_delete=models.CASCADE, related_name='pets')
    type = models.ForeignKey(PetType, verbose_name='тип', on_delete=models.CASCADE, related_name='pets', null=True)

    def __str__(self):
        return self.name + " " + str(self.owner.id) + " " + self.owner.full_name()

    def __repr__(self):
        return self.name + " " + str(self.owner.id) + " " + self.owner.full_name()

    class Meta:
        ordering = ['owner_id', 'name']
        unique_together = ['name', 'owner']
        verbose_name = 'петомец'
        verbose_name_plural = 'петомцы'


class HomeManager(models.Manager):
    pass


class Home(models.Model):
    objects = HomeManager()
    adress = models.CharField(max_length=64, verbose_name='адресс',
                              help_text='сюда адресс писать надо, максимум 64 символа',
                              unique=True)
    persons = models.ManyToManyField(Person, related_name='houses')
    pets = models.ManyToManyField(Pet, related_name='houses', blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        result = super().save(force_insert, force_update, using, update_fields)
        pets = []
        for person in self.persons.all():
            for pet in person.pets.all():
                pets.append(pet)
        archive_pets = list(self.pets.all())

        for pet in self.pets.all():
            if pet not in pets:
                del archive_pets[archive_pets.index(pet)]

        if list(self.pets.all()) != archive_pets:
            if archive_pets:
                self.pets.set(archive_pets)
            else:
                self.pets.clear()
            result = self.save()
            print('edited')
        print('sabed')
        return result

    def __str__(self):
        return self.adress

    def __repr__(self):
        return self.adress

    class Meta:
        ordering = ['adress']
        verbose_name = 'дом'
        verbose_name_plural = 'дома'
