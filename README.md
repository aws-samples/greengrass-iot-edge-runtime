## My Project

This repository demonstrates building, deploying, and managing software at the edge. This solution demonstrates implementing event driven inference using AWS IoT Greengrass. The use case assumes an upstream data acquisition process which makes data available for inference on a specified file system direcotry. We use a sample Greengrass component to monitor that directory and trigger our Greengrass inference process via Greengrass IPC.

![image](https://github.com/aws-samples/greengrass-iot-edge-runtime/assets/123971998/ce9ebe23-e4ad-4e94-94c4-08aa8c732a43)


## Setup

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

git add --all
git commit -m "initial commit"
git push
cdk deploy

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

