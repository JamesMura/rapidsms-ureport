from django.test import LiveServerTestCase


class SeleniumWrapper(LiveServerTestCase):
    def open(self, url):
        self.wd.get("%s%s", self.live_server_url, url)


from selenium.webdriver.firefox import webdriver as web_driver_module
from django.test import LiveServerTestCase


class SeleniumWrapper(LiveServerTestCase):
    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))


class CustomWebDriver(web_driver_module.WebDriver):
    def find_element_in_page(self, id):
        return self.find_element_by_id(id)


class PollsPage(SeleniumWrapper):
    def setUp(self):
        self.wd = CustomWebDriver()

    def tearDown(self):
        self.wd.quit()

    def test_login(self):
        self.open("/")
        self.wd.find_element_by_class_name("poll_list")


from ureport.spreadsheet_utils import XlsParsingException
from django.core.management import BaseCommand
from poll.models import Poll, Genre, Topic
from ureport.spreadsheet_utils import XlsParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
                Command to add Genre/Topic to existing polls by spreadsheet
                Expected to have headers --> ['Genre', 'Topic','ID']
        """
        if len(args) < 1:
            print "Please specify file with genres and topics"
            return
        print handle_excel_file(open(args[0]))


def handle_excel_file(file):
    try:
        parsed_values = XlsParser().parse(file.read())
        for values in parsed_values:
            genre = values.get('genre')
            topic = values.get('topic')
            poll_id = int(values.get('id')[:-2])
            try:
                poll = Poll.objects.get(id=poll_id)
                try:
                    poll_genre = Genre.objects.get(name=genre)
                except Genre.DoesNotExist as ex:
                    poll_genre = Genre.objects.create(name=genre)
                poll.genre = poll_genre
                try:
                    poll_topic = Topic.objects.get(name=topic)
                except Topic.DoesNotExist as ex:
                    poll_topic = Topic.objects.create(name=topic)
                poll.topic = poll_topic
                poll.save()
            except Poll.DoesNotExist as ex:
                print "Poll with ID : %s could not be found", poll_id
    except XlsParsingException:
        return "Invalid file"

    return "Successfully added Genres/Topics to Polls"