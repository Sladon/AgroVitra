from urllib.request import urlopen
from bs4 import BeautifulSoup

# products page
url = "https://www.agrovitra.com/productos/"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
results = soup.body.find('div', attrs={'id': 'categories-accordion'}).find_all('a')
links = [r['href'] for r in results]


products_data = []

for link in links:
    product_data = {}
    print(link)
    # each product page
    url = link
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
        
    image = soup.find('meta', property='og:image')
    product_data['image'] = image['content'] if image else None
    
    title = soup.body.find('span', attrs={'data-ui-id': "page-title-wrapper"})
    product_data['title'] = title.string
    
    data = soup.body.find('div', attrs={'class': 'product attribute overview'})
    if data != None:
        print(data)
        description = data.find('div', attrs={'class': 'value'})
        if description != None: product_data['description'] = description.string
        
        use_recomendation = data.find('div', attrs={'id': 'recomendacion_uso'})
        if use_recomendation != None: product_data['use_recomendation'] = use_recomendation.string
        
        chemical_cmp = data.find('div', attrs={'id': 'composicion_quimica'})
        print(chemical_cmp)
        if chemical_cmp!= None:
            chemicals = [val.strip() for val in chemical_cmp.strings if val != '\n' and val.strip() != '']
            chemicals = {chemicals[i].strip(':'): chemicals[i+1] for i in range(0,len(chemicals)-1,2)}
            product_data['chemicals'] = chemicals
        
        elements_div = data.find('ul', attrs={'id': 'elements'})
        if elements_div != None:
            elements = [e.string for e in elements_div.find_all('li')]
            product_data['elements'] = elements
    
    physical_cmp = soup.body.find('div', attrs={'class': "data item content", 'id': "product.info.composicionfisica"})
    if physical_cmp != None:
        list_obj = [val.strip() for val in physical_cmp.strings if val != '\n']
        physical_properties = {list_obj[i]: list_obj[i+1].replace(':', '').strip() for i in range(0,len(list_obj)-1,2)}
        product_data['physical_properties'] = physical_properties
    products_data.append(product_data)
    
for product_data in products_data:
    for key in product_data.keys():
        print(f"{key}: {product_data[key]}")
    print()