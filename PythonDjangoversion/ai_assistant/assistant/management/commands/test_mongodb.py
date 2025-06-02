from django.core.management.base import BaseCommand
from assistant.mongodb_utils import test_connection

class Command(BaseCommand):
    help = 'Tests the MongoDB connection'

    def handle(self, *args, **kwargs):
        if test_connection():
            self.stdout.write(self.style.SUCCESS('MongoDB connection successful!'))
        else:
            self.stdout.write(self.style.ERROR('MongoDB connection failed!'))