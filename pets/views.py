from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# custom imports
from pets.timer import RepeatedTimer as rt
from pets.models import *
from pets.forms import *
from pets.mixins import *


# Create your views here.
class PetCreateView(CreateView):

    template_name = 'pets/pet_form.html'
    form_class = NewPetForm
    success_url = '/'

    def form_valid(self, form):

        # We take the stats from the selected species and pass them to this pet
        species = Species.objects.get(name=str(form.instance.species))
        form.instance.description = species.description
        form.instance.happiness_gain_rate = species.happiness_gain_rate
        form.instance.happiness_loss_rate = species.happiness_loss_rate
        form.instance.fullness_gain_rate = species.fullness_gain_rate
        form.instance.fullness_loss_rate = species.fullness_loss_rate
        form.instance.owner = self.request.user
        valid_data = super(PetCreateView, self).form_valid(form)

        print(valid_data)
        return valid_data


class PetListView(LoginRequiredMixin, ListView):

    model = Pet

    def get_queryset(self):
        my_pets = Pet.objects.filter(owner=self.request.user)

        # # this is when we start managing user's pets' stats
        # for pet in my_pets:
        #
        #     # Change stats every x seconds
        #     interval = 10
        #     manage_hunger = rt(interval, pet.gain_hunger())
        #     manage_happiness = rt(interval, pet.lose_happiness())

        return my_pets.order_by('name')




