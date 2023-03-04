
from django.urls import path,include
from users import views
from users import user_attention

app_name='users'

urlpatterns = [

    path('register',views.register,name="register"),
    path('center',views.center,name="center"),
    path('attention',user_attention.follow,name="attention"),
    path('details',user_attention.details,name="details"),

]