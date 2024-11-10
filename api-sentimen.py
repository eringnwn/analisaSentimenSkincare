from fastapi import FastAPI
import tensorflow as tf
import joblib
import re
import string
from indoNLP.preprocessing import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class userInput(BaseModel):
    text: str

app = FastAPI()
def get_stopwords(file_path):
  stopwords=[]
  file_stopwords = open(file_path,'r')
  row = file_stopwords.readline()
  while row:
    word = row.strip()
    stopwords.append(word)
    row = file_stopwords.readline()
  file_stopwords.close()
  return stopwords

def handle_stopwords(review, stopwords):
  feature_vector = []
  review = review.split(' ')
  for word in review:
    val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word) #menghilangkan karakter selain huruf didalam kata
    if (word in stopwords or val is None):
      continue
    elif (word == 'enggak'):
      feature_vector.append('tidak')
    else:
      feature_vector.append(word)
  for_stemming = ' '.join(feature_vector)
  return feature_vector, for_stemming

def handle_negative(review):
  negative_review = []
  review = review.split(' ')
  for i in range(len(review)):
    word = review[i]
    if i == 0 or (review[i-1] != 'enggak' and review[i-1] != 'tidak'):
      negative_review.append(word)
    else:
      negative_review.pop()
      word = 'tidak_'+word
      negative_review.append(word)
  for_stemming = ' '.join(negative_review)
  return for_stemming

# Remove emoji, punctuation, symbol
def preprocess(text):
  # Casefolding to Lowercase
  text = text.lower()

  # Remove punctuation
  text = text.translate(str.maketrans('', '', string.punctuation))

  text = replace_word_elongation(text)  # replace WE

  # Remove HTML tags
  text = remove_html(text) 
  text = remove_url(text)  # remove url
  text = replace_slang(text)  # replace slang words

  file_path ='dataset/stopwords-indo.txt'
  stopwords = get_stopwords(file_path)
  feature, text = handle_stopwords(text, stopwords)

  # Remove numbers
  text = text.translate(str.maketrans('', '', string.digits))
  # Remove whitespaces at front and back
  text = ' '.join(text.split())

  # Stemming
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()
  text = stemmer.stem(text)
  text = handle_negative(text)
  return text


def predict_stage(model, vectorizer, input):
  preprocessed_input = [preprocess(input)]
  print(preprocessed_input)
  # print(input)
  input_tf = vectorizer.transform(preprocessed_input)
  prediction = model.predict(input_tf)
  res = prediction[0]
  print(res)
  if res == 1:
    res = "Sentimen Positif"
  else:
    res = "Sentimen Negatif"

  return {'data': res}

@app.post("/sentimen")
async def sentimen(text:userInput):
  model = joblib.load("./Skincare-Sentiment-Analysis-SVM.joblib")
  vectorizer = joblib.load('./skincare-vectorizer.pkl')
  prediction = predict_stage(model, vectorizer, text.text)
  return prediction