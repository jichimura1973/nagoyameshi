# from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "テストコマンド"
    
    # def handle(self, *args: Any, **options: Any) -> str | None:
    def handle(self, *args, **options):
        print('test')