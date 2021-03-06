"""My_Django_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path, include
#
# from django.conf.urls import include, url
# from django.contrib import admin
# from Instaclone.views import signup_view
#
#
# urlpatterns = [
#     path('', signup_view),
#     path('Instaclone/', include('Instaclone.urls')),
#     path('admin/', admin.site.urls),
# ]



from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Instaclone.views import signup_view,login_view,feed_view,post_view,like_view, comment_view
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('post/', post_view),
    url('feed/', feed_view),
    url('like/', like_view),
    url('comment/', comment_view),
    url('login/', login_view),
    url('', signup_view),


]