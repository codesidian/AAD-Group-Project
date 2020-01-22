from django.contrib.staticfiles.views import serve

def home(request):
    return serve(request, 'store/index.html')
