# Butcher Shop Management System

A modular, Django‑ and DRF‑based platform for managing multi‑tenant butcher shops in Rwanda. Provides core functionality for shop owners, suppliers, veterinarians, and end‑customers—including inventory, orders, dynamic JSON‑driven documents, email templates, and more—all secured with JWT authentication.

---

## 🚀 Features

- **Multi‑Role Authentication**  
  - `shop` (butcher owner/staff)  
  - `supplier` (external suppliers)  
  - `vet` (veterinarians)  
  - `client` (end customers)

- **Shop Management**  
  - Register shop profiles with name, contact, address  
  - Owner/staff can manage suppliers, inventory, orders, and document templates

- **Supplier Lifecycle**  
  - Invite suppliers by email (with tokenized links)  
  - Suppliers respond, submit quotations, record deliveries  
  - Shop staff approve/reject quotations and deliveries

- **Inventory Module**  
  - Categories, items (SKUs), stock entries (incoming) and exits (sales)  
  - Link stock entries to suppliers

- **Customer Orders**  
  - Clients browse shops & items  
  - Place orders with line items; shops confirm, ship, deliver, or cancel

- **Dynamic Documents**  
  - Define JSON‑schema document templates (e.g. delivery notes, checklists)  
  - Fill out form instances via API, store as JSON  
  - Render JSON into printable PDFs with WeasyPrint

- **Email Template Engine**  
  - Per‑shop, editable subject/body templates stored in database  
  - Fallback to file‑based defaults  
  - Render with context and send via SMTP (Gmail)

- **Veterinarian Approvals**  
  - Pre‑ and post‑slaughter inspections on cows  
  - Slaughter approval records per animal  
  - Vets have cross‑shop access; shop staff see status

---

## 📦 Tech Stack

- **Backend**  
  - Python 3.10+  
  - Django 4.x  
  - Django REST Framework  
  - djangorestframework-simplejwt (JWT auth)  
  - WeasyPrint (PDF generation)

- **Database**  
  - PostgreSQL

- **Email**  
  - SMTP via Gmail (App Password)

- **Deployment**  
  - Docker & docker‑compose (optional)  
  - GitHub Actions (CI/CD)

---

## 🏗 Architecture

- Client (Web/Mobile)
- ↕ JSON over HTTPS
- Django API (DRF + JWT + Email Templates)
- ↕ Psycopg2
- PostgreSQL


Apps:
- `users`  – custom `User` + `ShopProfile`/`VetProfile`/`Customer`/`SupplierProfile`  
- `clients` – shop directory & customer profiles  
- `inventory` – categories, items, stock entries/exits  
- `suppliers` – supplier profiles, invitations, quotations, deliveries  
- `orders`  – customer orders & line items  
- `docs`   – dynamic JSON document templates & instances  
- `vets`   – veterinarian inspections & slaughter approvals  
- `email_config` – editable email templates per shop  

---

## 🔧 Installation & Setup

1. **Clone & create virtualenv**
   ```bash
   git clone <repo_url>
   cd butcher_mgmt
   python3 -m venv venv
   source venv/bin/activate
```bash
pip install -r requirements.txt
```
```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=butcher_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

EMAIL_HOST_USER=you@gmail.com
EMAIL_HOST_PASSWORD=app-password

python manage.py collectstatic

python manage.py runserver
```

## ⚙ Configuration
- settings.py is configured for JWT auth, PostgreSQL, Gmail SMTP, and Africa/Kigali timezone.
- 
- ## Templates:
- 
- App‑level: APP_DIRS = True
- 
- Project level: templates/ folder in project root

## 📁 Directory Structure
butcher_mgmt/
├─ butcher_mgmt/        # Django project settings & URLs
├─ users/               
├─ clients/             
├─ inventory/           
├─ suppliers/           
├─ orders/              
├─ docs/                
├─ vets/                
├─ email_config/        
├─ templates/           # project-level templates
├─ manage.py
└─ requirements.txt
