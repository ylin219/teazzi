from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    # path('items/<str:pk>/',views.items,name='items'),
    path('topping/<str:pk>',views.topping,name='topping'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('delete/<str:pk>',views.deleteTopping,name='delete_Topping'),
    path('like/<str:pk>',views.likeDrinkt,name='like_Drink'),
    # path('update-user/',views.updateUser,name = 'update-user'),
]
