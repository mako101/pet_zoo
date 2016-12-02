from django.db import models as m
from django.contrib.auth.models import User


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


class Species(m.Model):

    name = m.CharField(max_length=20)
    description = m.TextField(blank=True)

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


class Pet(m.Model):

    species = m.ForeignKey(Species)
    name = m.CharField(max_length=20)
    owner = m.ForeignKey(User)
    description = m.TextField(blank=True)

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
        print("{}'s hunger is {}".format(self.name, self.current_hunger))
        self.save()

    def pet(self):
        self.current_happiness = increase(self.current_happiness, self.happiness_gain_rate)
        self.save()

    def lose_happiness(self):
        self.current_happiness = decrease(self.current_happiness, self.happiness_loss_rate)
        print("{}'s happiness is {}".format(self.name, self.current_happiness))
        self.save()

    def __str__(self):
        return "{} - {}'s {}".format(self.name,  str(self.owner).capitalize(), self.species)

