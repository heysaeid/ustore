from .forms import NewSubscriberForm

def new_subscribe_form(request):
    return {'subcriber_form':NewSubscriberForm()}