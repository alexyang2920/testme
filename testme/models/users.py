class UsersFolder(object):
    pass


def check_credentials(username, password, request):
    if username=='admin' and password == 'admin':
        return True
    return False
