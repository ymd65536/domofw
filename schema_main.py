
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

def create_data_provider(access_token, schema_file, output_enc, name, description):

  # CSVファイルを読み込む
  csv_file = open(schema_file,mode='r',encoding='utf-8')
  head_line = csv_file.readlines()

  # データセットのヘッダを作成
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

  # 完成したデータセットのヘッダを出力
  output_file = open(cur_dir + '\\csv\\' + name +'_schema_file.csv',mode='w',encoding=output_enc)
  output_file.write(head_schema)
  output_file.close

  # ヘッダをjsonに変換
  head_json = {}
  head_columns = []

  # データセットのスキーマを定義
  dataSet_schema = {'dataSet':{}}
  dataSet_schema['dataSet']['name'] = name
  dataSet_schema['dataSet']['description'] = description
  dataSet_schema['dataSet']['rows'] = 0
  # dataSet_schema['updateMethod'] = 'APPEND'
  dataSet_schema['updateMethod'] = 'REPLACE'

  # データセットのヘッダからスキーマを定義
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

  # DOMOにリクエストするデータセットのスキーマを出力
  output_file = open(cur_dir + '\\json\\'+ name +'_schema_json_file.json',mode='w',encoding=output_enc)
  output_file.write(post_schema_data)
  output_file.close

  # APIを実行
  res = cr.create_stream_append(access_token,post_schema_data,PROXY_INFO)

  # APIの実行結果をdataSetidを名前にしてjsonで保存
  output_file = open(cur_dir + '\\dataSet_id\\{0}.json'.format(res['dataSet']['id']),mode='w',encoding=output_enc)
  output_file.write(str(res).replace("\'","\"").replace("False","false"))
  output_file.close

if __name__=='__main__':

  # カレントディレクトリを取得
  cur_dir = os.getcwd()
  # スキーマを定義したCSVファイル(ヘッダ情報)
  schema_file = cur_dir + "\\csv\\" + "data_schema.csv"

  # アクセストークンを取得
  access_token = token.get_access_token_proc(domo_config,PROXY_INFO)

  # test.csv のデータセットスキーマ
  create_data_provider(access_token,schema_file,'utf-8','dataSet_Name','データセットの説明')
