from rest_framework import serializers as s
from pets.models import Pet, Species

from django.contrib.auth.models import User


# Serializers define the API representation.
class UserSerializer(s.ModelSerializer):

    # has to be called explicitly, as not included by default
    pets = s.PrimaryKeyRelatedField(many=True, queryset=Pet.objects.all())

    class Meta:
        model = User
        # fields = ('id', 'username', 'email', 'pets')


class PetSerializer(s.ModelSerializer):

    owner = s.ReadOnlyField(source='owner.username')

    class Meta:
        model = Pet


class SpeciesSerializer(s.ModelSerializer):

    class Meta:
        model = Species
