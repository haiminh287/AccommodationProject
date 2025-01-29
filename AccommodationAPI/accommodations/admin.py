from django.contrib import admin
from django.urls import path
from accommodations.models import User,HouseArticle,ImageHouse,AcquistionArticle,LookingArticle,AddtionallInfomaion
# Register your models here.
class MyAccommodationAdmin(admin.AdminSite):
    site_header = 'OU eCourse'

admin_site = MyAccommodationAdmin(name='myaccommodationadmin')
admin_site.register(User)
admin_site.register(HouseArticle)
admin_site.register(ImageHouse)
admin_site.register(AcquistionArticle)
admin_site.register(LookingArticle)
admin_site.register(AddtionallInfomaion)