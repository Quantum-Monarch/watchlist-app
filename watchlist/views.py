from django.urls import reverse_lazy

from .forms import UserListItemForm, UserListItemFormS, AddMovieForm, AddSeriesForm, MakePublic
from .models import Movies, Series, Film, UserListItem, UserList
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView,PasswordChangeView
from django.core.paginator import Paginator
from .tmdb_api import search_movies, save_tmdb_movie, get_movie_details_from_tmdb


def movie_list(request):
    movies = Movies.objects.all()
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/movies.html', {'movies': movies, 'page_obj': page_obj})


def series_list(request):
    series = Series.objects.all()
    paginator = Paginator(series, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/series.html', {'series': series, 'page_obj': page_obj})


def home_page(request):
    films = Film.objects.all()
    paginator = Paginator(films, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'films': films, 'page_obj': page_obj})


def movie_detail(request, pk):
    movie = get_object_or_404(Movies, pk=pk)
    film = get_object_or_404(Film, pk=pk)
    useritem=get_object_or_404(UserListItem, film=film)
    next_url = request.GET.get('next', None)
    #if next_url=='/':
    #next_url = request.META.get('HTTP_REFERER', '/')
    inwatchlist = False
    if request.user.is_authenticated:
        inwatchlist = UserListItem.objects.filter(userlist__user=request.user, film=film).exists()
    if next_url:
        request.session['next_url'] = next_url
    context = {'movie': movie, 'inwatchlist': inwatchlist, 'next': request.session.get('next_url', '/'),'useritem': useritem}
    return render(request, 'watchlist/movies_details.html', context)


def series_detail(request, pk):
    series = get_object_or_404(Series, pk=pk)
    film = get_object_or_404(Film, pk=pk)
    useritem=get_object_or_404(UserListItem, film=film)
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    #if next_url=='/':
    #next_url = request.META.get('HTTP_REFERER', '/')
    inwatchlist = False
    if request.user.is_authenticated:
        inwatchlist = UserListItem.objects.filter(userlist__user=request.user, film=film).exists()
    if next_url:
        request.session['next_url'] = next_url
    context = {'series': series, 'inwatchlist': inwatchlist, 'next': request.session.get('next_url', '/'),'useritem': useritem}
    return render(request, 'watchlist/series_details.html', context)


class NewLogout(LogoutView):
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
    return render(request, 'watchlist/signup.html', {'form': form})


@login_required(login_url='login')
def mylist(request):
    user_items, created=UserList.objects.get_or_create(
        user=request.user,
        defaults={'ispublic': False, 'name': 'My Watchlist'}
    )
    useritem=UserListItem.objects.filter(userlist=user_items)
    film=[]
    for item in useritem:
        film.append(item)
    paginator = Paginator(film, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/mylist.html', {'films': film, 'page_obj': page_obj,'user_items': user_items,'useritem': useritem})
@login_required(login_url='login')
def profile(request):
    user_items=UserListItem.objects.filter(userlist__user=request.user)
    user=request.user
    count=user_items.count()
    watchedcount=user_items.filter(status='watched').count()
    return render(request,'watchlist/profile.html',{'count':count,'watchedcount':watchedcount,'user':user})


def add_to_watchlist(request, pk):
    print(pk)
    film=Film.objects.filter(tmdb_id=pk).first() or Film.objects.filter(pk=pk).first()
    flag=False
    if not film:
        flag=True
        film=save_tmdb_movie(get_movie_details_from_tmdb(pk),request.user)
    films = Film.objects.all()
    messages.success(request, 'added to watchlist')
    if flag:
        pk=film.film.pk
        film=film.film
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=pk)

    return render(request, 'home.html', {'film': film, 'films': films})


def remove_from_watchlist(request, pk):
    film = get_object_or_404(Film, pk=pk)
    films = Film.objects.all()
    userlist, created=UserList.objects.get_or_create(
        user=request.user,
        defaults={'ispublic': False, 'name': 'My Watchlist'}
    )
    UserListItem.objects.filter(userlist=userlist, film=film).delete()
    messages.success(request, 'removed from watchlist')
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=pk)
    messages.success(request, 'removed from watchlist')
    return render(request, 'home.html', {'film': film, 'films': films})


def edit(request, pk):
    film = get_object_or_404(Film, pk=pk)
    useritem=get_object_or_404(UserListItem,film=film)
    if hasattr(film, 'movies'):
        film = get_object_or_404(Movies, pk=pk)
        form = UserListItemForm(request.POST, instance=useritem)
    else:
        film = get_object_or_404(Series, pk=pk)
        form = UserListItemFormS(request.POST, instance=useritem)
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

    return render(request, 'watchlist/edit.html', {'form': form, 'film': film})


def add_movie(request):
    if request.method == 'POST':
        form = AddMovieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'added movie')
            return redirect('home')
    else:
        form = AddMovieForm()
    return render(request, 'watchlist/add_movie.html', {'form': form})


def add_series(request):
    if request.method == 'POST':
        form = AddSeriesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'added movie')
            return redirect('home')
    else:
        form = AddSeriesForm()
    return render(request, 'watchlist/add_series.html', {'form': form})

def make_public(request):
    userlist=get_object_or_404(UserList, user=request.user)
    if request.method == 'POST':
        form=MakePublic(request.POST,instance=userlist)
        if form.is_valid():
            public_list=form.save(commit=False)
            public_list.ispublic=True
            public_list.save()
            messages.success(request, 'list is public')
            return redirect('watchlist:mylist')
    else:
        form=MakePublic()
    return render(request,'watchlist/makepublic.html', {'form': form})
def make_private(request):
    if request.method == 'POST':
        userlist=get_object_or_404(UserList, user=request.user)
        userlist.ispublic=False
        userlist.save()
        messages.success(request, 'list is private')
    return redirect('watchlist:mylist')


def community_list(request):
    userlists=UserList.objects.filter(ispublic=True)
    paginator = Paginator(userlists, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/communitylist.html', {'page_obj': page_obj, 'userlists': userlists})
def watchlist(request,pk):
    userlist= get_object_or_404(UserList, pk=pk, ispublic=True)
    items=userlist.items.select_related('film')
    films = [item.film for item in items]
    paginator = Paginator(films, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/watchlists.html', {'page_obj': page_obj, 'userlists': userlist,'films': films })

def search_view(request):
    query=request.GET.get('q')
    page_number = request.GET.get('page', 1)
    films=[]
    session_query = request.session.get('last_query')
    session_results = request.session.get('last_results', [])
    if query and query!=session_query:
        films=search_movies(query,page_number)
        request.session['last_query'] = query
        request.session['last_results'] = films
    else:
        films=session_results

    paginator = Paginator(films, 10)
    page_obj = paginator.get_page(page_number)
    request.session.set_expiry(600)
    return render(request,'watchlist/tmdb_search.html', {'films': films, 'query': query, 'page_obj': page_obj})

class CustomPassChange(PasswordChangeView):
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'password changed successfully')
        return super().form_valid(form)
