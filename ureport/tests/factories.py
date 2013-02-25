import datetime
from poll.models import Poll
from ureport.models import UreportContact
import factory


def get_date_from_string(start_date_string):
    return datetime.datetime.strptime(start_date_string, "%d/%m/%Y").date()

class PollFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Poll
    user_id=0
class UreportContactFactory(factory.Factory):
    FACTORY_FOR = UreportContact
    autoreg_join_date = get_date_from_string('13/1/2017')
    quit_date = get_date_from_string('13/1/2017')
    responses = 0
    questions = 0
    age = 19
    incoming = 0
    connection_pk = 0
    reporting_location_id = 0
    user_id = 0