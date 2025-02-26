from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Category, Thread, Post, Reply
from .forms import ThreadForm, PostForm, ReplyForm, CategoryForm
from accounts.models import CustomUser
from notifications.models import Notification  # For notifications on replies or pins

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('-created_at')
    can_add_category = request.user.role in ['agricultural_expert', 'admin']
    context = {
        'categories': categories,
        'can_add_category': can_add_category,
    }
    return render(request, 'discussions/category_list.html', context)

@login_required
def thread_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    threads = Thread.objects.filter(category=category).order_by('-updated_at')
    allowed_roles = ['farmer', 'agricultural_expert', 'admin']  # Define roles in the view
    context = {
        'category': category,
        'threads': threads,
        'allowed_roles': allowed_roles,
    }
    return render(request, 'discussions/thread_list.html', context)

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
            return redirect('discussions:thread_list', category_id=category.id)
    else:
        form = ThreadForm()
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'discussions/create_thread.html', context)

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = Post.objects.filter(thread=thread).order_by('created_at')
    can_pin = request.user.role in ['agricultural_expert', 'admin']
    form = PostForm() if request.user.role in ['farmer', 'agricultural_expert', 'admin'] else None
    context = {
        'thread': thread,
        'posts': posts,
        'form': form,
        'can_pin': can_pin,
    }
    return render(request, 'discussions/thread_detail.html', context)

@login_required
def create_post(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user.role not in ['farmer', 'agricultural_expert', 'admin']:
        messages.error(request, "You don’t have permission to post in discussions.")
        return redirect('discussions:thread_detail', thread_id=thread.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.thread = thread
            post.save()
            return redirect('discussions:thread_detail', thread_id=thread.id)
    else:
        form = PostForm()
    context = {
        'form': form,
        'thread': thread,
    }
    return render(request, 'discussions/create_post.html', context)

@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.role not in ['farmer', 'agricultural_expert', 'admin']:
        messages.error(request, "You don’t have permission to reply in discussions.")
        return redirect('discussions:thread_detail', thread_id=post.thread.id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.created_by = request.user
            reply.post = post
            reply.save()
            # Notify the thread creator or other participants
            Notification.objects.create(
                user=post.thread.created_by,
                title=f"New Reply in {post.thread.title}",
                message=f"{request.user.username} replied to your thread '{post.thread.title}'.",
                url=reverse('discussions:thread_detail', kwargs={'thread_id': post.thread.id})
            )
            return redirect('discussions:thread_detail', thread_id=post.thread.id)
    else:
        form = ReplyForm()
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'discussions/reply_to_post.html', context)

@login_required
def add_category(request):
    if request.user.role not in ['agricultural_expert', 'admin']:
        messages.error(request, "Only experts and admins can add categories.")
        return redirect('discussions:category_list')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            return redirect('discussions:category_list')
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'discussions/add_category.html', context)

@login_required
def pin_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user.role not in ['agricultural_expert', 'admin']:
        messages.error(request, "Only experts and admins can pin threads.")
        return redirect('discussions:thread_detail', thread_id=thread.id)
    
    thread.is_pinned = not thread.is_pinned
    thread.save()
    messages.success(request, f"Thread {'pinned' if thread.is_pinned else 'unpinned'} successfully.")
    return redirect('discussions:thread_detail', thread_id=thread.id)

@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.downvotes.all():
        post.downvotes.remove(user)
    post.upvotes.add(user)
    return redirect('discussions:thread_detail', thread_id=post.thread.id)

@login_required
def downvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.upvotes.all():
        post.upvotes.remove(user)
    post.downvotes.add(user)
    return redirect('discussions:thread_detail', thread_id=post.thread.id)