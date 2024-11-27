import requests
from requests.exceptions import RequestException

logged_in = False
current_oj = None
class OJSessionManager:
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
        login_url = "https://codeforces.comenter"
        payload = {
            'handleOrEmail': username,
            'password': password,
            '_tta': '385'  # 防止重复提交
        }

        try:
            response = self.session.post(login_url, data=payload)
            if "Wrong handle or password" in response.text:
                print("登录失败：用户名或密码错误")
                return False
            elif "Logout" in response.text:
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

    def _login_atcoder(self, username, password):
        """
        登录 AtCoder 平台
        :param username: 用户名
        :param password: 密码
        :return: 登录是否成功
        """
        login_url = "https://atcoder.jp/login"
        payload = {
            'name': username,
            'password': password,
        }

        try:
            response = self.session.post(login_url, data=payload)
            if "Invalid login or password" in response.text:
                print("登录失败：用户名或密码错误")
                return False
            elif "Logout" in response.text:
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
            print(f"登出失败：{e}")

    def is_logged_in(self):
        """
        检查当前是否已登录
        """
        return self.logged_in


def login():
    global logged_in
    logged_in = True
    # 实现登录逻辑

def logout():
    global logged_in
    logged_in = False
    # 实现登出逻辑

def set_oj(oj_name):
    global current_oj
    current_oj = oj_name
