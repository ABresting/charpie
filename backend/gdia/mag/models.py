from django.db import models

# Create your models here.


class Magazine(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    article_id = models.IntegerField(unique=True, default=0)
    author = models.CharField(max_length=200)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE)
    edition = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField()
    images = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
