import requests
import lxml.html
from lxml import html

print("Inicia")

page = requests.get('https://coinmarketcap.com/')
# print(page.text)
html_info = html.fromstring(page.content)

# coins = html_info.xpath("//a[@class='currency-name-container']/text()")
# coins = html_info.xpath("//tr[starts-with(@id,'id-')]/@id")

coins_parent = html_info.xpath("//tr[starts-with(@id,'id-')]")

for coin_root in html_info.xpath("//tr[starts-with(@id,'id-')]"):
    coin_id = coin_root.xpath("@id")
    #print (type(coin_root))
    print (coin_id)
    # coin_market = coin_root.xpath("//td[4]//a/@href")
    # print (coin_root.text_content())
    # print (lxml.html.tostring(coin_root))
    # print (lxml.html.tostring(coin_root.xpath("//td[4]")[0]))
    # print (lxml.html.tostring(coin_root.xpath("//td")[3]))
    # print (coin_root.iterdescendants())
    # print ((coin_root.iterchildren()))
    # print (lxml.html.tostring(coin_root.getchildren()[4]))
    # print (coin_root.getchildren()[4].xpath("a/@href"))
    coin_market = coin_root.xpath("td[4]//a/@href")
    print (coin_market)
    # break
    
# coins_id = coins_parent.xpath("/@id")

# print ('Coins: ', coins_id)