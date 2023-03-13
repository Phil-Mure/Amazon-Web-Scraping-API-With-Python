from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import views, status

from .serializers import MySerializer
from .models import ReactUrl

from bs4 import BeautifulSoup
import requests


@api_view(['GET', 'POST'])
def react_django(request):
    context = ''
    if request.method == 'GET':
        snippets = ReactUrl.objects.all()
        serializer = MySerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MySerializer(data=request.data)
        x = request.data
        value = ''
        for key, value in x.items():
            url = value
            print(value)
        if serializer.is_valid():
            # serializer.save()

            url = value
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding": "gzip, deflate",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

            page = requests.get(
                url,
                headers=headers
            )

            soup1 = BeautifulSoup(page.content, "html.parser")
            soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

            title = soup2.find("h1", id='title')
            if title is not None:
                title = title.get_text()

            price = soup2.find("span", class_='a-price a-text-price a-size-medium apexPriceToPay')
            if price is not None:
                price = price.get_text()

            cart = soup2.find("input", attrs={'id': 'add-to-cart-button'})
            if cart is not None:
                cart = cart.get('name')
            print(cart)

            buy = soup2.find("input", attrs={'id': 'buy-now-button'})
            if buy is not None:
                buy = buy.get('name')
            print(buy)

            print(title)
            print(price)

            context = {

                'url': url,
                'title': title,
                'price': price,
                'cart': cart,
                'buy': buy,

            }
        return Response(context)


@api_view(['GET'])
def url_detail(request, pk):
    try:
        url = ReactUrl.objects.get(pk=pk)
    except ReactUrl.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MySerializer(url)
        x = ReactUrl.objects.filter(pk=pk).values_list('url', flat=True)
        print(x)
        return Response(serializer.data)


def home(request):
    context = ''
    if 'product' in request.GET:
        product = request.GET.get('product')
        print(product)
        url = product

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get(
            url,
            headers=headers
        )

        soup1 = BeautifulSoup(page.content, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        title = soup2.find(id='productTitle')
        if title is not None:
            title = title.get_text()

        price = soup2.find(
            "span", attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'})
        if price is not None:
            price = price.get_text()

        cart = soup2.find("input", attrs={'id': 'add-to-cart-button'})
        if cart is not None:
            cart = cart.get('name')
        print(cart)

        buy = soup2.find("input", attrs={'id': 'buy-now-button'})
        if buy is not None:
            buy = buy.get('name')
        print(buy)

        print(title)
        print(price)

        context = {

            'url': url,
            'title': title,
            'price': price,
            'cart': cart,
            'buy': buy,

        }
    return render(request, 'api/home.html', {'context': context})
