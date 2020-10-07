# IoT-Project

## Description
The function of this project is to accomplish a whole IoT system, which include front-end, back-end, and local device. The web is used to control local device remotely through backend architecture.

This project is seperate in below four files: 
1. awsIoT.html: This is the code of a web that can used to control IoT Device.
2. IoT_Device_Simulator.py: This is the code of a IoT device simulator used in this project.
3. IoT_API.py: Frontend web call this API code when user want to control the IoT device.
4. sendMessageCode.py: It is used to send the text message which notify device owner the status of the device has changed when IoT Device's status changed.

## Usage
IoT_API.py and sendMessageCode.py shoud used in AWS Lambda. They are constructed in different way:
- IoT_API.py: This is a RESTful API. So after you create a lambda which running this code. You need to create a API Gateway connecting to the lambda you created.
- sendMessageCode.py: It will triggered by Rule Engine. So create a Iot thing after you created lambda function. Then select the lambda function as a target funciton.
- IoT_Device_Simulator.py: Run this code in Jupytor Notebook. Each part run in different section.
- awsIoT.html: Run this code in a server. Remember to change the API link to your API Gateway's endpoint.
