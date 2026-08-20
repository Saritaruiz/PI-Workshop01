from django.shortcuts import render
from .models import News

# Create your views here.


def news(request):
	news_list = News.objects.all().order_by('-date')
	return render(request, 'news.html', {'newss': news_list})
