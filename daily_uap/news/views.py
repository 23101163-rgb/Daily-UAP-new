from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
from .models import Post, Comment,SavedPost,RecentlyViewedPost
from .forms import CommentForm
from django.core.paginator import Paginator




# 🏠 Homepage view – shows all posts
from .models import Post, Category

def home(request):
    # ✅ Only published posts
    posts = Post.objects.filter(is_published=True).order_by('-published_date')

    # ✅ Pagination (6 per page)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ✅ Mark saved posts for logged-in users
    saved_posts_ids = []
    if request.user.is_authenticated:
        saved_posts_ids = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'news/home.html', {
        'page_obj': page_obj,
        'saved_posts_ids': saved_posts_ids,  # pass saved post IDs
    })
# 📰 Post detail view – shows post content and comments
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
    comments = Comment.objects.filter(post=post, parent=None).select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post

            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()
            messages.success(request, "✅ Your comment/reply was posted successfully!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedPost.objects.filter(user=request.user, post=post).exists()

    if request.user.is_authenticated:
        RecentlyViewedPost.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'viewed_at': timezone.now()}
        )
    return render(request, 'news/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_saved': is_saved,
    })



# 🗑 Delete comment (only post author or admin can delete)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.post.author or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', pk=comment.post.pk)
    else:
        return HttpResponseForbidden("You don't have permission to delete this comment.")
@login_required
def save_post(request, pk):
    """
    Allows logged-in users to save posts for later reading.
    Prevents duplicate saves and provides success/info messages.
    """
    post = get_object_or_404(Post, pk=pk)

    # Only allow saving published posts
    if not post.is_published:
        messages.warning(request, "You can only save published posts.")
        return redirect('post_detail', pk=post.pk)

    # Check if the post is already saved
    saved, created = SavedPost.objects.get_or_create(user=request.user, post=post)

    if not created:
        messages.info(request, "You’ve already saved this post.")
    else:
        messages.success(request, "✅ Post saved successfully!")

    return redirect('post_detail', pk=post.pk)
@login_required
def unsave_post(request, pk):
    """
    Allows users to remove a saved post from their Saved Posts list.
    """
    post = get_object_or_404(Post, pk=pk)
    saved_post = SavedPost.objects.filter(user=request.user, post=post)

    if saved_post.exists():
        saved_post.delete()
        messages.success(request, "🗑️ Post removed from your saved list.")
    else:
        messages.warning(request, "⚠️ This post wasn’t in your saved list.")

    return redirect('saved_posts')
