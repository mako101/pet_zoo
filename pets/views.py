from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# API Stuff
from pets.serializers import PetSerializer, SpeciesSerializer, UserSerializer
from rest_framework import (
                            generics as g,
                            permissions as p,
                            viewsets as v)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# custom imports
# from pets.models import Pet, Species
from pets.forms import *
from pets.mixins import *
from pets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request):
    return Response({
        'users': reverse('user-list', request=request),
        'pets': reverse('pet-list', request=request),
        'species': reverse('species-list', request=request),
    })


class SpeciesList(g.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    # permission_classes = (p.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class SpeciesDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = (p.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PetList(g.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = (p.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PetDetail(g.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = (p.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

#
# # User listing + details
# class UserViewSet(v.ReadOnlyModelViewSet):
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserList(g.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(g.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


##################### Class Based Views ######################

# Create your views here.
class GuiPetCreateView(CreateView):

    template_name = 'pets/pet_form.html'
    form_class = NewPetForm
    success_url = '/'

    def form_valid(self, form):

        # We take the stats from the selected species and pass them to this pet
        species = Species.objects.get(name=str(form.instance.species))
        form.instance.description = species.description
        form.instance.stat_change_interval = species.stat_change_interval
        form.instance.happiness_gain_rate = species.happiness_gain_rate
        form.instance.happiness_loss_rate = species.happiness_loss_rate
        form.instance.hunger_gain_rate = species.hunger_gain_rate
        form.instance.hunger_loss_rate = species.hunger_loss_rate
        form.instance.owner = self.request.user
        valid_data = super(GuiPetCreateView, self).form_valid(form)

        # start the stats counter for newly-created pet
        form.instance.start_counters()

        print(valid_data)
        return valid_data


class GuiPetListView(LoginRequiredMixin, ListView):

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




