from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.tag_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_details = models.TextField(default="No description provided.")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

    def popular(self):
        return self.articles.count

        
class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    summary = RichTextField(blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="articles/images")
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    post_views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def num_comments(self):
        return self.comments.count

class Comments(models.Model):
    name = models.CharField(max_length=255, blank=False, default="Anonymous")
    email = models.EmailField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=False)
    created_at = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.name

ad_choices = (
    ("square", "SQUARE"),
    ("horizontal_rectangle", "HORIZONTAL_RECTABGLE"),
    ("vertical_rectangle", "VERTICAL_RECTANGLE"),
)
class Advertisments(models.Model):
    alt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="advertisements")
    link = models.URLField(max_length=200)
    banner_type = models.CharField(max_length=30, choices=ad_choices, default="square")

    class Meta:
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return self.alt