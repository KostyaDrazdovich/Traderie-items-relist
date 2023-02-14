from ui.core.browser import Browser
from selenium.webdriver.common.by import By


class TraderiePage(object):

    main_url = 'https://traderie.com'
    login_url = 'https://traderie.com/login'

    @staticmethod
    def open_page(url):
        browser = Browser()
        browser.get(url)

    # Personal cabinet buttons
    profile_button = (By.CSS_SELECTOR, "a[class*='profile-link'][href*='/diablo2resurrected/profile']")
    hide_listing_button = (By.CSS_SELECTOR, "button[class='btn-alt toggle-listing-btn']")
    relist_button = (By.XPATH, "//button[contains(text(),'Relist')]")
    load_more_button = (By.XPATH, "//button[contains(text(),'Load More')]")

    # Authorization
    login_field_locator = (By.XPATH, "//input[@name='username']")
    password_field_locator = (By.XPATH, "//input[@name='password']")
    submit_login_button_locator = (By.XPATH, "//div[@class='login-btn-bar']//button[@type='submit']")
    diablo2_game_selection = (By.CSS_SELECTOR, "a[href='/diablo2resurrected']")
    traderie_main_button = (By.CSS_SELECTOR, "a[class*='nav-desktop']")
    save_consent_button = (By.XPATH, "//p[contains(text(),'Consent')]")

    close_pop_up_locator = (By.XPATH, '//div[@id="close-modal"]')
