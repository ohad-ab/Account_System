from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from accounts.forms import SignupForm, UpdateForm
from django.views import generic
from accounts.models import User
from django.views import View
from django.forms.models import model_to_dict

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "accounts/home.html"
    
    
class SignUpView(generic.CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = "accounts/signup.html"
    queryset = User.objects.all()

class UserProfileView(View):
    template_name = "accounts/profile.html"
    
    def get(self, request, slug):
        otheruser = User.objects.get(slug=slug)
        if otheruser is not None:
            form = UpdateForm(instance=otheruser)
            context = {
                'otheruser': otheruser,
                'form': form
            }
        return render(request, self.template_name, context)
    
    def post(self, request, slug):
        otheruser = User.objects.get(slug=slug)
        if otheruser is not None:
                
            form = UpdateForm(request.POST, instance=otheruser)
            if(form.is_valid()):
                form.save()
            context = {
                'otheruser': otheruser,
                'form': form
            }
            return HttpResponseRedirect("/profiles/"+slug)
        return render(request, self.template_name, context)
        
class UsersListView(generic.ListView):
    template_name = "accounts/user_list.html"
    queryset = User.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)