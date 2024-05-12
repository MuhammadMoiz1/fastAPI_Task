# FastAPI Project

This project provides APIs for user management and face detection using FastAPI and Mediapipe.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
Install dependencies:

```bash
pip install -r requirements.txt
```
Run the application:

```bash
uvicorn main:app --reload
```
## Endpoints

User Management

### POST /users/: 

Create a new user. Returns HTTP 201 Created on success.

```json
{
  "name": "string"
}
```
### GET /users/{id}: 

Get user details by ID. Returns HTTP 200 OK on success.

### GET /users_search/: 

Search users by name. Returns HTTP 200 OK on success.

Query parameter:
  - st: Search string.

### PUT /users/{id}: 

Update user details by ID. Returns HTTP 200 OK on success.

```json
{
  "name": "string"
}
```
### DELETE /users/{id}: 

Delete user by ID. Returns HTTP 200 OK on success.
Face Detection

### POST /detect_face/: 

Detect face in an uploaded image. Returns HTTP 201 Created on success.

Request body: 

Form-data with key as "image" and value as the image file.


## Contributing
Contributions to this project is welcomed. To contribute, follow these steps:

Fork the repository.
- Create a new branch: 
```bash
git checkout -b feature/your-feature.
```
- Make your changes and commit them: 
```bash
git commit -am 'Add new feature'.
```
- Push to the branch: 
```bash
git push origin feature/your-feature.
```
- Submit a pull request.



Demonstration Video

```css
https://www.loom.com/share/c09077a9113c4680aa84ad298dc31300?sid=8f660c97-f8d3-46f4-b102-f9dcbebfbc5e
```
