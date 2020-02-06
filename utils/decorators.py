from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from api.models import Staff

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def basic_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and Staff.objects.get(user_id=u.id).access_level == 'BA' or Staff.objects.get(user_id=u.id).access_level == 'MA',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and Staff.objects.get(user_id=u.id).access_level == 'MA',
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator