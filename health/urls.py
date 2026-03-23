from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(template_name='health/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.tracker_dashboard, name='dashboard'),
    path('edit/<int:update_id>/', views.tracker_dashboard, name='edit_mode'),
    path('delete/<int:pk>/', views.delete_log, name='delete'),
    path('bmr-setup/', views.bmr_setup, name='bmr_setup'),
    path('weight-tracking/', views.weight_tracking, name='weight_tracking'),
    path('products/', views.products, name='products'),
    path('community/', views.community, name='community'),
    path('mindfuel/', views.mindfuel, name='mindfuel'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('mpesa/checkout/', views.mpesa_checkout, name='mpesa_checkout'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('api/food-search/', views.food_search_api, name='food_search_api'),
    path('stk-push/', views.initiate_stk_push, name='stk_push'),
]

