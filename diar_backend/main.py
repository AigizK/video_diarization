from fastapi import FastAPI, Body, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import uuid
import shutil
import zipfile
from typing import List

app = FastAPI()

# Убедитесь, что папки results и static/video существуют
os.makedirs("results", exist_ok=True)
os.makedirs("speakers", exist_ok=True)
os.makedirs("static/video", exist_ok=True)

# Монтируем статическую папку
app.mount("/static", StaticFiles(directory="static"), name="static")

# Глобальные переменные для хранения данных в памяти
task_list = set()
results_files = set()


def load_video_data():
    global task_list
    video_dir = "video"
    task_list = {file for file in os.listdir(video_dir) if
                 file.endswith('.json')}


def load_results_files():
    global results_files
    results_dir = "results"
    results_files = set(os.listdir(results_dir))


@app.on_event("startup")
async def startup_event():
    load_video_data()
    load_results_files()


@app.get("/api/task")
async def get_task():
    load_video_data()
    load_results_files()
    
    available_tasks = task_list - results_files
    if not available_tasks:
        raise HTTPException(status_code=404, detail="Нет доступных задач")

    task_filename = available_tasks.pop()
    with open(os.path.join("video", task_filename), 'rb') as file:
        content = file.read()
        task_data = json.loads(content.decode('utf-8-sig'))
        task_data["file_id"] = task_filename

    channel_id = task_data["channel_id"]
    if os.path.exists(f"speakers/{channel_id}.json"):
        with open(f"speakers/{channel_id}.json", 'rb') as file:
            content = file.read()
            task_data["speakers"] = json.loads(content.decode('utf-8-sig'))
    else:
        task_data["speakers"] = [
            {"id": 'Speaker_1', "name": 'Спикер 1', "color": '#FF5733'},
            {"id": 'Speaker_2', "name": 'Спикер 2', "color": '#33C1FF'}
        ]

    return JSONResponse(content=task_data)


@app.post("/api/result")
async def post_result(data: dict = Body(...)):
    file_id = data.get('file_id')
    if not file_id:
        raise HTTPException(status_code=400,
                            detail="file_id отсутствует в данных")

    filename = f"results/{file_id}"
    with open(filename, "w") as file:
        json.dump(data, file)

    channel_id = data.get('channel_id')
    speakers = data.get("speakers")

    with open(f"speakers/{channel_id}.json", "w") as file:
        json.dump(speakers, file)

    results_files.add(file_id)

    return JSONResponse(
        content={"message": "Данные успешно сохранены", "filename": filename})


@app.get("/api/video/{filename}")
async def get_video(filename: str):
    video_path = f"video/{filename}"
    if os.path.isfile(video_path):
        return FileResponse(video_path)
    raise HTTPException(status_code=404, detail="Видео не найдено")


def clean_directory(directory: str) -> None:
    """Remove all files from specified directory"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


@app.post("/api/upload_tasks")
async def upload_tasks(file: UploadFile = File(...)):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Только ZIP файлы разрешены")
    
    # Create temporary file to store the upload
    temp_file = f"temp_{uuid.uuid4()}.zip"
    try:
        # Save uploaded file
        with open(temp_file, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Clean video directory
        clean_directory("video")
        
        # Extract zip to video directory
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall("video")
        
        # Reload video data
        load_video_data()
        
        return JSONResponse(content={
            "message": "Задачи успешно загружены",
            "tasks_count": len(task_list)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.unlink(temp_file)


@app.get("/api/downloads")
async def download_results():
    # Create a temporary zip file
    temp_zip = f"temp_{uuid.uuid4()}.zip"
    try:
        # Create zip archive containing all files from results directory
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("results"):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, "results")
                    zipf.write(file_path, arcname)
        
        # Return the zip file as a streaming response
        background_tasks = BackgroundTasks()
        background_tasks.add_task(os.unlink, temp_zip)
        return FileResponse(
            temp_zip,
            media_type="application/zip",
            filename="results.zip",
            background=background_tasks
        )
    except Exception as e:
        # Clean up temp file if something goes wrong
        if os.path.exists(temp_zip):
            os.unlink(temp_zip)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
