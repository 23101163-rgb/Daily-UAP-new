from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.shortcuts import render
from daily_uap.news.models import Post, Category, SavedPost

def search_results(request):
    # Get user inputs
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    sort_option = request.GET.get('sort', 'newest')
    page_number = request.GET.get('page')

    # Base queryset
    posts = Post.objects.filter(is_published=True)

    # Search filter
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    # Category filter
    if category_id and category_id != "all":
        posts = posts.filter(category_id=category_id)

    # Sorting
    if sort_option == 'oldest':
        posts = posts.order_by('published_date')
    elif sort_option == 'most_commented':
        posts = posts.annotate(comment_count=Count('comments')).order_by('-comment_count', '-published_date')
    else:
        posts = posts.order_by('-published_date')  # newest first

    # Pagination (6 posts per page)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(page_number)

    # Preload saved post IDs for authenticated users
    saved_post_ids = []
    if request.user.is_authenticated:
        saved_post_ids = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    # Load categories for dropdown
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
        'sort_option': sort_option,
        'saved_post_ids': saved_post_ids,   # 👈 Added this
    }

    return render(request, 'search/search_results.html', context)
