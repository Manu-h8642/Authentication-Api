from django.shortcuts import render
from myapp.serialisers import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import user
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
# Create your views here.
class reg(APIView):
    def post(self,request):
        obj = auth(data=request.data)
        obj.is_valid(raise_exception=True)
        obj.save()
        return Response(obj.data)
class loginview(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        x = user.objects.filter(email=email).first()
        if x is None:
            raise AuthenticationFailed("User not found")
        if not x.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        payload = {
            'id':x.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response

class Userview(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated...!")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated..!")
        User = user.objects.filter(id=payload['id']).first()
        serialiser = auth(User)
        return Response(serialiser.data)

class LogoutView(APIView):
    def post(self,request):
        respose = Response()
        respose.delete_cookie('jwt')
        respose.data = {
            'Logout':"Success"
        }
        return respose