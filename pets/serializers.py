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


class PetSerializer(s.HyperlinkedModelSerializer):

    owner = s.ReadOnlyField(source='owner.username')

    class Meta:
        model = Pet
        fields = ('url', 'name', 'owner',  'species',
                  'current_happiness', 'current_hunger')


class SpeciesSerializer(s.HyperlinkedModelSerializer):
    pets = s.HyperlinkedRelatedField(many=True, view_name='pet-detail', read_only=True)

    class Meta:
        model = Species
