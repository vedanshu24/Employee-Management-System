# Employee Management System

A comprehensive Django-based Employee Management System with RESTful APIs, authentication, filtering, pagination, and interactive visualizations.

## 🚀 Features

### Core Functionality
- **Employee Management**: Complete CRUD operations for employees with user authentication
- **Department Management**: Organize employees by departments
- **Attendance Tracking**: Record and track employee attendance with multiple status options
- **Performance Reviews**: Manage employee performance ratings and reviews
- **RESTful APIs**: Full API coverage with Django REST Framework
- **Authentication**: Token-based authentication system
- **Filtering & Search**: Advanced filtering and search capabilities
- **Pagination**: Efficient data pagination for large datasets

### API Documentation
- **Swagger UI**: Interactive API documentation at `/swagger/`
- **ReDoc**: Alternative API documentation at `/redoc/`

### Visualizations
- **Interactive Dashboard**: Real-time charts and analytics
- **Department Distribution**: Pie chart showing employee distribution
- **Attendance Overview**: Monthly attendance statistics
- **Performance Analytics**: Rating distribution and trends
- **Statistics Cards**: Key metrics and KPIs

### Additional Features
- **Docker Support**: Containerized deployment with Docker Compose
- **Database Seeding**: Management command to populate with fake data
- **Admin Interface**: Django admin for easy data management
- **Responsive Design**: Mobile-friendly dashboard interface

## 🛠 Tech Stack

- **Backend**: Django 4.2.24, Django REST Framework
- **Database**: PostgreSQL (with SQLite fallback)
- **Authentication**: DRF Token Authentication
- **Documentation**: drf-yasg (Swagger UI)
- **Visualization**: Chart.js
- **Data Generation**: Faker
- **Filtering**: django-filter
- **Containerization**: Docker, Docker Compose

