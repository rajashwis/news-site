from django.db import models

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField()
    image = models.ImageField(upload_to="articles/images")
    tags = models.ManyToManyField(Tag)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


