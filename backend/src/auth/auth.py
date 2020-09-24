import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


# AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
# ALGORITHMS = ['RS256']
# API_AUDIENCE = 'dev'

# https://spskelly.us.auth0.com/authorize?
# audience=http://localhost:5000
# &response_type=token&
# client_id=4VZgmO8D9NzovFgJrBn1e9DcBkA36h1Z&
# redirect_uri=http://localhost:8100

AUTH0_DOMAIN = 'spskelly.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'
#
# Token for Barista: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjVkNmI5NzVmZWE3NjAwNmIwOGI5NWQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDMyNDQsImV4cCI6MTYwMDkxMDQ0NCwiYXpwIjoiNFZaZ21POEQ5TnpvdkZnSnJCbjFlOURjQmtBMzZoMVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.pOQCs466LidTFI_-Cl3tluJ7p8Li5m-JXwh1fFLcs8NMG9Dhs0zdZg42GPSFGKn5dALQV5JTbZ4g5Fn2OuSWpe9Nnj4hJfWgMLVBSGGLuvg06_j9NCHDCCOqjG5dFm-WQDTYUrrpYlh7I4Rbif6PZUCmMRucKFeiBBjjZcxgR_fImb8qau0pAecn1WnvOOExvCmMrR9yrat13SPaqsJF_ctEG68259kXqUf32IuUc7F21D5Ku463mr9v8XDZkoW7idyR0N2QiXMT4qlk51DwZQSBHCn4r3GX-1xifLOnxzyY7rbCTXzEgHfKoYOUwrI2jm-v9cusdss6G7g_QXEvAg
# http://localhost:8100/
#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjVkNmI5NzVmZWE3NjAwNmIwOGI5NWQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDEzNTMsImV4cCI6MTYwMDkwODU1MywiYXpwIjoiMnhxQ1o2ZFo5ekVWZ0U3a2NVUzM3aXkweGh1eW9hRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.DyvUgoHBnB_5EYUSItU7NjG0-MOY4dIrgchMFnEf1o3hCFOwbeLINWdSLVbdkR6so84FnQQKi2Uz-F-oifK3EYxuCxhWtWF43wcep2Sdfw4HrjngmMTJKpeCB8FMQ5mY5Xgjbf6ZV1gXWw6-CfNTNGaDY7wm9PBWcUayDoqJBBag9rxuBAYSuw4pILlrR4vDCnw5VX5Xb6MJTzuuIy2SJvlwTc0ev96sg6MRlW9nAWn4oKRzvHU7wOa5_hn5WTb6JhR9ZrmpvI1ZF-wqhXvphicdYGIqw_3a-3OGGDat8GLcHGbxYqW-QxTvci1-Eh2-2z1JZuPv_Zea2kiHIfp4bw&expires_in=7200&token_type=Bearer

# Token for Manager: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjY4ZTIzYzYzMDAyNDAwNzE5MmZlMjAiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDM1MDEsImV4cCI6MTYwMDkxMDcwMSwiYXpwIjoiNFZaZ21POEQ5TnpvdkZnSnJCbjFlOURjQmtBMzZoMVoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.nycVH7f7PsWryxOCxB4t5idZ4DlW74ysXBeGcL0Zg3LxB6n08Zb-USG4zuOHuuLFhlQclU-ltdERrUhZMrVDg6gh9Sr2jJqO4uQ-wDhlqNj680KqrcO-24wTcW0PgYT5-stxJAOUG39C4m1KuMNB1Akq7TzTMYi2S7KiCwr0IytDRGnIY-gM2V0TBOHX6HyZ6i_aqAhLTG7S700522MMC7aZS_ZB9_KMTI3iJOJ20xZsRHgAz-bMr6539mM_4hJ47O4D1OIeayqXFQGIv1T04LavS8Fn1V9gh51PnpLS4A9we9peVfouiatXLWfzRazU_cd89DYn4UQhMkWwoOc53Q
# http://localhost:8100/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjY4ZTIzYzYzMDAyNDAwNzE5MmZlMjAiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDE1MDUsImV4cCI6MTYwMDkwODcwNSwiYXpwIjoiMnhxQ1o2ZFo5ekVWZ0U3a2NVUzM3aXkweGh1eW9hRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.mxgIqdqVnoCbdbhjXdbZ4m7y0b0PbzermaSjkDzfJRUKAZViq__VcIN7O1LeR65DuJuDA4FC1bdxEMYFkq1o5uVmNB6UXIkqPggrlZFTyBjygCpG3qrS8knuUShnGjWZ69AHZA1IbTPHyNL_pHRMdh84XlY9P1847blRqFjOEHRUSAShY6Cu0mY30QF1dt9TcrBpNwykB2sIzkDcm4HoA2kuu5Zmbzqqy6wBqA_4ueOoM2_2zAgjyxfHjOYZFqJut-RyDGk0zlBENU5Cpm9qgmv5vi-a6KYzlqhEacX6DrbJGsSqderCan0ezujrDRh7HJhvwrJXEs809NqJ9CHbTw&expires_in=7200&token_type=Bearer

