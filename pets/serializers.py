from rest_framework import serializers as s
from pets.models import Pet, Species

from django.contrib.auth.models import User


# Serializers define the API representation.
class UserSerializer(s.HyperlinkedModelSerializer):

    # has to be called explicitly, as not included by default
    owned_pets = s.HyperlinkedRelatedField(many=True, view_name='pet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'owned_pets')


class PetSerializer(s.ModelSerializer):

    owner = s.ReadOnlyField(source='owner.username')
    # feed = s.HyperlinkedIdentityField(view_name='pet-feed')
    # pet = s.HyperlinkedIdentityField(view_name='pet-pet')
    current_happiness = s.ReadOnlyField()
    current_hunger = s.ReadOnlyField()
    description = s.ReadOnlyField()

    class Meta:
        model = Pet
        fields = ('id', 'url', 'name', 'owner', 'species',
                  'description', 'current_happiness', 'current_hunger')


class SpeciesSerializer(s.HyperlinkedModelSerializer):
    pets = s.HyperlinkedRelatedField(many=True, view_name='pet-detail', read_only=True)

    class Meta:
        model = Species
