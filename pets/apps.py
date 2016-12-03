from django.apps import AppConfig


class PetsConfig(AppConfig):
    name = 'pets'

    def ready(self):
        # Start managing all pets' stats once the app is loaded
        from .models import Pet
        from .counter import PetStatCounter

        for pet in Pet.objects.all():
            try:
                pet.start_counters()
            except:
                print('Could not add jobs for {}'.format(pet))


        PetStatCounter.start()
        PetStatCounter.status()
