from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView

from pets.models import *
from pets.forms import *


# Create your views here.
class PetCreateView(CreateView):

    template_name = 'pets/pet_form.html'
    form_class = NewPetForm
    success_url = '/'

    def form_valid(self, form):

        # We take the stats from the selected species and pass them to this pet
        species = Species.objects.get(name=str(form.instance.species))
        form.instance.description = species.description
        # form.instance.current_happiness = species.current_happiness
        # form.instance.current_fullness = species.current_fullness
        form.instance.happiness_gain_rate = species.happiness_gain_rate
        form.instance.happiness_loss_rate = species.happiness_loss_rate
        form.instance.fullness_gain_rate = species.fullness_gain_rate
        form.instance.fullness_loss_rate = species.fullness_loss_rate
        form.instance.owner = self.request.user
        valid_data = super(PetCreateView, self).form_valid(form)

        print(valid_data)
        return valid_data









"""
    Code to get attribute data:

    In [6]: dog = Species.objects.get(name='Dog')

    In [7]: dog.description
    Out[7]: 'The easiest pet to raise!'

    In [8]: foo = dog.description

    In [9]: foo
    Out[9]: 'The easiest pet to raise!'

    In [10]: foo = dog.happiness_gain_rate

    In [11]: foo
    Out[11]: 3

"""