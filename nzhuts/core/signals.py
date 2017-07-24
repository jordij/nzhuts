from django.db.models.signals import post_save
from django.dispatch import receiver

from nzhuts.core.models import HutPage, HutPageFacility


@receiver(post_save, sender=HutPage)
def post_hut_save(sender, instance, **kwargs):
    existing_facilities = instance.facilities.all()
    # remove tags that don't exist anymore
    for existing_facility in existing_facilities:
        if existing_facility.name not in instance.raw_facilities:
            instance.facilities.remove(existing_facility)
    # add tags
    if instance.raw_facilities:
        for facility in instance.raw_facilities:
            instance.facilities.add(facility)
