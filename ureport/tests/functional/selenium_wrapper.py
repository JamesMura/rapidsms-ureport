from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select


class SeleniumTestCase(LiveServerTestCase):
    def assert_element_exists(self, element_selector):
        try:
            self.wd.find_element_by_css_selector(element_selector)
        except NoSuchElementException:
            raise AssertionError("Element  {0} does not exist.".format(element_selector))


    def assert_link_exists_with_text(self, text):
        try:
            self.wd.find_element_by_link_text(text)

        except NoSuchElementException:
            raise AssertionError("Link with  text: {0} does not exist.".format(text))

    def assert_element_exists_with_text(self, element_selector, text):
        try:
            element = self.wd.find_element_by_css_selector(element_selector)
            if text in element.text:
                pass
            else:
                print element.text
                raise AssertionError("Element {0} with  text: {1} does not exist.".format(element_selector, text))
        except NoSuchElementException:
            raise AssertionError("Element  {0} does not exist.".format(element_selector))

    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))

    def fill_input_with_text(self, element, username_text):
        username_element = self.wd.find_element_by_name(element)
        username_element.send_keys(username_text)


    def click_element(self, element_name):
        self.wd.find_element_by_css_selector(element_name).click()

    def create_and_sign_in_admin(self, password, username):
        self.open('/accounts/login')
        admin_user = User.objects.create_superuser(username, 'admin@test.com', password)
        self.open('/accounts/login')
        self.fill_input_with_text("username", username)
        self.fill_input_with_text("password", password)
        self.click_element("input[type=submit]")
        return admin_user

    def follow_link(self, text):
        self.assert_link_exists_with_text(text)
        (self.wd.find_element_by_link_text(text)).click()

    def select_option_by_text(self, option_text, select_id):
        select = Select(self.wd.find_element_by_id(select_id))
        print select.options
        print [o.text for o in select.options]
        select.select_by_visible_text(option_text)







