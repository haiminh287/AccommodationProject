from rest_framework import serializers
from accommodations.models import User,Conversation,ImageHouse,HouseArticle,AddtionallInfomaion,AcquistionArticle,LookingArticle,Like,Comment,AddressHouseArticle,FollowUser
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        data = validated_data.copy()
        print("main_data",data)
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u
    def update(self, instance, validated_data):
        data = validated_data.copy()
        user = User(**data)
        for attr, value in data.items():
            setattr(user,attr,value)
        user.set_password(user.password)
        user.save()
        return user
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar.url if instance.avatar else None
        return data
    class Meta:
        model = User
        fields=['id','username','password','first_name','last_name','avatar','phone','user_role','email','is_superuser']
        extra_kwargs ={
            'password':{
                'write_only':True
            }
        }

class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        if obj.image:
            if obj.image.name.startswith("http"):
                return obj.image.name
            request = self.context.get('request')
            if request and obj.image.name:
                return request.build_absolute_uri('/static/%s' % obj.image.name)


class ConversationSerializer(serializers.ModelSerializer):
    user_receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_receiver'] = UserSerializer(instance.user_receiver).data
        return representation


class HouseArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseArticle
        fields = '__all__'


class AddtionallInfomaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddtionallInfomaion
        fields = '__all__'


class ImageHouseSerializer(BaseSerializer):

    class Meta:
        model = ImageHouse
        fields = ['id', 'house', 'image']



class AcquistionArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = ImageHouseSerializer(many=True, source='imagehouse_set')
    acquisitions = AddtionallInfomaionSerializer(many=True, source='addtionallinfomaion_set')
    class Meta:
        model = AcquistionArticle
        fields = '__all__'


class LookingArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = LookingArticle
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    house = HouseArticleSerializer()
    user = UserSerializer()
    class Meta:
        model = Like
        fields = '__all__'  


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class AddressHouseArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHouseArticle
        fields = '__all__'



class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = '__all__'