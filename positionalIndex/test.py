import pickle
# from positional_index import Term
with open('positional_index.pkl', 'rb') as file:
    loaded_docs = pickle.load(file)

print(loaded_docs.get('fljsd'))
