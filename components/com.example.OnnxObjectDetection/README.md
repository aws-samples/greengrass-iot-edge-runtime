## My Project

### com.Example.OnnxObjectDetection

The ONNX Object detection contains the inference code and is dependent on the ONNX Model and ONNX Runtime components. The dependency ensures the Greengrass deployment contains a trained model and all runtime dependencies. This component also includes a Greengrass IPC Subscriber which handles messages from File System Monitor and performs inference on files referenced in the IPC message.