# Token for random user: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjZiZDFiZmE1MTFmZTAwNmI3ODliZjQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDE1NzEsImV4cCI6MTYwMDkwODc3MSwiYXpwIjoiMnhxQ1o2ZFo5ekVWZ0U3a2NVUzM3aXkweGh1eW9hRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.otnFZjWldw7Xfdb7b24gfhPbLUDTDjP9YKHP9tRfP1TDXprUL282EX1ffikSHHJe_T8Ru5lzMQlFL3q7MLSOXPd_yMhTkrMrKhdtSMVYEfX3YTjym5j0tnvYQVvbRVrqSlQrs2fIEB0qP1yimjXoJ-1dx1gpXuLaLklIq6BM9g9bGf4-C3gzsyT4rje-gPjpxmpccfkjfQNPz4AAaKsdjkARNxBYEPUXx5Wfm_aIxAyHzxpz-Rsw4F4-cdMkN8PvMkAD6pCK8N1N25vy51K2BEFNmWupz0DEth4VTd8ROIuDyMo9txdWljwU7VWvhdcfk8eyNfr-ZVGw_AmNIVUE-A
# http://localhost:8100/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJjLWY2dGdsenFrdllXWDN3YVBkMCJ9.eyJpc3MiOiJodHRwczovL3Nwc2tlbGx5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjZiZDFiZmE1MTFmZTAwNmI3ODliZjQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE2MDA5MDE1NzEsImV4cCI6MTYwMDkwODc3MSwiYXpwIjoiMnhxQ1o2ZFo5ekVWZ0U3a2NVUzM3aXkweGh1eW9hRjMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.otnFZjWldw7Xfdb7b24gfhPbLUDTDjP9YKHP9tRfP1TDXprUL282EX1ffikSHHJe_T8Ru5lzMQlFL3q7MLSOXPd_yMhTkrMrKhdtSMVYEfX3YTjym5j0tnvYQVvbRVrqSlQrs2fIEB0qP1yimjXoJ-1dx1gpXuLaLklIq6BM9g9bGf4-C3gzsyT4rje-gPjpxmpccfkjfQNPz4AAaKsdjkARNxBYEPUXx5Wfm_aIxAyHzxpz-Rsw4F4-cdMkN8PvMkAD6pCK8N1N25vy51K2BEFNmWupz0DEth4VTd8ROIuDyMo9txdWljwU7VWvhdcfk8eyNfr-ZVGw_AmNIVUE-A&expires_in=7200&token_type=Bearer



## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
get_token_auth_header() method.
Attempts to get the header from the request.
Raises an AuthError if no header is present.
Otherwise, attempts to split bearer and the token.
Raises an AuthError if the header is malformed.
When successful, returns the token part of the header
'''
def get_token_auth_header():
    print(" in get_token_auth_header")
    print("before doing anything")
    try:
        # attempt to get the header from the request
        auth_headers = request.headers['Authorization']
        # split bearer and the token
        header_parts = auth_headers.split(' ')
    except:
        # raise an AuthError if no header is present
        if request.headers is None:
            print("No header?")
            raise AuthError({
            'code': 'no_request_header',
            'description': 'There is no header on this request.'
            }, 401)
        if 'Authorization' not in request.headers:
            print("No authorization in header?")
            raise AuthError({
            'code': 'no_auth_in_header',
            'description': 'No authorization details in request header.'
            }, 401)
        # raise an AuthError if the header is malformed
        if len(header_parts) != 2:
            print("Too many parts in header!")
            raise AuthError({
            'code': 'too_many_parts',
            'description': 'Too many parts to Auth header.'
            }, 401)
        if header_parts[0].lower() != 'bearer':
            print("No bearer in header!")
            raise AuthError({
            'code': 'no_bearer_tag',
            'description': 'Bearer tag not present or malformed.'
            }, 401)
    # return the token part of the header
    print("payload is " , header_parts[1])
    return(header_parts[1])

'''
check_permissions(permission, payload)
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    Raises an AuthError if permissions are not included in the payload
    Raises an AuthError if the requested permission string is not in the payload permissions array
    returns true otherwise
'''
def check_permissions(permission, payload):
    # raise Exception('Not Implemented')
     # raise an AuthError if permissions are not included in the payload
    if 'permissions' not in payload:
        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)
# raise an AuthError if the requested permission string is not in the payload permissions array
    if permission not in payload['permissions']:
        raise AuthError({
                        'code': 'unauthorized',
                        'description': 'Permission not in payload.'
                        }, 401)
    return True

'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    Verifies the token using Auth0 /.well-known/jwks.json
    Decodes the payload from the token
    Validates the claims
    returns the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    # CHOOSE OUR KEY
    rsa_key = {}
    # check it is an Auth0 token with key id (kid)
    if 'kid' not in unverified_header:
        raise AuthError({
                            'code': 'invalid_header',
                            'description': 'Authorization malformed.'
                        }, 401)
    for key in jwks['keys']:
        # verify the token using Auth0 /.well-known/jwks.json
        if key['kid'] == unverified_header['kid']:
            # decode the payload from the token
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Finally, verify!!!
    if rsa_key:
        # validate the claims
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # return the decoded payload
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                                'code': 'token_expired',
                                'description': 'Token is expired.'
                            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                                'code': 'invalid_claims',
                                'description': 'Incorrect claims. Please, check the audience and issuer.'
                            }, 401)
        except Exception:
            raise AuthError({
                                'code': 'invalid_header',
                                'description': 'Unable to parse authentication token.'
                            }, 400)
    raise AuthError({
                        'code': 'invalid_header',
                        'description': 'Unable to find the appropriate key.'
                    }, 400)

'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    Uses the get_token_auth_header method to get the token
    Calls the verify_decode_jwt method to decode the jwt
    Calls the check_permissions method validate claims and check the requested permission
    returns the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            # try:
            payload = verify_decode_jwt(token)
            # except:
            #     raise AuthError({
            #                         'code': 'invalid_token',
            #                         'description': 'Invalid token.'
            #                     }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
