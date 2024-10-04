from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import uuid

app = FastAPI()

# Убедитесь, что папки results и static/video существуют
os.makedirs("results", exist_ok=True)
os.makedirs("static/video", exist_ok=True)

# Монтируем статическую папку
app.mount("/static", StaticFiles(directory="static"), name="static")

# Глобальные переменные для хранения данных в памяти
task_list = set()
results_files = set()


def load_video_data():
    global task_list
    video_dir = "video"
    task_list = set(os.listdir(video_dir))


def load_results_files():
    global results_files
    results_dir = "results"
    results_files = set(os.listdir(results_dir))


@app.on_event("startup")
async def startup_event():
    load_video_data()
    load_results_files()


@app.get("/task")
async def get_task():
    available_tasks = task_list - results_files
    if not available_tasks:
        raise HTTPException(status_code=404, detail="Нет доступных задач")

    task_filename = available_tasks.pop()
    with open(os.path.join("video", task_filename), 'rb') as file:
        content = file.read()
        task_data = json.loads(content.decode('utf-8-sig'))

    return JSONResponse(content=task_data)


@app.post("/result")
async def post_result(data: dict = Body(...)):
    file_id = data.get('file_id')
    if not file_id:
        raise HTTPException(status_code=400,
                            detail="file_id отсутствует в данных")

    filename = f"results/{file_id}"
    with open(filename, "w") as file:
        json.dump(data, file)

    results_files.add(file_id)

    return JSONResponse(
        content={"message": "Данные успешно сохранены", "filename": filename})

@app.get("/video/{filename}")
async def get_video(filename: str):
    video_path = f"video/{filename}"
    if os.path.isfile(video_path):
        return FileResponse(video_path)
    raise HTTPException(status_code=404, detail="Видео не найдено")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
