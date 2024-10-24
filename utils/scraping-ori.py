import requests #package perlu di install terlebih dahulu
from bs4 import BeautifulSoup #package bs4 untuk mendapatkan beautifulsoup
import csv #tampung file dalam format csv

url = 'https://reviews.femaledaily.com/products/treatment/serum-essence-23/essenherb/essenherb-tea-tree-ampoule-1?cat=&cat_id=0&age_range=&skin_type=&skin_tone=&skin_undertone=&hair_texture=&hair_type=&order=newest&page=' #masukan url sekalian + cari tahu variable halamannya; &page
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
} #informasi mengenai user agent diambil dari request header pada menu inspeksi

#MAINKAN HALAMAN
datas = [] #membuat variabel datas sebagai list kosong untuk menampung data
count_page = 0 #supaya tau sampe halaman berapa
for page in range(1, 5): # range 1, 3 hanya ada 2 halaman
  count_page+=1
  print('scraping page :', count_page)
  #DEFINISIKAN VARIABLE
  req = requests.get(url+str(page), headers=headers)  # kata get didapet dari request method yang ada pada menu inspeksi
                                                      #url+page perlu diganti string karena 1,2,3 integer
  soup = BeautifulSoup(req.text, 'html.parser') #mengubah format html agar bisa menjadi lebih singkat dengan menggunakan beautifulsoup
                                      #html ada di variabel req dalam bentuk text --> parser bisa diganti: lxml atau html5lib
  items = soup.findAll('div', 'review-card') #cari class; class = review-card
  for it in items: #it untuk items
    try : date = it.find('p', 'review-date').text
    except : date = '' #try dan except untuk menghilangkan kolom yang hilang agar tidak error
    try : name = it.find('p','profile-username').text #karena yang diambil text doang
                                                # p --> data "nama" berada di lokasi p,dan class = profile-username
                                                # Karena "class = profile-username" maka bisa langsung masukan kata profile-username
                                                # contoh bukan class (itemprop) --> ada di file YWS
    except : name = ''
    try : category = it.find('p','recommend').text
    except : category = ''
    try : review = it.find('p', 'text-content').text
    except : review = ''
    try : information = it.find ('div', 'information-wrapper').text.replace('Purchase',' Purchase Point') #Replace --> mengganti agar ada space
    except : information = ''
    datas.append([date, name, category, review, information]) #mengisi list datas

#MEMBUAT FILE CSV
kepala = ['Tanggal', 'UserName', 'merekomendasikan/tidak', 'Review', 'Informasi Tambahan'] #membuat kepala tabel
with open('EssenHERB/coba coba.csv', 'w', newline='', encoding='utf-8') as file: #memasukkan kedalam variabel file
  writer = csv.writer(file) #menyimpan dalam bentuk csv
  writer.writerow(kepala) #menuliskan kepala
  for d in datas: #looping data
      writer.writerow(d)