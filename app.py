# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 23:41:14 2019

@author: makala
"""

from nltk.tokenize import word_tokenize
import gensim
from collections import OrderedDict
import requests
import os
import json
from flask import Flask, render_template, request




app = Flask(__name__)
result = None
class NLP(object):
    def import_keywords(self):
        self.products_keywords = {}
        with open(os.path.join(os.getcwd(),'keywords.txt'),'r') as lines:
            for line in lines:
                try:
                    (key, val) = line.rstrip('\n').split(':')
                except ValueError:
                    pass
                self.products_keywords[(key)] = val.split(',')
        self.p_k = OrderedDict(sorted(self.products_keywords.items(), key = lambda t: t[0]))
        #print(self.p_k)
        self.keywords = []
        for key,value in self.p_k.items():
            self.keywords.append(value)
        return self.keywords
    def get_input(self, api, arg1,arg2):
        self.text = requests.get(api)
        if self.text.status_code !=200:
            raise ApiError('GET /get {}'.format(self.text.status_code))
        return self.text.json()[arg1][arg2]
    def similarity(self):
        self.dictionary = gensim.corpora.Dictionary(self.import_keywords())
        #print(self.dictionary)
        #for i in range(len(self.dictionary)):
            #print(i, self.dictionary[i])
        self.corpus = [self.dictionary.doc2bow(keyword) for keyword in self.import_keywords()]
        #print(self.corpus)
        tf_idf = gensim.models.TfidfModel(self.corpus)
        #print(tf_idf)
        s= 0
        for i in self.corpus:
            s += len(i)
            #print(s)
        self.sims = gensim.similarities.Similarity(os.getcwd(),tf_idf[self.corpus], num_features=len(self.dictionary))
        self.query_doc = [w.lower() for w in word_tokenize(str(result))]
        #print(self.query_doc)
        self.query_doc_bow = self.dictionary.doc2bow(self.query_doc)
        #print(self.query_doc_bow)
        self.query_doc_tf_idf = tf_idf[self.query_doc_bow]
        #print(self.query_doc_tf_idf)
        #print(self.corpus)
        #return self.sims[self.query_doc_tf_idf]
    def output(self):
        self.dictionary_results = dict(zip(list(self.p_k.keys()),self.sims[self.query_doc_tf_idf]))
        #print(self.dictionary_results)
        self.sorted_results = [key for key,val in sorted(self.dictionary_results.items(), reverse = True, key = lambda x:x[1])]
        #print(self.sorted_results)
        return self.sorted_results

@app.route("/", methods = ['GET','POST'])
def get_input():
    global result
    if request.method == 'GET':
        return render_template('input_text2.html')
    if request.method == 'POST':
        result = request.form.get('textfield')
        x = NLP()
        x.similarity()
        x.output()
        js =json.dumps({'Output':x.output()})
        return render_template('input_text2.html', out = js)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)




 
