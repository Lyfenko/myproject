from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .quotes import views
from .quotes.views import MyPasswordResetView, MyPasswordResetDoneView, MyPasswordResetConfirmView, \
    MyPasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('tag/<str:tag_name>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search, name='search'),
    path('top_tags/', views.top_tags, name='top_tags'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
