from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from predict import gen
import json

app = FastAPI()

class Query(BaseModel):
    question: str

async def generate_responses(question: str):
    async for response in gen(question):
        # JSON 형식으로 각 부분 응답을 생성
        yield json.dumps(jsonable_encoder{"part": response}) + "\n"

@app.post("/ask")
async def ask(query: Query):
    # 제너레이터를 사용하여 스트리밍 응답 생성
    return StreamingResponse(generate_responses(query.question), media_type="text/event-stream")