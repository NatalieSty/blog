from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        # list of comments somewhere, somw are approved some aren't
        # then show along with the post
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        #after create, go post_detail page with primary key
        #of the post -- class based view
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments',on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    #comments needs to get approved. 
    #after commenting, go back to main home page of all post list
    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
