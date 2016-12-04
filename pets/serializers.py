from rest_framework import serializers as s
from pets.models import Pet, Species


class PetSerializer(s.ModelSerializer):

    class Meta:
        model = Pet


class SpeciesSerializer(s.ModelSerializer):

    class Meta:
        model = Species
