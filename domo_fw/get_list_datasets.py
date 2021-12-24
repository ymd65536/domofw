# アクセストークンを取得する
import  requests
import  json

from requests.api import head

def get_list_datasets(access_token,proxy):
	url="https://api.domo.com/v1/datasets"
	proxies = { "https":proxy }
	header={
		'Authorization': 'bearer ' + access_token,
		'Accept': 'application/json',
		'Content-Type' : 'application/json'
	}
	params= {
			"sort":"lastUpdated",
			"offset":0,
			"limit":50
			}
	rr = requests.get(url,params=params,headers=header,proxies=proxies)
	json_str = rr.text
	reply_dict = json.loads(json_str)
	return reply_dict
