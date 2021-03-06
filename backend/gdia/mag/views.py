from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.core import serializers
from .models import Article, Magazine
from .search import GetSearch
# Create your views here.

import json


def search(request, query):
    return JsonResponse(GetSearch(query), safe=False)


def article(request, article_id):
    try:
        a = Article.objects.get(article_id=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    response = {
        "article_id": a.id,
        "title_article": a.title,
        "publishment_date": a.published_date,
        "magazine_edition": str(a.magazine) + '_' + a.edition,
        "article_text": a.content,
        "images": json.loads(a.images)
    }
    return JsonResponse(response, safe=False)


def magazine_edition(request, magazine_edition):
    magazine_name, edition_name = magazine_edition.split('_')
    magazine = Magazine.objects.get(name=magazine_name)
    articles = Article.objects.filter(magazine=magazine, edition=edition_name)
    articles_json = serializers.serialize('json', articles)
    return HttpResponse(articles_json, content_type="application/json")
