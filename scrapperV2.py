from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

links = []

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.agrovitra.com/productos/")
    html = page.inner_html('#categories-accordion')
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('a')
    for result in results:
        links.append(result['href'])
    page.close()

for link in links[:2]:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        content = page.inner_html('#maincontent')
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('span', attrs={'data-ui-id': "page-title-wrapper"})
        data = soup.find('div', attrs={'class': 'product attribute overview'})
        print(data)
        page.close()