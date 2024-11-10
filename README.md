# **ANALISIS SENTIMEN ULASAN PRODUK KECANTIKAN SERUM NIACINAMIDE PADA LAMAN FEMALE DAILY MENGGUNAKAN METODE NAÏVE BAYES DAN SVM BERBASIS SMOTE-TOMEK **

Sebuah detektor sentimen berbasis SVM, TF-IDF, and SMOTE-TOMEK yang dilatih dengan dataset review skincare serum niacinamide pada website Female Daily.
Terdiri dari dataset (csv), ML model, file notebook, web scraping code, API dan web app.
 
Slang data dan stopwords bersumber dari https://github.com/Hyuto/indo-nlp/ dengan penambahan data yang sesuai dengan dataset.

Project UTS Mata Kuliah Machine Learning
Program Studi Teknik Informatika, Fakultas Informatika, Universitas Mikroskil

## Anggota
1. 211110933 - DHEA ROMANTIKA MARPAUNG
2. 211110101 - ERIN GUNAWAN
3. 211111610 - FARRELL RIO FA
4. 211110183 – ALBERT CHRISTIANTO

## How to run app
- `pip install -r requirements.txt`, then
- to run web app  : `streamlit run app.py`
- to start API: `fastapi dev api-sentimen.py`
  Request body for API in JSON format:
  ```
    { "text" : "Ini adalah sentimen yang akan dianalisis" }
  ```