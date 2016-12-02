from django import forms as f
from pets.models import *


class NewPetForm(f.ModelForm):

    class Meta:
        model = Pet
        fields = ['name', 'species']
