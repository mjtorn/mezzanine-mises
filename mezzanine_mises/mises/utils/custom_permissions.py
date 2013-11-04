def allow_editors(self, request):
    """Method-like function to use with custom permission admins
    """

    qs = self.model._default_manager.get_query_set()

    ordering = self.get_ordering(request)
    if ordering:
        qs = qs.order_by(*ordering)

    if request.user.is_superuser:
        return qs
    elif request.user.groups.filter(name__icontains='editors').exists():
        return qs

    return qs.none()

# EOF

