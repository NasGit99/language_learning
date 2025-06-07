
class User_Profile:
  
    def __init__(self, userName, firstName, lastName, email):
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    
    def user_details(self):
        print(f"""
            USER DETAILS \n
            -----------------
            Username: {self.userName} \n
            First Name: {self.firstName} \n
            Last Name: {self.lastName} \n
            Email: {self.email}
                    """)
    
    def modify_profile(self, field, new_value):

    field = field.lower()

    if field == 'username':
        self.userName = new_value
    elif field == 'first name':
        self.firstName = new_value
    elif field == 'last name':
        self.lastName = new_value
    elif field == 'email':
        self.email = new_value
