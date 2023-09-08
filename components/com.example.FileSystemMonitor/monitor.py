import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import concurrent.futures
import traceback
import awsiot.greengrasscoreipc
from awsiot.greengrasscoreipc.model import (
    PublishToTopicRequest,
    PublishMessage,
    BinaryMessage,
    UnauthorizedError
)

# Configuration
path_to_watch = '/root'  # Replace with the directory path you want to monitor
topic = "my/topic"
TIMEOUT = 10

class MyHandler(LoggingEventHandler):
    def dispatch(self, event):
        if event.key[0].lower() == "created" and str(event.key[1]).endswith('.jpg'):
            print(event.key[1])
            time.sleep(2)
            send_ipc_message(event.key[1])

def send_ipc_message(file_path):
    try:
        request = PublishToTopicRequest()
        request.topic = topic
        publish_message = PublishMessage()
        publish_message.binary_message = BinaryMessage()
        publish_message.binary_message.message = bytes(file_path, "utf-8")
        request.publish_message = publish_message

        operation = ipc_client.new_publish_to_topic()
        operation.activate(request)
        future_response = operation.get_response()

        try:
            future_response.result(TIMEOUT)
            print('Successfully published to topic: ' + topic)
        except concurrent.futures.TimeoutError:
            print('Timeout occurred while publishing to topic: ' + topic, file=sys.stderr)
        except UnauthorizedError as e:
            print('Unauthorized error while publishing to topic: ' + topic, file=sys.stderr)
            raise e
        except Exception as e:
            print('Exception while publishing to topic: ' + topic, file=sys.stderr)
            raise e
    except Exception as e:
        print('Exception occurred when using IPC.', file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    ipc_client = awsiot.greengrasscoreipc.connect()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()