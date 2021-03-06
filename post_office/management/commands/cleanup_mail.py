import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from ...models import Email


class Command(BaseCommand):
    help = 'Place deferred messages back in the queue.'
    option_list = BaseCommand.option_list + (
        make_option('-d', '--days', type='int', default=90,
            help="Cleanup mails older than this many days, defaults to 90."),
    )

    def handle(self, verbosity, days, **options):
        # Delete mails and their related logs and queued created before X days

        today = datetime.date.today()
        cutoff_date = today - datetime.timedelta(days)
        count = Email.objects.filter(created__lt=cutoff_date).count()
        Email.objects.filter(created__lt=cutoff_date).delete()
        print "Deleted {0} mails created before {1} ".format(count, cutoff_date)