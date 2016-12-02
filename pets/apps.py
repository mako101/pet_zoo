from django.apps import AppConfig

class PetsConfig(AppConfig):
    name = 'pets'

    def ready(self):
        from .models import Pet
        from pets.timer import RepeatedTimer as rt
        # this is when we start managing user's pets' stats
        for pet in Pet.objects.all():
            # Change stats every x seconds
            interval = 20
            manage_hunger = rt(interval, pet.gain_hunger)
            manage_happiness = rt(interval, pet.lose_happiness)
