from django.shortcuts import render
from rest_framework import permissions
import django_filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from  rest_framework import viewsets, status


from Mountain_peaks.serializers import *
from Mountain_peaks.models import *


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CoordinateViewset(viewsets.ModelViewSet):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class SubmitDataViewset(viewsets.ModelViewSet):
    queryset = Peak.objects.all()
    serializer_class = PeakSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('user__email',)
    http_method_names = ['get', 'post', 'head', 'patch', 'options']

    # переопределяю метод, для вывода сообщения о результатах сохранения данных
    def create(self, request, *args, **kwargs):
        serializer = PeakSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response({f'status': status.HTTP_201_CREATED,
                             'message': 'Запись успешно добавлена',
                             'id': obj.id})
        if status.HTTP_400_BAD_REQUEST:
            return Response({'status': status.HTTP_400_BAD_REQUEST,
                             'message': serializer.errors})
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                             'message': serializer.errors})





