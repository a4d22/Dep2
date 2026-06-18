Final Architecture
                       GitHub
                          |
                          |
                          v
                 GitHub Actions
                          |
                    Unit Tests
                          |
                    Build Docker
                          |
                          v
                        ECR
                          |
                          |
                          v
                  SageMaker Pipeline
                          |
            ---------------------------
            |            |            |
            v            v            v
      Preprocess      Train      Evaluate
                                       |
                                       v
                               Model Registry
                                       |
                                 Manual Approval
                                       |
                                       v
                               SageMaker Endpoint
                                       |
                                       v
                              Customer Requests
                                       |
                                       v
                                CloudWatch
                                       |
                                       v
                               Model Monitor
                                       |
                                       v
                              Drift Detection
                                       |
                                       v
                                EventBridge
                                       |
                                       v
                             Retraining Pipeline
What We Will Actually Build
Stage 1

AWS Basics

Learn:

IAM
S3
ECR
CloudWatch
ECS

Project:

Create S3 bucket
Upload dataset
Stage 2

Build Model

Simple:

RandomForestClassifier

Files:

src/
   train.py
   predict.py

Output:

model.pkl
Stage 3

Docker

Create:

Dockerfile

Run:

docker build .
docker run .
Stage 4

Inference API

Using:

FastAPI

Endpoint:

POST /predict

Input:

{
  "tenure": 12,
  "monthly_charges": 75
}

Output:

{
  "churn_probability": 0.87
}
Stage 5

GitHub Actions

Workflow:

Push
  |
  v
pytest
  |
  v
build docker
Stage 6

ECR

Push image:

GitHub Actions
     |
     v
ECR
Stage 7

ECS

Deploy API.

Architecture:

Internet
    |
    v
ALB
    |
    v
ECS Fargate
Stage 8

SageMaker Training

Instead of local training:

train.py

run training inside SageMaker.

Learn:

SKLearn Estimator
Stage 9

Model Registry

After training:

Model v1

register automatically.

Stage 10

SageMaker Pipeline

Build:

Preprocessing
   |
Training
   |
Evaluation
   |
Registration
Stage 11

Feature Store

Store:

customer_id
tenure
monthly_charges
contract_type

inside SageMaker Feature Store.

Training and inference both use it.

Stage 12

Endpoint Deployment

Deploy:

Approved Model
     |
     v
SageMaker Endpoint
Stage 13

Monitoring

Track:

Latency
Errors
Predictions

using:

CloudWatch
SageMaker Monitoring
Stage 14

Drift Detection

Create synthetic drift.

Example:

Training:

monthly_charge
40-80

Production:

monthly_charge
100-180

Monitor detects drift.

Stage 15

Automatic Retraining

Drift Alert
    |
    v
EventBridge
    |
    v
Pipeline Execution

Retrains model automatically.

Stage 16

Terraform

Create:

S3
IAM
ECR
ECS
SageMaker
CloudWatch

from code.

No clicking in AWS Console.

Stage 17

Enterprise Deployment

Implement:

Dev
dev account
Staging
staging account
Production
production account
Canary Deployment
90% -> old model
10% -> new model

Monitor.

What You'll Learn at Each Step
Stage	AWS Skill
1	IAM, S3
2	ML training
3	Docker
4	FastAPI
5	GitHub Actions
6	ECR
7	ECS/Fargate
8	SageMaker Training
9	Model Registry
10	SageMaker Pipelines
11	Feature Store
12	Endpoints
13	CloudWatch
14	Drift Detection
15	Automated Retraining
16	Terraform
17	Enterprise MLOps

This project is small enough to complete on a personal AWS account, but rich enough that by the end you'll have touched nearly every major AWS MLOps service used in production. The nice part is that we can build it incrementally—starting with a local Random Forest and ending with a fully automated SageMaker pipeline with monitoring and retraining.