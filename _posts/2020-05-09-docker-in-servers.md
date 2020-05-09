---
author: Abhigyan Khaund
title: Phusion Passenger+Docker in Servers 
toc: true
toc_label: "On this page"
---

Passenger-Docker Impelementation in our SNTC Server

The SNTC server intends to host many student projects and open-source applications so that the student community and the general public can have access to it. The projects will be heterogeneous in terms of the software components required. We realize by deploying shared docker containers in terms of the software and services required.

This article documents how we are using docker to containerize applications of a particular technology stack, and using Phusion Passenger to manage HTTP requests to multiple apps in a single container. 

We are maintaing some basic restrictions  -

1) Main technology stack (eg. nodejs (not its dependencies) ) that an application developer uses can have one and only one version, i.e. one container supports only one version of the main technology. (This should be overcomed).
2) Each docker image have only one instance of service running. 
3) Two applications cannot have the same application name.

### Server's System Design

![]({{ "/assets/images/sntcserver.jpg" | relative_url }})

#### General Service Design Specifications

* Each service name will be corresponding to the software they host. Eg., Django service’s name will be
`webhosting_django`.

* Each service will have their port 22 mapped to a physical server’s port which will be 24000 and up. This
port will be used for SSH access to the container. This also means that each service will have an OpenSSH
server installed on their containers.

* Each service can have one additional port on their containers exposed. This port will be used for accessing
the main daemon of the technology hosted by the service. This port will be tried to map to one of the physical
server’s 8000-9000 ports. If anyone of these ports are already in use, we can extend the range. Eg. Port 80 of Django container is mapped to port 8003 of the main machine.

* The service specification will be written in the main `docker-compose.yml` configuration file for
the webhosting stack. One example is detailed in this post later.

* Each service will have at least two volumes mapped to the physical server. One will contain the data of
the applications that will use the software hosted by the service.

* Each container of the service will contain users corresponding to the applications using the software
hosted by the service.

* Every service will be connected to the main overlay network `webhosting_main`. This will allow
inter-networking between the services. Eg. Apache container can access the MySQL container.


#### Specific Service Design Specifications

##### Web Server services
Application is hosted as a virtual host on its own container.

