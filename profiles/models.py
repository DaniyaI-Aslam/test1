from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
# Create your models here.
# from profiles.forms import SignupForm
# from django_countries.fields import CountryField
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(max_length=60,blank=True,null=True)
    package_active = models.BooleanField(default=False)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    recommended_by1 = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by1')
    recommended_by2 = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by2')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    package_price = models.IntegerField(blank=True,null=True)
    oneorzero = models.IntegerField(default=0)
    get_date = models.CharField(max_length=12,blank=True,null=True)
    get_date2 = models.CharField(max_length=12,blank=True,null=True)
    earn_from_ads = models.FloatField(default=0)
    onee = models.BooleanField(default=True)
    twoo = models.BooleanField(default=True)
    threee = models.BooleanField(default=True)
    # city = models.CharField(max_length=12)
    
    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user ]
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs   


    def get_recommened_profiles1(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user ]
        my_recs = []
        for profile in qs:
            if profile.recommended_by1 == self.user:
                my_recs.append(profile)
        return my_recs  

    def get_recommened_profiles2(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user ]
        my_recs = []
        for profile in qs:
            if profile.recommended_by2 == self.user:
                my_recs.append(profile)
        return my_recs  

    def save(self,*args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code

        super().save(*args, **kwargs)