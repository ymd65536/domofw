# -*- coding: utf-8 -*-

import os
from domofw import get_token as token
from domofw import import_dataset as im

# 認証情報
PROXY_INFO = os.getenv('PROXY_INFO',None)
DOMO_USER = os.getenv('DOMO_USER',None)
PASSWORD = os.getenv('PASSWORD',None)
domo_config = {
  "user":DOMO_USER,
  "password":PASSWORD
}

# 証明書の参照先を変更
os.environ['REQUESTS_CA_BUNDLE']='D:\\py_env\\domo.pem'

def import_data_body(access_token, url, data_path, enc, head, req_enc):

  output_file = open(data_path,mode='r',encoding=enc)

  data_lines = output_file.readlines()
  line_cnt = 1
  
  for line in data_lines:
    if not head in line:
      line_cnt += 1

    if head in line:
      break

  # DOMOにインポートするデータを作成
  domo_data = data_lines[line_cnt:]

  # DOMOのAPIにリクエスト
  domo_req_data = ''.join(domo_data)

  res = im.import_dataset(access_token,url,domo_req_data.encode(req_enc),PROXY_INFO)
  print(str(res))
  output_file.close()


if __name__=='__main__':

  print("DOMO Request Test")

  # アクセストークンを発行
  cur_dir = os.getcwd()
  access_token = token.get_access_token_proc(domo_config,PROXY_INFO)

  # test.csv
  dataSet_id = "データセットID"
  url = "https://api.domo.com/v1/datasets/{0}/data".format(dataSet_id)
  data_file = 'test.csv'
  data_path = cur_dir + '\\csv\\' + data_file
  import_data_body(access_token,url,data_path,'shift-jis','ヘッダの一部分','utf-8')


