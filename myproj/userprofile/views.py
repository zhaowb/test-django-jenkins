from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def user_profile(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.profile)
    else:
        form = UserProfileForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'profile.html', {'form':form})
