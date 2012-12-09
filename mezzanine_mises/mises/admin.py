from django.contrib import admin

class PermissionAdmin(admin.ModelAdmin):
    """Push this to intercept .queryset() calls from OwnableAdmin
    """

    def queryset(self, request):
        """Return items based on request
        """

        qs = super(PermissionAdmin, self).queryset(request)

        if request.user.is_superuser:
            return qs
        elif request.user.groups.filter(name__icontains='editors').exists():
            return qs

        return qs.none()

from mezzanine.blog import admin as blog_admin
bpa_bases = list(blog_admin.BlogPostAdmin.__bases__)
bpa_bases_names = [b.__name__ for b in bpa_bases]
pa_idx = bpa_bases_names.index('OwnableAdmin')
bpa_bases.insert(pa_idx, PermissionAdmin)
blog_admin.BlogPostAdmin.__bases__ = tuple(bpa_bases)

# EOF

