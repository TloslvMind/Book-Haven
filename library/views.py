from django.db.migrations import swappable_dependency
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import CommentForm, EmailForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def library(request):
    return render(request, 'library/index.html', context={'section': 'main'})


def book_detail(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, status="PB")
    books_tags_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.published.filter(tags__in=books_tags_ids).exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {'book': book, "similar_books": similar_books}
    return render(request, 'library/book_detail.html', context)


def genres(request):
    genres_list = Genre.objects.all()
    return render(request, 'library/genres.html', {'genres_list': genres_list, 'section': 'genres'})


def get_books_by_genre(request, genre_name):
    books_by_genre_list = Book.published.filter(genre__genre_name=genre_name)
    return render(request, 'library/books_by_genre.html', {'books': books_by_genre_list})


def summary(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, status="PB")
    return render(request, 'library/summary.html', {'book': book})


def comment_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, status="PB")
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.book = book
            new_comment.save()
            messages.success(request, 'Ваш коментар було додано!')
            return redirect('library:book_detail', book_slug)

    return render(request, 'library/comment.html', {'book': book, 'form': form})


def recommend_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, status="PB")
    form = EmailForm()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            book_url = request.build_absolute_uri(book.get_absolute_url())
            subject = (f"{cd['name']} {cd['email']}"
                       f"рекомендує прочитати {book.title}")
            message = (f"Read {book.title} at {book_url}"
                       f"{cd['name']}' comment: {cd['comment']}")

            send_mail(subject=subject,
                      message=message,
                      from_email=cd['email'],
                      recipient_list=[cd['to']],)

            messages.success(request, 'Вашу рекомендацію було відправлено!')
            return redirect('library:book_detail', book_slug)
    return render(request, 'library/recommend_book.html', {"book": book, 'form': form})


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.published.annotate(similarity=
                              TrigramSimilarity('title', query) +
                              TrigramSimilarity('author', query) +
                              TrigramSimilarity('description', query) +
                              TrigramSimilarity('summary', query) +
                              TrigramSimilarity('genre__genre_name', query) +
                              TrigramSimilarity('genre__description', query) +
                              TrigramSimilarity('genre__slug', query) +
                              TrigramSimilarity('slug', query)
                                              ).filter(similarity__gt=0.15).order_by('-similarity')

        return render(request, 'library/search_results.html', {'results': results})


def books_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    books_by_tag_list = Book.published.filter(tags__in=[tag])
    return render(request, 'library/books_by_tag.html', {'books': books_by_tag_list})