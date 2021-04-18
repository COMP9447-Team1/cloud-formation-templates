# Cloud Formation Templates
This repository contains all our cloud formation templates of our use cases. This makes it easy to set up our SOAR solution on any account and easy to tear down if needed. Each template requires one manual change before you can successfully import it in AWS Cloud Formation. 

## What to change
Our primary choice of notification is through a Slack bot. This means that the templates require a private bot key to your own Slack bot. `{{INSERT_SLACK_WEBHOOK_HERE}}` marks where you should insert your personal URL. Your URL should look something like
"`https://hooks.slack.com/services/*`" where the symbol "`*`" is your unique bot webhook indentifier. 

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