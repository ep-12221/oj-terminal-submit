import unittest
from session_manager import OJSessionManager  # 假设你的类在一个叫做 oj_session_manager 的模块里


class TestOJSessionManagerIntegration(unittest.TestCase):

    def test_login_codeforces(self):
        # 使用有效的用户名和密码
        username = 'ss11111'
        password = 'zx051226'

        oj_manager = OJSessionManager()
        result = oj_manager.login('codeforces', username, password)

        self.assertTrue(result, "登录失败，请检查用户名和密码是否正确")
        self.assertTrue(oj_manager.logged_in, "登录状态没有正确设置")


if __name__ == '__main__':
    unittest.main()
