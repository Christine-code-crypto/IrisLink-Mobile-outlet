import requests
from django.http import JsonResponse

def get_access_token(request):
    consumer_key = "Lhefno4JQR7fUFTgcyPAI6anqXVwk9DlFUDGqHmPOsnKsdtc"  
    consumer_secret = "ouFWx8uZaAHQ0aAuWd4PUDDBDXgOa0r3epvsjBrWUOBcAumS5u1eYvVzg7uGBzH7"  
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status() 
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    