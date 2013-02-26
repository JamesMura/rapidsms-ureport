from selenium.webdriver.chrome.webdriver import WebDriver
from splinter import Browser
from ureport.tests.integration.splinter_wrapper import SplinterTestCase
from ureport.tests.factories import PollFactory


def home_page(driver):
    driver.open("/")
    assert driver.browser.is_text_present('0')
    assert driver.browser.is_text_present('HOME')
    assert driver.browser.is_text_present('POLL RESULTS')
    assert driver.browser.is_text_present('ABOUT UREPORT')
    assert driver.browser.is_text_present('HOW TO JOIN')
    assert driver.browser.is_text_present('PREVIOUS POLLS')


def home_page_visualisation( driver):
    PollFactory.create()
    PollFactory.create()
    PollFactory.create()
    driver.open('/')
    assert driver.browser.is_text_present('CURRENT POLL')
    assert driver.browser.is_element_present_by_css('span.poll-question')
    assert driver.browser.is_element_present_by_css('div.highcharts-container')


def home_page_map(driver):
    driver.open('/')
    assert driver.browser.is_element_present_by_css('div#OpenLayers.Map_2_events')
    assert driver.browser.is_element_present_by_css('div#OpenLayers.Map_2_OpenLayers_ViewPort')















