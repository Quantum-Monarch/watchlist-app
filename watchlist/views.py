from django.urls import reverse_lazy

from .forms import UserListItemForm, UserListItemFormS, AddMovieForm, AddSeriesForm
from .models import Movies, Series, Film, UserListItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView

def movie_list(request):
    movies = Movies.objects.all()
    return render(request, 'watchlist/movies.html', {'movies':movies})
def series_list(request):
    series = Series.objects.all()
    return render(request, 'watchlist/series.html', {'series':series})
def home_page(request):
    films = Film.objects.all()
    return render(request, 'home.html', {'films':films})

def movie_detail(request,pk):
    movie =  get_object_or_404(Movies,pk=pk)
    film =get_object_or_404(Film,pk=pk)
    next_url = request.GET.get('next',None)
    #if next_url=='/':
        #next_url = request.META.get('HTTP_REFERER', '/')
    inwatchlist=False
    if request.user.is_authenticated:
        inwatchlist=UserListItem.objects.filter(user=request.user,film=film).exists()
    if next_url:
        request.session['next_url'] = next_url
    context={'movie':movie, 'inwatchlist':inwatchlist, 'next':request.session.get('next_url','/')}
    return render(request, 'watchlist/movies_details.html', context)
def series_detail(request,pk):
    series = get_object_or_404(Series,pk=pk)
    film = get_object_or_404(Film, pk=pk)
    next_url = request.GET.get('next',request.META.get('HTTP_REFERER', '/'))
    #if next_url=='/':
        #next_url = request.META.get('HTTP_REFERER', '/')
    inwatchlist = False
    if request.user.is_authenticated:
        inwatchlist = UserListItem.objects.filter(user=request.user, film=film).exists()
    if next_url:
        request.session['next_url'] = next_url
    context = {'series': series, 'inwatchlist': inwatchlist, 'next': request.session.get('next_url', '/')}
    return render(request,'watchlist/series_details.html', context)

class newlogout(LogoutView):
    next_page = reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have successfully logged out')
        return super().dispatch(request, *args, **kwargs)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'there was an error with your signup please try again')
    else:
        form = UserCreationForm()
    return render(request,'watchlist/signup.html',{'form':form})
@login_required(login_url='login')
def mylist(request):
    user_items=UserListItem.objects.filter(user=request.user).select_related('film')
    films=[item.film for item in user_items]
    return render(request,'watchlist/mylist.html',{'films':films})
def add_to_watchlist(request,pk):
    film = get_object_or_404(Film,pk=pk)
    films=Film.objects.all()
    UserListItem.objects.create(user=request.user,film=film)
    messages.success(request, 'added to watchlist')
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=pk)

    return render(request,'home.html',{'film':film,'films':films})
def remove_from_watchlist(request,pk):
    film = get_object_or_404(Film,pk=pk)
    films=Film.objects.all()
    UserListItem.objects.filter(user=request.user,film=film).delete()
    messages.success(request, 'removed from watchlist')
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail',pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail',pk=pk)
    messages.success(request, 'removed from watchlist')
    return render(request,'home.html',{'film':film,'films':films})
def edit(request,pk):
    film = get_object_or_404(Film,pk=pk)
    if hasattr(film, 'movies'):
        film = get_object_or_404(Movies, pk=pk)
        form = UserListItemForm(request.POST, instance=film)
    else:
        film = get_object_or_404(Series, pk=pk)
        form = UserListItemFormS(request.POST, instance=film)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'changes saved')
            if isinstance(film, Movies):
                return redirect('watchlist:movie_detail', pk=pk)
            elif isinstance(film, Series):
                return redirect('watchlist:series_detail', pk=pk)

            return redirect('home')
        else:
            form = UserListItemForm(instance=film)

    return render(request,'watchlist/edit.html',{'form':form, 'film':film})

def add_movie(request):
    if request.method == 'POST':
        form=AddMovieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'added movie')
            return redirect('home')
    else:
        form=AddMovieForm()
    return render(request, 'watchlist/add_movie.html',{'form':form})

def add_series(request):
    if request.method == 'POST':
        form=AddSeriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'added movie')
            return redirect('home')
    else:
        form=AddSeriesForm()
    return render(request, 'watchlist/add_series.html',{'form':form})