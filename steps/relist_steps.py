import time

from steps import step
from ui.traderie_diablo2 import TraderiePage
from ui.core.ui_actions import UiActions

login = ''
password = ''


class RelistSteps(object):

    traderie_page = TraderiePage()
    ui_actions = UiActions()

    @step
    def open_traderie_login_page(self):
        self.traderie_page.open_page(url=self.traderie_page.main_url)
        self.accept_consents()
        self.traderie_page.open_page(url=self.traderie_page.login_url)

    @step
    def authorize_user(self):
        self.ui_actions.find_and_fill(self.traderie_page.login_field_locator, login)
        self.ui_actions.find_and_fill(self.traderie_page.password_field_locator, password)
        self.ui_actions.find_and_click(self.traderie_page.submit_login_button_locator)

    @step
    def accept_consents(self):
        self.ui_actions.find_and_click(self.traderie_page.save_consent_button)

    @step
    def open_diablo_game_section(self):
        if self.ui_actions.wait_for_element_is_displayed(self.traderie_page.close_pop_up_locator):
            self.ui_actions.find_and_click(self.traderie_page.close_pop_up_locator)
        self.ui_actions.find_and_click(self.traderie_page.traderie_main_button)
        self.ui_actions.find_and_click(self.traderie_page.diablo2_game_selection)

    @step
    def opep_player_profile(self):
        self.ui_actions.find_and_click(self.traderie_page.profile_button)
        self.ui_actions.wait_for_element_is_displayed(self.traderie_page.hide_listing_button)

    @step
    def load_all_items(self):
        self.ui_actions.remove_ads_in_footer()
        self.ui_actions.wait_for_element_missing_in_dom(self.traderie_page.load_more_button)

    @step
    def relist_all_items(self):
        items_to_relist = self.ui_actions.count_elements(self.traderie_page.relist_button)
        print(f'Total count of items to relist is: {items_to_relist}')
        for _ in range(items_to_relist):
            self.ui_actions.find_and_click(self.traderie_page.relist_button)
            time.sleep(0.8)
