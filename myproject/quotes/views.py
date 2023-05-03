from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Count
from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    quotes = Quote.objects.all().order_by('-id')
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'add_quote.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('home')
    else:
        form = QuoteForm()
        return render(request, 'add_quote.html', {'form': form})


def author_detail(request, author_id):
    author = Author.objects.get(pk=author_id)
    quotes = author.quote_set.all()
    return render(request, 'author_detail.html', {'author': author, 'quotes': quotes})


def tag_detail(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = tag.quote_set.all()
    return render(request, 'tag_detail.html', {'tag': tag, 'quotes': quotes})


def search(request):
    query = request.GET.get('q')
    if query:
        quotes = Quote.objects.filter(Q(text__icontains=query) | Q(tags__name__icontains=query))
    else:
        quotes = Quote.objects.all()
    return render(request, 'search_results.html', {'quotes': quotes, 'query': query})


def top_tags(request):
    tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'top_tags.html', {'tags': tags})
