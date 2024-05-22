# Django Channels Project

This project is a Django Channels application that includes chat functionality. It supports creating and listing chat rooms with user avatars and usernames in the chat logs.

## Table of Contents

- [Django Channels Project](#django-channels-project)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
  - [Route Details](#route-details)
    - [Home Page (List All Chat Rooms)](#home-page-list-all-chat-rooms)
    - [Create New Chat Room](#create-new-chat-room)
    - [Chat Room](#chat-room)
    - [User Sign-Up](#user-sign-up)
  - [Example Usage](#example-usage)

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/seethersan/django_chat.git
    cd django_chat
    ```

2. Build and start the application using Docker Compose:

    ```sh
    docker-compose -f docker-compose-dev.yml up --build
    ```

3. The application will be available at `http://localhost:8000`.

## Running the Application

To run the application locally using Docker Compose, follow these steps:

1. Ensure you are in the project directory.

2. Run the following command to start the application:

    ```sh
    docker-compose -f docker-compose-dev.yml up -d
    ```

3. The application will be accessible at `http://localhost:8000`.

## Running Tests

To run tests for the application, use the following command:

1. Ensure the application is running:

    ```sh
    docker-compose -f docker-compose-dev.yml up -d
    ```

2. Open a new terminal window and run the tests:

    ```sh
    docker-compose -f docker-compose-dev.yml exec web python manage.py test
    ```

This command will execute the test suite and display the results.

## Route Details

### Home Page (List All Chat Rooms)

- **URL**: `''`
- **View**: `Index`
- **Name**: `index`
- **Description**: Displays a list of all chat rooms.

### Create New Chat Room

- **URL**: `'create/'`
- **View**: `RoomCreate`
- **Name**: `create_room`
- **Description**: Provides a form to create a new chat room.

### Chat Room

- **URL**: `'room/<str:room_name>/'`
- **View**: `Room`
- **Name**: `room`
- **Description**: Displays a specific chat room where users can chat.

### User Sign-Up

- **URL**: `'signup/'`
- **View**: `SignUp`
- **Name**: `signup`
- **Description**: Provides a form for new users to sign up.

## Example Usage
To navigate to the chat rooms list, you can use the URL path:
```
http://localhost:8000/chatrooms/
```

To create a new chat room, you can use the URL path:
```
http://localhost:8000/chatrooms/create/
```

To join a specific chat room (e.g., room1), you can use the URL path:
```
http://localhost:8000/chatrooms/room/room1/
```

To sign up as a new user, you can use the URL path:
```
http://localhost:8000/users/signup/
```