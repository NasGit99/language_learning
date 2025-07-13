
# I might not need this right now. I can remove the class and just keep modify_profile for updating the db
class User_Profile:
  
    def __init__(self, username, first_name, last_name, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
    def modify_profile(self, field, new_value):
        allowed_fields = {'username', 'first_name', 'last_name', 'email'}
        normalized_field = field.strip().lower().replace(" ","_")
        if normalized_field in allowed_fields:
            setattr(self, normalized_field, new_value)
        else:
            raise AssertionError(f"Cannot update '{field}'. Invalid field.")

