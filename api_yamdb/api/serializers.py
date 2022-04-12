from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # я подумала, что лучше так, чем исключать 9 полей
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Невозможно использовать зарезвированное имя "me".')
        return value


class TokenAccessSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        category_serializer = CategorySerializer(value)
        return category_serializer.data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        genre_serializer = GenreSerializer(value)
        return genre_serializer.data


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id',)
        extra_kwargs = {'title': {'required': False}}

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        if request.method == 'POST' and (Review.objects.filter(
            author=request.user, title__id=title_id
        ).exists()):
            raise serializers.ValidationError('Нельзя оставить второй отзыв.')
        return data

    def validate_review(self, score):
        if 10 > score < 1:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне от 1 до 10.')
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'review')
