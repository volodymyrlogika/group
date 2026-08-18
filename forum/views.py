from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Thread, Post
from .forms import ThreadForm, PostForm

# Create your views here.

def forum_home(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'forum/home.html', {'threads': threads})

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

@login_required
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user.is_staff or request.user == thread.creator:
        thread.delete()
    return redirect('forum_home')