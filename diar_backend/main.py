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


@app.get("/task")
async def get_task():
    test_data = {"video": "/video/video.mov", "text": [
        {
            "sentence_id": "1",
            "words":
                [
                    {
                        "word": "Привет",
                        "start": 0.5,
                        "end": 1.0
                    },
                    {
                        "word": "мир",
                        "start": 1.0,
                        "end": 1.5
                    },
                    {
                        "word": "как",
                        "start": 2.0,
                        "end": 2.5
                    },
                    {
                        "word": "твои",
                        "start": 4.0,
                        "end": 5.5
                    },
                    {
                        "word": "дела",
                        "start": 7.0,
                        "end": 7.5
                    },
                    {
                        "word": "то",
                        "start": 8.0,
                        "end": 8.5
                    }
                ]
        },
        {
            "sentence_id": "2",
            "words":
                [
                    {
                        "word": "Это",
                        "start": 12.0,
                        "end": 12.5
                    },
                    {
                        "word": "тест",
                        "start": 12.5,
                        "end": 13.0
                    },
                    {
                        "word": "для",
                        "start": 14.5,
                        "end": 16.0
                    },
                    {
                        "word": "нас",
                        "start": 17.5,
                        "end": 23.0
                    }
                ]
        }
    ]
                 }
    return JSONResponse(content=test_data)


@app.post("/result")
async def post_result(data: dict = Body(...)):
    filename = f"results/{uuid.uuid4()}.json"
    with open(filename, "w") as file:
        json.dump(data, file)
    return JSONResponse(
        content={"message": "Данные успешно сохранены", "filename": filename})


@app.get("/video/{filename}")
async def get_video(filename: str):
    video_path = f"static/video/{filename}"
    if os.path.isfile(video_path):
        return FileResponse(video_path)
    raise HTTPException(status_code=404, detail="Видео не найдено")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
