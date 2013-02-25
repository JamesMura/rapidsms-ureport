from splinter import Browser
from ureport.tests.functional.splinter_wrapper import SplinterTestCase


class JoinPageTest(SplinterTestCase):
    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def test_join_page(self):
        self.open('/join/')
        assert self.browser.is_text_present('Ureport')
        assert self.browser.is_text_present('How To Join')