import pickle

with open('../preprocessing/preprocessed_docs.pkl', 'rb') as file:
    preprocessed_docs = pickle.load(file)


class Term:
    def __init__(self):
        self.total_freq = 0
        self.pos_in_doc = {}
        self.freq_in_doc = {}

    def update_posting(self, doc_id, term_position):
      if doc_id not in self.pos_in_doc:
            self.pos_in_doc[doc_id] = []
            self.freq_in_doc[doc_id] = 0
      self.pos_in_doc[doc_id].append(term_position)
      self.freq_in_doc[doc_id] += 1
      self.total_freq += 1


def positional_indexing(preprocessed_docs):
    p_inv_index = {}
    for doc_id in range(len(preprocessed_docs)):
        for pos in range(len(preprocessed_docs[doc_id])):
            term = preprocessed_docs[doc_id][pos]
            if term in p_inv_index:
                term_obj = p_inv_index[term]
            else:
                term_obj = Term()
            term_obj.update_posting(doc_id, pos)
            p_inv_index[term] = term_obj

    return p_inv_index


positional_index = positional_indexing(preprocessed_docs)

with open('positional_index.pkl', 'wb') as file:
    pickle.dump(positional_index, file)




