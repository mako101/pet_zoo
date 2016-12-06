# API Stuff
from pets.serializers import PetSerializer, SpeciesSerializer, UserSerializer
from rest_framework import permissions as p, viewsets as v
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

# custom imports
from django.contrib.auth.models import User
from pets.models import Pet, Species
from pets.permissions import IsOwnerOrReadOnly


class SpeciesViewSet(v.ReadOnlyModelViewSet):
    """
        Species are templates for pets

        Pets will inherit their stats (all values in seconds) form parent species
    """
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class UserViewSet(v.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PetViewSet(v.ModelViewSet):
    """
        All users can feed and pet all the pets

        Only authenticated users can add new pets, and they can only delete their own pets

        The pet and feed URLs are:

        http://localhost:8000/api/pets/id/pet

        http://localhost:8000/api/pets/id/feed
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






