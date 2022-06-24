from email import message
import json
import uuid
from django.http import response
from nameko.web.handlers import http
from nameko.rpc import RpcProxy
from werkzeug import Response 
from dependecies import session
from urllib.parse import unquote

class Service:
    name = 'gateway_service'
    
    user_rpc = RpcProxy('user_services')
    news_rpc = RpcProxy('news_services')
    
    
    @http('POST', '/register/')
    def register(self, request):
        data = request.get_data(as_text=True)
        array = data.split('&')
        username = ''
        password = ''
        for indices in array:
            element = indices.split('=')
            if (element[0] == 'username'):
                username = element[1]
            elif (element[0] == 'password'):
                password = element[1]
                
        (self.user_rpc.add_user(username, password))

        response = Response('new user added')
        
        return response
    
    @http('POST', '/login/')
    def login(self, request):
        data = request.get_data(as_text=True)
        array = data.split('&')
        username = ''
        password = ''
        for indices in array:
            element = indices.split('=')
            if (element[0] == 'username'):
                username = element[1]
            elif (element[0] == 'password'):
                password = element[1]
        status = self.user_rpc.login(username, password)
        message = 'login success'
        if (status == 0):
            message = 'wrong password or username'
            
        response = Response(message)
        
        if (status == 1):
            response.set_cookie('SESS_ID',str(uuid.uuid1)) 
            
        return response
    
    @http('GET', '/logout/')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            response = Response('logout')
            response.delete_cookie('SESS_ID')
        else:
            response = Response('Login first')
            
        return response
    
    @http('GET', '/get_news/')
    def get_news(self, request):
        return Response(json.dumps(self.news_rpc.get_news()))
    
    @http('GET', '/get_news/<int:id>')
    def get_news_id(self, request, id):
        return Response(json.dumps(self.news_rpc.get_news_id(id)))
    
    @http('POST', '/post_news/')
    def post_news(self, request):
        cookie = request.cookies
        if cookie:
            data = request.get_data(as_text=True)
            element = data.split('=')
            content = ''
            if (element[0] == 'content'):
                content = element[1]
                
            content = unquote(content)
            message  = (self.news_rpc.post_news(content))
        
        else:
            message = 'Please login first'
        
        response = Response(message)
        
        return response
    
    @http('PUT', '/edit_news/<int:id>')
    def update_news(self, request, id):
        cookie = request.cookies
        if cookie:
            data = request.get_data(as_text=True)
            element = data.split('=')
            content = ''
            if (element[0] == 'content'):
                content = element[1]
                
            content = unquote(content)
            message  = (self.news_rpc.edit_news(content, id))
        
        else:
            message = 'please login first'
            
        response = Response(message)
        
        return response
        
    @http('DELETE', '/delete_news/<int:id>')
    def delete_news(self, request, id):
        cookie = request.cookies
        if cookie:
            message = self.news_rpc.delete_news(id)
        else:
            message = 'please login first'
            
        response = Response(message)
        return response
        
    
    @http('GET', '/hello/')
    def hello(self, request):
        return Response('hello')
        