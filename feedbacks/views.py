from django.shortcuts import render
from .models import Feedback

def admin_feedback_view(request):
    feedback = Feedback.objects.all().order_by('-id')
    context = {'feedback':feedback}
    return render(request, 'admin_feedback.html', context)