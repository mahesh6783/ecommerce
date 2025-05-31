# 🛍️ Django eCommerce Web App

A full-featured eCommerce web application built using Django. This project includes user registration, login, cart, product ordering, OTP-based order confirmation, admin panel, and order tracking.

## 🌟 Features

- User Registration and Login
- Admin Login and Product Management
- Product Listing with Categories and Ratings
- Add to Cart and Cart Management
- Place Orders with Dynamic Address Input
- 4-digit OTP generation for each order
- Session-based OTP storage for order verification
- Order Status Tracking: Processed → Shipped → En Route → Arrived
- Admin: View Orders, Deliver and Update Delivery Date
- Order History with Past Ordered Products

## 🖼️ Screenshots

> *(Add your own screenshots here if available)*

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (default), can be configured for PostgreSQL/MySQL
- **Session**: Django Session Framework
- **Media Uploads**: Django ImageField

## 🧾 Models

- `User`: Stores user info (name, phone, address, gender, email, password)
- `Product`: Product details (name, price, rating, image, category)
- `Cart`: User’s cart items
- `Order`: Order details (user, delivery address, total amount, status)
- `P_order`: Individual product details within an order
- `Admin`: Admin login info

## 📦 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ecommerce-django.git
cd ecommerce-django
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the app
- Frontend: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

## 📂 Project Structure

```
ecommerce/
├── templates/
│   └── order.html, login.html, etc.
├── static/
│   └── css, js, images
├── media/
│   └── product_images/
├── models.py
├── views.py
├── urls.py
└── manage.py
```

## 🔐 Session-based OTP Handling

- OTP is generated during order creation:
```python
otp = random.randint(1000, 9999)
request.session[f'otp_{order_obj.id}'] = otp
```
- It is later accessed securely from the session to verify order delivery.

## 🧼 Logout Function

Handled safely using key checking:
```python
def log_out(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    elif 'admin_id' in request.session:
        del request.session['admin_id']
    return redirect('../login')
```

## 🧾 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

📧 **Contact:** your.email@example.com  
🌐 **Portfolio:** [maheshh.vercel.app](https://maheshh.vercel.app)