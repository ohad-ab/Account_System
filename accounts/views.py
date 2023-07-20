from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from accounts.forms import SignupForm, UpdateForm
from django.views import generic
from accounts.models import User, Friend_Request, Chat_Users
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
        otheruser = get_object_or_404(User, slug=slug)
        is_friend = False
        if otheruser.friends.contains(request.user):
            is_friend = True
        if otheruser is not None:
            form = UpdateForm(instance=otheruser)
            context = {
                'otheruser': otheruser,
                'form': form,
                'is_friend': is_friend,
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
    
class SendFriendRequest(View):
    template_name = 'accounts/friend_request.html'

    def get(self, request, slug):
        from_user = request.user
        to_user = User.objects.get(slug=slug)
        if(from_user.is_authenticated and to_user is not None):
            context = {'to_user':to_user}
            if to_user.friends.contains(from_user):
                context['message'] = f"You are already friends with {to_user.username}."
                return render(request, self.template_name, context)
            else:
                object, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
                
                if created:
                    context['message'] = f"Friend request sent to {to_user.username}."
                    return render(request, self.template_name, context)
                else:
                    context['message'] = f"Friend request was already sent to {to_user.username}"
                    return render(request, self.template_name, context)
        else:
            return reverse_lazy('login')

class accept_friend_request(View):
    template_name = "accounts/friend_request_list.html"

    def get(self,request):
            friend_requests = Friend_Request.objects.all()
            context = {'requests': friend_requests}
            return render(request, self.template_name ,context)
    
    def post(self, request):
        current_user = request.user
        request_ID = request.POST['accept']
        friend_request = Friend_Request.objects.get(id=request_ID)
        other_user = friend_request.from_user
        current_user.friends.add(other_user)
        other_user.friends.add(current_user)
        friend_request.delete()
        return HttpResponseRedirect("/profiles/"+current_user.slug)
    
def room(request, room_name):
    
    try:
        creator = User.objects.get(username=room_name)
    except:
        creator = None
    if(room_name == 'main' or creator is not None):
        chat_room,created = Chat_Users.objects.get_or_create(name=room_name)       
        return render(request, 'accounts/chat_room.html', {
            'room_name': room_name,
            'room':chat_room,
            'creator': creator
        })
    return HttpResponse("You are not Authorized")
    

