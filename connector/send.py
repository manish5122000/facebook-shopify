from rest_framework.views import APIView
from myproject.serializer import YourModelSerializer
from rest_framework.response import Response
from .models import *
from django.shortcuts import render
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from urllib.parse import unquote
class YourAPIView(APIView):
    def get(self, request):
        queryset = Products.objects.all()
        serializer = YourModelSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = YourModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

def facebookAouthredirect(req):
    print('ggggggggggggggggggggggggggggggggg')
    print(req)
    # response = redirect(url)

def facebookAouth(req):
    # print(req)
    # appid = 253343950955737
    # url = "https://www.facebook.com/v17.0/dialog/oauth?client_id="+appid+"&redirect_uri={"https://www.domain.com/login"}&state={"{st=state123abc,ds=123456789}"}

    base_url = "https://www.facebook.com/v17.0/dialog/oauth"
    client_id = "253343950955737"
    redirect_uri = "https://74cf-2405-201-600b-1eca-9c9a-4332-a0e8-64b7.ngrok-free.app/connector/facebokredirect/"
    state = '{"st": "state123abc", "ds": "123456789"}'

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state
    }

    url = f"{base_url}?{requests.compat.urlencode(params)}"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        print("Request successful!")
        print("Response content:")
        print(response.text)
        # rew = requests.get(response)
        decoded_content = unquote(response.text)
        return HttpResponse(decoded_content, content_type='text/html')
    else:
        print(f"Request failed with status code: {response.status_code}")

    response = redirect(url)
    print(response)
    return HttpResponse(f"Request failed with status code: {response.status_code}", status=500)

