# -*- coding: utf-8 -*-
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException, TimeoutException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from waiting import wait

from ui.core.browser import Browser

UI_TIMEOUT = 10


def update_locator_type(locator):
    if isinstance(locator, str):
        return By.CSS_SELECTOR, '{}'.format(locator)
    else:
        return locator


class UiActions(object):

    @staticmethod
    def count_elements(locator):
        locator = update_locator_type(locator)
        return len(Browser.webdriver.find_elements(locator[0], locator[1]))

    @staticmethod
    def wait_for_element_is_displayed(locator, timeout_seconds=UI_TIMEOUT):
        locator = update_locator_type(locator)

        driver_wait = WebDriverWait(Browser.webdriver,
                                    timeout_seconds,
                                    ignored_exceptions=StaleElementReferenceException)

        return driver_wait.until(ec.visibility_of_element_located(locator),
                                 message=u'Element {} was not found.'.format(locator))

    @staticmethod
    def remove_ads_in_footer():
        Browser.webdriver.execute_script('document.getElementById("pw-oop-bottom_rail").remove();')

    @staticmethod
    def wait_for_element_missing_in_dom(locator, click_on_element=True, timeout_seconds=16):
        locator = update_locator_type(locator)

        def waiter():
            try:
                Browser.webdriver.find_element(locator[0], locator[1])
                if click_on_element:
                    Browser.webdriver.find_element(locator[0], locator[1]).click()
                return False

            except NoSuchElementException:
                return True

        wait(waiter,
             timeout_seconds=timeout_seconds,
             sleep_seconds=3,
             waiting_for=u'Element {} seems to be visible.'.format(locator))

    @staticmethod
    def find_and_fill(locator, text, timeout_seconds=UI_TIMEOUT):
        locator = update_locator_type(locator)
        text = str(text)

        def locate_fill():
            driver_wait = WebDriverWait(Browser.webdriver, 1)
            try:
                el = driver_wait.until(
                    ec.visibility_of_element_located(locator), message=u'Element {} was not found.'.format(locator))

                el.clear()
                el.send_keys(text)
                return True

            except (StaleElementReferenceException, TimeoutException):
                return False

        return wait(
            locate_fill,
            timeout_seconds=timeout_seconds,
            sleep_seconds=2,
            waiting_for=u'Element {} was not found or text was not entered.'.format(locator),
        )

    @staticmethod
    def find_and_click(locator,
                       wait_for_element_in_dom=True,
                       wait_for_element_is_visible=True,
                       wait_for_element_is_enabled=False,
                       click_until_button_is_hidden=False,
                       timeout_seconds=UI_TIMEOUT):
        locator = update_locator_type(locator)

        def locate_click():
            el = None
            driver_wait = WebDriverWait(driver=Browser.webdriver,
                                        timeout=2,
                                        ignored_exceptions=StaleElementReferenceException)
            try:
                if wait_for_element_in_dom:
                    el = driver_wait.until(
                        ec.presence_of_element_located(locator),
                        message=u'find_and_click: element_in_dom: element {} was not found.'.format(locator)
                    )
                if wait_for_element_is_visible:
                    el = driver_wait.until(
                        ec.visibility_of_element_located(locator),
                        message=u'find_and_click: wait_for_element_is_visible:'
                                u' element {} was not found.'.format(locator)
                    )
                if wait_for_element_is_enabled:
                    el = driver_wait.until(
                        ec.element_to_be_clickable(locator),
                        message=u'find_and_click: wait_for_element_is_enabled:'
                                u' element {} was not found.'.format(locator)
                    )

                if click_until_button_is_hidden:
                    def repeated_click():
                        try:
                            el.click()
                        except WebDriverException:
                            pass
                        return driver_wait.until(
                            ec.invisibility_of_element_located(locator)
                        )
                    wait(repeated_click,
                         timeout_seconds=timeout_seconds,
                         sleep_seconds=1,
                         waiting_for=u'find_and_click: repeated_click: element {} is still visible')
                else:
                    try:
                        el.click()
                    except WebDriverException as e:
                        if 'Reached error page' not in e.msg:
                            raise e

                return True

            except TimeoutException:
                return False

            except StaleElementReferenceException:
                return True

        return wait(
            locate_click,
            timeout_seconds=timeout_seconds,
            sleep_seconds=2,
            waiting_for=u'find_and_click: element {} was not found.'.format(locator),
        )
