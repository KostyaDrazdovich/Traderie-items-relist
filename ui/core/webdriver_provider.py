from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service

BROWSER_TYPE = 'chrome'


class BrowserType(object):
    CHROME = 'chrome'


def init_driver():
    driver = None

    if BROWSER_TYPE.lower() == BrowserType.CHROME:
        options = ChromeOptions()
        options.add_argument("disable-notifications")
        options.add_argument("ignore-certificate-errors")

        # Avoid Cloudflare
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("prefs", prefs)
    else:
        raise NotImplementedError('Unsupported browser type: {}.'.format(BROWSER_TYPE))

    if BROWSER_TYPE.lower() == BrowserType.CHROME:
        service = Service(executable_path=r"..\chromedriver\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)
        # Avoid Cloudflare
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source': '''
                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                   delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                                   '''})

    driver.implicitly_wait(0)
    driver.maximize_window()

    return driver
