from .forms import NewSubscriberForm

def new_subscribe_form(request):
    return {'form':NewSubscriberForm()}