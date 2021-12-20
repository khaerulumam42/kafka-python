from fastapi import HTTPException, FastAPI, Request
from kafka import KafkaProducer

import logging
import asyncio
import uvicorn
import traceback
import json

producer = KafkaProducer(bootstrap_servers=["kafka:9092"],
                         value_serializer=lambda x:
                         json.dumps(x).encode("utf-8"))

logging.basicConfig(level=logging.WARNING)
app = FastAPI()

@app.post("/v1/webhook")
def webhook(request: Request):
    try:
        payload = asyncio.run(request.json())
        event_id = payload["event_id"]

        topic = "tutorial_topic"

        producer.send(topic, payload)

        logging.warning(f"payload {payload} sent to topic {topic}")

        return {"event_id": event_id, "payload": payload, "topic": topic, "status": "OK"}
    except Exception as e:
        error_message = f"error on main function {e}"
        detail = {"status": "error", "message": error_message}
        logging.warning(traceback.print_exc())
        return HTTPException(status_code=500, detail=detail)        


if __name__ == '__main__':
    uvicorn.run(app, debug=False)
