from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import os

DIR_NAME = os.path.dirname(__file__)


@login_required
def home(request):
    with open(os.path.join(DIR_NAME, 'static/store/index.html'), 'r') as index:
        return HttpResponse(index.read(), content_type='text/html')
