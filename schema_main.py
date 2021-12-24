import sys
import os
from domofw import get_token as token
from domofw import create_stream as cr

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

if __name__=='__main__':
  # カレントディレクトリを取得
  cur_dir = os.getcwd()
  schema_file = cur_dir + "\\csv\\" + "data_schema.csv"

  # CSVファイルを読み込む
  csv_file = open(schema_file,mode='r',encoding='utf-8')
  head_line = csv_file.readlines()

  head_line_1 = head_line[0].split(",")
  head_line_2 = head_line[1].split(",")
  len_head = len(head_line_2)
  head = []
  for cnt in range(len_head):
    if '\n' in head_line_1[cnt]:
      head_line_1[cnt] = head_line_1[cnt].replace('\n','')

    if ' ' in head_line_1[cnt]:
      head_line_1[cnt] = head_line_1[cnt].replace(' ','')

    if '\n' in head_line_2[cnt]:
      head_line_2[cnt] = head_line_2[cnt].replace('\n','')
    head.append(head_line_1[cnt] + head_line_2[cnt] + '_' + str(cnt))

  csv_file.close
  head_schema = ','.join(head)

  output_file = open(cur_dir + '\\schema_file.csv',mode='w',encoding='utf-8')
  output_file.write(head_schema)
  output_file.close

  # ヘッダをjsonに変換
  head_json = {}
  head_columns = []
  # データセットのスキーマを定義
  dataSet_schema = {'dataSet':{}}
  dataSet_schema['dataSet']['name'] = 'test'
  dataSet_schema['dataSet']['description'] = 'test'
  dataSet_schema['dataSet']['rows'] = 0
  # dataSet_schema['updateMethod'] = 'APPEND'
  dataSet_schema['updateMethod'] = 'REPLACE'

  for head_tmp in head:
    head_json['type'] = 'STRING'
    column_name = head_tmp
    if ' ' in column_name:
      column_name = column_name.replace(' ','')
      column_name = column_name.strip()
      column_name = column_name.replace('\r\n','')

    head_json['name'] = column_name
    head_columns.append(head_json)
    head_json={}

  dataSet_schema['dataSet']['schema'] ={'columns':[]}
  dataSet_schema['dataSet']['schema']['columns'] = head_columns
  post_schema_str = str(dataSet_schema)
  post_schema_data = post_schema_str.replace("\'","\"")

  output_file = open(cur_dir + '\\schema_json_file.json',mode='w',encoding='utf-8')
  output_file.write(post_schema_data)
  output_file.close

  # APIを実行
  access_token = token.get_access_token_proc(domo_config,PROXY_INFO)
  res = cr.create_stream_append(access_token,post_schema_data,PROXY_INFO)

  output_file = open(cur_dir + '\\dataSet_id\\{0}.json'.format(res['dataSet']['id']),mode='w',encoding='utf-8')
  output_file.write(str(res).replace("\'","\"").replace("False","false"))
  output_file.close
