# from django.http import HttpResponse
# import datetime
# from django.shortcuts import render,redirect
# from Instaclone.models import UserModel
# from Instaclone.forms import SignUpForm
# from django.contrib.auth.hashers import make_password
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
#
# # def signup_view(request):
# #     if request.method == "GET":
# #             today = datetime.now()
# #             return render(request, 'index.html', {'today': today})
#
# def signup_view(request):
#   if request.method == 'GET':
#     signup_form = SignUpForm()
#     return render(request, 'index.html', {'signup_form' : signup_form})

# from django.shortcuts import render, redirect
# from .forms import SignUpForm,LoginForm
#
# from .models import UserModel
# from django.http import HttpResponse
# from django.contrib.auth.hashers import make_password,check_password


from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm
from .models import UserModel, SessionToken, PostModel
from django.contrib.auth.hashers import make_password, check_password
from My_Django_Project.settings import BASE_DIR
from datetime import timedelta
from django.utils import timezone

from imgurpython import ImgurClient
# Create your views here.

#Imgur Api keys
client_id='bb757ba09859d12'
client_secret='2aded6fc536c97caca644aba2280729e931f9c23'





def signup_view(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      name = form.cleaned_data['name']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      #saving data to DB
      user = UserModel(name=name, password=make_password(password), email=email, username=username)
      user.save()
      return render(request, 'success.html')

  elif request.method == "GET":
    form = SignUpForm()

  return render(request, 'index.html', {'form' : form})



  #views.py


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient(client_id, client_secret)
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')





def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('created_on')

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login/')





#For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None
