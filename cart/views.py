from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum


from .utils import calculate_cart_total
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})


def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    
    # Get user's location from session or request (simplified for demo)
    # In production, you'd use IP geolocation or user profile data
    order.region = request.session.get('region', 'Unknown')
    order.latitude = request.session.get('latitude', None)
    order.longitude = request.session.get('longitude', None)
    
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})

@login_required
def map_view(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'
    # Get user's recent purchases for comparison
    user_orders = Order.objects.filter(user=request.user).prefetch_related('item_set__movie')
    user_movies = []
    for order in user_orders:
        for item in order.item_set.all():
            user_movies.append({
                'id': item.movie.id,
                'name': item.movie.name,
                'quantity': item.quantity,
                'date': order.date.strftime('%Y-%m-%d')
            })
    template_data['user_purchases'] = user_movies
    return render(request, 'cart/map.html', {'template_data': template_data})

@login_required
def map_data_api(request):
    """API endpoint to get trending movies by region"""
    # Define sample regions with coordinates (in production, use a real geo database)
    regions = {
        'North America': {'lat': 39.8283, 'lng': -98.5795},
        'Europe': {'lat': 54.5260, 'lng': 15.2551},
        'Asia': {'lat': 34.0479, 'lng': 100.6197},
        'South America': {'lat': -8.7832, 'lng': -55.4915},
        'Africa': {'lat': -8.7832, 'lng': 34.5085},
        'Oceania': {'lat': -22.7359, 'lng': 140.0188},
    }
    
    # Get trending data by region
    regional_data = []
    
    for region_name, coords in regions.items():
        # Get orders for this region
        region_orders = Order.objects.filter(region=region_name)
        
        # If no specific region data, assign random sample data for demo
        if not region_orders.exists():
            # Get top movies overall and assign to regions for demo
            top_items = Item.objects.values('movie__id', 'movie__name', 'movie__price').annotate(
                total_quantity=Sum('quantity'),
                purchase_count=Count('id')
            ).order_by('-total_quantity')[:3]
            
            movies_list = []
            for item in top_items:
                movies_list.append({
                    'movie_id': item['movie__id'],
                    'movie_name': item['movie__name'],
                    'purchase_count': item['purchase_count'],
                    'total_quantity': item['total_quantity']
                })
        else:
            # Get actual trending movies for this region
            items_in_region = Item.objects.filter(
                order__region=region_name
            ).values('movie__id', 'movie__name').annotate(
                total_quantity=Sum('quantity'),
                purchase_count=Count('id')
            ).order_by('-total_quantity')[:5]
            
            movies_list = []
            for item in items_in_region:
                movies_list.append({
                    'movie_id': item['movie__id'],
                    'movie_name': item['movie__name'],
                    'purchase_count': item['purchase_count'],
                    'total_quantity': item['total_quantity']
                })
        
        regional_data.append({
            'region': region_name,
            'latitude': coords['lat'],
            'longitude': coords['lng'],
            'trending_movies': movies_list
        })
    
    return JsonResponse({'regions': regional_data})

def set_location(request):
    """Allow users to set their location (simplified for demo)"""
    if request.method == 'POST':
        region = request.POST.get('region', 'Unknown')
        latitude = request.POST.get('latitude', None)
        longitude = request.POST.get('longitude', None)
        
        request.session['region'] = region
        if latitude:
            request.session['latitude'] = float(latitude)
        if longitude:
            request.session['longitude'] = float(longitude)
        
        return JsonResponse({'success': True, 'region': region})