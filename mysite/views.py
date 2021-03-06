from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
import os,json
from dotenv import load_dotenv
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.views.decorators.csrf import csrf_exempt

twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_token(request):
    room_name = 'My Room'
    if request.method=="POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except json.decoder.JSONDecodeError as err:
            return JsonResponse({"status":"Missing required parameter 'username'"})
  
        username = body.get("username")
        
        if not username:
            return HttpResponse(401)
        print("username=",username)
        token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                            twilio_api_key_secret, identity=username)
        token.add_grant(VideoGrant(room=room_name))
        
        return JsonResponse({'token': token.to_jwt().decode(),'room_name':room_name})
    return HttpResponse("Error")