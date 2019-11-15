import requests
from bs4 import BeautifulSoup
import smtplib
from colorama import *
init()
import time

URL=input('Unesite link kola sa poloviniautobili.com: ')
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
to_mail=input('Unesite Vas mail: ')

def check_price():
    page=requests.get(URL, headers=headers)
    soup=BeautifulSoup(page.text, 'html.parser')

    # title=soup.find(id="productTitle").get_text().strip()
    price=soup.find("div", class_="price-item position-relative").get_text().strip()

    converted_price=float(price[0:5])

    desired_price=input('Ispod koje cene zelite da opadne da bi bili obavesteni? (u formatu: npr. 5.200): ')

    new_price=float(desired_price)/1000
    # print(new_price)

    if (converted_price<=new_price):
        send_mail()
    else:
        print(Fore.RED + 'Cena nije pala! Proverava se na svakih 12 sati! ' + Fore.LIGHTYELLOW_EX + 'Trenutna cena je: ' + str(converted_price) + ' hljada eura')
    
    while(converted_price>new_price):
        time.sleep(21600)
        check_price()

def send_mail():
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('dane.sto@gmail.com','fkpblyybpcnmuqin')
    to_mail

    subject='Cena je pala'
    body=f'Proverite link {URL}'
    msg=f'Subject {subject}\n\n{body}'

    server.sendmail(
        'dane.sto@gmail.com',
        to_mail,
        msg
    )

    print(Fore.BLUE + 'Cena je opala, poruka sa linkom proizvoda je poslata na Vas mail')
    server.quit()

check_price()
