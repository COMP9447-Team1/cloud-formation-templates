# Cloud Formation Templates
This repository contains all our cloud formation templates of our use cases. This makes it easy to set up our SOAR solution on any account and easy to tear down if needed. Each template needs to be customised and uploaded to an S3 Bucket before you can successfully import it in AWS Cloud Formation. 

## What to do before you upload to AWS Cloud Formation
### Remediation Python File
Our primary choice of notification is through a Slack bot. This means that there are two things to customise: your personal Slack bot and your own channel where you want your notifications to be in. This can be customised in the python file.

Firstly, the templates require a private bot key to your own Slack bot. `{{INSERT_SLACK_WEBHOOK_HERE}}` marks where you should insert your personal URL. Your URL should look something like "`https://hooks.slack.com/services/...`".

Secondly, you need to add your channel name. `{{INSERT_CHANNEL_NAME_HERE}}` marks where you should insert your channel name.

Save your changes and create a zipfile with your remediation python file inside. This can be done using the command
`zip {filename}.zip {pythonfile}`. An example of this command would be `zip auto-S3-encryption.zip index.py`.

Upload the .zip file to an S3 bucket. You can do this by going to the home page of the AWS S3 service. Click on "Create bucket". Enter a unique bucket name. Upload your .zip file to the bucket by clicking on the bucket name and then clicking on the button "Upload".

### CloudFormation Template
There are two things to change on the template. Firstly, you would need the bucket name which you have just saved your .zip file in. Replace `{{INSERT_BUCKET_NAME}}` with your bucket name. Replace `{{INSERT_ZIPFILE_NAME}}` with your .zip file name. Save the file.

## How to upload it to AWS Cloud Formation
Start by creating a new stack with new resources (standard).

<p align="center">
  <img src="images/new-stack.png" />
</p>
</br>

Select the options "Template is ready" and "Upload a template file" as shown below. Import the AWS Cloud Formation template that you wish to implement.

<p align="center">
  <img src="images/upload-template.png" />
</p>
</br>

Enter a name for your stack. Make sure that the name you enter is short and informative.

<p align="center">
  <img src="images/stack-name.png" />
</p>
</br>

Since the template has already has everything configured for you, you can skip past the next step and go onto creating your stack. Make sure to tick off the box indicating that you wish to create IAM resources.

<p align="center">
  <img src="images/create-stack.png" />
</p>
</br>

You should be redirected to a page that looks similar to this. 

<p align="center">
  <img src="images/stack-in-progress.png" />
</p>
</br>

Wait for your stack to be created. When the stack creation is complete, it should be indicated on the left with a green tick and the message "CREATE_COMPLETE".

<p align="center">
  <img src="images/completed-stack.png" />
</p>
</br>

## What to do next
The CloudFormation template has created all the necessary resources for you. Remediation should be automatic and require no further action.