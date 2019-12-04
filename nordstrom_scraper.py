from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import score_calculator as sc

def header(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def main():
    queries = ['Sweaters & Cardigans', 'Shirts', 'Jeans', 'Jackets & Coats', 'Hoodies & Sweatshirts', 'Pants', 'T-shirts & Tank tops', 'Basics', 'Jackets & Suits', 'Accessories', 'Shoes', 'Underwear & Loungewear', 'Sportswear', 'Swimwear', 'Shorts', 'Casual', 'Divided', 'H&M Man', 'Modern Classics']
    output = "picture,price,link,material,score,name,section,brand,keyword"
    for key in queries:
        output += query(key)
    f = open('nordstrom2.csv','w',errors='ignore')
    f.write(output)
    f.close()

def query(key):
    url = "http://shop.nordstrom.com/sr?contextualsectionid=60137519&origin=keywordsearch&keyword=" + key.replace(" ","+")
    soup = header(url)
    links = soup.find_all('a', {'class': 'product-href'})
    output = ""
    for link in links:
        output += "\n" + parse_item("https://nordstrom.com" + link.get('href'))
        output += key
    print("-----COMPLETED " + key)
    print(output)
    return output

def parse_item(url):
    soup = header(url)
    row = ""

    # image
    #div = soup.find('div', {'class' : 'main-content-image-wrapper'})
    #if div :
    #    image = div.findChildren()[0].get('src')
    #    row += image + ","
    #else:
    #    row += ","

    # price
    if soup.find('div', {'class' : '3p7kp'}):
        p = soup.find('div', {'class' : 3p7kp'}).text
    else:
        p = soup.find('div', {'class' : 'price-display-item regular-price'}).text
    q = re.compile("\d+\.\d+")
    price = q.findall(p)[0]
    row += price + ","

    # link
    row += url + ","

    # material and score
    div2 = soup.find('div', {'class' : "ErtZY"})
    r = re.compile("\d+\%")
    ul = div2.findChildren()[0].find_next_sibling()
    m = ul.find('li', {'data-reactid' : r})
    if m:
        material = m.text
        row += material.replace(',',' ') + "," + str(sc.calculate_score(material)) + ","
        print(sc.calculate_score(material))
    else:
        row += ",,"

    # name
    section = soup.find('section', {'class' : 'np-product-title'})
    name = section.findChildren()[0].text
    row += name + ","

    # section
    li = soup.find('li', {'data-element' : 'item_1'})
    if li:
        section = li.findChildren()[0].text
        row += section + ","
    else:
        row += ","

    # brand
    section = soup.find('section', {'class' : 'brand-title'})
    data = section.findChildren()
    row += "Nordstorm,"
    print("processing" + name)
    return row


def computeScore(material):
    energy_consumption = {
        'cotton': 49,
        'wool': 8,
        'polyester': 109,
        'viscose': 71,
        'spandex': 135,
        'rayon': 68,
        'acrylic': 2,
        'nylon': 68,
        'metallic fiber': 536,
        'lyocell': 36,
        }
    water_consumption = {
        'cotton': 12500,
        'wool': 125,
        'polyester': 0,
        'viscose': 640,
        'spandex': 26,
        'rayon': 190,
        'acrylic': 2,
        'nylon': 2,
        'metallic fiber': 12,
        'lyocell':12,
        }
    materials = material.split('  ')
    score = 0.0
    for m in materials:
        m = m.split('% ')
        try:
            score += int(m[0]) / 100 * (energy_consumption[m[1]] + water_consumption[m[1]]) / 2
        except:
            score += 6.12
    return score

main()
