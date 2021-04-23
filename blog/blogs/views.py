from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import BlogPost
from .forms import BlogPost as BlogPostForm

def index(request):
    """ The home page for blogs also displays all blogs. """
    blog_posts = BlogPost.objects.order_by('date_added')
    context = {'blog_posts': blog_posts}
    return render(request, 'blogs/index.html', context)


@login_required
def new_blog(request):
    """ Create a new blog post. """
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = BlogPostForm()
    else:
        # POST data submitted; process data
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_blog_post = form.save(commit=False)
            new_blog_post.owner = request.user
            new_blog_post.save()
            return HttpResponseRedirect(reverse('blogs:index'))
    
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)


def edit_blog(request, blog_id):
    """ Edit a particular blogs title and text. """
    blog_post = BlogPost.objects.get(id=blog_id)
    if blog_post.owner != request.user:
        return HttpResponseRedirect(reverse('blogs:index'))

    if request.method != 'POST':
        # Initial request; pre-fill form with current blog info
        form = BlogPostForm(instance=blog_post)
    else:
        # POST data submitted; process data
        form = BlogPostForm(instance=blog_post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:index'))
    
    context = {'blog_post': blog_post, 'form': form}
    return render(request, 'blogs/edit_blog.html', context)


def delete_blog(request, blog_id):
    """ Deletes selected blog from website. """
    blog_post = BlogPost.objects.get(id=blog_id)
    blog_post.delete()
    
    if blog_post.owner != request.user:
        return HttpResponseRedirect(reverse('blogs:index'))

    return HttpResponseRedirect(reverse('blogs:index'))

