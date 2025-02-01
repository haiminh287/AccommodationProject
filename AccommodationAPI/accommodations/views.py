from django.shortcuts import render
from rest_framework import viewsets,generics,permissions,status
from rest_framework.decorators import action
from rest_framework.response import Response
from accommodations import serializers
from accommodations.models import User,HouseArticle,UserEnum,ImageHouse,AddtionallInfomaion,Like,AcquistionArticle,LookingArticle
from accommodations import perms
class UserViewSet(viewsets.ViewSet,generics.CreateAPIView):
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
    
    # @action(methods=['get'],url_path='conversations',detail=True)
    # def get_users_conversations(self,request,pk=None):
    #     user = self.get_object()
    #     conversations = Conversation.objects.filter(owner=user)
    #     return Response(serializers.ConversationSerializer(conversations,many=True).data)
    
    # @action(methods=['get'],url_path='messages',detail=True)
    # def get_user_chats(self,request,pk=None):
    #     user = self.get_object()    
    #     chat_id = Conversation.objects.filter(user_receiver=user,owner=request.user)
    #     print("Chat:",chat_id)
    #     chats = ConversationChat.objects.filter(conversation__in=chat_id)
    #     return Response(serializers.ConversationChatSerializer(chats,many=True).data)


# class ConversationViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
#     queryset = Conversation.objects.filter(active=True)
#     serializer_class = serializers.ConversationSerializer
    
#     @action(methods=['get'],url_path='messages',detail=True)
#     def get_conversation_chats(self,request,pk=None):
#         conversation = self.get_object()
#         chats = ConversationChat.objects.filter(conversation=conversation)
#         return Response(serializers.ConversationChatSerializer(chats,many=True).data)
    


# class ConversationChatViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
#     queryset = ConversationChat.objects.all()
#     serializer_class = serializers.ConversationChatSerializer


class HouseArticleViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = HouseArticle.objects.filter(active=True)
    serializer_class = serializers.HouseArticleSerializer

    
        

class AddtionallInfomaionViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = AddtionallInfomaion.objects.all()
    serializer_class = serializers.AddtionallInfomaionSerializer

class AcquistionArticleViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = AcquistionArticle.objects.filter(active=True)
    serializer_class = serializers.AcquistionArticleSerializer

    def get_permissions(self):
        if self.action in ['post_like'] and self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'],url_path='images',detail=True)
    def get_house_images(self,request,pk=None):
        acquistion = self.get_object()
        
        images = AcquistionArticle.objects.filter(house=acquistion)
        return Response(serializers.AcquistionArticleSerializer(images,many=True,context={'request': request}).data)
    
    @action(methods=['post'], url_path='likes', detail=True)
    def like_acquistion(self, request, pk=None):
        acquisition = self.get_object()
        liked_articles = request.session.get('liked_articles', [])
        if request.user.is_authenticated:
            like,created =  Like.objects.get_or_create(user=request.user,acquisition=acquisition)
            if not created:
                like.delete()
                return Response({'status': 'UnLiked'})
            return Response({'status': 'Liked'})
        else:
            if acquisition.id in liked_articles:
                liked_articles.remove(acquisition.id)
                request.session['liked_articles'] = liked_articles
                print('articles',request.session['liked_articles'])
                return Response({'status': 'UnLiked'})
            else:
                liked_articles.append(acquisition.id)
                request.session['liked_articles'] = liked_articles
                return Response({'status': 'Liked'})


class LookingArticleViewSet(viewsets.ViewSet,generics.ListCreateAPIView):
    queryset = LookingArticle.objects.filter(active=True)
    serializer_class = serializers.LookingArticleSerializer


class LikeViewSet(viewsets.ViewSet,generics.ListAPIView):
    serializer_class = serializers.LikeSerializer
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Like.objects.filter(user=user)
        else:
            liked_articles = self.request.session.get('liked_articles', [])
            return AcquistionArticle.objects.filter(id__in=liked_articles)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.user.is_authenticated:
            liked_articles = request.session.get('liked_articles', [])
            for article_id in liked_articles:
                article = AcquistionArticle.objects.get(id=article_id)
                Like.objects.get_or_create(user=request.user, acquisition=article)
            request.session['liked_articles'] = []
            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            articles = queryset
            article_serializer = serializers.AcquistionArticleSerializer(articles, many=True, context={'request': request})
            return Response(article_serializer.data)
