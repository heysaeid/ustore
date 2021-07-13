from django.shortcuts import redirect

def is_login(func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func()
        else:
            return redirect('shop:home')
    return wrap