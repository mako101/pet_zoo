from django.db import models as m
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete

from .apps import PetsConfig
from pets.timer import RepeatedTimer as rt
from pets.counter import PetStatCounter as psc


# some helper functions
# limit minimum stat value to 0 and max to 10
def increase(x, y):
    if x < 10:
        x += y
        if x > 10:
            x = 10
    return x


def decrease(x, y):
    if x > 0:
        x -= y
        if x < 0:
            x = 0
    return x


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
    owner = m.ForeignKey(User)
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
        self.current_hunger = decrease(self.current_hunger, self.hunger_loss_rate)
        self.save()

    def gain_hunger(self):
        self.current_hunger = increase(self.current_hunger, self.hunger_gain_rate)
        # print("{}'s hunger is {}".format(self.name, self.current_hunger))
        self.save()

    def pet(self):
        self.current_happiness = increase(self.current_happiness, self.happiness_gain_rate)
        self.save()

    def lose_happiness(self):
        self.current_happiness = decrease(self.current_happiness, self.happiness_loss_rate)
        # print("{}'s happiness is {}".format(self.name, self.current_happiness))
        self.save()

    # adds 2 jobs to the global scheduler using the name of the relevant pet
    def start_counters(self):
        interval = self.stat_change_interval
        psc.add_job(self.gain_hunger, interval, str.lower('{}_hunger'.format(self.name)))
        psc.add_job(self.lose_happiness, interval, str.lower('{}_happiness'.format(self.name)))

    def __str__(self):
        return "{} - {}'s {}".format(self.name, str(self.owner).capitalize(), self.species)


def stop_counters(sender, instance, *args, **kwargs):

    psc.remove_job(str.lower('{}_hunger'.format(instance.name)))
    print('Deleted {} job'.format(str.lower('{}_hunger'.format(instance.name))))

    psc.remove_job(str.lower('{}_happiness'.format(instance.name)))
    print('Deleted {} job'.format(str.lower('{}_happiness'.format(instance.name))))

pre_delete.connect(stop_counters, sender=Pet)
