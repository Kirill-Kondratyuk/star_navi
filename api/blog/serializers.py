from rest_framework import serializers

from blog import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostModel
        fields = [
            'id',
            'title',
            'body',
            'created',
            'user',
            'likes'
        ]
