# Aditya Rao | Personal portfolio
A local, server-rendered FastAPI portfolio with Jinja2 inheritance, technology filters and a contact form.

## Run locally
Install Python 3.10 or newer. Open a terminal in portfolio_app and run:

    python -m venv .venv

Activate the environment on Windows PowerShell with `.\.venv\Scripts\Activate.ps1`.
On macOS or Linux use `source .venv/bin/activate`. Then run:

    python -m pip install -r requirements.txt
    python -m uvicorn main:app --reload

Open http://127.0.0.1:8000/ in a browser. Press Ctrl+C to stop the server.

## Lab walkthrough
1. Open the home page in a fresh browser profile. Check the default light theme and use the navigation links.
2. Select Dark mode. In DevTools > Network, enable Preserve log. The POST to /set-theme returns 303 and redirects to /. Inspect Set-Cookie for Max-Age=2592000, HttpOnly and SameSite=Lax.
3. Open DevTools > Application > Storage > Cookies, select the local origin and refresh. The theme row should still show dark. Close and reopen the browser using the same normal profile and origin to confirm persistence. Toggle back to light.
4. In Projects, filter by Python. To check the empty state, visit /?tech=Rust#projects.
5. Use Contact to save a test message. Entries are stored in the messages table in ~/.fastapi-portfolio/contact.sqlite3 on the computer running the server. The form does not send email.

## Personalize and submit
Replace static/images/profile.jpg with your own professional headshot. The supplied sample is Grace Hopper’s U.S. Navy portrait distributed with Matplotlib. Update the image description and caption in templates/index.html. If you change the project, update the source document and screenshots to match. Publish the portfolio_app contents to your own public GitHub repository. Publish the LinkedIn draft with your screenshots. Paste both direct URLs into the links document and the LMS, then upload the ZIP.
