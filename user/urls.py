from django.urls import include, path
from rest_framework import routers
from .views import RegistrationViewSet, PhoneVerifyView, RegisterUpdateView, LoginAPIView, LoginPhoneView

router = routers.DefaultRouter()
router.register(r'registrations', RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify-phone/', PhoneVerifyView.as_view(), name='verify-phone'),
    path('birth-date/', RegisterUpdateView.as_view(), name='birth-date'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-code/', LoginPhoneView.as_view(), name='login-code')
]
