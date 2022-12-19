from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, Comment

links = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.agrovitra.com/productos/")
    html = page.inner_html('#categories-accordion')
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a')
    for result in results:
        links.append(result['href'])
    page.close()

for link in links[7:]:
    print(link)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        page.wait_for_function
        content = page.inner_html('#maincontent')
        soup = BeautifulSoup(content, 'html.parser')
        for element in soup(text=lambda text: isinstance(text, Comment)):
                element.extract()
        soup.prettify()

        product_data = {}
        title = soup.find('span', attrs={'data-ui-id': "page-title-wrapper"}).string
        product_data['title'] = title
        data = soup.find('div', attrs={'class': 'product attribute overview'})
        if data != None:
            description = data.find('div', attrs={'class': 'value'}).string
            use_recomendation = data.find('div', attrs={'id': 'recomendacion_uso'}).string
            chemical_cmp = data.find('div', attrs={'id': 'composicion_quimica'})
            chemicals = [val.strip() for val in chemical_cmp.strings if val != '\n' and val.strip() != '']
            chemicals = {chemicals[i].strip(':'): chemicals[i+1] for i in range(0,len(chemicals)-1,2)}
            elements_div = data.find('ul', attrs={'id': 'elements'})
            elements = [e.string for e in elements_div.find_all('li')]
            
            product_data['elements'] = elements
            product_data['description'] = description
            product_data['use_recomendation'] = use_recomendation
            product_data['chemicals'] = chemicals
        physical_cmp = soup.find('div', attrs={'class': "data item content", 'id': "product.info.composicionfisica"})
        
        if physical_cmp != None:
            list_obj = [val.strip() for val in physical_cmp.strings if val != '\n']
            physical_properties = {list_obj[i]: list_obj[i+1].replace(':', '').strip() for i in range(0,len(list_obj)-1,2)}
            product_data['physical_properties'] = physical_properties
        
        print(product_data)
        page.close()