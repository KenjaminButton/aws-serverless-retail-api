# AWS Serverless Retail Data API – Environment Setup & Permission Validation

**Objective:**  
Establish a secure, production-ready AWS environment capable of hosting a fully serverless Retail Data API using **AWS Lambda**, **Amazon API Gateway**, and **Amazon DynamoDB**.

---

## ✅ Skills Demonstrated

- **AWS CLI configuration** with named profiles and credential management  
- **IAM best practices:** created a non-root IAM user with least-privilege policies  
- **AWS Toolkit integration** within **VS Code** for CLI + GUI synchronization  
- **Multi-profile workflow** using `--profile` flags (industry standard)  
- **End-to-end permission validation** for Lambda, API Gateway, and DynamoDB  
- **Command-line automation & cleanup** to test lifecycle operations

---

## ⚙️ Technical Validation Process

### 1. CLI & IAM Setup
- Installed and verified AWS CLI (`aws --version`)
- Configured credentials via `aws configure --profile serverless-retail-api-user`
- Confirmed authentication with:
  ```bash
  aws sts get-caller-identity --profile serverless-retail-api-user
  ```

# AWS Serverless Retail Data API – Environment Setup & Permission Validation

**Objective:**  
Establish a secure, production-ready AWS environment capable of hosting a fully serverless Retail Data API using **AWS Lambda**, **Amazon API Gateway**, and **Amazon DynamoDB**.

---

## ✅ Skills Demonstrated

- AWS CLI configuration with named profiles and credential management  
- IAM best practices: created a non-root IAM user with least-privilege policies  
- AWS Toolkit integration within VS Code for CLI and GUI synchronization  
- Multi-profile workflow using `--profile` flags (industry standard)  
- End-to-end permission validation for Lambda, API Gateway, and DynamoDB  
- Command-line automation and cleanup to test lifecycle operations

---

## ⚙️ Technical Validation Process

### 1. CLI and IAM Setup
- Installed and verified AWS CLI.  
- Configured credentials through a secure, named profile.  
- Confirmed account identity and authentication using AWS STS.  
- Ensured non-root credentials and correct region configuration.  

---

### 2. Lambda Permissions
- Validated the ability to create, read, and delete Lambda functions.  
- Confirmed that the IAM role was correctly attached and usable.  
- Successfully demonstrated function deployment and teardown.  

---

### 3. API Gateway Permissions
- Confirmed full read and write permissions by creating a REST API.  
- Validated lifecycle operations, including creation, verification, and deletion.  
- Demonstrated control of endpoint configuration and API region management.  

---

### 4. DynamoDB Permissions
- Created a temporary DynamoDB table to validate database permissions.  
- Inserted and retrieved records to verify read and write capabilities.  
- Deleted the table to confirm cleanup and resource management.  

---

## 🧠 Key Takeaways

- Configured a fully functional AWS environment for serverless development.  
- Implemented secure IAM practices with isolated project profiles.  
- Verified operational access across Lambda, API Gateway, and DynamoDB.  
- Established best practices for SAM/CLI development and VS Code integration.  
- Confirmed a clean, repeatable setup for future AWS serverless projects.  

---

## 🚀 Next Phase

Initialize and deploy the full project using the AWS Serverless Application Model (SAM).  
Build and deploy a production-ready **Serverless Retail Data API** that integrates Lambda, API Gateway, and DynamoDB for real-world cloud operations.

---

**Tech Stack:**  
AWS Lambda · Amazon API Gateway · Amazon DynamoDB · IAM · AWS CLI · AWS Toolkit for VS Code · Python 3.12 · SAM (Serverless Application Model)

**Author:** Kenjamin  
**Date:** October 2025
