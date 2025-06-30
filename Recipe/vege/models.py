from django.db import models
from django.contrib.auth.models import User

class Recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name=models.CharField(max_length=100)
    recipe_description=models.TextField()
    recipe_image=models.ImageField(upload_to="receipe")
    recipe_view_count =models.IntegerField(default=0)




        