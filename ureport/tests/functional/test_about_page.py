from splinter import Browser
from ureport.tests.functional.splinter_wrapper import SplinterTestCase


class AboutPageTest(SplinterTestCase):
    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def test_about_ureport_page(self):
        self.browser.visit(self.live_server_url + '/about_ureport/')
        assert self.browser.is_text_present('About Ureport')