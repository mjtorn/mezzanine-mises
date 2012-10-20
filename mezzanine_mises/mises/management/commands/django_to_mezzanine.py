from django.core.management.base import BaseCommand

from django.contrib.auth import models as auth_models

from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

from django.db import transaction

from ... import models

class Command(BaseCommand):
    """Deal with data migration
    """

    def _tx(self, from_model, to_model, from_db='django_mises', to_db='default'):
        """Transfer data from one place to the other
        """

        to_model.objects.using(to_db).all().delete()

        field_names = [f.name for f in from_model._meta.fields]

        print 'Transferring "%s" -> "%s"' % (from_model, to_model)
        from_obs = from_model.objects.using(from_db).all().order_by('id')
        for fob in from_obs:
            kwargs = {
                field_name: getattr(fob, field_name) for field_name in field_names
            }

            to_model.objects.using(to_db).create(**kwargs)
        print to_model.objects.using(to_db).all().count()

    @transaction.commit_on_success
    def handle(self, *args, **options):
        """JFDI method
        """

        if not settings.DATABASES.has_key('django_mises'):
            raise ImproperlyConfigured('Need django_mises db conf')

        from django_mises.users import models as dmu_models
        from django_mises.main import models as dmm_models

        self._tx(dmm_models.Slogan, models.Slogan)
        self._tx(auth_models.User, auth_models.User)
        self._tx(auth_models.Group, auth_models.Group)
        self._tx(dmu_models.UserProfile, models.UserProfile)

# EOF

