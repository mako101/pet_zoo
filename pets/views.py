from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# API Stuff
from pets.models import Pet
from pets.serializers import PetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# custom imports
from pets.forms import *
from pets.mixins import *


class PetList(ListCreateAPIView):
    # my_pets = Pet.objects.filter(owner=self.request.user)
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


class PetDetail(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

# class PetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request):
#         pets = Pet.objects.all()
#         serializer = PetSerializer(pets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return Pet.objects.get(pk=pk)
#         except Pet.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         pet = self.get_object(pk)
#         serializer = PetSerializer(pet)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         pet = self.get_object(pk)
#         serializer = PetSerializer(pet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         pet = self.get_object(pk)
#         pet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def pet_list(request):
#     """
#     List all code pets, or create a new pet.
#     """
#     if request.method == 'GET':
#         pets = Pet.objects.all()
#         serializer = PetSerializer(pets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def pet_detail(request, pk):
#     """
#     Retrieve, update or delete a pet.
#     """
#     try:
#         pet = Pet.objects.get(pk=pk)
#     except Pet.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PetSerializer(pet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PetSerializer(pet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         pet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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




