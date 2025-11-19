def user_groups(request):
    """
    Context processor to add user group information to all templates.
    """
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name', flat=True))
        return {
            'user_groups': groups,
            'user_is_admin': 'Admin' in groups,
            'user_is_logistica': 'Logística' in groups,
            'user_is_lectura': 'Lectura' in groups,
        }
    return {}
