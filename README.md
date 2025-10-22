```markdown
Netflix Dashboard (Flask)
=================================

This small Flask app reproduces visualizations from `uts_Netflix_Movies_and_TV_Shows.ipynb` using `netflix_titles.csv` from the repository root.

Files created
- `app.py` - Flask application that loads data and builds Plotly figures.
- `templates/index.html` - simple Bootstrap template that embeds Plotly graphs.
- `requirements.txt` - Python dependencies.

Run locally
1. Create a virtual environment (recommended) and install requirements:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1; pip install -r netflix_flask_app\requirements.txt
```

2. Start the app (from workspace root):

```powershell
python .\netflix_flask_app\app.py
```

3. Open http://127.0.0.1:5000 in your browser.

Deploy to PythonAnywhere (manual steps)
1. Create an account at https://www.pythonanywhere.com/ and log in.
2. Upload the project folder (`netflix_flask_app`) and the `netflix_titles.csv` to your PythonAnywhere Files (via the web UI).
3. Create a virtualenv on PythonAnywhere (use the same Python version as your account supports) and install `-r requirements.txt`.
4. In the Web tab, create a new web app (Flask). Set the WSGI file to point to `app.py` and the Flask app variable `app`.
5. Reload the web app. Visit the provided PythonAnywhere URL to see the dashboard.

Notes
- I cannot upload to your PythonAnywhere account for you because I don't have your credentials. Follow the steps above or paste any error messages here and I will help.
```
