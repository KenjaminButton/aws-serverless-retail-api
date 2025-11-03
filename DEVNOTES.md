```yaml
Outputs:
  # 3) REPLACE: REST output with HTTP API output (no /Prod suffix)
  ApiEndpoint:
    Description: HTTP API base URL ($default stage)
    Value: !Sub "https://${HttpApiGateway}.execute-api.${AWS::Region}.${AWS::URLSuffix}"
  HelloWorldFunction:
    Description: Hello World Lambda Function ARN
    Value: !GetAtt HelloWorldFunction.Arn
  HelloWorldFunctionIamRole:
    Description: Implicit IAM Role created for Hello World function
    Value: !GetAtt HelloWorldFunctionRole.Arn

```

```bash
ggshield secret scan path . --recursive
```

# ⚾ Serverless Baseball Rookie Cards API (Japanese MLB Players)

A step-by-step roadmap for evolving the AWS SAM Hello World project into a professional serverless API featuring curated MLB rookie cards of Japanese players — all graded PSA 10.

---

## ✅ Phase 1 — Baseline Hello World (Completed)
- [x] Initialize project with AWS SAM
- [x] Run locally and confirm "Hello World" works
- [x] Deploy successfully to AWS
- [x] Test the live endpoint (received `{"message":"hello world"}`)
- [x] Commit baseline: initial working Hello World deployment

---

## 🧩 Phase 2 — Convert to HTTP API + DynamoDB Setup
**Goal:** Replace REST API with an HTTP API and add a DynamoDB table to store rookie card data.

- [x] Switch event type from REST to HTTP API
- [x] Add DynamoDB table (`CardsTable`) with partition and sort keys  
  - PK: `player#<PlayerName>`  
  - SK: `card#<Year>#<Brand>#<Set>#<CardNo>#PSA10`
- [x] Add DynamoDB environment variable and CRUD policy
- [x] Add Outputs for API URL and table name
- [x] Validate and build successfully
- [x] Commit: conversion to HTTP API + DynamoDB setup

---

## 🔐 Phase 3 — JWT Authorization for Protected Routes
**Goal:** Secure admin actions (like seeding data) with JWT authentication.

- [x] Select an identity provider (Amazon Cognito or external OIDC)
- [X] Add a JWT authorizer to the HTTP API in template
- [x] Protect the `POST /cards/seed` route (admin-only)
- [x] Keep all `GET` routes public
- [x] Commit: added JWT authorizer and secure routes

---

## ⚙️ Phase 4 — Lambda Routing Logic
**Goal:** Replace hello world handler with clean API routing logic.

**Public routes**
- [ ] `/cards` → list all rookie cards  
- [ ] `/cards/{cardId}` → details of one card  
- [ ] `/cards/top3?player=<name>` → top three cards by price (PSA 10 only)

**Protected route**
- [ ] `/cards/seed` → write curated dataset (admin-only)

**Implementation**
- [ ] Organize handler into routing functions  
- [ ] Add helper for DynamoDB queries and item mapping  
- [ ] Commit: implemented Lambda routing for baseball cards API

---

## 🧠 Phase 5 — Curated Data Seeding
**Goal:** Add real mock data for the Japanese MLB rookie cards (PSA 10 only).

- [ ] Create curated seed data:
  - Shohei Ohtani — 2018 Bowman Chrome  
  - Ichiro Suzuki — 2001 Topps  
  - Hideki Matsui — 2003 Topps  
  - Hideo Nomo — 1995 Topps  
  - Daisuke Matsuzaka — 2007 Bowman Chrome  
  - Yu Darvish — 2012 Topps  
  - Masahiro Tanaka — 2014 Topps  
  - Seiya Suzuki — 2022 Topps  
  - Kodai Senga — 2023 Topps  
  - Yoshinobu Yamamoto — 2024 Topps
- [ ] Ensure seeding is idempotent (no duplicates)
- [ ] Commit: add curated Japanese MLB rookie card dataset

---

## 🧪 Phase 6 — Testing
**Goal:** Verify local and cloud functionality.

- [ ] Add lightweight unit tests for key building and routing logic  
- [ ] Add integration tests for listing and detail endpoints  
- [ ] Verify data appears correctly in DynamoDB after seeding  
- [ ] Commit: added unit and integration tests

---

## 📊 Phase 7 — Observability & Logging
**Goal:** Add professional-grade monitoring.

- [ ] Use structured JSON logs (requestId, path, latency, result)  
- [ ] Confirm logs stream to CloudWatch  
- [ ] Optionally set simple alarms for 5XX errors  
- [ ] Commit: enable structured logging and observability

---

## 🧾 Phase 8 — Documentation & Cost Notes
**Goal:** Make the README clear and recruiter-ready.

- [ ] Explain architecture (SAM, Lambda, HTTP API, DynamoDB)  
- [ ] Document endpoints and expected JSON responses  
- [ ] Include monthly cost note (≈ $0 at low traffic)  
- [ ] Add deployment and testing instructions  
- [ ] Commit: expanded README with architecture and cost details

---

## 🌟 Phase 9 — Final Deployment & Portfolio Polish
**Goal:** Prepare for public viewing.

- [ ] Deploy final version  
- [ ] Verify all endpoints and data integrity  
- [ ] Add `/players` or `/cards/search` optional route  
- [ ] Add screenshots or usage examples  
- [ ] Commit: finalize project for portfolio showcase

---

## 🚀 Optional Enhancements (Future)
- [ ] Add query filters (year, brand, grader)  
- [ ] Add search endpoint  
- [ ] Add lightweight front-end or dashboard  
- [ ] Add USD/JPY price conversions  
- [ ] Extend dataset to NPB rookies or other regions  

---

## 🏁 Summary
This project demonstrates:
- AWS SAM (Infrastructure as Code)
- Lambda + HTTP API design
- DynamoDB key modeling and GSIs
- JWT authorization
- Testing, logging, and cost awareness
- Clean documentation and a unique cultural dataset
