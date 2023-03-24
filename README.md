# Hello 😊 This is the back-end for the second coding test for Foodles.

## How to use

This project is composed of two services managed by [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) which are :

- A Python environment on [Django](https://www.djangoproject.com/) to serve the API.
- A PostgreSQL database to store the data.

Be sure Docker and Docker-compose are installed on your os then you can run the server by entering the following commands one after the other :

```
docker-compose build
```

and

```
docker-compose run
```

This should start the server at [http://127.0.0.1:8000](https://127.0.0.1:8000).

To run the tests, you can enter the shell of the api container and run the following command :

```
npm run test
```
