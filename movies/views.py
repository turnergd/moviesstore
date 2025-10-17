from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib import messages


# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    
    # Get user's rating if logged in
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(user=request.user, movie=movie)
        except Rating.DoesNotExist:
            user_rating = None
    
    # Calculate average rating
    avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    # Count total ratings
    total_ratings = Rating.objects.filter(movie=movie).count()
    
    # Get all ratings with usernames for display
    all_ratings = Rating.objects.filter(movie=movie).select_related('user').order_by('-date')
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    template_data['avg_rating'] = avg_rating
    template_data['total_ratings'] = total_ratings
    template_data['all_ratings'] = all_ratings
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        reviews = Review.objects.filter(movie=movie)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def submit_rating(request, id):
    if request.method == 'POST':
        try:
            rating_value = int(request.POST.get('rating'))
            if rating_value < 1 or rating_value > 5:
                messages.error(request, 'Rating must be between 1 and 5 stars.')
                return redirect('movies.show', id=id)
            
            movie = Movie.objects.get(id=id)
            
            # Update or create rating
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'rating': rating_value}
            )
            
            if created:
                messages.success(request, f'You rated {movie.name} {rating_value} stars!')
            else:
                messages.success(request, f'You updated your rating for {movie.name} to {rating_value} stars!')
                
        except (ValueError, Movie.DoesNotExist):
            messages.error(request, 'Invalid rating or movie.')
        except Exception as e:
            messages.error(request, 'An error occurred while saving your rating.')
    
    return redirect('movies.show', id=id)