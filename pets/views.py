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
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

# custom imports
import re
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
    # permission_classes = (p.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


# User listing + details
class UserViewSet(v.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PetViewSet(v.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide `pet` and `feed` functions
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = (p.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route()
    def pet(self, *args, **kwargs):
        pet = self.get_object()
        return Response(pet.pet())

    @detail_route()
    def feed(self, *args, **kwargs):
        pet = self.get_object()
        return Response(pet.feed())

    def create(self, request, *args, **kwargs):

        # use parent species stats and pass them to the pet
        species = Species.objects.get(pk=request.data.get('species'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user,
                        description=species.description,
                        stat_change_interval=species.stat_change_interval,
                        happiness_gain_rate=species.happiness_gain_rate,
                        happiness_loss_rate=species.happiness_loss_rate,
                        hunger_gain_rate=species.hunger_gain_rate,
                        hunger_loss_rate=species.hunger_loss_rate)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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

        return my_pets.order_by('name')