##### PHP-Apache like webhosting services
These services have their base-image derived from `phusion/baseimage`. This allows running multiple daemons on the containers. [Read more](https://github.com/phusion/baseimage-docker) for details.

##### Services hosting Django, Nodejs, Ruby etc
In such applications, each application binds to a port which serves the requests, so each web server needs different ports and additional daemons running the server. We utilize `phusion/passenger` images for this. Passenger is a deployment software which uses a middleman (Nginx) to host multiple web servers on different ports. [Read more](https://github.com/phusion/assenger-docker) for details.

##### Database services
* Each database has it’s storage directory mounted on the physical server.
* These services currently do not have application-based Linux users, but will have specific user-like abstraction
within the database. For eg., MySQL will have different users for each application with reduced privileges,
and MongoDB will have different password-protected databases for each application using the service. **This maybe enhanced in the future to be more secure.**
* SSH access to these containers are restricted to root user.
* We use public docker image of respective database. In future, to serve more daemons to enhance security, we should shift to `passenger/baseimage`.


#### A bit about Phusion Passenger
Phusion Passenger is an open source web application server. Passenger daemon coordinates requests between the Nginx server and the application.
![Design of a container with Phusion Passenger]({{ "/assets/images/sntcserver-passenger.jpg" | relative_url }})


### Configuration Details

#### Docker Stack

A part of the docker-compose file that we use for stack configuration for deploying docker stack is below. 
```yaml
version: '3.x'
services:
  phpapache:
    image: sntcserver/phpapache:v1
    ports:
      - "1234:80"
      - "12345:22"
    volumes:
      - ./path/to/php-apache2/data:/home
      - ./path/to/php-apache2/apache2-conf:/etc/apache2
    networks:
      - main
  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: <mysql_root_passwor>
    logging:
      driver: "json-file"
    ports:
      - "1235:3306"
      - "12346:22"
    volumes:
      - ./mysql/data-dir:/var/lib/mysql
      - ./mysql/mysql-conf.d:/etc/mysql/conf.d
      - ./mysql/mysqld-conf.d:/etc/mysql/mysql.conf.d
  django:
    image: sntcserver/django2:v1
    ports:
      - "1236:80"
      - "12347:22"
    volumes:
      - ./path/to/django-2/data:/home
      - ./path/to//django-2/nginx-conf:/etc/nginx
    networks:
      - main
  networks:
    main:
      driver: overlay
```


#### Dockerfiles

Example of a dockerfile - PHP-Apache Image

```dockerfile
FROM phusion/baseimage
# OpenSSH-server
RUN cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original_copy
RUN rm -f /etc/service/sshd/down
RUN echo "root:phpapache2" | chpasswd
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN /etc/init.d/ssh restart
# Apache
RUN apt-get update
RUN apt-get -y install apache2
# PHP
RUN apt-get -y install php libapache2-mod-php php-mcrypt php-mysql
# Starting apache2
RUN mkdir /etc/service/apache
ADD apache.sh /etc/service/apache/run
RUN chmod +x /etc/service/apache/run
```


### How we deplay containers for new tech

An example of how we deploy a container for tech that doesn't already exists in stack. We will deploy Flask for this example.

1) Create `Dockerfile` for this new service.

  ```dockerfile
  FROM phusion/passenger-customizable
  CMD ["/sbin/my_init"]
  # OpenSSH-server
  RUN cp /etc/ssh/sshd_config /etc/ssh/sshd_config.original_copy
  RUN rm -f /etc/service/sshd/down
  RUN echo "root:phpapache2" | chpasswd
  RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
  RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
  RUN /etc/init.d/ssh restart
  # Nginx
  RUN rm -f /etc/service/nginx/down
  # Python and Django
  RUN apt-get update
  RUN apt-get install -y python3 python3-pip
  RUN pip3 install flask
  ```

  * Make a directory flask in the `containers` directory on the server -
  ```bash
  mkdir flask
  cd flask
  ```
  * Save the above `Dockerfile`
  * Run the following commands to build and push the image to the `sntcserver` Docker ID
  ```bash
  docker build −t sntcserver/flask:v1
  docker login
  docker push sntcserver/flask:v1
  ```

2) Append the following in the main stack docker-compose.yml configuration file.

  ```yaml
  flask:
    image: sntcserver/flask:v1
    ports :
      - "1237:80"
      - "12348:22"
    volumes:
  	- ./flask/data : /code
  	- ./flask/nginx−conf:/etc/nginx
    networks:
      - main
  ```

3) Update stack -
  `docker stack deploy −c docker−compose.yml webhosting`
<br>
  **Add an application to the new container** 

4) Change the Nginx configuration file within the container

  * Open bash of the container - `docker exec − i t <container_name > bash`
  * Create a new file `/etc/nginx/sites-enabled/<app_name>.conf` and add the following lines in the file.
  ```
  server {
  	listen 80;
  	server_name <app_name >.iitmandi.co.in ;
  	root <path to staticfiles’ folder >;
  	passenger_enabled on ;
  	passenger_python /usr/bin/python3 ;
  }
  ```

5) Then we update Nginx configuration on our main server -
  Add the following server block in the `/etc/nginx/nginx.conf` -
  ```
  server {
  	listen 80;
  	server_name <app_name >.iitmandi.co.in ;
  	location / {
  		proxy_pass http://127.0.0.1:1237;
  		proxy_set_header Host $host;
  		proxy_set_header X−Real−IP $remote_addr;
  		...
  		...
  		}
  }
  ```
Reload `nginx` and then good to go!

Note: Take care of SSL requests and create a certificate for the new domain as well.

-----------------------------

This concludes our post on how we are using Phusion Passenger and Docker containerization for our SNTC Server and also steps to create new containers and add new application/webapps to these multi daemon containers.