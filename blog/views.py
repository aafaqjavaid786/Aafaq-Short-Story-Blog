# from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Author, Tag
from django.views.generic import ListView, DetailView
from django.views import View
from .forms import CommentForm 


# Create your views here.

# all_posts = [
#     {
#         "slug": "hiking-on-a-hill-station",
#         "image": "mountains.jpg",
#         "author": "Aafaq",
#         "date": date(2022, 10, 25),
#         "title": "Hiking on a Hill Station",
#         "excerpt": """He was at the zenith of the ladder of nature. The sun was about to return home. The bright
#         clouds were overshadowed by the dark clouds.""",
#         "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam."""

#     },
#     {
#         "slug": "hiking-on-a-hill-station",
#         "image": "mountains.jpg",
#         "author": "Aafaq",
#         "date": date(2022, 10, 20),
#         "title": "Hiking on a Hill Station",
#         "excerpt": """He was at the zenith of the ladder of nature. The sun was about to return home. The bright
#         clouds were overshadowed by the dark clouds.""",
#         "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam."""

#     },
#     {
#         "slug": "hiking-on-a-hill-station",
#         "image": "mountains.jpg",
#         "author": "Aafaq",
#         "date": date(2022, 10, 10),
#         "title": "Hiking on a Hill Station",
#         "excerpt": """He was at the zenith of the ladder of nature. The sun was about to return home. The bright
#         clouds were overshadowed by the dark clouds.""",
#         "content": """Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam.

#         Lorem ipsum dolor sit amet consectetur adipisicing elit. Ipsa accusamus reiciendis quos. Sit ratione illo sunt
#         dignissimos sequi alias commodi qui? Id modi fugit officia, molestias ipsam fugiat aspernatur quisquam."""

#     }
# ]


# def get_date(post):
#     return post['date']

class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset[:3]
    

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     # sorted_posts = sorted(all_posts, key=get_date)
#     # latest_posts = sorted_posts[-3:]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
    

# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all-posts.html",{
#         "all_posts": all_posts
#     })

# class PostDetailView(DetailView):
#     template_name = "blog/post-detail.html"
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tag.all()
#         context["comment_form"] = CommentForm()
#         return context


class PostDetailView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "comment_form": form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    

# def post_details(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     # identified_post = next(post for post in all_posts if post['slug'] == slug)
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tag.all()
#     })

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts)

            context["posts"]= posts
            context["has_posts"]= True

        return render(request, "blog/stored-posts.html", context)

    
    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("post-detail-page", args=[request.POST["post_slug"]]))
