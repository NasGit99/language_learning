def profile_data_query():
    query = "select username, first_name, last_name, email from users where username = %s"
    return query