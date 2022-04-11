from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer, TokenAccessSerializer,
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)
from .filters import TitleFilter
from .permissions import (
    IsAdminOrSuperUser, IsAdminOrSuperUserOrReadOnly, PermissionReviewComment
)
from reviews.models import User, Category, Genre, Title, Review
from api_yamdb.settings import ADMIN_EMAIL


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    username = request.data.get('username')
    serializer.save(email=email, username=username)
    user = get_object_or_404(User, email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code for getting token',
        f'Confirmation code: {confirmation_code}',
        ADMIN_EMAIL,
        [email],
        fail_silently=False,
    )
    data = {'email': email, 'username': username}
    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def token_access(request):
    serializer = TokenAccessSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            user.save()
            return Response({'token': str(token.access_token)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('=username',)

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, pk=None):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.data, status=status.HTTP_400_BAD_REQUEST
        )


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def filter_queryset(self, queryset):
        queryset = super(TitleViewSet, self).filter_queryset(queryset)
        return queryset.order_by('-id')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (PermissionReviewComment,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (PermissionReviewComment,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
