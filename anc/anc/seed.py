import random
from faker import Faker

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anc.settings')
django.setup()

from employees.models import Employee

faker = Faker()


def run():
    # Create top level managers
    top_managers = [Employee.objects.create(
        full_name=faker.name(),
        position='Top Manager',
        hire_date=faker.date_this_century(),
        email=faker.email(),
        manager=None
    ) for _ in range(10)]

    # Create a function to recursively add subordinates
    def add_subordinates(manager, level):
        if level > 7:
            return
        num_subordinates = random.randint(5, 10)
        for _ in range(num_subordinates):
            employee = Employee.objects.create(
                full_name=faker.name(),
                position=f'Level {level} Employee',
                hire_date=faker.date_this_century(),
                email=faker.email(),
                manager=manager
            )
            add_subordinates(employee, level + 1)

    for manager in top_managers:
        add_subordinates(manager, 1)


if __name__ == "__main__":
    run()
