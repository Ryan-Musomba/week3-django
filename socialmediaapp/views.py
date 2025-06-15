from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post, Comment
import cloudinary.uploader

@login_required
def home(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            messages.error(request, "Post cannot be empty")
            return redirect('home')
        
        image = request.FILES.get('image')
        post = Post(user=request.user, text=text)
        
        if image:
            try:
                result = cloudinary.uploader.upload(image, folder='posts')
                post.image = result['secure_url']
            except Exception as e:
                messages.error(request, "Error uploading image")
                print(f"Image upload error: {e}")
        
        post.save()
        messages.success(request, "Post created successfully")
        return redirect('home')

    posts = Post.objects.all().order_by('-created')
    return render(request, 'home.html', {'posts': posts})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, "Please fill all fields")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not all([username, email, password]):
            messages.error(request, "Please fill all fields")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, "Error creating account")
            print(f"Registration error: {e}")
    
    return render(request, 'register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        if request.user == profile_user:
            # Update profile
            bio = request.POST.get('bio', '').strip()
            picture = request.FILES.get('picture')
            
            profile_user.bio = bio
            if picture:
                try:
                    result = cloudinary.uploader.upload(picture, folder='profiles')
                    profile_user.picture = result['secure_url']
                    messages.success(request, "Profile picture updated")
                except Exception as e:
                    messages.error(request, "Error updating profile picture")
                    print(f"Profile picture error: {e}")
            
            profile_user.save()
            messages.success(request, "Profile updated")
            return redirect('profile', username=username)
        elif 'follow' in request.POST:
            # Handle follow/unfollow
            if request.user in profile_user.followers.all():
                profile_user.followers.remove(request.user)
                request.user.following.remove(profile_user)
                messages.success(request, f"You have unfollowed {profile_user.username}")
            else:
                profile_user.followers.add(request.user)
                request.user.following.add(profile_user)
                messages.success(request, f"You are now following {profile_user.username}")
            return redirect('profile', username=username)
    
    posts = profile_user.post_set.all().order_by('-created')
    is_following = request.user in profile_user.followers.all() if request.user.is_authenticated else False
    return render(request, 'profile.html', {
        'profile': profile_user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': profile_user.followers.count(),
        'following_count': profile_user.following.count()
    })

@login_required
def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        if 'delete' in request.POST and request.user == post.user:
            post.delete()
            messages.success(request, "Post deleted")
            return redirect('home')
        
        if 'comment' in request.POST:
            text = request.POST.get('text', '').strip()
            if text:
                Comment.objects.create(post=post, user=request.user, text=text)
                messages.success(request, "Comment added")
            else:
                messages.error(request, "Comment cannot be empty")
            return redirect('post', pk=pk)
    
    return render(request, 'post.html', {'post': post})

@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    users = []
    if query:
        users = User.objects.filter(username__icontains=query)
    return render(request, 'search.html', {
        'users': users,
        'query': query
    })

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))