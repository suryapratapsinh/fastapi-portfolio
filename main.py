# main.py

# -----------------------------
# Imports
# -----------------------------
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from supabase import create_client

# -----------------------------
# Initialize app and templates
# -----------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -----------------------------
# Supabase client
# -----------------------------
url = "https://gdckwwozlrhczbvsxrzl.supabase.co"
key = "sb_publishable_WGukgYeoBzb3eUG2keuCrQ_7jp0BZwm"  # Use service_role key for full access in backend
supabase = create_client(url, key)

# -----------------------------
# Home page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -----------------------------
# Contact form submission
# -----------------------------
@app.post("/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):

    # Save data to Supabase
    supabase.table("contacts").insert({
        "name": name,
        "email": email,
        "message": message
    }).execute()

    # Redirect to thank you page
    return RedirectResponse(url="/thank-you", status_code=303)

# -----------------------------
# Thank You page
# -----------------------------
@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})