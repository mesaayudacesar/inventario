def user_groups(request):
    """
    Añade información del rol del usuario al contexto de todas las plantillas
    """
    if request.user.is_authenticated:
        return {
            'user_rol': request.user.rol,
            'user_is_admin': request.user.rol == 'admin',
            'user_is_logistica': request.user.rol == 'logistica',
            'user_is_lectura': request.user.rol == 'lectura',
            'user_is_asignador': request.user.rol == 'asignador',
        }
    return {}
