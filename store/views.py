from django.contrib.staticfiles.views import serve
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return serve(request, 'store/index.html')
