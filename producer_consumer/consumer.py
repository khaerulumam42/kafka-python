import logging

from json import loads
from kafka import KafkaConsumer

logging.basicConfig(level=logging.WARNING)

consumer = KafkaConsumer(
    "tutorial_topic",
    bootstrap_servers=["kafka:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")))

for message in consumer:
    message = message.value
    logging.warning(f"get message {message}")