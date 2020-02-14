from api.models import Staff
def setBaseContext(request):
    test_context_var = 'test context var'
    if request.user.is_authenticated:
        users_firstname = Staff.objects.get(user_id=request.user.id).first_name
    else:
        users_firstname = ''
    context = {
        'title' : '',
        'test_context_var' : test_context_var,
        'users_firstname':users_firstname
    }
    return context