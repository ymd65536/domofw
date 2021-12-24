import os
from domofw import get_token as token

PROXY_INFO = os.getenv('PROXY_INFO',None)
DOMO_USER = os.getenv('DOMO_USER',None)
PASSWORD = os.getenv('PASSWORD',None)
os.environ['REQUESTS_CA_BUNDLE']='D:\\py_env\\domo.pem'

if __name__=='__main__':
	domo_config = {
		"user":DOMO_USER,
		"password":PASSWORD
	}
	access_token = token.get_access_token_proc(domo_config,PROXY_INFO)
	print(access_token)	
