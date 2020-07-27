from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
# Create your views here.
def home(request):
    return render(request, 'base.html')


baseCraig='https://warsaw.craigslist.org/search/?query={}'
def new_search(request):
    search= request.POST.get('search').title()
    models.Search.objects.create(search=search)
    url=baseCraig.format(quote_plus(search))
    #print(url)
    data=requests.get(url).text
    soup= BeautifulSoup(data, features='html.parser')
    post_listings= soup.find_all('li',{'class':'result-row'})
    postings=[]
    for post in post_listings:
        post_title=post.find(class_='result-title').text
        post_url=post.find('a').get('href')
        try:
            post_price=post.find(class_='result-price').text
        except:
            post_price=0
        try:
            post_image_id=post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url="https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
        except:
            post_image_url='https://craigslist.org/images/peace.jpg'
        postings.append((post_title,post_url,post_price,post_image_url))
    context={
        'search':search,
        'postings':postings,
    }
    return render(request,'my_app/new_search.html',context)