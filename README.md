E-commerce APP steps to run the project

GitHub Link:-
https://github.com/thomasbibi/Django_e-commerce

1. **Clone the repository:**
   
   git clone https://github.com/yourusername/django-ecommerce.git
   cd django-ecommerce

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies:
pip install -r requirements.txt

4.Set up PostgreSQL database:
Create a database named ecommerce_db.
Update settings.py with your database credentials:

5.Apply migrations
python manage.py makemigrations
python manage.py migrate

6.python manage.py createsuperuser

7. STRIPE_SECRET_KEY = 'your-secret-key'
STRIPE_PUBLISHABLE_KEY = 'your-publishable-key'


8. python manage.py runserver

9.Access the site:
Visit http://127.0.0.1:8000/ for the homepage.
Admin panel: http://127.0.0.1:8000/admin/.
