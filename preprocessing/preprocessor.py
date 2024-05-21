from parsivar import Normalizer, Tokenizer, FindStems
from hazm import stopwords_list
import json
import pickle

def read_json(path):
  file = open(path)
  data = json.load(file)
  return data

news_data = read_json('../IR_data_news_12k.json')
data_len = len(news_data)
contents = [list(news_data.values())[i]['content'] for i in range(data_len)]

normalizer = Normalizer()
tokenizer = Tokenizer()
stemmer = FindStems()

stopwords = {stopwords_list()[i] for i in range(0, len(stopwords_list()) - 1)}
extra_stopwords = ['،', '.', ')', '(', '}', '{', '«', '»', '؛', ':', '؟', '>', '<', '|',
                   '+', '-', '*', "^", '%', '#', '=', '_', '/', '«', '»', '$', '[', ']',
                   '&', "❊", '«', '»']
stopwords.update(extra_stopwords)

def preprocess(contents):
    preprocessed_docs = []
    for content in contents:
        # normalizing
        normalized_content = normalizer.normalize(content)
        content_tokens = tokenizer.tokenize_words(normalized_content)
        tokens = []
        for token in content_tokens:
            token = stemmer.convert_to_stem(token)
            if token in stopwords:
                continue
            tokens.append(token)
        preprocessed_docs.append(tokens)
        # tokens of each doc
    return preprocessed_docs


preprocessed_docs = preprocess(contents)


with open('preprocessed_docs.pkl', 'wb') as file:
    pickle.dump(preprocessed_docs, file)


