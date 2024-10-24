import tensorflow as tf
import joblib
import streamlit as st
import re
import string
from indoNLP.preprocessing import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Currently using ML_NLP.ipynb model
st.write('''
# Sentiment Classification
''')
st.write("Sebuah detektor sentimen berbasis Random Forest, TF-IDF, and SMOTE-TOMEK yang dilatih dengan dataset review skincare pada website Female Daily")
input_str = st.text_area('Review')

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
    else:
      feature_vector.append(word)
  for_stemming = ' '.join(feature_vector)
  return feature_vector, for_stemming

# Remove emoji, punctuation, symbol
def preprocess(text):
  # Casefolding to Lowercase
  text = text.lower()

  # Remove punctuation
  text = text.translate(str.maketrans('', '', string.punctuation))

  text = replace_word_elongation(text)  # replace WE

  # Change emoji to words
  text = emoji_to_words(text)
  text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))

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
  return text


def predict_stage(model, vectorizer, input):
    preprocessed_input = [preprocess(input)]
    input_tf = vectorizer.transform(preprocessed_input)
    prediction = model.predict(input_tf)
    res = prediction[0]
    if res == 2:
        st.success(f"Sentimen Positif")
    elif res == 1:
        st.info(f"Sentimen Netral")
    else :
        st.error(f"Sentimen Negatif")

    return prediction


if input_str is None:
    st.text("Please fill in your review")
else:
    model = joblib.load("../Skincare-Sentiment-Analysis.joblib")
    vectorizer = joblib.load('../skincare-vectorizer.pkl')
    predict = st.button("Submit Review")
    if predict:
        prediction = predict_stage(model, vectorizer, input_str)