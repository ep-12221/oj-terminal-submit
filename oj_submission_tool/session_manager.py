import time

import requests
from Demos.win32ts_logoff_disconnected import session
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--window-size=1920x1080")  # 设置窗口大小，避免被 Cloudflare 判断为机器人
driver = webdriver.Chrome(options=options)

class OJSessionManager:
    logged_in = False
    current_oj = None
    oj_name = "codeforces"
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.username = None
        self.password = None
        self.oj_url = None

    def login(self, oj_name, username, password):
        """
        根据OJ平台名称进行登录操作
        :param oj_name: OJ平台名称，如 'codeforces', 'atcoder' 等
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功
        """
        if oj_name.lower() == 'codeforces':
            return self._login_codeforces(username, password)
        elif oj_name.lower() == 'atcoder':
            return self._login_atcoder(username, password)
        else:
            print(f"不支持的OJ平台: {oj_name}")
            return False

    def _login_codeforces(self, username, password):
        """
        登录 Codeforces 平台
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功
        """

        login_url = "https://codeforces.com/enter?back=%2F"
        driver.get(login_url)
        time.sleep(20)
        driver.find_element(By.ID, "handleOrEmail").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "submit").click()
        cookies = driver.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        if "Login successful" in driver.page_source:
            print("登录成功！")
        else:
            print("登录失败！")

    def _login_atcoder(self, username, password):
        """
        登录 AtCoder 平台
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功
        """
        self.session.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
        login_url = "https://atcoder.jp/login"

        response_get = self.session.get(login_url)
        if response_get.status_code == 200:
            print("加载页面成功")
        else:
            print("加载页面失败")
            exit()
        soup = BeautifulSoup(response_get.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        print(csrf_token)
        payload = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token,
        }

        try:
            response = self.session.post(login_url, data=payload)
            if "Invalid login or password" in response.text:
                print("登录失败：用户名或密码错误")
                return False
            elif "logged_in" in response.text:
                self.username = username
                self.password = password
                self.oj_url = login_url
                self.logged_in = True
                print("登录成功！")
                return True
            else:
                print("登录失败：未知错误")
                return False
        except RequestException as e:
            print(f"网络错误: {e}")
            return False

    def logout(self):
        """
        登出当前OJ平台
        """
        if not self.logged_in:
            print("您尚未登录！")
            return
        
        logout_url = f"{self.oj_url}/logout"
        try:
            response = self.session.get(logout_url)
            self.logged_in = False
            self.username = None
            self.password = None
            self.oj_url = None
            print("登出成功！")
        except RequestException as e:
            print("登出失败：{e}")

    def is_logged_in(self):
        """
        检查当前是否已登录
        """
        return self.logged_in

oj_session = OJSessionManager()

def login():
    username = input()
    password = input()
    success = oj_session.login(OJSessionManager.oj_name, username, password)
    return success

