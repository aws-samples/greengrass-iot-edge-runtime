import time
import traceback
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

class InferenceRequestHandler(client.SubscribeToTopicStreamHandler):
    inference = None
    
    def __init__(self, model_path, confidence):
        super().__init__()
        self.inference = ONNXInference(model_path, confidence)

    def on_stream_event(self, event: SubscriptionResponseMessage) -> None:
        try:
            message = str(event.binary_message.message, "utf-8")
            # Handle message.
            print("Received message")
            print(message)
            result = self.inference.process(str(message))
            print(result)
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        print("Received a stream error.", file=sys.stderr)
        traceback.print_exc()
        return False  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        print('Subscribe to topic stream closed.')

# Configuration
TIMEOUT = 10
model_path = str(os.environ['MODEL_DIR'])
image_path = str(os.environ['IMAGES'])
confidence = float(os.environ['CONFIDENCE'])
topic = str(os.environ['TOPIC'])

# Create ONNXInference object
# inference = ONNXInference(model_path, confidence)

# Setup IPC Message Handler
ipc_client = awsiot.greengrasscoreipc.connect()

request = SubscribeToTopicRequest()
request.topic = topic
handler = InferenceRequestHandler(model_path, confidence)
operation = ipc_client.new_subscribe_to_topic(handler)
operation.activate(request)
future_response = operation.get_response()


# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)
                  
# To stop subscribing, close the operation stream.
operation.close()