import pickle

with open('preprocessed_docs.pkl', 'rb') as file:
    loaded_docs = pickle.load(file)

print(loaded_docs[0])