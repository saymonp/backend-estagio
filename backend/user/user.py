class User(object):

    def __init__(self):
        pass


    def login(self):
        ...
    
    def register(self, name: str, email: str, permissions: str = None):
        ...

    def email_confirmation(self):
        ...
    
    def delete(self):
        ...
    
    def add_permissions(self):
        ...
    
    def revoke_permissions(self):
        ...