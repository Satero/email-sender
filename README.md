# AWS-based Automated Email Sender Prototype

I used Amazon Web Services (AWS, for short) to build an automatic email sender that would send emails for me every
hour to a list of desired recipients.

## AWS Services Used
* Chalice - Serverless app framework
* DynamoDB - Database to store email content
* Lambda - Code-running platform supporting events
* Simple Email Service (SES) - Email-sending services for marketing, notifications
* CloudWatch - Scheduling and monitoring resource for AWS

## Prerequisites
1. Install Python
2. Install AWS Chalice
3. Get an AWS Account and verify your credentials

## Getting Started
First, you can download app.py and Reasons.csv from the repo (or if you'd like to store your own email messages,
feel free to make your own Reasons.csv).

The following lines are Linux-based examples in Terminal detailing how to get the application up and running.

First, create a new Chalice project with

```
$ chalice new project [name of app]
```

which will create a new folder.

Next, you will want to replace the new app.py in the new folder with the app.py you downoaded, and you also
should place Reasons.csv in the directory as well.

Lastly, you can launch the project with

```
$ chalice deploy
```

## Conceptual Rundown
The Chalice-based email sender automatically sends emails every hour by using CloudWatch to schedule the event, 
pulling information from DynamoDB as email content. The main function is a Lambda function. The current iteration 
of the application is limited to 2 receivers, but can easily be scaled.

## Author
* Justin Picar
