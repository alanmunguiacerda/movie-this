from __future__ import unicode_literals

from django.db import models

class UserPost(models.Model):
    user = models.ForeignKey('Users.UserProfile', null=True,  on_delete=models.CASCADE)
    content = models.TextField(max_length=3000)
    postDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return ('({!s}) {!s} : {!s}').format(postDate, user, content)
