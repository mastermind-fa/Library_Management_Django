from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Book, Review, Category
from accounts.models import UserAccount
from transactions.models import Transaction
from .forms import ReviewForm
from transactions.views import send_mail



class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.GET.get('category')
        if slug:
            queryset = queryset.filter(categories__slug=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Add all categories to the context
        return context


# Book Detail View
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

# Borrow Book
@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_account = request.user.account

    if user_account.balance < book.borrowing_price:
        messages.error(request, "Insufficient balance to borrow this book.")
        return redirect('book_detail', pk=pk)

    # Deduct the amount
    user_account.balance -= book.borrowing_price
    user_account.save()

    # Log the transaction
    Transaction.objects.create(
        account=user_account,
        amount=book.borrowing_price,
        balance_after_transaction=user_account.balance,
        transaction_type=3  # Borrow Transaction
    )

    messages.success(request, f"You have successfully borrowed '{book.title}'!")
    send_mail(request.user, request.user.email, book.borrowing_price, 'Borrowed Book Succesfully', 'books/email.html')
    return redirect('book_detail', pk=pk)

# Return Book
@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_account = request.user.account

    # Refund the borrowing price
    user_account.balance += book.borrowing_price
    user_account.save()

    # Log the transaction
    Transaction.objects.create(
        account=user_account,
        amount=-book.borrowing_price,
        balance_after_transaction=user_account.balance,
        transaction_type=2  # Return Transaction
    )

    messages.success(request, f"You have successfully returned '{book.title}'.")
    return redirect('book_detail', pk=pk)

# Review Book
@login_required
def review_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been added!")
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'books/review_form.html', {'form': form, 'book': book})
