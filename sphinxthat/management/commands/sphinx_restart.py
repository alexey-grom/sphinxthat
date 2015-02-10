# encoding: utf-8

from django.core.management.base import BaseCommand

from sphinxthat import control


class Command(BaseCommand):
    def handle(self, debug=None, *args, **options):
        control.restart()
