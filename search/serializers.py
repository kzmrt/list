from rest_framework import serializers
from search.models import Post
from search.models import CustomUser


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    url = serializers.HyperlinkedRelatedField(
        view_name="post-detail",
        read_only=True,
        lookup_field='id'
    )

    class Meta:
        model = Post
        fields = ('url', 'id', 'author',
                  'title', 'text', 'created_at', 'updated_at',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    url = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        read_only=True,
        lookup_field='id'
    )

    class Meta:
        model = CustomUser
        fields = ('url', 'id', 'username', 'email', 'posts')
