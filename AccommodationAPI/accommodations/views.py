from django.shortcuts import render
from rest_framework import viewsets,generics,permissions,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from accommodations import serializers
from accommodations.models import User,HouseArticle,UserEnum,HouseArticle,AddtionallInfomaion,Like,AcquistionArticle,LookingArticle,Comment,FollowUser
from accommodations import perms
from django.db.models.functions import TruncMonth, TruncYear, TruncQuarter
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from accommodations import paginators
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['list', 'retrieve']:
            if self.request.user.user_role == UserEnum.ADMIN.value:
                return [perms.IsAdmin()]
            elif self.request.user.user_role == UserEnum.INKEEPER.value:
                return [perms.IsInnkeeper()]
            elif self.request.user.user_role == UserEnum.TENANT.value:
                return [perms.IsTenant()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)
    
    @action(methods=['get','post'],url_path='follow-user',detail=False)
    def follow_user(self,request):
        if request.method == 'POST':
            follow_user_id = request.data.get('follow_user_id')
            follow_user = User.objects.filter(id=follow_user_id).first()
            if not follow_user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            follow_instance = FollowUser.objects.filter(user=request.user, followed_user=follow_user)
            if follow_instance.exists():
                follow_instance.delete()
                return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
            else:
                FollowUser.objects.create(user=request.user, followed_user=follow_user)
                return Response({'message': 'Followed successfully'}, status=status.HTTP_201_CREATED)
        follow_users = FollowUser.objects.filter(user=request.user)
        return Response(serializers.FollowUserSerializer(follow_users,many=True).data)

class HouseArticleViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = HouseArticle.objects.filter(active=True)
    serializer_class = serializers.HouseArticleSerializer

    def get_queryset(self):
        query = self.queryset
        state = self.request.query_params.get('state')
        print('state',state)
        if state:
            query = query.filter(state=state)
        return query
    @action(methods=['get','post'],url_path='comments',detail=True)
    def get_comments(self,request,pk=None):
        house = self.get_object()
        if request.method == 'POST':
            content = request.data.get('content')
            comment = Comment.objects.create(user=request.user,house=house,content=content)
            return Response(serializers.CommentSerializer(comment).data)
        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializer(comments,many=True, context={'request': request}).data)
    
    @action(methods=['get'],url_path='address',detail=False)
    def get_address(self,request):
        house = self.get_object()
        address = house.addresshousearticle_set.first()
        return Response(serializers.AddressHouseArticleSerializer(address).data)
    
    @action(methods=['post'], url_path='likes', detail=True)
    def like_acquistion(self, request, pk=None):
        house = self.get_object()
        liked_articles = request.session.get('liked_articles', [])
        if request.user.is_authenticated:
            like,created =  Like.objects.get_or_create(user=request.user,house=house)
            if not created:
                like.delete()
                return Response({'status': 'UnLiked'})
            return Response({'status': 'Liked'})
        else:
            if house.id in liked_articles:
                liked_articles.remove(house.id)
                request.session['liked_articles'] = liked_articles
                print('articles',request.session['liked_articles'])
                return Response({'status': 'UnLiked'})
            else:
                liked_articles.append(house.id)
                print('articles dont in',request.session['liked_articles'])
                request.session['liked_articles'] = liked_articles
                return Response({'status': 'Liked'})

class AddtionallInfomaionViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = AddtionallInfomaion.objects.all()
    serializer_class = serializers.AddtionallInfomaionSerializer

class AcquistionArticleViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = AcquistionArticle.objects.filter(active=True).order_by('-id')
    serializer_class = serializers.AcquistionArticleSerializer

    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('kw')
        deposit = self.request.query_params.get('deposit')
        number_people = self.request.query_params.get('number_people')
        district = self.request.query_params.get('district')
        province = self.request.query_params.get('province')
        if kw:
            query = query.filter(title__icontains=kw)
        if deposit:
            deposit_value = float(deposit)
            query = query.filter(deposit__gte=deposit_value - 100, deposit__lte=deposit_value + 100)
        if number_people:
            query = query.filter(number_people=number_people)
        if district:
            query = query.filter(district__icontains=district)
        if province:
            query = query.filter(city__icontains=province)
        return query

    @action(methods=['get'],url_path='images',detail=True)
    def get_house_images(self,request,pk=None):
        images = self.get_object().imagehouse_set.all()
        return Response(serializers.ImageHouseSerializer(images,many=True,context={'request': request}).data)
    
    
    


class LookingArticleViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = LookingArticle.objects.filter(active=True).order_by('-id')
    serializer_class = serializers.LookingArticleSerializer
    # pagination_class = paginators.ItemPaginator
    

class LikeViewSet(viewsets.ViewSet,generics.ListAPIView):
    serializer_class = serializers.LikeSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Like.objects.filter(user=user)
        else:
            liked_articles = self.request.session.get('liked_articles', [])
            print('articles like',liked_articles)
            return HouseArticle.objects.filter(id__in=liked_articles)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_authenticated:
            liked_articles = request.session.get('liked_articles', [])
            for article_id in liked_articles:
                article = HouseArticle.objects.get(id=article_id)
                Like.objects.get_or_create(user=request.user, house=article)
            request.session['liked_articles'] = []
            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            articles = queryset
            article_serializer = serializers.HouseArticleSerializer(articles, many=True, context={'request': request})
            return Response(article_serializer.data)





class UserStatisticsView(APIView):
    def get(self, request):
        period = request.GET.get('period', 'year')
        trunc_func = self.get_trunc_func(period)
        if not trunc_func:
            return Response({'error': 'Invalid period parameter'}, status=400)
        start_date = timezone.now() - timedelta(days=600)
        end_date = timezone.now()
        user_statistics = self.get_statistics(User.objects.filter(date_joined__range=[start_date, end_date]), trunc_func, period)
        inkeeper_statistics = self.get_statistics(User.objects.filter(date_joined__range=[start_date, end_date], user_role="Chủ Nhà Trọ"), trunc_func, period)
        return Response({
            'user_statistics': user_statistics,
            'inkeeper_statistics': inkeeper_statistics
        })

    def get_trunc_func(self, period):
        if period == 'month':
            return TruncMonth
        elif period == 'quarter':
            return TruncQuarter
        elif period == 'year':
            return TruncYear
        return None

    def get_statistics(self, queryset, trunc_func, period):
        statistics = queryset.annotate(period=trunc_func('date_joined')) \
                             .values('period') \
                             .annotate(count=Count('id')) \
                             .order_by('period')

        formatted_statistics = []
        for stat in statistics:
            formatted_period = self.format_period(stat['period'], period)
            formatted_statistics.append({
                'period': formatted_period,
                'count': stat['count']
            })
        return formatted_statistics

    def format_period(self, period, period_type):
        if period_type == 'month':
            return period.strftime('%m-%Y')
        elif period_type == 'quarter':
            quarter = (period.month - 1) // 3 + 1
            return f"Quý {quarter} {period.year}"
        elif period_type == 'year':
            return period.strftime('%Y')
        return ''
    


    
    