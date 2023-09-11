## My Project

### com.Example.FileSystemMonitor

This component is a proof of concept for sending events when new files are created on the file system. For the given use case, we assume an upstream process is interfacing with sensors to perform data acquisition. Using the watchdog python library, we can send an IPC message to a specified topic to trigger inference on an adjacent component.
