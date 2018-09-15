from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.views.generic import ListView
from django.http import HttpResponseRedirect




def index(request):
    cast = Post.objects.order_by('-publish')[:4]
    return render(request, 'index.html', {'cast':cast})

"""
def post_index(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2) #2 post on one page
    page = request.GET.get('page')
    try:
        mypost = paginator.page(page)
        
    except PageNotAnInteger:
        #if page is not integer deliver first
        mypost = paginator.page(1)
    except EmptyPage:
        #if page is empty
        mypost = paginator.page(paginator.num_pages)
    return render(request,
    'post/post_index.html',
    {'page':page,
        'posts':mypost})
"""
#class view

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name= 'post/post_index.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug = post,
                             status = 'published',
                             publish__year = year,
                             publish__month = month, 
                             publish__day = day
                            )


    #List of active comment
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        #comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment obj not save
            new_comment = comment_form.save(commit=False)
            #Assign comment to specific post
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect("")    
    else:
        comment_form  = CommentForm()
        return render(request, 
            'post/post_detail.html',
            {'post': post,
            'comments':comments,
            'new_comment':new_comment,
            'comment_form':comment_form})