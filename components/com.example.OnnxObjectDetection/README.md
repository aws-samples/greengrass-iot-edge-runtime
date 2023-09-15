## com.example.OnnxObjectDetection

The ONNX Object detection contains the inference code and is dependent on the ONNX Model and ONNX Runtime components. The dependency ensures the Greengrass deployment contains a trained model and all runtime dependencies. This component also includes a Greengrass IPC Subscriber which handles messages from File System Monitor and performs inference on files referenced in the IPC message.

Files in this directory:

- images/: directory which includes sample image for inference
- src/: directory which includes ONNX Inference class
- buildspec.yml: build commands for AWS CodeBuild
- gdk-config.json: GDK configuration, used during build
- main.py: Inference source code
- monitor.py: source code for the file monitoring
- recipe.yaml: Greengrass recipe which is filled in during the GDK build process. Note how this recipe can reference configuration variables from dependent components
- requirements.txt: optional build dependencies which may be needed
