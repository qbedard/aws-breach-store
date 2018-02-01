# AWS Breach Store
This project includes a parser for breached credentials and an API for accessing the data after it has been ingested into an Elasticsearch instance. It leverages Amazon Web Services in the following manner:
* Elasticsearch - used as a NoSQL database for indexing breach data
* API Gateway - used to create a simple API with authentication for accessing the breach data
* Lambda - used to execute API functions tied to the API Gateway endpoints
* CloudWatch - used to log API requests.

The guidelines and test data for this project were provided by SpyCloud.

## The Parser
The parser takes a file name as a command line argument, which it parses and outputs the results as a .json file.

It expects the data to be in the format `<email>:<password>` with one record per line. It will reject lines which are not in this format and/or do not contain a valid email.

## The API
The API provides 4 endpoints for retrieving breach data:
* email
* username (the username portion of the email)
* domain (the domain portion of the email)
* password

## The Lambda Function
Since the scheme of the API bears a 1-to-1 relationship to the indexed fields, the Lambda function leans on the API for controlling what fields can be queried by dynamically retrieving the pathParameters and filtering the query based on the parameter names/values.
