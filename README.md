# READ ME

Welcome to the Team Deneb README for the **AUTOGRADER** assignment.

#### Installation:
Requires [Docker CE](https://docs.docker.com/install/) to run.

- If you are using Linux and running with *sudo*, please configure Linux to [run Docker as a non-root user](https://docs.docker.com/install/linux/linux-postinstall/). (Sudo does not resolve ${PWD} correctly and it will have issues creating the mount point for Django.) 
- If you are using a Windows machine, you may need to [upgrade to Education](https://potsdam.onthehub.com/) to run Docker for Windows.

After configuring Docker, build the image with docker-compose:
```
cd autograder
docker-compose build
```
> See wiki for modified commands for set-up in lab or production mode.

This should create images (viewed with `docker images`), *django:dev* and *mysql:dev*.

#### Superuser Credentials (on the demo machine):
>*user*=admin1, *password*=password

#### To Run:
After building, for development mode:
```
docker-compose up -d
```
> The `-d` flag runs in detached mode so you can use the same terminal and have the containers running. If you wish to see the server output (for initial set-up or if you aren't sure if something is working), remove the flag.

In Windows you will need to run `docker-compose up db` first, most likely, since the django container can build before mysql finishes.

This will create running containers (view with `docker ps`) *django_dev* and *mysql_dev*.

Verify the server is running correctly by visiting your [web browser](127.0.0.1:8080) at the mapped port specified --such as when running with an override, as in DJANGO_PORT for the lab implementation -- otherwise usually 8080.

You can start and stop the running containers with `docker-compose stop` and `docker-compose start`.

To remove the running or stopped containers, use:
```
docker-compose down
```

> See wiki for further details on running Django commands, or accessing mysql and the shell within the containers.

#### Running Tests
Workaround: `docker-compose run django manage.py test` currently runs with sqlite3 by default.

(This is quick and not ideal fix, to be extracted into a different settings file.)

If you'd like to run tests with mysql, before merging code to the main repo, it requires extra configuration on each new build of the mysql image. Follow the steps below:

```
docker-compose exec db bash
```

This will open a shell in the django container. You can then access the mysql client with the following:

```
root@<containerid>:/# mysql -u root -p 
# enter the dev password ('django') to connect to mysql
mysql> GRANT ALL PRIVILEGES ON test_djangodocker_db.* TO 'django'@'%';
mysql> exit;
root@<containerid>:/# exit
```

`docker-compose run django python manage.py test` should now work.
