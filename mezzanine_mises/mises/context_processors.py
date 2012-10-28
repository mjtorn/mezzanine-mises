from django.contrib.sites import models as sites_models

def site(request):
    return {
        'site': sites_models.Site.objects.get_current(),
    }

# EOF

