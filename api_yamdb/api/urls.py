from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet
from api_yamdb.users.views import RegisterUserView, APIGetToken

app_name = 'api'

router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', RegisterUserView.as_view(), name='register_user'),
    path('v1/', include(router.urls)),
    path('api/v1/', include('reviews.urls')),
]
