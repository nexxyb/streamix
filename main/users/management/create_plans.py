from django.core.management.base import BaseCommand
from apps.repo.models import Plan

class Command(BaseCommand):
    help = 'Create payment plans'

    def handle(self, *args, **options):
        try:
            plans= Plan.objects.get(name='Starter')
        except Plan.DoesNotExist:
            Plan.objects.create(name='Starter',amount=7500, tokens=50000,seconds=3600)
            Plan.objects.create(name='Regular',amount=15000, tokens=150000,seconds=7200)
            Plan.objects.create(name='Premium',amount=30000, tokens=1150000,seconds=73600)
