import random
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Subscribe
from .forms import NewSubscriberForm
from .tasks import subscribe_complete
# Create your views here.

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@require_POST
def new(request):
    data = {}
    if request.is_ajax():
        form = NewSubscriberForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.confirm_num = random_digits()
            sub.save()
            subscribe_complete.delay(sub.id)
            data['status'] = 'ok'
        else:
            data['error'] = 'This email already exists'
        return JsonResponse(data)

def confirm(request):
    sub = get_object_or_404(Subscribe, email=request.GET['email'])
    if sub.confirm_num == request.GET['conf_num'] and not sub.confirmed:
        sub.confirmed = True
        sub.save()
        message = 'Your newsletter subscription was successful'
    else:
        message = 'The following link has expired'
    return render(request, 'newsletter/confirm.html', {'message':message})