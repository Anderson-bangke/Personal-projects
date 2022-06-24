from unicodedata import name
from nameko.rpc import rpc

from dependecies import dependencies, session

class userServices:
    name = 'user_services'
    
    database = dependencies.Database()
    
    @rpc 
    def hello(self):
        return 'hello'
    
    @rpc
    def add_user(self, username, password):
        return self.database.add_user(username, password)
    
    @rpc 
    def login(self, username, password):
        return self.database.login(username, password)