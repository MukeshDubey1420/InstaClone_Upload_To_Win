from django.test import TestCase

# Create your tests here.
from clarifai import rest
from clarifai.rest import ClarifaiApp

def upload_win(post):
    app = ClarifaiApp(api_key='a0ea20f39c7940df8fff210c4798e3b4')
    model = app.models.get