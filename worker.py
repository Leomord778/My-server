from fastapi import FastAPI, UploadFile, File
import subprocess, shutil, uuid, os

app = FastAPI()

@app.get("/")
@app.get("/status")
def status():
    return {"status": "idle", "ffmpeg": "ready"}

@app.post("/render")
async def render_test(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())
    in_file = f"/tmp/in_{uid}.mp4"
    out_file = f"/tmp/out_{uid}.mp4"
    with open(in_file, "wb") as f:
        shutil.copyfileobj(file.file, f)
    subprocess.run(
        ["ffmpeg", "-y", "-i", in_file, "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", out_file],
        check=True
    )
    os.remove(in_file)
    return {"status": "done", "output": out_file}
