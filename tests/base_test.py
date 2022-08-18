import atexit
from unittest import TestCase
from ui.core.browser import Browser


class BaseTest(TestCase):
    def __init__(self, methodName='runTest'):
        super(BaseTest, self).__init__(methodName=methodName)


def close_browser_at_the_end():
    Browser.quit_browser()


atexit.register(close_browser_at_the_end)
