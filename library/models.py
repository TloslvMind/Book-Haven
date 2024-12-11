from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=False)
    genre_image = models.ImageField(upload_to='genre_images/', null=True)


    def __str__(self):
        return self.genre_name


class Book(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'PUBLISHED'

    title = models.CharField(max_length=120, blank=False)
    slug = models.SlugField(max_length=120, unique=True, blank=False)
    author = models.CharField(max_length=120, blank=False)
    description = models.TextField(blank=False)
    summary = models.TextField()
    file = models.FileField(upload_to='books/', blank=True)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='cover_images/')
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('library:book_detail', args=[self.slug])


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.book}"