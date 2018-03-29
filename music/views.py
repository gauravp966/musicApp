from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Album
from .forms import UserForm, UserLoginForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def user_login(request):
    user = False
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request,user)
                request.session['username'] = username
                return redirect('music:index')
            else:
                return redirect('music:login')

    else:
        login_form = UserLoginForm()
    return render(request, 'music/login.html', {'login_form':login_form, 'user':user})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        user = False
        return render(request, self.template_name,{'form': form, 'user':user})

    #process form data
    def post(self,request):
        form = self.form_class(request.POST)
        user = form.save(commit=False)
        if form.is_valid():
            user = form.save(commit=False)

            #remove unwanted data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user object if username and password are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form, 'user': user})


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

