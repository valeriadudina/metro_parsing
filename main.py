from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome()
driver.get('https://online.metro-cc.ru/virtual/assortiment_rioba-4887')
data = []
# click button to watch catalog
btn_offline = driver.find_element(by = By.XPATH , value = '//*[@id="__layout"]/div/div/div[7]/div[2]/div[1]/button')
btn_offline.click()
#click button to agree with region
btn_shop = driver.find_element(by = By.XPATH, value = '//*[@id="__layout"]/div/div/div[7]/div[2]/div[4]/button[1]')
btn_shop.click()
#click button to show more
# this may be cycled to get more products 
btn_more = driver.find_element(by = By.XPATH, value = '//*[@id="catalog-wrapper"]/main/div[3]/button')
btn_more.click()
# get data from page
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, 'html.parser')
#fid products on page
products = soup.find_all('div', {'class': 'catalog-2-level-product-card product-card subcategory-or-type__products-item catalog--offline offline-prices-sorting--best-level with-prices-drop'})
base_url = 'https://online.metro-cc.ru'
id = 0
for p in products:
    id += 1
    card = p.find('div', {'class': 'product-card__content'})
    card_2 = card.find('div', {'class': 'product-card__top'})
    name = card_2.find('a').get('title')
    price_regular = card.find('span', {'class':'product-price__sum'}).text
    #discount = card.find('div', {'class': 'product-discount nowrap catalog-2-level-product-card__offline-range-icon-discount style--catalog-2-level-product-card catalog--offline offline-prices-sorting--best-level'})
    discount = card.find('div', {'class': 'catalog-2-level-product-card__offline-range'})
    if discount:
        print('discount')
        discount_2 = discount.find('div', {'class':'product-discount nowrap catalog-2-level-product-card__offline-range-icon-discount style--catalog-2-level-product-card catalog--offline offline-prices-sorting--best-level'})
        if discount_2:
            print('discount_2')
            discount_div = discount.find('div', {'class': 'product-range-prices catalog-2-level-product-card__offline-range-prices style--catalog-2-level-product-card catalog--offline offline-prices-sorting--best-level'})
            discount_div_span = discount_div.find('span', {'class': 'product-price nowrap product-price-discount-above__actual-price style--catalog-2-level-product-card-range-primary-actual color--red catalog--offline offline-prices-sorting--best-level'})
            if discount_div_span:

                price_promo = discount_div_span.text

        else:
            price_promo = False
    else:
        price_promo = False
    brand = 'Rioba'
    link = base_url+card.find('a', {'class':'product-card-name'}).get('href')

    data.append({'id': id, 'name':name, 'brand':brand, 'regular_price': price_regular, 'promo_price' : price_promo, 'url': link })
data_final = {'data':data}
data_json = json.loads('{}')
data_json['data']= data
#write to json file
with open('data.json', 'w') as f:
    json.dump(data_json, f, ensure_ascii=False)
# close browser
driver.quit()
