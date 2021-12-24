# アクセストークンを取得する
import  requests
import  json

def get_access_token_proc(config,proxy):
	url="https://api.domo.com/oauth/token"
	proxies = { "https":proxy }
	params= {
			"grant_type": "client_credentials",
			'scope': 'data'
			}
	rr = requests.get(url,params=params,proxies=proxies,auth=(config['user'],config['password']))
	json_str = rr.text
	dict_aa = json.loads(json_str)
	if 'access_token' in dict_aa:
		print('Success')
	else:
		print(dict_aa)
	access_token = dict_aa['access_token']
	return access_token
