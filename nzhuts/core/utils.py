from django.conf import settings
from django.core.exceptions import ValidationError
#  A place to define methods used in different parts of the app


def validate_only_one_instance(obj):
    """
    Allow only one instance
    """
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError("We're sorry but a %s already exists, only one is allowed." % model.__name__)
