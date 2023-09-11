## My Project

This repository demonstrates building, deploying, and managing software at the edge. This solution demonstrates event driven ML inference using AWS IoT Greengrass. The use case assumes an upstream data acquisition process makes raw data available for inference on a specified file system directory. We use a sample Greengrass component to monitor that directory and trigger our inference process via Greengrass IPC.

![image](https://github.com/aws-samples/greengrass-iot-edge-runtime/assets/123971998/ce9ebe23-e4ad-4e94-94c4-08aa8c732a43)

### AWS Greengrass Components

This section describes the functionality of each of the Greengrass components.

#### File System Monitor

The File System Monitor component is a proof of concept for monitoring a file system for new files to be created. As previously stated, the use case assumes we want to perform inference when new data is available. A better pattern could be having the data acquisition process send the Greengrass IPC message directly rather than responding and filtering all new file creations within our directory.

#### ONNX Runtime

The ONNX runtime component contains the script that installs the machine learning framework and its dependencies on the Greengrass core device. When deploying to Edge devices with limited outbound connectivity, an alternative option is to install dependencies from locally source packages or as docker containers.

#### ONNX Model

The ONNX Model contains a pre-trained machine learning model. By decoupling the model from the inference component, we can revise our model without needing to rebuild our inference code.

#### ONNX Object Detection

The ONNX Object detection contains the inference code and is dependent on the ONNX Model and ONNX Runtime components. The dependency ensures the Greengrass deployment contains a trained model and all runtime dependencies. This component also includes an Greengrass IPC Subscriber which handles messages from File System Monitor and performs inference on files referenced in the IPC message.

### Continuous Integration and Continuous Delivery (CI/CD)

This repository utilizes CI/CD to simplify the process for building, managing, and deploying AWS IoT Greengrass components. An AWS CodePipeline will be dynamically created for each component which is checked into the component directory of the specified CodeCommit repository. An AWS Lambda function will determine which components are impacted by new commits and thereby need to be rebuilt. This process results in selective builds which can help to manage and scale our build process. This pattern is described in detail in the following [blog post](https://aws.amazon.com/blogs/iot/trigger-aws-iot-greengrass-component-deployments-from-aws-codecommit/).

## Setup

The code provided in the repository represents an AWS Cloud Development Kit (CDK) project. To implement into your own account,

1. Create a CodeCommit repository in your AWS account
2. Configure the cdk.json file with your account details
3. Ensure CDK is installed, run the following:

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

4. After requirements have been installed, check the assets in this repository into your CodeCommit repository

```
git add --all
git commit -m "initial commit"
git push
cdk deploy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
