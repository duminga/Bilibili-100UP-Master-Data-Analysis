import re

from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_up_info(up_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(up_url)
        time.sleep(5)  # 等待页面加载完成

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 获取昵称
        name_element = soup.find('span', {'id': 'h-name'})
        name = name_element.text.strip() if name_element else None

        # 获取UID
        uid_element = soup.find('div', {'class': 'info-wrap'}).find('span', {'class': 'info-command'}, string='UID')
        uid = uid_element.find_next('span', {'class': 'info-value'}).text.strip() if uid_element else None

        # 获取粉丝数
        followers_element = soup.find('a', {'class': 'n-fs'})
        followers = followers_element.find('p', {'class': 'n-data-v'}).text.strip() if followers_element else None

        # 打印获取的信息
        print("昵称:", name)
        print("UID:", uid)
        print("粉丝数:", followers)

        # 返回信息
        return f"{name}, {uid}, {followers}"

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    finally:
        driver.quit()

if __name__ == '__main__':
    input_file_path = 'up_urls.txt'
    output_file_path = 'up_info.txt'

    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            up_url = line.strip()
            up_info = get_up_info(up_url)
            if up_info:
                output_file.write(up_info + '\n')