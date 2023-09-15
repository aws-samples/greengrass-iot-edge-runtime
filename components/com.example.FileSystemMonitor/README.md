## com.example.FileSystemMonitor

The File System Monitor component is a proof of concept for monitoring a file system for new files to be created. The use case assumes the inference process should trigger when new data is available. A better pattern could be having the data acquisition process send the Greengrass IPC message directly rather than responding to file system events. This component is purely just a way to mock event creation for the given use case.

Files in this directory:

- buildspec.yml: build commands for AWS CodeBuild
- gdk-config.json: GDK configuration, used during build
- monitor.py: source code for the file monitoring
- recipe.yaml: Greengrass recipe which is filled in during the GDK build process
- requirements.txt: optional build dependencies which may be needed
