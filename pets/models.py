from django.db import models as m
from django.contrib.auth.models import User


# some helper functions
# limit minimum stat value to 0 and max to 10
def up_to_ten(x, y):
    if x < 10:
        x += y
        if x > 10:
            x = 10
    return x


def down_to_zero(x, y):
    if x > 0:
        x -= y
        if x < 0:
            x = 0
    return x

# Create your models here.
class Species(m.Model):

    name = m.CharField(max_length=20)
    description = m.TextField(blank=True)
    happiness_gain_rate = m.IntegerField(default=1)
    happiness_loss_rate = m.IntegerField(default=1)
    fullness_gain_rate = m.IntegerField(default=1)
    fullness_loss_rate = m.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Species'

    def __str__(self):
        return self.name


class Pet(m.Model):

    species = m.ForeignKey(Species)
    name = m.CharField(max_length=20)
    owner = m.ForeignKey(User)
    description = m.TextField(blank=True)
    current_happiness = m.IntegerField(default=5)
    current_fullness = m.IntegerField(default=5)
    happiness_gain_rate = m.IntegerField()
    happiness_loss_rate = m.IntegerField()
    fullness_gain_rate = m.IntegerField()
    fullness_loss_rate = m.IntegerField()

    def feed(self):
        self.current_fullness = up_to_ten(self.current_fullness, self.fullness_gain_rate)
        self.save()

    def gain_hunger(self):
        self.current_fullness = down_to_zero(self.current_fullness, self.fullness_loss_rate)
        self.save()

    def pet(self):
        self.current_happiness = up_to_ten(self.current_happiness, self.happiness_gain_rate)
        self.save()

    def lose_happiness(self):
        self.current_happiness = down_to_zero(self.current_happiness, self.happiness_loss_rate)
        self.save()

    def __str__(self):
        return "{} - {}'s {}".format(self.name,  str(self.owner).capitalize(), self.species)

