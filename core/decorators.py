from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_if_superadmin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            logout(request)
            return redirect('account:login') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view
