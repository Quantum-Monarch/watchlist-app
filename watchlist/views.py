

from .forms import UserListItemForm,UserListItemFormS
from .models import Movies, Series, Film, UserListItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
def movie_list(request):
    movies = Movies.objects.all()
    return render(request, 'watchlist/movies.html', {'movies':movies})
def series_list(request):
    series = Series.objects.all()
    return render(request, 'watchlist/series.html', {'series':series})
def home_page(request):
    films = Film.objects.all()
    return render(request, 'watchlist/films.html', {'films':films})

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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=pk)

    return render(request,'watchlist/films.html',{'film':film,'films':films})
def remove_from_watchlist(request,pk):
    film = get_object_or_404(Film,pk=pk)
    films=Film.objects.all()
    UserListItem.objects.filter(user=request.user,film=film).delete()
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail',pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail',pk=pk)

    return render(request,'watchlist/films.html',{'film':film,'films':films})
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
            if isinstance(film, Movies):
                return redirect('watchlist:movie_detail', pk=pk)
            elif isinstance(film, Series):
                return redirect('watchlist:series_detail', pk=pk)

            return redirect('home')
        else:
            form = UserListItemForm(instance=film)
    return render(request,'watchlist/edit.html',{'form':form})
