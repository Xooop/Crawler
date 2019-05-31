import os
import re

import cn2an
import sys
import yagmail
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# 发送邮件的邮箱配置
user = "" # xxx@qq.com(其他邮箱请对应修改smtp服务器)
password = "" # 邮箱密码
# 发送更新邮件到哪个邮箱
email_address = ""
# chrome浏览器位置
chrome_position = "/opt/google/chrome/google-chrome"
# chromedriver驱动位置
chrome_driver = "/root/chromedriver"

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.binary_location = chrome_position
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")

detailUrl = "detail-url"
latestChapter = "latest-chapter"


def load_config():
    file_path = './books.yaml'
    if not os.path.exists(file_path):
        os.system(r"touch{}".format(file_path))
    # 读取yaml文件
    file = open(file_path, encoding='utf-8')
    dct = yaml.load(file)
    file.close()
    return dct


def dump_config(dct):
    # 写入yaml文件
    file = open("./books.yaml", 'w+', encoding='utf-8')
    yaml.dump(dct, stream=file, encoding='utf-8', allow_unicode=True)
    file.close()


def send_email(subject, content, send_to):
    yag = yagmail.SMTP(user=user, password=password, host='smtp.qq.com')
    yag.send(to=send_to, subject=subject, contents=content)


def monitor(bookname):
    dct = load_config()
    if dct is None:
        dct = {}
    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
    # 如果文件中不包含书籍的详情地址，则去搜索栏搜索并拿到详细地址，存入文件
    if bookname not in dct or dct[bookname] is None or dct[bookname][detailUrl] is None \
            or dct[bookname][detailUrl] == '':
        init_url = 'https://www.biquge5.com/'
        driver.get(init_url)
        driver.find_element_by_id("searchkey").send_keys(bookname)
        driver.find_element_by_id("sss").click()
        detail_url = driver.find_element_by_xpath(
            "//div[@class=\"container body-content\"]//child::node()[@href]").get_attribute("href")
        tmp = {detailUrl: detail_url, latestChapter: None}
        dct[bookname] = tmp
        dump_config(dct)

    # 爬取详情地址对应的最新章节，与yaml里记录的最新章节进行比对
    url = dct[bookname][detailUrl]
    driver.get(url)
    locator = (By.XPATH, "//div[@id=\"maininfo\"]/div/p/a")
    WebDriverWait(driver, 20, 0.1) \
        .until(expected_conditions.presence_of_element_located(locator))
    raw = driver.find_element_by_xpath("//div[@id=\"maininfo\"]/div/p/a").text
    refer_url = driver.find_element_by_xpath("//div[@id=\"maininfo\"]/div/p/a").get_attribute("href")
    pattern = re.compile("第(.*)章")
    num = cn2an.cn2an(pattern.search(raw).group(1), "strict")
    driver.close()
    driver.quit()

    # 如果更新了，则发送邮件
    subject = '小说更新提示'
    content = '小说: ' + bookname + '更新了~' + '\n快戳这里->' + refer_url
    if dct[bookname][latestChapter] is None or num > int(dct[bookname][latestChapter]):
        send_email(subject, content, email_address)
        dct[bookname][latestChapter] = num
        dump_config(dct)


if __name__ == '__main__':
    monitor(sys.argv[1])
