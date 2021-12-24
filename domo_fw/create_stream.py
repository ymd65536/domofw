# アクセストークンを取得する
import  requests
import  json

url = "https://api.domo.com/v1/streams"

def create_stream_append(access_token,params,proxy):

	proxies = { "https":proxy }
	header={
	'Authorization': 'bearer ' + access_token,
	'Accept': 'application/json',
	'Content-Type' : 'application/json'
	}
	rr = requests.post(url,headers=header,data=params.encode("UTF-8"),proxies=proxies)
	json_str = rr.text
	reply_dict = json.loads(json_str)
	return reply_dict

def create_stream_replace(access_token,proxy):

	proxies = { "https":proxy }
	header={
	'Authorization': 'bearer ' + access_token,
	'Accept': 'application/json',
	'Content-Type' : 'application/json'
	}
	params="""
	{
		"dataSet":{
			"name" : "Data_RAW",
			"description" : "APIでdataSetを作成",
			"rows" : 0,
			"schema" : {
			"columns" : [
			{
				"type" : "STRING",
				"name" : "Friend"
			},
			{
				"type" : "STRING",
				"name" : "Attending"
			}				
			]
			}
			},
			"updateMethod" : "REPLACE"
		}
		"""
	rr = requests.post(url,headers=header,data=params.encode("UTF-8"),proxies=proxies)
	json_str = rr.text
	reply_dict = json.loads(json_str)
	return reply_dict
