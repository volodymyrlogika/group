from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Thread, Post
from .forms import ThreadForm, PostForm

def is_staff_user(user):
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        return True
    raise PermissionDenied

def forum_home(request):
    threads_list = Thread.objects.all().order_by('-created_at')
    
    # Кількість тредів на сторінку (залиште 1 для тесту або змініть на 20)
    paginator = Paginator(threads_list, 10) 
    
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
    except ValueError:
        page_number = 1
        
    threads = paginator.get_page(page_number)
    total_pages = paginator.num_pages

    # 🟢 РОЗРАХУНОК ФІКСОВАНИХ 5 СТОРІНОК ДЛЯ ШАБЛОНУ
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        start = page_number - 2
        end = page_number + 2
        
        # Перевірка меж, щоб завжди виводилося рівно 5 кнопок
        if start < 1:
            start = 1
            end = 5
        elif end > total_pages:
            end = total_pages
            start = total_pages - 4
            
        page_range = range(start, end + 1)

    return render(request, 'forum/home.html', {
        'threads': threads,
        'custom_page_range': page_range
    })

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all().order_by('created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.thread = thread
            new_post.author = request.user
            new_post.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        post_form = PostForm()

    return render(request, 'forum/thread_detail.html', {'thread': thread, 'posts': posts, 'post_form': post_form})

@user_passes_test(is_staff_user)
def thread_create(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            new_thread = form.save(commit=False)
            new_thread.creator = request.user 
            new_thread.save()
            return redirect('thread_detail', thread_id=new_thread.id)
    else:
        form = ThreadForm()
    return render(request, 'forum/thread_create.html', {'form': form})

@require_POST
def increment_views(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.views_count += 1
    thread.save(update_fields=['views_count'])
    return JsonResponse({'status': 'success', 'views_count': thread.views_count})

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user.is_staff or request.user == thread.creator:
        thread.delete()
    return redirect('forum_home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.dislikes.remove(request.user)
        post.likes.add(request.user)
    return redirect('thread_detail', thread_id=post.thread.id)

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
    return redirect('thread_detail', thread_id=post.thread.id)
