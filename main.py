# Import FastAPI framework
from fastapi import FastAPI, Request, Form

# Used for rendering HTML templates
from fastapi.templating import Jinja2Templates

# Used for serving CSS files
from fastapi.staticfiles import StaticFiles

# Create FastAPI app
app = FastAPI()

# Folder where HTML templates are stored
templates = Jinja2Templates(directory="templates")

# Mount static folder for CSS
app.mount("/static", StaticFiles(directory="static"), name="static")



from supabase import create_client

url = "https://gdckwwozlrhczbvsxrzl.supabase.co"
key = "sb_publishable_WGukgYeoBzb3eUG2keuCrQ_7jp0BZwm"

supabase = create_client(url, key)


# =============================
# Home page route
# =============================
@app.get("/")
def home(request: Request):

    # Render index.html page
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# =============================
# Contact form submission
# =============================
@app.post("/contact")
def receive_contact(
        name: str = Form(...),
        email: str = Form(...),
        message: str = Form(...)
):

    # Save data into file
    with open("messages.txt", "a") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Message: {message}\n")
        file.write("--------------\n")

    return {"message": "Form submitted successfully"}






@app.post("/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):

    data = {
        "name": name,
        "email": email,
        "message": message
    }

    supabase.table("contacts").insert(data).execute()

    return {"message": "Form submitted successfully"}