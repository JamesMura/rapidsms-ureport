from selenium.webdriver.chrome.webdriver import WebDriver
from splinter import Browser
from ureport.tests.functional.splinter_wrapper import SplinterTestCase
from ureport.tests.factories import PollFactory


class HomePageTest(SplinterTestCase):
    def setUp(self):
        self.browser = Browser('chrome')

    def tearDown(self):
        self.browser.quit()


    def test_home_page(self):
        self.open("/")
        assert self.browser.is_text_present('0')
        assert self.browser.is_text_present('HOME')
        assert self.browser.is_text_present('POLL RESULTS')
        assert self.browser.is_text_present('ABOUT UREPORT')
        assert self.browser.is_text_present('HOW TO JOIN')
        assert self.browser.is_text_present('PREVIOUS POLLS')

    def test_visulisation_on_home_page(self):
        PollFactory.create()
        PollFactory.create()
        PollFactory.create()
        self.open('/')
        assert self.browser.is_text_present('CURRENT POLL')
        assert self.browser.is_element_present_by_css('span.poll-question')
        assert self.browser.is_element_present_by_css('div.highcharts-container')

    def test_map_shows_on_home_page(self):
        self.open('/')
        assert self.browser.is_element_present_by_css('div#OpenLayers.Map_2_events')
        assert self.browser.is_element_present_by_css('div#OpenLayers.Map_2_OpenLayers_ViewPort')















