import requests as rq
import csv 
from bs4 import BeautifulSoup 
from tqdm import tqdm 
 
 
last_page_number = 27 
 
URL = 'https://www.kivano.kg/mobilnye-telefony' 
 
def get_page(url): 
    response = rq.get(url) 
    return response.text 
 
 
 
def get_soup(page_content): 
    soup = BeautifulSoup(page_content, 'html.parser') 
    return soup 
 
 
 
def get_product_cards(soup): 
    products_list = soup.find('div', class_ = 'list-view') 
    product_cards = products_list.find_all ('div', class_= 'item') 
    return product_cards 
 
 
def get_product_info(product_card): 
    title_element = product_card.find('div',class_ = 'pull-right').find('div',class_='product_text').find('div',class_ = 'listbox_title').find('a') 
    title = title_element.text 
    ditail_link = title_element.get('href') 
    price_element = product_card.find('div', class_='pull-right').find('div',class_='motive_box').find('div', class_='listbox_price') 
    price = price_element.text 
 
    image_element = product_card.find('div',class_='listbox_img').find('a').find('img') 
    # linc = 'https://www.kivano.kg' 
    images_link = image_element.get('src') 
 
    info = { 
        'title':title, 
        'price':price, 
        'details':ditail_link, 
        'image':f'https://www.kivano.kg{images_link}\n' 
    } 
     
    return info  
 
 
 
def write_to_csv(data): 
    with open('products.csv', 'w') as file: 
        fieldnames = ['title', 'price', 'image','details'] 
        writer = csv.DictWriter(file,fieldnames=fieldnames) 
        writer.writeheader() 
        writer.writerows(data) 
 
 
def main(): 
    product = [] 
    for num in tqdm(range(1, last_page_number + 1)): 
        page_url = f'{URL}?page={num}' 
        page_content = get_page(page_url) 
        page_soup = get_soup(page_content) 
        product_cards = get_product_cards(page_soup) 
        page_products = [] 
        for card in tqdm(product_cards, f'проходим по странице {num}'): 
            prod = get_product_info(card) 
            page_products.append(prod) 
        product.extend(page_products) 
    write_to_csv(product) 
 
 
    return product 
 
print(main())