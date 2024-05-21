from itertools import permutations
import re
import pickle
from preprocessing.preprocessor import preprocess
import json

with open('../positionalIndex/positional_index.pkl', 'rb') as file:
    positional_index = pickle.load(file)

def read_json(path):
  file = open(path)
  data = json.load(file)
  return data

news_data = read_json('../IR_data_news_12k.json')

def positional_intersect(pos_dict_1, pos_dict_2, k):
    # used when we have phrase queries
    # to find intersection between words of our query based on distance

    doc_ids_1 = list(pos_dict_1.keys())
    doc_ids_2 = list(pos_dict_2.keys())
    doc_ids_1.sort()
    doc_ids_2.sort()

    answer = []
    i, j = 0, 0

    while i < len(doc_ids_1) and j < len(doc_ids_2):
        doc_id_1 = doc_ids_1[i]
        doc_id_2 = doc_ids_2[j]

        if doc_id_1 == doc_id_2:
            pos_list_1 = pos_dict_1[doc_id_1]
            pos_list_2 = pos_dict_2[doc_id_2]

            for pos in pos_list_1:
                if pos + k in pos_list_2 or pos - k in pos_list_2:
                    answer.append(doc_id_1)

            i, j = i + 1, j + 1

        elif doc_id_1 < doc_id_2:
            i += 1
        else:
            j += 1

    return answer


def process_phrase(tokens):
    result = []
    # used when we have more than 2 words in our phrase
    # split it to 2 biword index
    # aggregate the results
    for biword in permutations(tokens, 2):
        w1 = biword[0]
        w2 = biword[1]
        if (w1 not in positional_index.keys()) or (w2 not in positional_index.keys()):
            return []

        indx1 = tokens.index(w1)
        indx2 = tokens.index(w2)
        pos_dic_1 = positional_index.get(w1).pos_in_doc
        pos_dic_2 = positional_index.get(w2).pos_in_doc
        k = abs(indx1 - indx2)

        docs = positional_intersect(pos_dic_1, pos_dic_2, k)

        if len(result) == 0:
            result = docs
        else:
            result = list(set(result) & set(docs))

    return result


def process_query(not_words=[], phrases=[], words=[]):
    ranks = {}

    # find words
    for token in words:
        if token in positional_index.keys():
            for doc_id in positional_index[token].pos_in_doc.keys():
                if doc_id in ranks.keys():
                    ranks[doc_id] += 1
                else:
                    ranks[doc_id] = 1
    # find phrases
    for phrase in phrases:
        for doc_id in process_phrase(phrase):
            if doc_id in ranks.keys():
                ranks[doc_id] += 1
            else:
                ranks[doc_id] = 1
    # find ! not words
    not_words_docs = []
    for word in not_words:
        doc_ids = positional_index[word].pos_in_doc.keys()
        for doc_id in doc_ids:
            not_words_docs.append(doc_id)

    # from results remove docs which contain not
    if len(ranks) > 0:
        for doc in not_words_docs:
            if doc in ranks.keys():
                del ranks[doc]

    ranks = dict(sorted(ranks.items(), key=lambda x: x[1], reverse=True))

    return ranks


def not_terms(query):
    splitted_query = query.split()
    indices = [i for i in range(len(splitted_query)) if splitted_query[i] == '!']
    result = [splitted_query[i + 1] for i in indices]
    return result


def get_phrase(query):
    res = []
    quoted = re.compile('"[^"]*"')
    for value in quoted.findall(query):
        value = value.replace('"', '').strip().split()
        res.append(value)
    return res


def search_query(query):
    # preprocessed query
    query = ' '.join(preprocess([query], True, True)[0])
    phrases = get_phrase(query)
    flat_phrases = [item for sublist in phrases for item in sublist]
    not_words = not_terms(query)
    query = query.replace('"', '')
    query = query.replace('!', '')
    splitted_query = query.split()
    looking_words = []
    for x in splitted_query:
        if x not in not_words and x not in flat_phrases:
            looking_words.append(x)
    output = process_query(not_words=not_words, phrases=phrases, words=looking_words)
    return output


def print_output(output_dict):
    ids = list(output_dict.keys())[:5]
    for i in range(len(ids)):
        print(f'Rank {i + 1}:')
        title = news_data[str(ids[i])]['title']
        url = news_data[str(ids[i])]['url']
        print('title: ', title, '\nurl: ', url)
        print('------------')


query = 'تحریم‌های آمریکا علیه ایران'
res = search_query(query)
print_output(res)
