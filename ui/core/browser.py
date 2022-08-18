from selenium.common.exceptions import WebDriverException

from ui.core.webdriver_provider import init_driver


class Browser(object):

    webdriver = None

    @staticmethod
    def get_webdriver():
        if not Browser.webdriver:
            Browser.webdriver = init_driver()
        return Browser.webdriver

    def get(self, *args, **kwargs):
        # Fix cases when browser is down but webdriver object still exists

        try:
            return self.get_webdriver().get(*args, **kwargs)
        except WebDriverException as e:
            if any(['Malformed URL' in e.msg, 'Reached error page' in e.msg, 'ERR_NAME_NOT_RESOLVED' in e.msg]):
                pass
            elif 'Session timed out or not found' in e.msg:
                Browser.webdriver = None
                return self.get_webdriver().get(*args, **kwargs)
            else:
                Browser.quit_browser()

    def __getattr__(self, item):
        return getattr(self.get_webdriver(), item)

    @staticmethod
    def is_webdriver_inited():
        return getattr(Browser, 'webdriver', None) is not None

    def get_cookies(self):
        cookies = {}
        for cookie in self.webdriver.get_cookies():
            cookies[cookie['name']] = {'value': cookie.get('value'),
                                       'expiry': cookie.get('expiry'),
                                       'sameSite': cookie.get('sameSite')}
        return cookies

    def get_raw_cookies(self):
        """Return browser cookies as is."""
        return self.webdriver.get_cookies()

    @staticmethod
    def quit_browser():
        if Browser.is_webdriver_inited():
            Browser.webdriver.quit()
            Browser.webdriver = None
