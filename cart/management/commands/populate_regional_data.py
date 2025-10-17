from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cart.models import Order, Item
from movies.models import Movie
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populates sample regional purchase data for the trending map'

    def handle(self, *args, **kwargs):
        regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Oceania']
        region_coords = {
            'North America': {'lat': 39.8283, 'lng': -98.5795},
            'Europe': {'lat': 54.5260, 'lng': 15.2551},
            'Asia': {'lat': 34.0479, 'lng': 100.6197},
            'South America': {'lat': -8.7832, 'lng': -55.4915},
            'Africa': {'lat': -8.7832, 'lng': 34.5085},
            'Oceania': {'lat': -22.7359, 'lng': 140.0188},
        }

        # Get all movies
        movies = list(Movie.objects.all())
        if not movies:
            self.stdout.write(self.style.WARNING('No movies found in database. Please add movies first.'))
            return

        # Get or create a demo user
        user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@moviesstore.com'}
        )
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created demo user: demo_user'))

        # Create sample orders for each region
        orders_created = 0
        for region in regions:
            coords = region_coords[region]
            
            # Create 5-15 random orders per region
            num_orders = random.randint(5, 15)
            
            for i in range(num_orders):
                # Random date within last 30 days
                days_ago = random.randint(0, 30)
                order_date = datetime.now() - timedelta(days=days_ago)
                
                # Select random movies (1-3 movies per order)
                num_movies = random.randint(1, 3)
                selected_movies = random.sample(movies, min(num_movies, len(movies)))
                
                # Calculate total
                total = sum(movie.price * random.randint(1, 3) for movie in selected_movies)
                
                # Create order
                order = Order.objects.create(
                    user=user,
                    total=total,
                    region=region,
                    latitude=coords['lat'] + random.uniform(-5, 5),  # Add some variation
                    longitude=coords['lng'] + random.uniform(-5, 5),
                )
                order.date = order_date
                order.save()
                
                # Create items for this order
                for movie in selected_movies:
                    quantity = random.randint(1, 3)
                    Item.objects.create(
                        movie=movie,
                        price=movie.price,
                        order=order,
                        quantity=quantity
                    )
                
                orders_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {orders_created} sample orders across {len(regions)} regions'))
        self.stdout.write(self.style.SUCCESS('You can now view the trending map at /cart/map/'))

