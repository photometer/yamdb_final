from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, send_confirmation_code, token_access,
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

authpatterns = [
    path('token/', token_access),
    path('signup/', send_confirmation_code),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(authpatterns)),
]
