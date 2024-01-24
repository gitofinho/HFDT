from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from predict import gen
import json

app = FastAPI()

async def response_generator(query):
    # Start the generation process
    start_generation(query)

    # Starting an infinite loop
    while True:
        # Obtain the value from the streamer queue
        value = streamer_queue.get()
        # Check for the stop signal, which is None in our case
        if value == None:
            # If stop signal is found break the loop
            break
        # Else yield the value
        yield value
        # statement to signal the queue that task is done
        streamer_queue.task_done()

        # guard to make sure we are not extracting anything from 
        # empty queue
        await asyncio.sleep(0.1)

class Query(BaseModel):
    question: str

async def generate_responses(question: str):
    async for response in gen(question):
        yield response

@app.get('/ask/')
async def stream(query: str):
    print(f'Query receieved: {query}')
    return StreamingResponse(generate_responses(query), media_type='text/event-stream')

@app.post("/ask")
async def ask(query: Query):
    # 제너레이터를 사용하여 스트리밍 응답 생성
    return StreamingResponse(generate_responses(query.question), media_type="text/event-stream")