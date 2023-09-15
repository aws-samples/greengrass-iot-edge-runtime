## My Project

### com.Example.OnnxModelStore

The ONNX Model contains a pre-trained machine learning model. By decoupling the model from the inference component, we can revise our model without needing to rebuild our inference code.

Files in this directory:

- buildspec.yml: build commands for AWS CodeBuild
- gdk-config.json: GDK configuration, used during build
- recipe.yaml: Greengrass recipe which is filled in during the GDK build process
- requirements.txt: optional build dependencies which may be needed
- yolov8n.onnx: pre-trained Yolov8 model which has been converted to ONNX for runtime
