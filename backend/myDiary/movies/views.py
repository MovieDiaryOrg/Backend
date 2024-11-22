from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.pagination import LimitOffsetPagination

class MoviePagination(LimitOffsetPagination):
    default_limit = 20

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filter_backends = [filters.SearchFilter]    # filters에 SearchFilter 지정
    search_fields = ['^title']                   # search가 적용될 fields 지정



# Create your views here.
def movieList(request):
    pass

def createMovie(request):
    pass

def movieDetail(request):
    pass

def deleteMovie(request):
    pass