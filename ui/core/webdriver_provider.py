from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

BROWSER_TYPE = 'chrome'


class BrowserType(object):
    CHROME = 'chrome'
    FIREFOX = 'firefox'


def init_driver():
    driver = None

    if BROWSER_TYPE.lower() == BrowserType.CHROME:
        options = ChromeOptions()
        options.add_argument('disable-notifications')
        options.add_argument('ignore-certificate-errors')
    else:
        raise NotImplementedError('Unsupported browser type: {}.'.format(BROWSER_TYPE))

    if BROWSER_TYPE.lower() == BrowserType.CHROME:
        service = Service(executable_path=r"..\chromedriver\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(0)
    driver.maximize_window()

    return driver
