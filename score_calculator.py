import csv
from collections import Counter
energy_consumption = Counter({
       'cotton': 4.9,
       'wool': 0.8,
       'polyester': 10.9,
       'viscose': 7.1,
       'spandex': 13.5,
       'rayon': 6.8,
       'acrylic': 0.2,
       'nylon': 6.8,
       'metallic-fiber': 53.6,
       'lyocell': 3.6,
       'polyurethane': 2.5,
       })
water_consumption = Counter({
    'cotton': 125.0,
    'wool': 12.5,
    'polyester': 0,
    'viscose': 64.0,
    'spandex': 2.6,
    'rayon': 19.0,
    'acrylic': 0.2,
    'nylon': 0.2,
    'metallic-fiber': 1.2,
    'lyocell': 1.2,
    'polyurathane': 79.0,
})

def read_materials(m):
    remove = "[]'"
    for char in remove:
        if char in m:
            m = m.replace(char,'')
    n = m.split(', ')
    while len(n) < 3:
        n.append('0 Nothing')
    materials = []
    for e in n:
        a = []
        try:
            percentage = float(e.split(" ")[0].replace("%",""))/100
        except:
            continue
        a.append(percentage)
        if e.split(" ")[1] != 'Nothing':
            fabric = e.split(" ")[1].lower()
            a.append(fabric)
            materials.append(a)
    return materials
def calculate_score(m):
    m = read_materials(m)
    score = 0
    for item in m:
        score += item[0] * water_consumption[item[1]] + item[0] * energy_consumption[item[1]]
    score = round((score + 20) / 2)
    return score
        
