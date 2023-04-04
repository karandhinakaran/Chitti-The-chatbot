from bs4 import BeautifulSoup
import requests, lxml

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
params = {"q": 'how old is trump'}


r = requests.get('https://www.google.com/search', headers=headers, params=params)
soup = BeautifulSoup(r.text, 'lxml')

def bot(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    params = {"q": query}


    r = requests.get('https://www.google.com/search', headers=headers, params=params)
    soup = BeautifulSoup(r.text, 'lxml')

    selectors = ['.CfV8xf', '#cwos', '#wob_tm', '#wob_dc', '.SwHCTb', '.t2b5Cf', '.hgKElc', '.bjhkR', '.wT3VGc', '.UdvAnf']
    for select in selectors:
        try:
            result = soup.select(select)
            return result[-1].text
        except:
            pass
    return ''
