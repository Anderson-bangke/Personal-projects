from unicodedata import name
from nameko.rpc import rpc

from dependecies import dependencies, session

class userServices:
    name = 'news_services'
    
    database = dependencies.Database()
    
    @rpc 
    def hello(self):
        return 'hello'
    
    @rpc 
    def get_news(self):
        return self.database.get_news()
    
    @rpc 
    def get_news_id(self, id):
        return self.database.get_news_id(id)
    
    @rpc 
    def post_news(self, content):
        return self.database.post(content)
    
    @rpc 
    def edit_news(self, content, id):
        return self.database.edit(content, id)
    
    @rpc
    def delete_news(self, id):
        return self.database.delete(id)