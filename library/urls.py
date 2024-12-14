from django.urls import path
from . import views
app_name = 'library'

urlpatterns = [
    path('', views.library, name='index'),
    path('books_by_tag/<slug:tag_slug>', views.books_by_tag, name="books_by_tag"),
    path('books_by_genre/<str:genre_name>/', views.get_books_by_genre, name='books_by_genre'),
    path('comment_book/<slug:book_slug>/', views.comment_book, name='comment_book'),
    path('recommend_book/<slug:book_slug>/', views.recommend_book, name='recommend_book'),
    path('search/', views.search, name='search'),
    path('genres/', views.genres, name='genres'),
    path('summary/<slug:book_slug>/', views.summary, name='summary'),
    # path('pdf/<slug:book_slug>/<str:file_url>/', views.book_detail, name='book_detail'),
    path('book_detail/<slug:book_slug>/', views.book_detail, name='book_detail'),
]