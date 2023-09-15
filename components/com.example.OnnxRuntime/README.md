## My Project

### com.Example.FileSystemMonitor

The ONNX runtime component contains the script that installs the machine learning framework and its dependencies on the Greengrass core device. When deploying to Edge devices with limited outbound connectivity, an alternative option is to install dependencies from locally sourced packages or as docker containers.

Files in this directory:

- buildspec.yml: build commands for AWS CodeBuild
- gdk-config.json: GDK configuration, used during build
- recipe.yaml: Greengrass recipe which is filled in during the GDK build process
- requirements.txt: optional build dependencies which may be needed
