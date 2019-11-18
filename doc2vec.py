#Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd
import json

amazon = pd.read_csv('./cleanAmazon_reviewtextOnly.csv', header=0)
amazon['cleanText'].dropna(inplace=True)            #ugh
data = amazon['cleanText'].tolist()

tagged_data = [TaggedDocument(words=word_tokenize(_d),
        tags=[str(i)]) for i, _d in enumerate(data)]
max_epochs = 10
vec_size = 25
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                dm =1)

model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

# to find most similar doc using tags
similar_doc = model.docvecs.most_similar('2')
print(similar_doc)
print(model.docvecs[0])