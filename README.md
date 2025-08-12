# Tamil Nadu Tourism - Django Web Application

A full-stack dynamic web application showcasing popular tourist destinations in Tamil Nadu, built with Django.

## 🌟 Features

### Core Features
- **Tourist Places Grid**: Responsive grid layout displaying tourist destinations
- **User Authentication**: Signup, login, and logout functionality
- **Admin Panel**: Complete CRUD operations for managing tourist places
- **Detail Pages**: Individual pages for each tourist destination
- **Image Upload**: Support for tourist place images

### Phase 2 Bonus Features
- **🔍 Search & Filter**: Search by name, district, or description
- **🏷️ Category & District Filters**: Filter places by category or district
- **⭐ Favorites System**: Bookmark favorite places (login required)
- **🎠 Featured Carousel**: Auto-advancing carousel for featured destinations
- **📄 Pagination**: Navigate through multiple pages of results
- **📱 Responsive Design**: Mobile-first approach with media queries

## 🛠️ Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Google Fonts, CSS Variables, Flexbox/Grid
- **Images**: Pillow for image processing

## 📁 Project Structure

```
tourist_places/
├── tamilnadu_tourism/          # Django project settings
├── destinations/               # Main app
│   ├── models.py              # TouristPlace and Favorite models
│   ├── views.py               # Views for home, detail, favorites
│   ├── urls.py                # URL patterns
│   ├── admin.py               # Admin panel configuration
│   └── templates/             # Django templates
│       ├── base.html          # Base template
│       ├── destinations/      # App-specific templates
│       └── registration/      # Auth templates
├── static/                    # Static files
│   └── css/
│       └── style.css          # Main stylesheet
├── media/                     # Uploaded images
├── manage.py                  # Django management script
└── add_sample_data.py         # Sample data script
```

## 🚀 Setup Instructions

### 1. Clone and Setup Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django pillow
```

### 2. Database Setup
```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Add Sample Data
```bash
# Add sample tourist places
python add_sample_data.py
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Home Page**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin
- **Signup**: http://localhost:8000/accounts/signup/
- **Login**: http://localhost:8000/accounts/login/

## 🎨 Design Features

### Responsive Design
- **Mobile**: Single column layout, optimized touch targets
- **Tablet**: Two-column grid, improved navigation
- **Desktop**: Multi-column grid, full feature set

### Modern UI Elements
- **CSS Variables**: Easy theme customization
- **Google Fonts**: Roboto font family
- **Smooth Transitions**: Hover effects and animations
- **Card-based Layout**: Clean, modern card design
- **Color Scheme**: Professional blue-green theme

### Interactive Features
- **Carousel**: Auto-advancing featured destinations
- **Search**: Real-time search functionality
- **Favorites**: Heart icons for bookmarking
- **Pagination**: Easy navigation through results

## 📊 Data Models

### TouristPlace
- `name`: Place name
- `image`: Uploaded image
- `category`: Temple, Beach, Hill Station, etc.
- `district`: District location
- `short_description`: Brief description
- `featured`: Boolean for carousel display
- `created_at`: Timestamp

### Favorite
- `user`: Foreign key to User
- `place`: Foreign key to TouristPlace
- `created_at`: Timestamp

## 🔧 Customization

### Adding New Tourist Places
1. Access admin panel at `/admin`
2. Login with superuser credentials
3. Click "Tourist Places" → "Add Tourist Place"
4. Fill in details and upload image
5. Mark as "Featured" for carousel display

### Styling Customization
Edit `static/css/style.css`:
```css
:root {
  --primary: #2d3e50;    /* Main color */
  --accent: #4ecdc4;     /* Accent color */
  --bg: #f7f9fa;         /* Background */
  --card-bg: #fff;       /* Card background */
  --radius: 16px;        /* Border radius */
}
```

### Adding New Categories
Update `CATEGORY_CHOICES` in `destinations/models.py`:
```python
CATEGORY_CHOICES = [
    ('Temple', 'Temple'),
    ('Beach', 'Beach'),
    ('Hill Station', 'Hill Station'),
    ('Monument', 'Monument'),
    ('Wildlife', 'Wildlife'),
    ('New Category', 'New Category'),  # Add here
]
```

## 🧪 Testing Features

### Search & Filter
- Search by place name, district, or description
- Filter by category (Temple, Beach, Hill Station, etc.)
- Filter by district
- Clear filters to reset

### Favorites System
- Click heart icon to add/remove favorites
- Favorites persist across sessions
- Visual feedback with color changes

### Carousel
- Auto-advances every 5 seconds
- Manual navigation with arrow buttons
- Displays featured destinations

### Pagination
- 9 places per page
- Previous/Next navigation
- Maintains search/filter state

## 📱 Mobile Responsiveness

The application is fully responsive with:
- **Mobile-first CSS**: Base styles for mobile devices
- **Media Queries**: Progressive enhancement for larger screens
- **Touch-friendly**: Optimized button sizes and spacing
- **Flexible Grid**: Adapts to different screen sizes

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF tokens
- **User Authentication**: Secure login/logout system
- **Admin Panel**: Protected admin interface
- **Input Validation**: Form validation and sanitization

## 🚀 Deployment Ready

The application is ready for deployment with:
- **Static Files**: Configured for production
- **Media Files**: Proper upload handling
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Environment Variables**: Easy configuration management

## 📈 Future Enhancements

Potential Phase 3 features:
- **User Reviews**: Rating and review system
- **Advanced Search**: Location-based search
- **Maps Integration**: Google Maps for locations
- **Social Sharing**: Share places on social media
- **Email Notifications**: Updates about new places
- **API Endpoints**: REST API for mobile apps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Django for showcasing the beautiful tourist destinations of Tamil Nadu!** 