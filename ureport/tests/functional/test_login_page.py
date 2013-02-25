from selenium.webdriver.chrome.webdriver import WebDriver
from ureport.tests.functional.splinter_wrapper import SplinterTestCase
from splinter import Browser


class LoginPageTest(SplinterTestCase):
    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def test_login_fails_without_user(self):
        self.open('/accounts/login')
        self.browser.fill("username", "a")
        self.browser.fill("password", "a")
        self.browser.find_by_css("input[type=submit]").first.click()
        assert self.browser.is_text_present('Oops. Your username and password didn\'t match. Please try again.')

    def test_login_succeeds_with_super_user(self):
        user = self.create_and_sign_in_admin("pass", "jamo")
        assert self.browser.is_text_present('POLL ADMIN')
        assert self.browser.is_text_present('MESSAGE LOG')
        assert self.browser.is_text_present('MESSAGE CLASSIFICATION')
        assert self.browser.is_text_present('UREPORTERS')
        assert self.browser.is_text_present('FLAGGED MESSAGES')
        assert self.browser.is_text_present('Real Time')