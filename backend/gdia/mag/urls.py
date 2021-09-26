from . import views
from django.urls import path

urlpatterns = [
    path('article/<article_id>/', views.article, name='article'),
    path('search/<query>/', views.search, name='search'),
    path('magazine/<magazine_edition>/', views.magazine_edition, name='magazine'),    
]
