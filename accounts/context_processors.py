def user_name_processor(request):
    """
    Adds the user's name to the context for all templates.
    """
    context = {}
    if request.user.is_authenticated:
        welcome_name = request.user.first_name if request.user.first_name else request.user.username
        context['welcome_name'] = welcome_name
    return context 