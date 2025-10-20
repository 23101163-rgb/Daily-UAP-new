from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from daily_uap.accounts.models import Profile
from daily_uap.news.models import Post, Comment, SavedPost,RecentlyViewedPost
from daily_uap.news.forms import PostForm


@login_required
def dashboard_home(request):
    profile = Profile.objects.get(user=request.user)
    if profile.role == 'author':
        return redirect('author_dashboard')
    else:
        return redirect('reader_dashboard')


# ---------- AUTHOR DASHBOARD ----------
@login_required
def author_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    published_posts = Post.objects.filter(author=request.user, is_published=True)
    pending_posts = Post.objects.filter(author=request.user, is_published=False)

    # ✅ Latest comments on this author’s posts
    recent_comments = Comment.objects.filter(
        post__author=request.user
    ).select_related('post', 'user').order_by('-created_at')[:5]

    # ✅ Count stats for dashboard header
    published_count = published_posts.count()
    pending_count = pending_posts.count()
    total_count = published_count + pending_count

    return render(request, 'dashboard/author_dashboard.html', {
        'profile': profile,
        'published_posts': published_posts,
        'pending_posts': pending_posts,
        'recent_comments': recent_comments,
        'published_count': published_count,
        'pending_count': pending_count,
        'total_count': total_count,
    })




# ---------- READER DASHBOARD ----------
@login_required
def reader_dashboard(request):
    profile = Profile.objects.get(user=request.user)

    # My comments
    my_comments = Comment.objects.filter(user=request.user).select_related('post').order_by('-created_at')[:5]

    # Saved posts
    saved_posts = SavedPost.objects.filter(user=request.user).select_related('post').order_by('-saved_at')

    # ✅ Recently viewed posts (new system using model)
    recent_views = RecentlyViewedPost.objects.filter(user=request.user) \
                       .select_related('post') \
                       .order_by('-viewed_at')[:5]

    return render(request, 'dashboard/reader_dashboard.html', {
        'profile': profile,
        'my_comments': my_comments,
        'saved_posts': saved_posts,
        'recent_posts':[view.post for view in recent_views],
    })


# ---------- CREATE, EDIT, DELETE POST ----------
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_published = False  # admin must approve
            post.save()
            messages.success(request, "Post created successfully and sent for admin approval!")
            return redirect('author_dashboard')
    else:
        form = PostForm()
    return render(request, 'dashboard/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Post updated successfully!")
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)

    return render(request, 'dashboard/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('author_dashboard')
@login_required
def save_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    existing = SavedPost.objects.filter(user=request.user, post=post)
    if existing.exists():
        messages.info(request, "You’ve already saved this post.")
    else:
        SavedPost.objects.create(user=request.user, post=post)
        messages.success(request, "Post saved successfully!")
    return redirect('post_detail', pk=post.pk)


@login_required
def saved_posts(request):
    saved = SavedPost.objects.filter(user=request.user).select_related('post')
    return render(request, 'news/saved_posts.html', {'saved': saved})
