from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import TouristPlace, Favorite, ChatMessage
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignUpForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .chatbot import TouristChatbot
import json
import uuid
from django.contrib.auth import logout
from django.shortcuts import render

# Create your views here.

def home(request):
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    district_filter = request.GET.get('district', '')
    
    # Get all places
    places = TouristPlace.objects.all()
    
    # Apply search filter
    if search_query:
        places = places.filter(
            Q(name__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Apply category filter
    if category_filter:
        places = places.filter(category=category_filter)
    
    # Apply district filter
    if district_filter:
        places = places.filter(district=district_filter)
    
    # Get featured places for carousel
    featured_places = TouristPlace.objects.filter(featured=True)[:5]
    
    # Pagination
    paginator = Paginator(places, 9)  # 9 places per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique categories and districts for filter dropdowns
    categories = TouristPlace.objects.values_list('category', flat=True).distinct()
    districts = TouristPlace.objects.values_list('district', flat=True).distinct()
    
    # Check if user has favorites
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('place_id', flat=True)
    
    context = {
        'places': page_obj,
        'featured_places': featured_places,
        'categories': categories,
        'districts': districts,
        'search_query': search_query,
        'category_filter': category_filter,
        'district_filter': district_filter,
        'user_favorites': user_favorites,
    }
    return render(request, 'destinations/home.html', context)

def place_detail(request, pk):
    place = get_object_or_404(TouristPlace, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, place=place).exists()
    
    context = {
        'place': place,
        'is_favorite': is_favorite,
    }
    return render(request, 'destinations/place_detail.html', context)

@login_required
@require_POST
def toggle_favorite(request, pk):
    place = get_object_or_404(TouristPlace, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, place=place)
    
    if not created:
        favorite.delete()
        return JsonResponse({'success': True, 'action': 'removed'})
    else:
        return JsonResponse({'success': True, 'action': 'added'})

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_login')
    else:
        form = CustomSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def chatbot(request):
    """Main chatbot interface"""
    places = TouristPlace.objects.all().order_by('name')
    selected_place_id = request.GET.get('place_id')
    
    context = {
        'places': places,
        'selected_place_id': selected_place_id,
    }
    return render(request, 'destinations/chatbot.html', context)

@login_required
@csrf_exempt
def chat_api(request):
    """API endpoint for chatbot responses"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            place_id = data.get('place_id')
            session_id = data.get('session_id')
            
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            # Initialize chatbot
            chatbot = TouristChatbot()
            
            # Get place if specified
            place = None
            if place_id:
                try:
                    place = TouristPlace.objects.get(id=place_id)
                except TouristPlace.DoesNotExist:
                    pass
            
            # Get chat history for context
            chat_history = []
            if session_id:
                chat_history = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
            
            # Generate response
            if place:
                response = chatbot.generate_response(message, place, chat_history)
            else:
                response = chatbot.get_general_response(message)
            
            # Save chat message
            chat_message = ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                place=place,
                message=message,
                response=response,
                session_id=session_id
            )
            
            return JsonResponse({
                'response': response,
                'message_id': chat_message.id,
                'timestamp': chat_message.created_at.isoformat()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def get_chat_history(request):
    """Get chat history for a session"""
    session_id = request.GET.get('session_id')
    if not session_id:
        return JsonResponse({'messages': []})
    
    messages = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
    message_list = []
    
    for msg in messages:
        message_list.append({
            'id': msg.id,
            'message': msg.message,
            'response': msg.response,
            'timestamp': msg.created_at.isoformat(),
            'is_user': True
        })
        message_list.append({
            'id': f"resp_{msg.id}",
            'message': msg.response,
            'response': '',
            'timestamp': msg.created_at.isoformat(),
            'is_user': False
        })
    
    return JsonResponse({'messages': message_list})

def custom_logout(request):
    logout(request)
    return render(request, 'account/logout.html')
