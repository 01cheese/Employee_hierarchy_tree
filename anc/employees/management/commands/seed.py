import random
import logging
from django.core.management.base import BaseCommand
from employees.models import Employee
from faker import Faker

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Seed the database with employees'

    def handle(self, *args, **kwargs):
        logger.info("Starting the seeding process.")
        fake = Faker()
        managers = [None]
        try:
            for i in range(50000):
                manager = random.choice(managers)
                employee = Employee.objects.create(
                    full_name=fake.name(),
                    position=fake.job(),
                    date_of_hire=fake.date_this_decade(),
                    email=fake.email(),
                    manager=manager
                )
                managers.append(employee)
                if i % 1000 == 0:  # Логування кожні 1000 записів
                    logger.info(f"{i} employees created.")
            logger.info("Seeding process completed.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
