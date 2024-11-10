import tensorflow as tf
import joblib
import streamlit as st
import re
import string
from indoNLP.preprocessing import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import sys

sys.path.append('../../dataset')
from dataset.slang_data import SLANG_DATA

st.write('''
# Sentiment Classification
''')
st.write("Sebuah detektor sentimen berbasis SVM, TF-IDF, and SMOTE-TOMEK yang dilatih dengan dataset review skincare serum niacinamide pada website Female Daily")
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
    elif (word == 'enggak'):
      # kata ini dihandle terpisah karena pada slang dictionary, semua padanan kata 'tidak' yang tidak baku, ditranslate menjadi 'enggak'
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
      word = 'tidak_' + word
      if (i != len(review)-1) and (review[i+1] == 'buruk' or review[i+1] == 'jelek'):
        word = word + '_' + review[i+1]
        i += 1 #increase index agar kata 'buruk' dan 'jelek' tidak di-consider lagi
      if (i < len(review)-2) and (review[i+1] == "efek" and (review[i+2] == 'buruk' or review[i+2] == 'jelek')):
        word = 'tidak_'+ review[i+1] + '_' + review[i+2]
        i += 2 #increase index agar kata 'efek', 'buruk' dan 'jelek' tidak di-consider lagi
      negative_review.append(word)
  for_stemming = ' '.join(negative_review)
  return for_stemming

def handle_slang(text):
  SLANG_PATTERN = rf"(?i)\b({'|'.join(SLANG_DATA.keys())})\b"
  return re.sub(SLANG_PATTERN, lambda mo: SLANG_DATA[mo.group(0).lower()], text)

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

def preprocess(text):
  # Casefolding to Lowercase
  text = text.lower()
  # print('1. Casefolding:', text)

  # Remove punctuation
  text = text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))) #ubah tanda baca jadi spasi dulu
  text = ' '.join(text.split()) #lalu hapus multiple spasi jadi satu spasi
  # kenapa begini? karena ini teks review, beberapa orang membuat ulasan dengan tanda baca yang tidak rapi.
  # misalnya "bagusbaget.rekomen" kalau langsung dihapus titiknya tanpa kasih spasi dulu, ntar kalimatnya jadi aneh
  text = re.sub(r'[^\x00-\x7F]+', ' ', text) #remove non-ascii character (misalnya emoji). [^\x00-\x7F] artinya hanya ambil yang ascii-nya dari 0 sd 127

  text = replace_word_elongation(text)  # replace WE
  # Change emoji to words, then remove the punctuation from emoji-to-word process
  # text = emoji_to_words(text)
  # text = text.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))

  # Remove HTML tags
  text = remove_html(text)
  text = remove_url(text)  # remove url
  # text = replace_slang(text)  # replace slang words
  text = handle_slang(text)

  # Remove numbers
  text = text.translate(str.maketrans('', '', string.digits))

  # Remove whitespaces at front and back
  text = ' '.join(text.split())
  # print('2. Cleaning: ', text)

  # Remove Stop Words
  file_path ='dataset/stopwords-indo.txt'
  stopwords = get_stopwords(file_path)
  feature, text = handle_stopwords(text, stopwords)
  # print('3. Stop Words: ', text)

  # Stemming
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()
  text = stemmer.stem(text)
  # print('4. Stemming: ', text)

  text = handle_negative(text)
  # print('5. Handle Negative: ', text)
  return text

def predict_stage(model, vectorizer, input):
  preprocessed_input = [preprocess(input)]
  input_tf = vectorizer.transform(preprocessed_input)
  prediction = model.predict(input_tf)
  res = prediction[0]
  if res == 1:
    st.info(f"Sentimen Positif")
  else :
    st.error(f"Sentimen Negatif")

  return prediction


if input_str is None:
  st.text("Please fill in your review")
else:
  model = joblib.load("./Skincare-Sentiment-Analysis-SVM.joblib")
  vectorizer = joblib.load('./skincare-vectorizer.pkl')
  predict = st.button("Submit Review")
  if predict:
    prediction = predict_stage(model, vectorizer, input_str)