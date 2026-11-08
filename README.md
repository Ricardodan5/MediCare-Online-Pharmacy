# MediCare Online Pharmacy

An academic Django web application developed as a learning project. The
prototype demonstrates customer account management and a
prescription-submission workflow in which uploaded prescriptions are
reviewed by authorised staff.

> **Academic prototype only:** This project is not ready for real
> patient information or live pharmacy operations. Real-world deployment
> requires a formal security review, privacy and data-protection
> controls, professional pharmacy oversight, regulatory compliance,
> secure hosting, backups, and operational procedures.

## Project objectives

-   Allow customers to create accounts and sign in.
-   Allow customers to maintain delivery information.
-   Allow customers to submit prescription files for review.
-   Allow customers to see the status of submitted prescriptions.
-   Allow authorised staff to review prescriptions, update statuses, and
    add pharmacist notes.

## Main features

### Customer accounts

-   Customer registration and login.
-   Customer profile with phone number, delivery address, and city.
-   Profile updates by the logged-in customer.
-   Logout functionality.

### Prescription workflow

1.  A customer signs in and opens the prescription page.
2.  The customer uploads a prescription and may provide a description.
3.  The prescription is saved with a `Pending` status.
4.  An authorised staff member reviews it in Django Admin.
5.  Staff can change the status to `Approved` or `Rejected` and add a
    pharmacist note.
6.  The customer can view the status and note on the prescription page.

### Access controls currently implemented

-   Prescription listings are filtered to the logged-in customer.
-   The protected download view requires authentication.
-   Customers can download only their own prescriptions.
-   Staff users (`is_staff`) can access prescriptions for review.
-   Unauthorised access to another customer's prescription returns a 404
    response.
-   Logged-out visitors are redirected to the login page.
-   Uploaded media is not served through Django's development `static()`
    media route; downloads use the protected view.

These are initial academic controls, not a complete security
certification. Staff access currently relies on Django's `is_staff` flag
and should be refined into dedicated pharmacist permissions before
production use.

## Technology stack

-   Python
-   Django 6.1.2
-   HTML and CSS
-   SQLite (default local development database)
-   Django built-in authentication and administration

## Main project structure

``` text
ProjectPharmacy/
├── medicare/
│   ├── settings.py
│   └── urls.py
├── customers/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── customers/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       └── prescriptions.html
├── static/
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
└── README.md
```

Your local folder names may have different capitalisation depending on
the current project state and Windows filesystem.

## Requirements

-   Python
-   Git
-   Windows Command Prompt or another terminal
-   A copy of this repository

## Installation and setup

### 1. Clone the repository

``` bash
git clone https://github.com/Ricardodan5/MediCare-Online-Pharmacy.git
cd MediCare-Online-Pharmacy
```

### 2. Create and activate a virtual environment

On Windows Command Prompt:

``` cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

``` cmd
pip install -r requirements.txt
```

### 4. Apply database migrations

``` cmd
python manage.py migrate
```

### 5. Create an administrator account

``` cmd
python manage.py createsuperuser
```

Follow the prompts to create the account.

### 6. Run the development server

``` cmd
python manage.py runserver
```

Open:

-   Website: http://127.0.0.1:8000/
-   Django Admin: http://127.0.0.1:8000/admin/

## Basic testing checklist

-   Register a customer account.
-   Sign in and update the customer profile.
-   Upload a sample prescription file.
-   Confirm it appears in the customer's prescription list.
-   Sign in as an authorised staff user and review the prescription in
    Django Admin.
-   Update the status and add a review note.
-   Confirm the customer sees the updated status and note.
-   Confirm the customer can download their own prescription.
-   Confirm a different customer receives a 404 when trying to access
    that protected download URL.
-   Confirm a logged-out visitor is redirected to the login page.

Use dummy documents for academic testing. Do not use real patient
records.

## Security and deployment notes

Before production use, the project needs further work, including:

-   Keep `SECRET_KEY` and other credentials out of source control.
-   Set `DEBUG = False` and configure `ALLOWED_HOSTS`.
-   Use HTTPS and secure session and CSRF cookie settings.
-   Use private, access-controlled file storage and appropriate backup
    and retention practices.
-   Add robust file validation, file-size limits, and malware scanning.
-   Replace broad `is_staff` access with dedicated pharmacist roles and
    least-privilege permissions.
-   Add audit logging for prescription access and review decisions.
-   Review privacy, consent, data-protection, pharmacy, and other
    applicable legal requirements.
-   Configure a production database, hosting, monitoring, and recovery
    procedures.
-   Conduct security testing before handling real customer or patient
    information.

## Team collaboration

1.  Pull the latest changes before starting work.
2.  Create a separate branch for substantial features or fixes.
3.  Test changes locally.
4.  Use clear, descriptive commit messages.
5.  Push the branch and open a pull request for review before merging
    into `main`.

## Project status

The current version demonstrates registration, login, profile
management, prescription upload, staff review through Django Admin, and
protected prescription downloads. Development is ongoing.
