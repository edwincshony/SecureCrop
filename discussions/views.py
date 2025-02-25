# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Thread, Post, Reply
from .forms import ThreadForm, PostForm, ReplyForm,CategoryForm

# views.py
@login_required
def category_list(request):
    categories = Category.objects.all()
    can_add_category = request.user.role == 'botanist'
    return render(request, 'cdiscussions/category_list.html', {'categories': categories, 'can_add_category': can_add_category})

def thread_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = Thread.objects.filter(category=category)
    return render(request, 'cdiscussions/thread_list.html', {'category': category, 'threads': threads})

@login_required
def create_thread(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.category = category
            thread.save()
            return redirect('thread_list', category_id=category.id)
    else:
        form = ThreadForm()
    return render(request, 'cdiscussions/create_thread.html', {'form': form, 'category': category})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = Post.objects.filter(thread=thread)
    return render(request, 'cdiscussions/thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.thread = thread
            post.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'cdiscussions/create_post.html', {'form': form, 'thread': thread})

@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.created_by = request.user
            reply.post = post
            reply.save()
            return redirect('thread_detail', thread_id=post.thread.id)
    else:
        form = ReplyForm()
    return render(request, 'cdiscussions/reply_to_post.html', {'form': form, 'post': post})

@login_required
def add_category(request):
    if request.user.role != 'botanist':
        return redirect('category_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'cdiscussions/add_category.html', {'form': form})