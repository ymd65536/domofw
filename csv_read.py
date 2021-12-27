# coding: utf-8
import os

if __name__ == '__main__':
  cur_dir = os.getcwd()
  data_file = 'test.csv'
  data_path = cur_dir + '\\csv\\' + data_file
  output_file = open(data_path,mode='r',encoding='shift_jis')

  data_lines = output_file.readlines()
  line_cnt = 1
  
  for line in data_lines:
    if not 'A' in line:
      line_cnt += 1

    if 'A' in line:
      break

  # DOMOにインポートするデータを作成
  domo_data = data_lines[line_cnt:]

  # DOMOのAPIにリクエスト
  domo_req_data = ''.join(domo_data)
  
  print(domo_req_data)
