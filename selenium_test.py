from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import time,sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') # Change default encoding to utf8  
options = webdriver.ChromeOptions()
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--proxy-server=http://127.0.0.1:8080')
#options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, 20)
#不加载图片,加快访问速度
resutls = []

def index_page(KEYWORD,PAGE):
    url = 'https://s.taobao.com/search?q=' + KEYWORD
    browser.get(url)
    for i in range(1, PAGE + 1):
        try:
            if(i > 1):
                input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
                submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(i)
                time.sleep(5)
                submit.click()
            wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(i)))
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            get_products()
        except TimeoutError:
            print("Time error ")
        time.sleep(10)
    browser.close()
    save_content()
    
      
def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        resutls.append(product)

def save_content():
    if(len(resutls) < 0):
        return
    f = open("D:/下载/TAOBAO.TXT","w",encoding='utf-8')
    for result in resutls:
        f.writelines(resutl)
    f.flush()
    f.close()

if __name__ == '__main__':
    index_page("汉服",5)