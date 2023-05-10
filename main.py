from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import string
import random
app = FastAPI()
class URL(BaseModel):
    url: str
database = {'l':'https://youtube.com'}
def generate_short_link():
    """Generate a random string of 6 characters for the short link"""
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
@app.post("/shorten")
def shorten_url(url: URL):
    short_link = generate_short_link()
    database[short_link] = url.url
    return {"short_link": short_link}
@app.get("/{short_link}")
def redirect(short_link: str, response: Response):
    if short_link not in database:
        raise HTTPException(status_code=404, detail="Link not found")
    response.headers["Location"] = database[short_link]
    response.status_code = 302
    return response