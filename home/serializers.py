from rest_framework import serializers
from .models import Article, User, Tag, Category, Comments, Advertisments

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'image', 'content', 'category', 'tags', 'created_at']

        author = serializers.ReadOnlyField(source='author.username')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'category_details']

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'comment']

class AdvertismentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisments
        fields = ['alt', 'image', 'link', 'banner_type']