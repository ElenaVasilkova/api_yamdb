from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, GetToken,
                    ReviewViewSet, Signup, TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('/auth/token/', GetToken.as_view(), name='get_token'),
    path('/auth/signup/', Signup.as_view(), name='signup'),
    path('/', include(router.urls)),
]
