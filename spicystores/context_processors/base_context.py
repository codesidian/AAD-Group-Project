def setBaseContext(request):
    test_context_var = 'test context var'
    context = {
        'title' : '',
        'test_context_var' : test_context_var,
    }
    return context