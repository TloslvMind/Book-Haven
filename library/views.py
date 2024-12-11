from django.db.migrations import swappable_dependency
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import CommentForm, EmailForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib import messages
# Create your views here.
def library(request):
    return render(request, 'library/index.html')


def latest_books(request):
    latest_books_list = Book.published.all()
    return render(request, 'library/landing.html', {'books': latest_books_list})


def book_detail(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, status="PB")

    context = {'book': book}
    return render(request, 'library/book_detail.html', context)


def genres(request):
    genres_list = Genre.objects.all()
    return render(request, 'library/genres.html', {'genres_list': genres_list})


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