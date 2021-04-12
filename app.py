# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 22:10:29 2021

@author: prems
"""

import spacy
import spacy.cli
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import json
from bson import ObjectId
  
#------------------------------------------------------------------------------------------------------------
#flask code
  
app = Flask(__name__)

spacy.cli.download("en_core_web_sm")
client=MongoClient('mongodb+srv://hussain:9773669443@enhance.bo4mo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
nlp = spacy.load('en_core_web_sm')
db=client.Enhance

class geeks: 
    def __init__(self, ids , name, roll): 
        self.id=ids
        self.name = name 
        self.roll = roll

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
        

fi=[]  
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    result=db.questions.find()
    #print(result) 
    #print('hello')
    for q in result:#{"_id":{"$oid":"5fa2aa3c7540c00017dc0b90"},"topics":[{"$oid":"5f77483d15314e0f04a9e7c1"}],"votes":{"$numberInt":"2"},"reportStatus":{"$numberInt":"0"},"user":{"$oid":"5fa2a7c57540c00017dc0b8f"},"question":"Why am I so afraid of failure?","description":"People are afraid of failure for a different kind of reason. I have had experienced fear of failure before and one of the reason for me was that I was to much concerned about what people would think of me after my failure. Also I didn’t want to disappoint people whose opinion I value. But then I realize that it is ok to fail and everybody fail once in a while. Failing has taught me a lot of thing about life. The main point is to get back up again after you fail!","time":{"$date":{"$numberLong":"1604495932357"}},"__v":{"$numberInt":"0"},"requestStatus":{"$numberInt":"0"}}
        #print("hiii")
        #print(q['_id'])
        #print(q['question'])
        fi.append({'id': q['_id'],'question' : q['question']})
        
    data=request.get_json()
    
    output=[]
    y=[]
    sent1=data['sent1'] 
    main_doc = nlp(sent1)
    for tu in fi:
        sent2=tu['question']
        search_doc=nlp(sent2)
        #print(sent2)
        
        search_doc_no_stop_words = nlp(' '.join([str(t) for t in search_doc if not t.is_stop]))
        main_doc_no_stop_words = nlp(' '.join([str(t) for t in main_doc if not t.is_stop]))
        percentage=search_doc_no_stop_words.similarity(main_doc_no_stop_words)
        output.append( geeks(tu['id'],sent2, percentage))
    output.sort(key=lambda x: x.roll,reverse=True)
    for obj in output:
        y.append({'id': obj.id,'question' : obj.name,'percentage':obj.roll})
        
       
    print(data['sent1'])
    return json.dumps(y, cls=JSONEncoder)

if __name__ == "__main__":
    app.run(debug=True)
