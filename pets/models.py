from django.db import models as m
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save

from pets.counter import PetStatCounter as psc
from . import model_helpers as mh

# Templates for various pet types
class Species(m.Model):

    name = m.CharField(max_length=20)
    description = m.TextField(blank=True)

    # how often the pet's stats will change
    stat_change_interval = m.IntegerField(default=20)

    # Happiness increases with petting and decreases with time
    happiness_gain_rate = m.IntegerField(default=1)
    happiness_loss_rate = m.IntegerField(default=1)

    # Hunger increases with time and decreases with feeding
    hunger_gain_rate = m.IntegerField(default=1)
    hunger_loss_rate = m.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Species'

    def __str__(self):
        return self.name


# Pet inherits characteristics from its species + its own attributes
class Pet(m.Model):

    species = m.ForeignKey(Species)
    name = m.CharField(max_length=20)
    slug = m.SlugField(blank=True)
    # related name makes it avaiable as a User model attribute
    owner = m.ForeignKey(User, related_name='pets', on_delete=m.CASCADE)
    description = m.TextField(blank=True)
    stat_change_interval = m.IntegerField()

    # The defaults will be used for all new pets
    current_happiness = m.IntegerField(default=5)
    current_hunger = m.IntegerField(default=5)

    happiness_gain_rate = m.IntegerField()
    happiness_loss_rate = m.IntegerField()

    hunger_gain_rate = m.IntegerField()
    hunger_loss_rate = m.IntegerField()

    def feed(self):
        self.current_hunger = mh.decrease(self.current_hunger, self.hunger_loss_rate)
        self.save()

    def gain_hunger(self):
        self.current_hunger = mh.increase(self.current_hunger, self.hunger_gain_rate)
        # print("{}'s hunger is {}".format(self.name, self.current_hunger))
        self.save()

    def pet(self):
        self.current_happiness = mh.increase(self.current_happiness, self.happiness_gain_rate)
        self.save()

    def lose_happiness(self):
        self.current_happiness = mh.decrease(self.current_happiness, self.happiness_loss_rate)
        # print("{}'s happiness is {}".format(self.name, self.current_happiness))
        self.save()

    # adds 2 jobs to the global scheduler using the name of the relevant pet
    def start_counters(self):
        interval = self.stat_change_interval
        psc.add_job(self.gain_hunger, interval, str.lower('{}_hunger'.format(self.name)))
        psc.add_job(self.lose_happiness, interval, str.lower('{}_happiness'.format(self.name)))

    def __str__(self):
        return "{} - {}'s {}".format(self.name, str(self.owner).capitalize(), self.species)


pre_save.connect(mh.create_slug, sender=Pet)

pre_delete.connect(mh.stop_counters, sender=Pet)





