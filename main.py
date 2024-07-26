from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import aiofiles

app = FastAPI()

templates = Jinja2Templates(directory="temlates")

app.mount("/static", StaticFiles(directory="static"), name="static")

tracks = [filename for filename in os.listdir(os.path.join("static", "tracks"))]
print('Tracks Database: ')
print(tracks)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "Index.html", context={"tracks": enumerate(tracks)})

@app.get("/track/add")
def add_track_form(request: Request):
    return templates.TemplateResponse(request, "add.html")

@app.post("/tracks/add")
async def add_track(request: Request, track: UploadFile):
    contents = await track.read()
    fuul_path = os.path.join("static", "tracks", track.filename)
    async with aiofiles.open(track.filename, "wb") as f:
        f.write(contents)

    tracks.append(track.filename)
    return RedirectResponse("/track/" + str(len(tracks)-1), status_code=303)

@app.get("/tracks/{track_id}")
def get_track(request: Request, track_id: int):
    return templates.TemplateResponse(request, "track.html", context={"track": tracks("track_id")})
