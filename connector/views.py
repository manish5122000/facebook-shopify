from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.shortcuts import redirect
from django.http import JsonResponse
from urllib.parse import urlparse, parse_qs
import json
from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import unquote
from rest_framework.views import APIView
from myproject.serializer import YourModelSerializer
from rest_framework.response import Response
# Create your views here.
def home(request):
    return render(request,'home.html')
def oauth_shopify(req):
    print(req)
    shop = req.GET['shop']
    hmac = req.GET['hmac']
    # scopes =  "write_inventory,write_locations,read_locations,write_merchant_managed_fulfillment_orders,read_orders,write_products,read_products,write_resource_feedbacks,read_resource_feedbacks"
    # url = "https://"+shop+"/admin/oauth/authorize?client_id=3c1c07b2bb5602cfd617bce29c628736&scope="+ scopes +"&redirect_uri=http://127.0.0.1:8000/connector/commense_auth/&state=1245"
    scopes = "write_inventory,write_locations,read_locations,write_merchant_managed_fulfillment_orders,read_orders,write_products,read_products,write_resource_feedbacks,read_resource_feedbacks"
    url = "https://" + shop + "/admin/oauth/authorize?client_id=fe806c9fb2fc33a2cd2adbaac35ed29f&scope=" + scopes + "&redirect_uri=http://127.0.0.1:8000/connector/commense_auth/&state=1245"

    print(url)
    print('hello')
    response = redirect(url)
    return response

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

             
def required_data_app_shop(data,shop):
    check_for_available = app_shop.objects.get(shop_name = shop)
    if(check_for_available):
        check_for_available.shop_name = shop
        check_for_available.access_token = data['access_token']
        check_for_available.save()
        return 
    else:
        create = app_shop.objects.create(shop_name=shop,access_token=data['access_token'])
        return 

def entry_user_details(shop_name,access_token):
    data = get_current_user(shop_name,access_token)

    if(data['errors']):
        return
    else:
        user = user_details.objects.create(user_id=data['user']['id'],shop_name = shop_name,marketplace={0:{data},1:{}} )
        return
    
@csrf_exempt
def getwebhook(req):
    print(req)
    name_webhook = req.GET['webhook']
    store  = req.GET['store']
    if req.method == 'POST':
        request_body = req.body
        print(request_body)
        # Process the request_body as needed
        return JsonResponse({"message": "Request body received"})
    print(req)
    print("\n------------------------\n")
    return True



def get_current_user(shop_name,access_token):
    url = 'https://'+shop_name+'/admin/api/2023-01/users/current.json'
    header = {
        'Content-Type' : 'application/json',
        'X-Shopify-Access-Token' : access_token
    }
    r = requests.get(url = url, headers=header)
    data = r.json()
    return data


def get_access_token(req):
    print(":welcome")
    code = req.GET['code']
    print("code")
    print(code)
    shop = req.GET['shop']
    url = 'https://'+shop+'/admin/oauth/access_token?client_id=fe806c9fb2fc33a2cd2adbaac35ed29f&client_secret=66e38eda7208ed139c8209516a87e99f&code='+code
    print(url)
    r = requests.post(url = url)
    data = r.json()
    print(data)
    get_shop = checkInstallation(shop,data['access_token'])
    print(get_shop)
    if(get_shop):
        print("entry")
        # entry in user_details
    print(data['access_token'])
    # app_shop = required_data_app_shop(data,shop)
    webhook = create_webhook(shop,data['access_token'])
    print(webhook)
    dataa = get_bulk_product_from_shopify(shop,data['access_token'])
    if dataa["success"]:
        entry_product = entry_product_container(dataa)
    else:
        dataa = get_bulk_product_from_shopify(shop,data['access_token'])

    # return redirect('https://50d5-2409-4063-431d-be37-1076-17ae-7ae-7dc.ngrok-free.app')
    return "done"
def checkInstallation(shop_name,access_token):
    shop = user_details.objects.filter(shop_name=shop_name)
    print("user_details")
    if(shop):
        return True
    else:
        entry_user_details(shop_name,access_token)
        # user_details.objects.create()

        return False
    # print(shop)
    # return shop

def entry_product_container(data):
    print(data)
    val = data['data']['products']
    # gf = {}
    # for i,k in val:
    #     gf[i]=k
    #         # for l,j in i.items():
    # print(gf)
    # Products.objects.create(gf)

    idd = 4
    title = 'k'
    vendor = 'k'
    variants = {}
    for i in val:
        for k,j in i.items():
            # print(i)
            if(k == 'id'):
                idd = j
            if(k == 'title'):
                title = j
            if(k == 'vendor'):
                vendor = j
            if(k == 'variants'):
                variants = j
        Products.objects.create(_id= idd, title = title, vendor = vendor , variants=variants)
            
    print("----------------------------------------------------------")


def get_bulk_product_from_shopify(shop,access_token):
    url2 = 'https://'+shop+'/admin/api/2023-07/products.json'
    headers = {
        'X-Shopify-Access-Token': access_token
    }

    response = requests.get(url2, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Process the response data
        response = {
                "success": True,
                "data": data
        }
    else:
        response = {
                "success": False,
                "message": "please re import product"
        }
        print(f"Request failed with status code: {response.status_code}")
    return response

def create_webhook(store,access_token):
    url = "https://"+store+"/admin/api/2023-07/webhooks.json"
    print(url)
    # webhooks = ["app/uninstalled", "orders/cancelled", "orders/create","orders/delete","orders/edited","orders/fulfilled","orders/paid","orders/partially_fulfilled","orders/updated","fulfillment_orders/moved","product_listings/add","product_listings/remove","product_listings/update", "products/create","products/delete", "products/update", "variants/in_stock", "variants/out_of_stock", "inventory_levels/connect", "inventory_levels/update", "inventory_levels/disconnect", "inventory_items/create", "inventory_items/update", "inventory_items/delete", "locations/activate", "locations/deactivate", "locations/create", "locations/update", "locations/delete", "tender_transactions/create", "app_purchases_one_time/update"]
    webhook = ["locations/create", "locations/update", "locations/delete"]
    headers = {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json'
    }
    for topic in webhook:
        value = topic.replace('/', '_')
        data = {
            "webhook": {
                "address": "https://86b9-2405-201-600b-1eca-a472-6e24-88ad-5ddf.ngrok-free.app/connector/webhook?webhook="+ value +"&store="+ store,
                "topic":topic,
                "format": "json"
            }
        }
        print(data)

        response = requests.post(url, json=data, headers=headers)
        print(response)
        print(" created =>"+topic)
    if response.status_code == 201:
        print("\n-------created---------\n")
        return JsonResponse({ "success": True,"message": "Webhook created successfully"})
        
    else:
        return JsonResponse({ "success": False,"message": "Failed to create webhook"}, status=response.status_code)
