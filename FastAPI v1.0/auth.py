from imports import *

security = HTTPBearer()
secretkey = 'Th1s1ss3cr3t'


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials

    if not token:  # check if we get it, if yes save it, if no empty string
        return {'message': 'Token is missing!'}

    try:
        # decoding the token to get the data
        data = jwt.decode(token, secretkey)
    except Exception as e:
        print(e)
        return {'message': 'Token is invalid!'}

    return data
