from django.shortcuts import render

# Create your views here.
import boto3

ACCESS_KEY = 'your_access_key'
SECRET_KEY = 'your_secret_key'
SELLER_ID = 'your_seller_id'
MARKETPLACE_ID = 'your_marketplace_id'

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='us-east-1'  # Use the appropriate region
)

def creatSbscriptionAmazon():
    subscription_client = session.client('subscriptions', region_name='us-east-1')

    subscription_request = {
        'SellerId': SELLER_ID,
        'MarketplaceId': MARKETPLACE_ID,
        'Subscription': {
            'NotificationType': 'AnyOfferChanged',  # Specify the desired notification type
            'Destination': 'https://your-webhook-url.com',  # Your webhook URL
            # Other subscription details...
        }
    }


def requestSubscription(subscription_request):
    response = subscription_client.register_destination(subscription_request)
    if 'ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Subscription created successfully!')
    else:
        print('Error creating subscription:', response)
