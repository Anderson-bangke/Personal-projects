
import json
from nameko.exceptions import BadRequest

import os
import requests
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from nameko.rpc import RpcProxy

from session import SessionProvider

class GatewayService:
    name = "gateway_service"
    
    session_provider = SessionProvider()
    
    @http('POST', '/login')
    def login(self, request):
        responses = {
            'status': None,
            'message': None,
        }

        cookies = request.cookies
        if cookies:
            responses['status'] = "Error"
            responses['message'] = "User already logged in"
            return Response(str(responses))
        else:
            data = format(request.get_data(as_text=True))

            username = ""
            password = ""

            node = data.split("=")
            if (node[0] == "username"):
                username = node[1]
            username = requests.utils.unquote(username)
            password = requests.utils.unquote(password) 
            
            responses['status'] = "Success"
            responses['message'] = "Succesful Login"
            
            response = Response(str(responses))
            session_id = self.session_provider.set_session(responses)
            response.set_cookie('SESS_ID', session_id)
            response.set_cookie('username', username)
            
            return response

    @http("POST", "/upload")
    def upload_file(self, request):
        cookies = request.cookies
        if cookies:
            responses = {
                    'status': None,
                    'message': None,
                    'data': None,
                }

            path = 'Storage/'+ cookies['username']

            if os.path.exists(path):
                responses['status'] = 'Error'
                responses['message'] = 'File already exists'
            else:
                responses['message'] = 'Folder Created'
                os.makedirs(path)
            for file in request.files.items():
                _, storage = file
                storage.save(f"{path}/{storage.filename}")
                responses['status'] = "Success"

            return Response(str(responses))