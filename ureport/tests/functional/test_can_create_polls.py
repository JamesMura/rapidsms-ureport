from splinter import Browser
from ureport.tests.functional.splinter_wrapper import SplinterTestCase


class CreatePollTest(SplinterTestCase):
    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()

    def create_group(self, name):
        self.open('/admin/auth/group/')
        self.browser.click_link_by_partial_text('Add group')
        self.browser.fill("name", name)
        self.browser.find_by_name('_save').first.click()

    def create_backend(self, name):
        self.open('/admin/rapidsms/backend/')
        self.browser.click_link_by_partial_text('Add backend')
        self.browser.fill("name", name)
        self.browser.find_by_name('_save').click()

    def create_contact(self, name, phone, username, group_name, backend_name):
        self.open('/admin/rapidsms/contact/')
        self.browser.click_link_by_partial_text('Add contact')
        self.browser.fill("name", name)
        self.select_by_text('user', username)
        self.select_by_text('groups', group_name)
        self.browser.fill('birthdate_0', '2013-02-22')
        self.browser.fill('birthdate_1', '12:55:40')
        self.select_by_text('gender', 'Male')
        self.select_by_text('connection_set-0-backend', backend_name)
        self.browser.fill("connection_set-0-identity", phone)
        self.browser.find_by_name('_save').click()

    def create_poll(self, poll_name, question, group_name):
        self.open('/mypolls/')
        self.browser.click_link_by_partial_href('/createpoll/')
        self.browser.fill("name", "%s" % poll_name)
        self.browser.fill("question_en", question)
        self.select_by_text('groups', group_name)
        self.browser.click_link_by_partial_href('javascript:void(0);')


    def test_admin_can_create_poll(self):
        group_name = 'group1'
        backend_name = 'dmark'
        user = self.create_and_sign_in_admin("pass", "jamo")
        self.create_backend(backend_name)
        self.create_group(group_name)
        self.create_contact("jamo", "999", user.username, group_name, backend_name)
        poll_name = "our poll"
        question = "question 12"
        self.create_poll(poll_name, question, group_name)
        self.open('/polls/')
        assert self.browser.is_text_present(question)
        # self.browser.click_link_by_partial_text('Edit')
        # assert self.browser.is_text_present(poll_name)
        # self.browser.click_link_by_partial_text('Start Poll')

