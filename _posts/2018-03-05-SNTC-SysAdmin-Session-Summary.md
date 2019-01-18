---
  layout: single
  title: SNTC SysAdmin Session Summary
  author_profile: true
  author: Shikhar Gupta
  toc: true
  toc_label: "On this page"
  comments: true
  share: true
---

As mentioned in [previous post](https://kamandprompt.github.io/events/2018-02-21-SNTC-System-Administration-Test/) by [Sahil](https://www.facebook.com/sahilarora535), we selected some students to work on improving the SNTC server. Details of selection criteria, the [sys-admin test](https://github.com/KamandPrompt/sysadmin-test) and results can be found in Sahil's post. To discuss the problems and issues regarding the server deployment, I and Sahil held a session with the newly appointed SysAdmin team. This document serves as a summary for the same.

## The Issues

### 1. Containerization

   The goal of the server is to allow developers to host their apps built on heterogenous platforms (such as nodejs, RubyOnRails, php-apache and MySQL, PostgreSQL, mongodb). To keep these platforms seperate, we would like to have them run in independent docker containers. 

   *Benefits*

   * Dev gets a virtual environment and is abstracted from system's complexity
   * Distributing container-wise sudo rights and ssh rights
   * Several softwares operate on conflicting ports. We can use a custom mapping for ports (acceptable over IITMandi_Wifi, namely ports `1025 - 9000`) and keep the dev abstracted from all this
   * Easier to manage container backups
   * If one container gets messed up, the others are unaffected
   * Easier to maintain multiple versions of same software

### 2. Hierarchical DNS

   We may wish to host apps with URLS in the `appname.sntc.iitmandi.ac.in` format. For the same, we want to have control over DNS entries after `sntc.iitmandi.ac.in` is resolved. We would want to point a URL to a particular port as in `appname.sntc.iitmandi.ac.in -> sntc.iitmandi.ac.in:1234`.  

   Read: <https://www.dnsknowledge.com/whatis/authoritative-name-server/> 

### 3. Reverse Proxy and Web Server - Nginx

   We need to setup Nginx to properly resolve paths and perform redirections. For example, `sntc.iitmandi.ac.in/appname` should point to `sntc.iitmandi.ac.in:1234`.  Nginx can also help in resolving the port problem mentioned above. 

   Read: <https://stackoverflow.com/questions/23649444/redirect-subdomain-to-port-nginx-flask>  

### 4. SSL Certificate

   We need to obtain a valid SSL certificate as well as enable proper encryption and secure Auth for all our apps to gain trust from the end-users.  

### 5. Unified Auth - OpenID

   *Auth* (Authentication and Authorization) is one of the most common problems that every App handles. As an organization, it makes sense to have a unified Auth service. Thanks to Sahil's extensive research on this topic, we have decided to use OpenID as a solution. There are a lot of OpenID implementations, we need to figure out what works the best and how to integrate all our apps with it.

### 6. Third Party Apps

   We also wish to setup several Third Party Apps such as 

   * [Discourse](https://www.discourse.org/) - Discussion Forum
   * [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) - Wiki Pages
   * [WordPress](https://wordpress.com/) - Blogs
   * [Askbot](https://github.com/ASKBOT/askbot-devel) - Q&A forum like StackExchange

   For some of these, docker images are available online. Configuring them with our usecase is the major task here

### 7. Documentation

   Documenting our work is extremely important. As an organisation, where <sup>1</sup>/<sub>4</sub> of the community leaves the org and another <sup>1</sup>/<sub>4</sub> joins each year, documentation is crucial to carry forward our developments.

### 8. Managing Users and Rights

   We can choose to have multiple users according to use cases for various containers.

### 9. Backup and Restore

   We would like to have regular backups which can be easily restored to recover from failures. `docker` allows us to easily manage backups of containers.

### 10. Exposing APIs for databases

   To have looser coupling between front-end and back-end, we should expose datastores with APIs so that front-end (Web, Android, iOS) can be developed independently of the back-end. This way, the front-end developer doesn't need to worry about the schematics and implementation at the back-end.

## The Current Implementation

As a part of [System Practicum](http://www.iitmandi.ac.in/academics/courses/even_feb-june2017/CS307.pdf) Project, our team took up the task of setting up the server. You can find some of the documentation [here](https://drive.google.com/drive/folders/1tHxK25fe4KHVHMHopBqLq2N07Ovi6QVv?usp=sharing). However, the linked documentation is not very good and insufficient. Feel free to contact me to gather further clarity on the same. I would attempt to explain our system in this section.

![SNTC Server Architecture](https://github.com/shikhar-gupta/SystemPracticumDocker/blob/master/Flowchart.png?raw=true "SNTC Server Architecture")

For Containerization, we chose docker-compose against docker since our server is going to host multi-container applications and requires various configuration that can be easily maintained with docker-compose.yml files. 

With docker-compose backups-and-restores for containers are easily maintained by default and can be configured easily as well.

**UPD:** [Docker v13](https://blog.docker.com/2017/01/whats-new-in-docker-1-13/) was released after we deployed our system and adds support for `docker stack ` and [compose-file v3](https://docs.docker.com/compose/compose-file/). Look into it as it is related to docker-compose.yml files.

For each container, we decided to expose atleast two ports, one for ssh and other for the platform's endpoint (80 for Apache, 3000 for nodejs, 3306 for MySQL).

We also decided to give the option of storing files directly to disk instead of within container. For this we mounted a folder on host's disk in each container.

Also, containers need to have connections with each other. Once again, docker-compose helps and automatically creates docker-networks (bridge mode) after mentioning the connections in docker-compose.

```yaml
# docker-compose.yml - nodejs
version: '2'
services:
  nodejs:
    build: .
    container_name: nodejs # Use better names :P
    ports:
     - "7300:3000" # maps host's port 7300 to container's port 3000
     - "23000:22"
    volumes:
     - ./data/:/code #mounts data dir in pwd as /code in container
    network_mode: "bridge"
    external_links:
     - mysql #makes mysql container available within this container
```

We voted against using docker images that served a particular technology out-of-the-box (e.g. [Node docker-image](https://hub.docker.com/_/node/), [MySql docker-image](https://hub.docker.com/_/mysql/) ) and instead chose to install packages on a ubuntu docker-image to have better control and have the devs face a familiar OS across the various containers.

**UPD:** Sahil found a better alternative to using the standard ubuntu image. Please go through: <http://phusion.github.io/baseimage-docker/>

A normal `docker run` only executes one process. We used `supervisor` to manage the background processes and services including the ssh-daemon. Read more at: <http://supervisord.org/introduction.html>

```yaml
; snippet - supervisord.conf - nodejs - InventoryManager
[program:sshd]
command = /usr/sbin/sshd -D

[program:InventoryManager]
command=node /home/InventoryManager/app.js
autostart=true
autorestart=true
environment=NODE_ENV=production
stderr_logfile=/var/log/InventoryManager.err.log
stdout_logfile=/var/log/InventoryManager.out.log
user=root
```

All the requests are actually received by the host machine and are then forwarded to individual docker containers. This is handled by configuring nginx server.

```perl
# snippet - nginx.conf - host 
server { 
    listen       80;
    location / {
        proxy_pass      http://127.0.0.1:10080/;
    }
    location /inv_man {
        rewrite ^/inv_man(.*) http://sntc.iitmandi.ac.in:7300/$1 break;
    }
    location /discourse {
        rewrite ^/discourse(.*) /$1 break;
        proxy_pass      http://127.0.0.1:10180/;
    }
}

```

## Teams

Each team will have some set of students responsible for solving the problem as well as the documentation. One students from each team is responsible for the overall documentation of the work done by the team. For all the teams, the Programming Club coordinators and the Technical Secretary, who are [Abhishek](mailto:abhishekbhardwaj540@gmail.com), [Hitesh Ramchandani](mailto:hitr9831@gmail.com) and [Kushagra](mailto:kushagra.s.888@gmail.com), will look at the documentation of every team and will be responsible for the coordination between the different teams.

**1. Containerization**

* [Abhishek](mailto:abhishekbhardwaj540@gmail.com) (Overall Documentation)
* [Sai Tarun Reddy Palla](mailto:saitarunreddypalla@gmail.com)
* [Aashish Kumar](mailto:kumaraashish118@gmail.com)
* [Prabhakar Prasad](mailto:b16069@students.iitmandi.ac.in)

**2. Heirarchical DNS, Nginx and SSL**

* [Hitesh Ramchandani](mailto:hitr9831@gmail.com) (Overall Documentation)
* [AMRENDRA SINGH](mailto:b16010@students.iitmandi.ac.in)
* [Dheeraj](mailto:b17041@students.iitmandi.ac.in)

**3. Managing Users, Backup, Restore and Server Security and Maintenance**

* [Kushagra](mailto:kushagra.s.888@gmail.com) (Overall Documentation)
* [Abhigyan Khaund](mailto:b16082@students.iitmandi.ac.in)
* [Lakshay arora](mailto:b16060@students.iitmandi.ac.in)

**4. Unified login using OpenID Connect**

* [Sahil Yadav](mailto:sahil_yadav@students.iitmandi.ac.in) (Overall Documentation)
* [Aman Khandelwal](mailto:amankh1999@gmail.com)
* [Swapnil Rustagi](mailto:b17104@students.iitmandi.ac.in)
* [Vipul Sharma](mailto:vsvipul555@gmail.com)

**5. Third party applications**

* [Aditya Singh](mailto:b16085@students.iitmandi.ac.in) (Overall Documentation)
* [Aaditya Arora](mailto:B17071@students.iitmandi.ac.in)
* [Akshat Malviya](mailto:ancientfuture1337@gmail.com)

## Summary

I hope that this document helps you get a better understanding of the various problems associated with the server and transfers the knowledge I gained while developing the server. I wish to see a robust and refined implementation before the end of this semester. Feel free to contact me, in case of doubts.

***All the best !!*** 