## 📦 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL (optional, SQLite works for development)
- Docker (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed Database (Optional)**
   ```bash
   python manage.py seed_data --employees 50 --departments 8
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### Docker Setup

1. **Using Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - API Documentation: http://localhost:8000/swagger/
   - Dashboard: http://localhost:8000/charts/
   - Admin Panel: http://localhost:8000/admin/

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout

### Employees
- `GET /api/v1/employees/` - List employees
- `POST /api/v1/employees/` - Create employee
- `GET /api/v1/employees/{id}/` - Get employee details
- `PUT /api/v1/employees/{id}/` - Update employee
- `DELETE /api/v1/employees/{id}/` - Delete employee
- `GET /api/v1/employees/statistics/` - Employee statistics
- `GET /api/v1/employees/{id}/attendance_summary/` - Employee attendance summary
- `GET /api/v1/employees/{id}/performance_summary/` - Employee performance summary

### Departments
- `GET /api/v1/departments/` - List departments
- `POST /api/v1/departments/` - Create department
- `GET /api/v1/departments/{id}/` - Get department details
- `PUT /api/v1/departments/{id}/` - Update department
- `DELETE /api/v1/departments/{id}/` - Delete department
- `GET /api/v1/departments/{id}/employees/` - Department employees

### Attendance
- `GET /api/v1/attendance/` - List attendance records
- `POST /api/v1/attendance/` - Create attendance record
- `GET /api/v1/attendance/{id}/` - Get attendance details
- `PUT /api/v1/attendance/{id}/` - Update attendance record
- `DELETE /api/v1/attendance/{id}/` - Delete attendance record
- `GET /api/v1/attendance/statistics/` - Attendance statistics
- `GET /api/v1/attendance/monthly_summary/` - Monthly attendance summary
- `GET /api/v1/attendance/employee_attendance/` - Employee-specific attendance

### Performance
- `GET /api/v1/performance/` - List performance reviews
- `POST /api/v1/performance/` - Create performance review
- `GET /api/v1/performance/{id}/` - Get performance details
- `PUT /api/v1/performance/{id}/` - Update performance review
- `DELETE /api/v1/performance/{id}/` - Delete performance review
- `GET /api/v1/performance/statistics/` - Performance statistics
- `GET /api/v1/performance/rating_summary/` - Rating distribution
- `GET /api/v1/performance/department_performance/` - Department performance

## 🔍 Filtering & Search

### Employee Filters
- `department` - Filter by department
- `is_active` - Filter by active status
- `position` - Filter by position (contains)
- `date_of_joining_after` - Filter by joining date (from)
- `date_of_joining_before` - Filter by joining date (to)
- `salary_min` - Minimum salary
- `salary_max` - Maximum salary

### Attendance Filters
- `employee` - Filter by employee ID
- `department` - Filter by department name
- `status` - Filter by attendance status
- `date_after` - Filter by date (from)
- `date_before` - Filter by date (to)
- `year` - Filter by year
- `month` - Filter by month

### Performance Filters
- `employee` - Filter by employee ID
- `department` - Filter by department name
- `rating` - Filter by rating
- `rating_min` - Minimum rating
- `rating_max` - Maximum rating
- `review_date_after` - Filter by review date (from)
- `review_date_before` - Filter by review date (to)
- `reviewed_by` - Filter by reviewer

## 📊 Dashboard Features

### Statistics Cards
- Total Employees
- Number of Departments
- Attendance Records Count
- Attendance Rate Percentage
- Performance Reviews Count
- Average Performance Rating

### Interactive Charts
1. **Employees by Department** (Pie Chart)
   - Visual distribution of employees across departments

2. **Monthly Attendance Overview** (Bar Chart)
   - Current month's attendance status breakdown

3. **Performance Rating Distribution** (Doughnut Chart)
   - Distribution of performance ratings (1-5)

4. **Attendance Status Distribution** (Polar Area Chart)
   - Overall attendance status breakdown

## 🔧 Management Commands

### Seed Data Command
```bash
python manage.py seed_data --employees 50 --departments 8
```

**Options:**
- `--employees`: Number of employees to create (default: 50)
- `--departments`: Number of departments to create (default: 8)

**Features:**
- Creates realistic fake data using Faker
- Generates 6 months of attendance records
- Creates 1-3 performance reviews per employee
- Skips weekends for attendance generation
- Realistic salary ranges and job positions

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Manual Docker Build
```bash
# Build image
docker build -t employee-management .

# Run container
docker run -p 8000:8000 employee-management
```

## 🔐 Authentication

### Token Authentication
1. **Get Token**: `POST /api/v1/auth/login/`
2. **Use Token**: Include `Authorization: Token <your-token>` in headers
3. **Admin Access**: Use Django admin at `/admin/`

### Default Credentials
- **Username**: admin
- **Password**: admin123

## 📁 Project Structure

```
employee_project/
├── employees/               # Employee management app
│   ├── models.py           # Employee and Department models
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views and dashboard
│   ├── urls.py             # URL routing
│   ├── filters.py          # Filtering logic
│   ├── admin.py            # Admin configuration
│   └── management/commands/seed_data.py
├── attendance/              # Attendance tracking app
│   ├── models.py           # Attendance model
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   ├── filters.py          # Filtering logic
│   └── admin.py            # Admin configuration
├── performance/             # Performance management app
│   ├── models.py           # Performance model
│   ├── serializers.py      # API serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   ├── filters.py          # Filtering logic
│   └── admin.py            # Admin configuration
├── employee_project/        # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── templates/               # HTML templates
│   └── charts.html         # Dashboard template
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🧪 Testing

### API Testing
Use the Swagger UI at `/swagger/` to test all API endpoints interactively.

### Sample API Calls

**Get all employees:**
```bash
curl -H "Authorization: Token <your-token>" http://localhost:8000/api/v1/employees/
```

**Create new employee:**
```bash
curl -X POST -H "Authorization: Token <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"username": "john.doe", "password": "password123", "first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "+1234567890", "address": "123 Main St", "date_of_joining": "2023-01-01", "department": 1, "position": "Software Engineer", "salary": 75000}' \
     http://localhost:8000/api/v1/employees/
```

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Set proper `SECRET_KEY`, `DEBUG=False`
2. **Database**: Use PostgreSQL in production
3. **Static Files**: Configure static file serving
4. **Security**: Use HTTPS, secure headers
5. **Monitoring**: Add logging and monitoring
6. **Backup**: Implement database backup strategy

### Environment Variables
```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/swagger/`
- Review the Django admin at `/admin/`
- Check the dashboard at `/charts/`

## 🎯 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced reporting features
- [ ] Mobile app integration
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Multi-tenant support
- [ ] API rate limiting
- [ ] Caching implementation

