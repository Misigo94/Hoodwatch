
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from PIL import Image
from django.urls import reverse
# Create your models here.

class Neighborhood(models.Model):
    name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    occupant_count=models.IntegerField()
    police=models.IntegerField()
    health=models.IntegerField()
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    @classmethod
    def create_neighborhood(self):
        self.save()
    @classmethod
    def delete_neighborhood(self):
        self.delete()
    @classmethod
    def find_neighborhood(cls,neighborhood_id):
        return cls.objects_filter(id=neighborhood_id)

    @classmethod
    def update_neighborhood(cls,neighborhood_id,location):
      return cls.objects_filter(id=neighborhood_id).update(location=location)

    @classmethod
    def update_occupants(cls,neighborhood_id,occupant_count):
        return cls.objects_filter(id=neighborhood_id).update(occupant_count)


class Profile(models.Model):
    name=models.CharField(max_length=255)
    about=models.TextField(max_length=255)
    email=models.EmailField(max_length=255)
    image=models.ImageField(upload_to='photos/')
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    location=models.CharField(max_length=255,null=True)
    neighborhood=models.ForeignKey(Neighborhood,on_delete=models.CASCADE,null=True, related_name='members')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        super().save( **kwargs)
        img= Image.open(self. image.path)
        if img.height > 250 or img.width > 250:
            output_size = (250, 2500)
            img.thumbnail(output_size)
            img.save(self. image.path)

class Business(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    location=models.ForeignKey(Neighborhood,on_delete=models.CASCADE,null=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_business(self):
        self.save()
    @classmethod
    def delete_business(self):
        self.delete()
    @classmethod
    def find_business(cls,business_id):
        return cls.objects_filter(id=business_id)

    @classmethod
    def update_business(cls,business_id,location):
      return cls.objects_filter(id=business_id).update(location=location)

    @classmethod
    def search_business(cls,search_name):
        search_results = cls.objects.filter(Q(name__icontains=search_name))
        return search_results


class Post(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(max_length=500)
    location=models.ForeignKey(Neighborhood,on_delete=models.CASCADE,null=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def save_post(self):
        self.save()

    @classmethod
    def delete_post(self):
        self.delete()

    def user_post(self,cls,username):
        posts=cls.objects.filter(author_username=username)
        return posts

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    class Meta:
      ordering = ['-id']

        
