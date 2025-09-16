from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')


def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')


# Create your views here.
#from django.contrib.auth.forms import UserCreationForm
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

def get_subscription_level(total_spent):
    """Calculate subscription level based on total spending"""
    if total_spent < 15:
        return 'Basic'
    elif total_spent < 30:
        return 'Medium'
    else:
        return 'Premium'

@login_required
def subscription(request):
    template_data = {}
    template_data['title'] = 'My Subscription'
    
    # Calculate total spending from all orders
    user_orders = Order.objects.filter(user=request.user)
    total_spent = sum(order.total for order in user_orders)
    
    # Get subscription level
    subscription_level = get_subscription_level(total_spent)
    
    # Calculate progress to next level
    if subscription_level == 'Basic':
        progress_to_next = (total_spent / 15) * 100
        next_level = 'Medium'
        amount_needed = 15 - total_spent
    elif subscription_level == 'Medium':
        progress_to_next = ((total_spent - 15) / 15) * 100
        next_level = 'Premium'
        amount_needed = 30 - total_spent
    else:  # Premium
        progress_to_next = 100
        next_level = None
        amount_needed = 0
    
    template_data['total_spent'] = total_spent
    template_data['subscription_level'] = subscription_level
    template_data['progress_to_next'] = min(progress_to_next, 100)
    template_data['next_level'] = next_level
    template_data['amount_needed'] = amount_needed
    template_data['orders_count'] = user_orders.count()
    
    return render(request, 'accounts/subscription.html',
        {'template_data': template_data})