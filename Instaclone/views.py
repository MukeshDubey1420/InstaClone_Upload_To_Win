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
from django.http import JsonResponse,HttpResponse
from .forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from .models import UserModel, SessionToken, PostModel, LikeModel, CommentModel
from django.contrib.auth.hashers import make_password, check_password
from My_Django_Project.settings import BASE_DIR,client_secret,client_id
from datetime import timedelta
from django.utils import timezone
import os
from imgurpython import ImgurClient
from datetime import datetime
# Create your views here.





def signup_view(request):
  now_time = datetime.now()
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

  return render(request, 'index.html', {'form' : form , 'now':now_time})



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
            else:
                response_data['message'] = 'User does not exist!!!!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)

def logout_view(request):
    response = redirect("/")
    response.delete_cookie("session_token")
    return response


def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                newpost = PostModel(user=user, image=image, caption=caption)
                newpost.save()
                path = os.path.join(BASE_DIR, newpost.image.url)
                client = ImgurClient(client_id, client_secret)
                newpost.image_url = client.upload_from_path(path,anon=True)['link']
                newpost.save()
                return redirect('/feed/')

        elif request.method == 'GET':
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')



#For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            # time_to_live = session.created_on + timedelta(days=1)
            # if time_to_live > timezone.now():
                return session.user
    else:
        return None



def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = LikeModel.objects.filter(post=post, user=user).first()
            if existing_like:
                # post is already liked
                post.is_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            current_post = PostModel.objects.filter(id=post_id).first()
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                data = {
                    'flag': True
                }

            else:
                existing_like.delete()
                data = {
                    'flag': False
                }
                return JsonResponse(data)

            return redirect('/feed/')

    else:
        return redirect('/login/')



def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')