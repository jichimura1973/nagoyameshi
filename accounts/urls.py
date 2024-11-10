from django.urls import path
from . import views

urlpatterns = [
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
    path("subscribe-register/", views.SubscribeRegisterView.as_view(), name="subscribe_register"),
    path("subscribe-stripe_register/", views.SubscribeStripeRegisterView.as_view(), name="subscribe_stripe_register"),
    path('subscribe-stripe-success/', views.SubscribeStripeSuccessView.as_view(), name='subscribe_stripe_success'),
    path('subscribe-stripe-cancel/', views.SubscribeStripeCancelView.as_view(), name='subscribe_stripe_cancel'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout_session'),
    path("subscribe-cancel/", views.SubscribeCancelView.as_view(), name="subscribe_cancel"),
    path("subscribe-payment/", views.SubscribePaymentView.as_view(), name="subscribe_payment"),
    path("user-list/", views.UserListView.as_view(), name="user_list"),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), #追加
    path('password_reset_done/', views.PasswordResetDone.as_view(), name='password_reset_done'), #追加
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), #追加
    path('password_reset_complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), #追加
    # path('sales/', views.SalesListView.as_view(), name="sales_detail"),
    path('sales/', views.MonthlySalesListView.as_view(), name="sales_list"),
    # path("confirm-email/", views.VerificationSentView.as_view(), name="confirm_email")

]
