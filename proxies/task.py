import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from lxml import html
import pandas as pd

proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1910,1070")
chrome_options.add_argument("--headless")
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")


def func1():
    url = 'http://spys.ru/free-proxy-list/IE'
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)
    select = Select(driver.find_element_by_xpath("//select[@id='xpp']"))
    time.sleep(2)
    select.select_by_visible_text("500")
    time.sleep(3)
    tree = html.fromstring(driver.page_source)
    driver.close()
    driver.quit()
    rows = tree.xpath("//table//tr[contains(@class,'spy')]//td//a[@href]/parent::td/parent::tr")
    ips = []
    ports = []
    for row in rows:
        ip = "".join(row.xpath("./td//text()")[2])
        port = "".join(row.xpath("./td//text()")[5])
        if ip.strip() != '' and port.strip() != '':
            ips.append(ip)
            ports.append(port)
    dataframe = pd.DataFrame({'IP': ips, 'Ports': ports})
    dataframe.to_csv("./f1.csv", index=False, sep=',')


if __name__ == '__main__':
    func1()
