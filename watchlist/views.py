from django.core.cache import cache
from django.urls import reverse_lazy
from .load_data import userprefs,userlists,userlistitems
from .forms import UserListItemForm, UserListItemFormS, MakePublic
from .models import Movies, Series, Film, UserListItem, UserList, UserPreferences
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LogoutView,PasswordChangeView
from django.core.paginator import Paginator
from .tmdb_api import search_movies, save_tmdb_movie, get_movie_details_from_tmdb
from .MLrecomender import  recommend
films_qs=cache.get('all_films')
if not films_qs:
    films_qs=Film.objects.all()
    cache.set('all_films',films_qs,timeout=300)

def movie_list(request):
    m=Movies.objects.all().order_by('id')
    paginator = Paginator(m, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/movies.html', {'movies': m, 'page_obj': page_obj})


def series_list(request):
    s=Series.objects.all()
    paginator = Paginator(s, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/series.html', {'series': s, 'page_obj': page_obj})


def home_page(request):
    reclist=[]
    if request.user.is_authenticated:
        user=request.user
        p,created=UserPreferences.objects.get_or_create(user=user)
        recs=recommend(p.main_vector,films_qs)
        for item in recs:
            reclist.append(get_object_or_404(films_qs,tmdb_id=item))
    f=Film.objects.all().order_by('id')
    paginator = Paginator(f, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'films': f, 'page_obj': page_obj,'reclist':reclist})


def movie_detail(request, pk):
    movie = get_object_or_404(Movies, pk=pk)
    film = get_object_or_404(Film, pk=pk)
    next_url = request.GET.get('next', None)
    useritem=movie
    #if next_url=='/':
    #next_url = request.META.get('HTTP_REFERER', '/')
    inwatchlist = False
    if request.user.is_authenticated:
        inwatchlist = UserListItem.objects.filter(userlist__user=request.user, film=film).exists()
        if inwatchlist:
            useritem = get_object_or_404(UserListItem, film=film)
    if next_url:
        request.session['next_url'] = next_url
    context = {'movie': movie, 'inwatchlist': inwatchlist, 'next': request.session.get('next_url', '/'),'useritem': useritem}
    return render(request, 'watchlist/movies_details.html', context)


def series_detail(request, pk):
    serie = get_object_or_404(Series, pk=pk)
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
    context = {'series': serie, 'inwatchlist': inwatchlist, 'next': request.session.get('next_url', '/'),'useritem': useritem}
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
            user=form.save()
            UserPreferences.objects.create(user=user)
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'there was an error with your signup please try again')
    else:
        form = UserCreationForm()
    return render(request, 'watchlist/signup.html', {'form': form})


@login_required(login_url='login')
def mylist(request):
    user_items, created=userlists.get_or_create(
        user=request.user,
        defaults={'ispublic': False, 'name': 'My Watchlist'}
    )
    useritem=userlistitems.filter(userlist=user_items)
    film=[]
    for item in useritem:
        film.append(item)
    paginator = Paginator(film, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/mylist.html', {'films': film, 'page_obj': page_obj,'user_items': user_items,'useritem': useritem})
@login_required(login_url='login')
def profile(request):
    user_items=userlistitems.filter(userlist__user=request.user)
    user=request.user
    count=user_items.count()
    watchedcount=user_items.filter(status='watched').count()
    return render(request,'watchlist/profile.html',{'count':count,'watchedcount':watchedcount,'user':user})


def add_to_watchlist(request, pk,b=Film.objects):
    print(pk)
    user=request.user
    film= b.filter(pk=pk).first()
    if not film:
        film=save_tmdb_movie(get_movie_details_from_tmdb(pk),user)
    user_items, created=userlists.get_or_create(
        user=request.user,
        defaults={'ispublic': False, 'name': 'My Watchlist'}
        )
    UserListItem.objects.get_or_create(userlist=user_items, film=film)
    prefs,created=userprefs.get_or_create(user=user)
    prefs.edit_main_vector(film.main_vector)
    messages.success(request, 'added to watchlist')
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=film.id)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=film.id)

    return render(request, 'home.html', {'film': film, 'films': b})


def remove_from_watchlist(request, pk):
    film = get_object_or_404(Film, pk=pk)
    userlist, created=userlists.get_or_create(
        user=request.user,
        defaults={'ispublic': False, 'name': 'My Watchlist'}
    )
    userlistitems.filter(userlist=userlist, film=film).delete()
    prefs,created=userprefs.get_or_create(user=request.user)
    prefs.edit_main_vector_remove(film.main_vector)
    messages.success(request, 'removed from watchlist')
    if hasattr(film, 'movies'):
        return redirect('watchlist:movie_detail', pk=pk)
    elif hasattr(film, 'series'):
        return redirect('watchlist:series_detail', pk=pk)
    messages.success(request, 'removed from watchlist')
    return render(request, 'home.html', {'film': film, 'films': films_qs})


def edit(request, pk):
    film = get_object_or_404(Film, pk=pk)
    useritem=get_object_or_404(userlistitems,film=film)
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

def make_public(request):
    userlist=get_object_or_404(userlists, user=request.user)
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
        userlist=get_object_or_404(userlists, user=request.user)
        userlist.ispublic=False
        userlist.save()
        messages.success(request, 'list is private')
    return redirect('watchlist:mylist')


def community_list(request):
    user_lists=userlists.filter(ispublic=True)
    paginator = Paginator(user_lists, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'watchlist/communitylist.html', {'page_obj': page_obj, 'userlists': user_lists})
def watchlist(request,pk):
    userlist= get_object_or_404(userlists, pk=pk, ispublic=True)
    items=userlistitems.select_related('film')
    films = [item.film for item in items]
    paginator = Paginator(films, 12)
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

