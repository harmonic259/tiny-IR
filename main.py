import json


def read_json(path):
  file = open(path)
  data = json.load(file)
  return data

news_data = read_json('IR_data_news_12k.json')
data_len = len(news_data)
contents = [list(news_data.values())[i]['content'] for i in range(data_len)]

print(contents[0])


