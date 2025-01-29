
from rest_framework.routers import DefaultRouter
from accommodations import views
from django.urls import path,include
route = DefaultRouter()
route.register(r'users', views.UserViewSet, basename='user')
route.register(r'house-articles', views.HouseArticleViewSet, basename='house-article')
route.register(r'addtionall-infomaion', views.AddtionallInfomaionViewSet, basename='addtionall-infomaion')
route.register(r'acquistion-article', views.AcquistionArticleViewSet, basename='acquistion-article')
route.register(r'looking-article', views.LookingArticleViewSet, basename='looking-article')
route.register(r'like', views.LikeViewSet, basename='like')
urlpatterns = [
    path('', include(route.urls)),
]
