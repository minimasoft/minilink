from base58 import b58encode
from hashlib import sha256
from hmac import HMAC
from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter,Retry


def crawl_session():
    session = Session()
    retries = Retry(total=3, backoff_factor=0.35, status_forcelist=[500,502,503,504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        })
    return session


def short_link(target_link: str, key: str='test') -> str:
    return b58encode(HMAC(key.encode('utf-8'),target_link.encode('utf-8'),sha256).digest()).decode('utf-8')[-6:]


def gen_page(target_link: str):
    session = crawl_session()
    with session.get(target_link) as response:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('head').find('title')
        metas = "\n".join(str(meta) for meta in soup.find('head').find_all('meta'))
    result = f"<!DOCTYPE html><html>\n<head>\n{title}\n{metas}\n</head>\n<body>\n"
    result += f'<h1>Ir a <a href="{target_link}">{target_link}</a></h1>\n</body>\n</html>\n'
    return result



#print(short_link("https://www.google.com/"))
print(gen_page("https://www.infobae.com/politica/2025/04/15/javier-milei-todos-los-factores-monetarios-empujan-para-que-el-tipo-de-cambio-caiga/"))
