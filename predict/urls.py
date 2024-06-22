from django.urls import path , include
from . import views

app_name = 'predict'

urlpatterns = [
    path("", views.predict , name="prediction"),
    path("result", views.result , name="Result"),
    path("diet", views.diets, name="Dite_plan"),
    path("compass", views.compass, name="compass"),
]
