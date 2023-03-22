# Hello 😊 This is the back-end for the second coding test for Foodles.

## How to use

This project is composed of two services managed by [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) which are :

- A Python environment on [Django](https://www.djangoproject.com/) to serve the API.
- A PostgreSQL database to store the data.

You'll need to create a self-signed certificate to run the server, to do this you can use [mkcert](https://github.com/FiloSottile/mkcert).
<br />
Create a folder named `certs` in foodles_second_coding_test_backend/, generate two certificates named `0.0.0.0-key.pem` and `0.0.0.0.pem` and copy them in the `certs` folder.
<br />
<br />
Once done, be sure Docker and Docker-compose are installed on your os then you can run the server by entering the following commands one after the other :

```
docker-compose build
```

and

```
docker-compose run
```

This should start the server at [https://0.0.0.0:8000](https://0.0.0.0:8000).

To run the tests, you can enter the shell of the api container and run the following command :

```
npm run test
```
