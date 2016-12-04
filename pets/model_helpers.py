from pets.counter import PetStatCounter as psc


# some helper functions to assist with managing models

# limit minimum stat value to 0 and max to 10
def increase(x, y):
    if x < 10:
        x += y
        if x > 10:
            x = 10
    return x


def decrease(x, y):
    if x > 0:
        x -= y
        if x < 0:
            x = 0
    return x


def stop_counters(instance, *args, **kwargs):

    psc.remove_job(str.lower('{}_hunger'.format(instance.name)))
    print('Deleted {} job'.format(str.lower('{}_hunger'.format(instance.name))))

    psc.remove_job(str.lower('{}_happiness'.format(instance.name)))
    print('Deleted {} job'.format(str.lower('{}_happiness'.format(instance.name))))


def create_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = "{}-{}".format(str.lower(instance.name), str(instance.id))