# Customer Order Management

This is a repository that demonstrates managing customer orders via a Django rest Framework

### API Endpoints

1. **api/v1/authenticate/** Methods allowed are: GET
1. **api/v1/user/** Methods allowed are: GET, PUT, PATCH
1. **api/v1/logout/** Methods allowed are: GET
1. **api/v1/customers/** Methods allowed are: GET, POST
2. **api/v1/customers/{id}/** Methods allowed are: GET, PUT, PATCH, DELETE
3. **api/v1/orders/** Methods allowed are: GET, POST
4. **api/v1/orders/{id}/** Methods allowed are: GET, PUT, PATCH, DELETE

# Development

Following are instructions on setting up your development environment.

The recommended way for running the project locally and for development is using Docker.

It's possible to also run the project without Docker.

## Docker Setup (Recommended)

This project is set up to run using [Docker Compose](https://docs.docker.com/compose/) by default. It is the recommended way. You can also use existing Docker Compose files as basis for custom deployment, e.g. [Docker Swarm](https://docs.docker.com/engine/swarm/), [kubernetes](https://kubernetes.io/), etc.

1. Install Docker:
   - Linux - [get.docker.com](https://get.docker.com/)
   - Windows or MacOS - [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Clone this repo and `cd savannah_informatics`
3. Make sure `Pipfile.lock` exists. If it doesn't, generate it with:
   ```sh
   $ docker run -it --rm -v "$PWD":/django -w /django python:3.7 pip3 install --no-cache-dir -q pipenv && pipenv lock
   ```
4. Create `.env`:

5. Start up the containers:

   ```sh
   $ docker compose -f docker-compose.yml up --build

   ```

   This will build the necessary containers and start them, including the web server on the host and port you specified in `.env`.

   Current (project) directroy will be mapped with the container meaning any edits you make will be picked up by the container.

6. Create a superuser if required:
   ```sh
   $ docker-compose exec web python3 manage.py createsuperuser
   ```
   You will find an activation link in the server log output.
