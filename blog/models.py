from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=15)

    def __str__(self):
        return self.caption
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to="images", null=True)
    # image_name = models.CharField(max_length=50)
    content = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique=True, db_index=True)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, related_name="posts")
    tag = models.ManyToManyField(Tag, related_name="posts")

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    

