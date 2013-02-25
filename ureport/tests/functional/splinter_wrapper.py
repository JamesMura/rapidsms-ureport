from django.contrib.auth.models import User
from django.test import LiveServerTestCase


class SplinterTestCase(LiveServerTestCase):
    def follow_link(self, text):
        (self.browser.find_element_by_link_text(text)).click()


    def select_by_text(self, name, text):
        self.browser.find_by_xpath(
            '//select[@name="%s"]/option[normalize-space(.)="%s"]' % (name, text)).first._element.click()


    def create_and_sign_in_admin(self, password, username):
        self.open('/accounts/login')
        admin_user = User.objects.create_superuser(username, 'admin@test.com', password)
        self.open('/accounts/login')
        self.browser.fill("username", username)
        self.browser.fill("password", password)
        self.browser.find_by_css("input[type=submit]").first.click()
        return admin_user


    def open(self, url):
        self.browser.visit("%s%s" % (self.live_server_url, url))
