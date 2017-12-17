import requests
import lxml.html
from lxml import html

print("Inicia")

page = requests.get('https://coinmarketcap.com/currencies/bitcoin/#markets')
# print(page.text)
html_info = html.fromstring(page.content)

# coins = html_info.xpath("//a[@class='currency-name-container']/text()")
# coins = html_info.xpath("//tr[starts-with(@id,'id-')]/@id")

for coin_root in html_info.xpath("//table[@id='markets-table']/tbody/tr"):
    # coin_id = coin_root.xpath("@id")
    #print (type(coin_root))
    # print (lxml.html.tostring(coin_root))
    # print (coin_id)
    # coin_market = coin_root.xpath("//td[4]//a/@href")
    # print (coin_root.text_content())
    # print (lxml.html.tostring(coin_root))
    # print (lxml.html.tostring(coin_root.xpath("//td[4]")[0]))
    # print (lxml.html.tostring(coin_root.xpath("//td")[3]))
    # print (coin_root.iterdescendants())
    # print ((coin_root.iterchildren()))
    # print (lxml.html.tostring(coin_root.getchildren()[4]))
    row = coin_root.getchildren()[1].xpath("a/text()")
    notes = coin_root.getchildren()[3].xpath("text()")[0].replace("\n","").strip()
    row.append(notes + coin_root.getchildren()[3].xpath("span/text()")[0].replace("\n","").strip())
    print (row)
    # coin_market = coin_root.xpath("td[4]//a/@href")
    # print (coin_market)
    # break
    
# coins_id = coins_parent.xpath("/@id")

# print ('Coins: ', coins_id)