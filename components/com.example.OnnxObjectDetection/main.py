import time
import traceback
import boto3
import os
import sys

from src.inference import ONNXInference

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    SubscribeToTopicRequest,
    SubscriptionResponseMessage,
    UnauthorizedError
)

class StreamHandler(client.SubscribeToTopicStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message = str(event.binary_message.message, "utf-8")
            # message = str(event.message.payload, "utf-8")
            # topic_name = event.message.topic_name
            # Handle message.
            print("Received message")
            print(message)
            result = inference.process(str(message))
            print(result)
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        print("Received a stream error.", file=sys.stderr)
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        print('Subscribe to topic stream closed.')

# Configuartion
TIMEOUT = 10
model_path = str(os.environ['MODEL_DIR'])
image_path = str(os.environ['IMAGES'])
confidence = float(os.environ['CONFIDENCE'])
topic = str(os.environ['TOPIC'])

# Create ONNXInference object
inference = ONNXInference(model_path, confidence)

# Setup IPC Message Handler
ipc_client = awsiot.greengrasscoreipc.connect()

request = SubscribeToTopicRequest()
request.topic = topic
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_topic(handler)
operation.activate(request)
future_response = operation.get_response()


# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)
                  
# To stop subscribing, close the operation stream.
operation.close()