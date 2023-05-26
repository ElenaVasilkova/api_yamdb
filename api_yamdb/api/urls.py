from django.urls import include, path
from rest_framework import routers
from users.views import (
    MeViewSet, SignUpViewSet, TokenViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpViewSet.as_view(), name='sign_up'),
    path('auth/token/', TokenViewSet.as_view(), name='activation'),
    path('users/me/', MeViewSet.as_view(), name='user_detail'),
]
