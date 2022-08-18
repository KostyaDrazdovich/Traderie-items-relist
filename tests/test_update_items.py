from base_test import BaseTest
from steps.relist_steps import RelistSteps


class RelistTest(BaseTest):

    relist_steps = RelistSteps()

    def test_relist_available_items(self):
        self.relist_steps.open_traderie_login_page()
        self.relist_steps.authorize_user()
        self.relist_steps.open_diablo_game_section()
        self.relist_steps.opep_player_profile()
        self.relist_steps.load_all_items()
        self.relist_steps.relist_all_items()
