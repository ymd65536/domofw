# アクセストークンを取得する
import  requests
import  json

def import_dataset(access_token,url,csv,proxy):
	proxies = { "https":proxy }
	header={
		'Authorization': 'bearer ' + access_token,
		'Accept': 'text/csv',
		'Content-Type' : 'text/csv'
	}

	rr = requests.put(url,headers=header,data=csv,proxies=proxies)
	json_str = rr.text

	if len(json_str) > 0 :
		reply_dict = json.loads(json_str,strict=False)
	else:
		reply_dict = {'Success':'import ok'}
	return reply_dict
