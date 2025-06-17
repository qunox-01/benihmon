# BenihMon

*BenihMon* is a starter template for building web applications using FastAPI on the backend and Tailwind CSS for the frontend. The name "BenihMon" is derived from the Malay word "benih," meaning seedling, as this project is intended to be a starting point for other projects.

It comes with pre-configured features like Google Single Sign-On (SSO), basic page routing, and a clean project structure to help you get started quickly.

## ✨ Features

  * **FastAPI Backend**: A modern, fast (high-performance), web framework for building APIs with Python.
  * **Jinja2 Templating**: For rendering dynamic HTML pages on the server side.
  * **Tailwind CSS**: A utility-first CSS framework for rapid UI development, included via a CDN.
  * **Google SSO Integration**: Pre-configured user authentication using Google OAuth 2.0 with the `Authlib` library.
  * **Session Management**: Handles user sessions using Starlette's `SessionMiddleware`.
  * **Protected Routes**: Includes an example of a protected route that only authenticated users can access (`/account`).
  * **Basic Pages**: Comes with templates for essential pages like Home, About, Contact, Login, Account, and basic legal pages (Privacy, Cookies, Terms).
  * **Configuration Management**: Uses a `.env` file to manage environment variables and secrets.
  * **Dynamic Sitemap**: Generates a `sitemap.xml` file based on the available routes.

## 🛠️ Tech Stack

  * **Backend**: FastAPI, Uvicorn, Starlette
  * **Authentication**: Authlib, google-auth-oauthlib
  * **Templating**: Jinja2
  * **Frontend**: Tailwind CSS
  * **Environment Variables**: python-dotenv

## 🗂️ Project Structure

The project follows a simple and intuitive structure:

```
├── app/
│   ├── static/             # Static assets (CSS, JS, images)
│   ├── templates/          # Jinja2 HTML templates
│   │   ├── partials/       # Header and footer partials
│   │   └── legal/          # Templates for legal pages
│   ├── main.py             # FastAPI app initialization and main configuration
│   ├── routes.py           # Application routes for different pages
│   └── sso.py              # Google SSO authentication logic
├── .gitignore              # Files to be ignored by Git
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

Follow these steps to get the application running on your local machine.

### 1\. Prerequisites

  * Python 3.8+
  * A Google Cloud project with OAuth 2.0 credentials enabled.

### 2\. Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd benihmon
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root directory and add your Google OAuth credentials and a secret key. You can generate a secret key using `openssl rand -hex 32`.

    ```env
    GOOGLE_CLIENT_ID="your-google-client-id"
    GOOGLE_CLIENT_SECRET="your-google-client-secret"
    SECRET_KEY="your-strong-secret-key"
    APP_VERSION="0.1.0"
    ```

5.  **Configure Google OAuth Redirect URIs**: In your Google Cloud Console, make sure to add the following URL to the "Authorized redirect URIs" for your OAuth 2.0 client:

      * `http://127.0.0.1:8000/auth/auth/google`

### 3\. Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will be available at **[http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**.
