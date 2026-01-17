# import json
# import requests
# from kafka import KafkaConsumer

# SEMLOG_API_URL = "http://localhost:8000/v1/ingest"
# KAFKA_TOPIC = "logs.raw"

# consumer = KafkaConsumer(
#     KAFKA_TOPIC,
#     bootstrap_servers=['localhost:9092'],
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# print(f"🔌 Kafka Adapter connected to {KAFKA_TOPIC}. Forwarding to SemLog...")

# for message in consumer:
#     try:
#         # We just act as a bridge
#         payload = {
#             "source": "kafka-stream",
#             "payload": message.value
#         }
#         requests.post(SEMLOG_API_URL, json=payload)
#         print(f"Forwarded offset {message.offset}")
#     except Exception as e:
#         print(f"Error forwarding: {e}")