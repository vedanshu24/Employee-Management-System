from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from datetime import datetime, timedelta
import random
from employees.models import Department, Employee
from attendance.models import Attendance
from performance.models import Performance

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--employees', type=int, default=50, help='Number of employees to create')
        parser.add_argument('--departments', type=int, default=8, help='Number of departments to create')

    def handle(self, *args, **options):
        self.stdout.write('Starting to seed database...')
        
        # Create departments
        departments = self.create_departments(options['departments'])
        
        # Create employees
        employees = self.create_employees(options['employees'], departments)
        
        # Create attendance records
        self.create_attendance_records(employees)
        
        # Create performance records
        self.create_performance_records(employees)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded database with {len(departments)} departments, {len(employees)} employees, and related data!')
        )

    def create_departments(self, count):
        departments = []
        department_names = [
            'Human Resources', 'Engineering', 'Marketing', 'Sales', 
            'Finance', 'Operations', 'Customer Support', 'Research & Development'
        ]
        
        for i in range(min(count, len(department_names))):
            dept, created = Department.objects.get_or_create(
                name=department_names[i],
                defaults={
                    'description': fake.text(max_nb_chars=200)
                }
            )
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        return departments

    def create_employees(self, count, departments):
        employees = []
        
        for i in range(count):
            # Create user
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name()
            
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            
            # Create employee
            employee_id = f"EMP{i+1:04d}"
            employee = Employee.objects.create(
                user=user,
                employee_id=employee_id,
                phone=fake.phone_number()[:15],
                address=fake.address(),
                date_of_joining=fake.date_between(start_date='-5y', end_date='today'),
                department=random.choice(departments),
                position=fake.job(),
                salary=random.randint(30000, 150000),
                is_active=True
            )
            employees.append(employee)
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1} employees...')
        
        return employees

    def create_attendance_records(self, employees):
        self.stdout.write('Creating attendance records...')
        
        # Create attendance for the last 6 months
        start_date = datetime.now().date() - timedelta(days=180)
        
        for employee in employees:
            current_date = start_date
            while current_date <= datetime.now().date():
                # Skip weekends
                if current_date.weekday() < 5:
                    status = random.choices(
                        ['present', 'absent', 'late', 'half_day'],
                        weights=[70, 10, 15, 5]
                    )[0]
                    
                    check_in_time = None
                    check_out_time = None
                    
                    if status in ['present', 'late', 'half_day']:
                        check_in_time = fake.time()
                        if status != 'half_day':
                            check_out_time = fake.time()
                    
                    Attendance.objects.create(
                        employee=employee,
                        date=current_date,
                        status=status,
                        check_in_time=check_in_time,
                        check_out_time=check_out_time,
                        notes=fake.text(max_nb_chars=100) if random.random() < 0.1 else None
                    )
                
                current_date += timedelta(days=1)

    def create_performance_records(self, employees):
        self.stdout.write('Creating performance records...')
        
        for employee in employees:
            # Create 1-3 performance reviews per employee
            num_reviews = random.randint(1, 3)
            
            for i in range(num_reviews):
                review_date = fake.date_between(
                    start_date=employee.date_of_joining,
                    end_date='today'
                )
                
                Performance.objects.create(
                    employee=employee,
                    rating=random.randint(1, 5),
                    review_date=review_date,
                    goals_achieved=fake.text(max_nb_chars=300),
                    areas_for_improvement=fake.text(max_nb_chars=300),
                    comments=fake.text(max_nb_chars=200),
                    reviewed_by=fake.name()
                )
