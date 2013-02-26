from splinter import Browser
from ureport.tests.integration.login_page import login_succeeds_with_super_user, login_fails_without_user
from ureport.tests.integration.about_page import about_ureport_page
from ureport.tests.integration.create_poll import admin_can_create_poll
from ureport.tests.integration.join_page import join_page
from ureport.tests.integration.home_page import home_page, home_page_visualisation, home_page_map
from ureport.tests.integration.splinter_wrapper import SplinterTestCase

BROWSER = Browser('firefox')


class UreportTest(SplinterTestCase):
    @classmethod
    def tearDownClass(cls):
        BROWSER.quit()

    def tearDown(self):
        self.open('/account/logout')

    def setUp(self):
        self.browser = BROWSER
        self.open('/')

    def test_home_page(self):
        home_page(self)

    # def test_home_page_visualisation(self):
        # home_page_visualisation(self)

    def test_home_page_map(self):
        home_page_map(self)

    def test_join_page(self):
        join_page(self)

    def test_create_poll(self):
        admin_can_create_poll(self)

    def test_about_page(self):
        about_ureport_page(self)

    def test_login_for_admin(self):
        login_succeeds_with_super_user(self)

    def test_login_fails_for_non_user(self):
        login_fails_without_user(self)