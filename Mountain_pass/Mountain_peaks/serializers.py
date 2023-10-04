from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
       model = Author
       fields = ['surname', 'name', 'patronymic', 'email', 'telephone']

    # При сохранении пользователя, проверяем его наличие в БД по email
    #def save(self, **kwargs):
    #    self.is_valid()
    #    current_user = Author.objects.filter(email=self.validated_data.get['email'])
    #    if current_user.exists():
    #        return current_user.first()
    #    else:
    #        new_user = Author.objects.create(
    #            surname=self.validated_data.get('surname'),
    #            name=self.validated_data.get('name'),
    #            patronymic=self.validated_data.get('patronymic'),
    #            telephone=self.validated_data.get('telephone'),
    #            email=self.validated_data.get('email'),
    #        )
    #        return new_user


class CoordinateSerializer(serializers.ModelSerializer):
   class Meta:
       model = Coordinate
       fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
       model = Level
       fields = ['winter', 'spring', 'summer', 'autumn']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
       model = Image
       fields = ['title', 'photo']

class PeakSerializer(WritableNestedModelSerializer):
#class PeakSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()
    coords = CoordinateSerializer()
    level = LevelSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Peak
        fields = ['country', 'category', 'title', 'other_titles', 'connect', 'add_time', 'status', 'method_of_passage', 'user', 'coords', 'level',
                  'images']

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        images = validated_data.pop('images')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')

        user, created = Author.objects.get_or_create(**user)

        #current_user = Author.objects.filter(email=user['email'])
        #if current_user.exists():
        #    user_serializer = AuthorSerializer(data=user)
        #    user_serializer.is_valid(raise_exception=True)
        #    user = user_serializer.save()
        #else:
        #    user = Author.objects.create(**user)

        coords = Coordinate.objects.create(**coords)
        level = Level.objects.create(**level)

        peak = Peak.objects.create(**validated_data, user=user, coords=coords, level=level)

        if images:
            for image in images:
                image_name = image.pop('title')
                image = image.pop('photo')
                Image.objects.create(peak=peak, title=image_name, photo=image)

        peak.save()
        return peak

