
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse_lazy
from hoodapp.forms import NeighborhoodForm, RegistrationForm
from .models import *
from django.views.generic import TemplateView,View,CreateView,ListView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    neigh=Neighborhood.objects.all()
    return render(request, 'index.html',{'neigh':neigh})

def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            # password=form.cleaned_data.get('password')

            return redirect('login')
    else:
        form=RegistrationForm()
    return render(request, 'register/registration.html',{'form':form})

@login_required()
def create_neighborhood(request):
    if request.method == 'POST':
        form=NeighborhoodForm(request.POST)
        if form.is_valid():
            hood=form.save(commit=False)
            hood.admin=request.user.profile
            hood.save()
            return redirect('index')
    
    else:
        form=NeighborhoodForm()
    return render(request,'hood.html',{'form':form})


def display_hood(request,hood_id):
    hood=Neighborhood.objects.get(id=hood_id)
    business=Business.objects.filter(location=hood)
    post=Post.objects.filter(location=hood)
    return render(request,'single_hood.html',{'business':business, 'post':post,'hood':hood})

class UpdateHood(UpdateView):
    template_name='update.html'
    model=Neighborhood
    fields ='__all__'
    success_url =reverse_lazy('all')

# class UpdateHood(LoginRequiredMixin, UserPassesTestMixin, UpdateView):                     
#     model = Neighborhood  
#     fields = ['image','name', 'caption']
#     def form_valid(self, form):       
#         form.instance.admin = self.request.user      
#         return super().form_valid(form)
#     def test_func(self):  
#             post = self.get_object()      
#             if self.request.user == post.admin:           
#                 return True        
#             return False

class DeleteHood(DeleteView):
    template_name='delete.html'
    model=Neighborhood
    fields='__all__'
    success_url=reverse_lazy('index')

# def join(request):
#     neighborhood=Neighborhood.objects.all()
#     request.user.profile.neighborhood=neighborhood
#     request.user.profile.save()
#     return redirect('index')
def join_hood(request,hood_id):
    '''	View function that enables users join a hood	'''	
    neighborhood = Neighborhood.objects.get(pk = hood_id)	
   
    return redirect('index')

def leave(request):
    request.user.profile.neighborhood=None
    request.user.profile.save()
    return redirect('index')



def profile(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated!')
            return redirect('profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
        current_profile = Profile.objects.get(user_id = request.user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'current_profile':current_profile
    }
    return render(request, 'register/profile.html', context)

def user_profile(request, id):
   try:
     user_detail = Profile.objects.get(id=id)
     current_post = Post.user_post(user_detail.username)
     if request.user.username == str(user_detail.username):
       return redirect('profile')
     else:
       return render(request, 'userprofile.html', {'userdetail':user_detail, ' current_post': current_post})
   except Profile.DoesNotExist:
      return HttpResponseRedirect(" Sorry the Page You Looking For Doesn't Exist.")

def create_post(request):
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    else:
        form=PostForm()
    return render(request,'post_form.html',{'form':form})

def display_post(request):
    posts=Post.objects.all()
    return render(request, 'display_post.html',{'posts':posts})

def search_business(request):
    # if request.method == 'GET':
    #     name=request.GET.get('name')
    #     search_results=
    if 'search' in request.GET and request.GET['search']:
        search_name=request.GET.get('search')
        search_results=Business.search_business(search_name)
        return render(request, 'search.html', {'search_results': search_results,'search_name': search_name})

    else:
        return redirect('index')

def business(request):
    if request.method == 'POST':
        form=BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    else:
        form=BusinessForm()
    return render(request,'business.html',{'form':form})

def business_details(request,hood_id):
    business=Business.objects.filter(neighborhood=hood_id).all()
    return render(request, 'single_hood.html',{'business':business})




