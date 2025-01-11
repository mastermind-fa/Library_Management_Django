from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('borrow/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('review/<int:pk>/', views.review_book, name='review_book'),
]
