import requests #package perlu di install terlebih dahulu
from bs4 import BeautifulSoup #package bs4 untuk mendapatkan beautifulsoup
import csv #tampung file dalam format csv

def scrape(url: str, page_limit: int):
  headers = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36'
  } #informasi mengenai user agent diambil dari request header pada menu inspeksi

  datas = [] #menampung data hasil scraping
  count_page = 0
  for page in range(1, page_limit+1):
    count_page += 1
    print('Loading, scraping page', count_page)
    
    # HTTP GET to page url
    req = requests.get(url+'?&page='+str(page), headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser') #mengubah format html agar bisa menjadi lebih singkat dengan menggunakan beautifulsoup
    
    items = soup.findAll('div', 'review-card')
    for it in items:
      try : 
        date = it.find('p', 'review-date').text
        if ('2020' in date):
          break
      except : date = '' #try dan except untuk menghilangkan kolom yang hilang agar tidak error
      try : name = it.find('p','profile-username').text
      except : name = ''
      try : category = it.find('p','recommend').text
      except : category = ''
      try : review = it.find('p', 'text-content').text
      except : review = ''
      datas.append([date, name, category, review])

def writeFile(data: list, path: str):
  # output ke file CSV
  heading = ['Tanggal', 'Username', 'Rekomendasi', 'Review'] #membuat heading tabel
  with open(path, 'w', newline='', encoding='utf-8') as file: #memasukkan kedalam variabel file
    writer = csv.writer(file) #menyimpan dalam bentuk csv
    writer.writerow(heading) #menuliskan heading
    for d in data: #looping data
        writer.writerow(d)
        
# MAIN PROGRAM
page_info = [
  {
    'url': 'https://reviews.femaledaily.com/products/treatment/serum-essence/somethinc/5-niacinamide-moisture-sabi-beet-serum',
    # 'page_limit': 100, #data ~2022
    'page_limit': 635,
    'path': 'scraped-somethinc-niacinamide-all.csv',
  },
  {
    'url': 'https://reviews.femaledaily.com/products/treatment/serum-essence/whitelab/brightening-face-serum-32',
    # 'page_limit': 50, #data ~2022
    'page_limit': 348,
    'path': 'scraped-whitelab-niacinamide-all.csv',
  },
  {
    'url': 'https://reviews.femaledaily.com/products/treatment/serum-essence/the-ordinary/the-ordinary-niacinamide-10-zinc-1',
    # 'page_limit': 50, #data~2022
    'page_limit': 543,
    'path': 'scraped-the-ordinary-niacinamide-all.csv',
  }
]

for info in page_info:
  sze = 0
  try:
    result = scrape(info['url'], info['page_limit'])
    sze = len(result)
    writeFile(result, info['path'])
  except:
    writeFile(result, info['path'] + 'error.csv')
    print('stopeed', sze)