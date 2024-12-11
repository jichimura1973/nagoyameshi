from django.urls import path
from . import views

urlpatterns = [
    path("", views.TopPageView.as_view(), name="top_page"),
    path("company/", views.CompanyView.as_view(), name="company_page"),
    path("terms/", views.TermsView.as_view(), name="terms_page"),
    path("restaurant-detail/<int:pk>/", views.RestaurantDetailView.as_view(), name="restaurant_detail"),  
    path("restaurant-list/", views.RestaurantListView.as_view(), name="restaurant_list"),
    path("favorite-list/", views.FavoriteListView.as_view(), name="favorite_list"),
    path("favorite-delete/", views.favorite_delete, name="favorite_delete"),
    path('reservation-create/<int:pk>/', views.ReservationCreateView.as_view(), name="reservation_create"),
    path("reservation-list/", views.ReservationListView.as_view(), name="reservation_list"),
    path('reservation-delete', views.reservation_delete, name='reservation_delete'),
    path('review-list/<int:pk>/', views.ReviewListView.as_view(), name="review_list"),
    path('review-create/<int:pk>/', views.ReviewCreateView.as_view(), name="review_create"),
    path('review-update/<int:pk>/', views.ReviewUpdateView.as_view(), name="review_update"),
    path('review-delete', views.review_delete, name='review_delete'),
    path("restaurant-update/<int:pk>/", views.RestaurantUpdateView.as_view(), name="restaurant_update"),
    path("restaurant-create/", views.RestaurantCreateView.as_view(), name="restaurant_create"),
    path("restaurant-list-admin/", views.RestaurantListAdminView.as_view(), name="restaurant_list_admin"),
    path("restaurant-delete", views.restaurant_delete, name="restaurant_delete"),
    path("category-list/", views.CategoryListView.as_view(), name="category_list"),
    path("category-detail/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("category-update/<int:pk>/", views.CategoryUpdateView.as_view(), name="category_update"),
    path("category-create/", views.CategoryCreateView.as_view(), name="category_create"),
    path('category-delete', views.category_delete, name='category_delete'),
    
    
]

