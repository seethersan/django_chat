# Django Channels Project

This project is a Django Channels application that includes chat functionality. It supports creating and listing chat rooms with user avatars and usernames in the chat logs.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)

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