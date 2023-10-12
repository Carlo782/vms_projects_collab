<h1 align="center">
  Variamos Projects Microservice
</h1>

## Description
```
Microservice that allows to get Variamos projects.
```

## Building of the project
```
docker build --no-cache --progress plain -t vms_projects .\ 
```

### Project deployment
```
docker run -p 10000:10000 --rm --name vms_projects -t vms_projects
```
# API Documentation

This document outlines the available endpoints and their usage for the project's API.

---

### Generate Token
Get a token for a user.
Parameter | Value
-- | --
Verb | `POST`
URL | `/token`
Payload | ```{"user_id": "«user id»"}```
Response | ```{"access_token": "«token value»", "token_type": "bearer"}```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Save Project
Save the user's project.
Parameter | Value
-- | --
Verb | `POST`
URL | `/saveProject`
Authentication | `Bearer`
Payload | ```{"project": «project data»}```
Response | ```{ "project": «project data»}```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Get Projects
Get the user's projects.
Parameter | Value
-- | --
Verb | `GET`
URL | `/getProjects`
Authentication | `Bearer`
Response | ```{ "projects": [ { "id": "1", "name": "Project 1" }, { "id": "2", "name": "Project 2" }, ...] }```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Get Project
Get a specific project by ID.
Parameter | Value
-- | --
Verb | `GET`
URL | `/getProject?project_id=«project id»`
Authentication | `Bearer`
Response | ```{ "project": «project data»}```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Share Project
Share a project with another user.
Parameter | Value
-- | --
Verb | `POST`
URL | `/shareProject`
Authentication | `Bearer`
Payload | ```{ "project_id": "«project id»", "user_id": "«user id»" }```
Response | ```{ "project": «project data»}```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Get Users of Project
Get users associated with a specific project.
Parameter | Value
-- | --
Verb | `GET`
URL | `/usersProject?project_id=«project id»`
Authentication | `Bearer`
Response | ```{ "users": [ { "userId": "«user id»", "permissionIds": ["«permission id1»", "«permission id2»", ...] }, ...] }```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

### Find User by Email
Find a user based on their email address.
Parameter | Value
-- | --
Verb | `GET`
URL | `/findUser?user_mail=«user email»`
Authentication | `Bearer`
Response | ```{ "userId": "«user id»", "userName": "«user name»", "userEmail": "«user email»" }```
Exception response | `Http response code 40x, body: {message:«message error»}`

---

*Note: Replace placeholder values like «project id» with actual values as appropriate.*
