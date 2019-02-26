Welcome to the Team Deneb README for the AUTOGRADER Assignment.

#############
# TO SET-UP #
#############
(Source: https://cs-devel.potsdam.edu/drbcladd/cis405)
(Note: You can specify a different DJANGO_PORT value; '8888' is by example.)

Set-up container with following command:
$ HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 \
$ docker-compose build

NOTICE: If you exclude the shell var args, the Dockerfile config file is not
properly populated and an incorrect image may be created. If so, remove with:
$ docker rmi <IMAGE_ID>

You should see new repository/images created when using:
$ docker images

These include the following: deneb_django, python, deneb_db, mysql.

-----
Launch the containers with command:
$ HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 \
$ docker-compose up &

This will launch a dialogue for the mysql; in your browser,
navigate to "localhost:8888/" to see the live site.

Exiting with ^C will stop the running containers. You can then see the new
repository/images created when using:
$ docker ps -a

These include the following: django_1000_1000, mysql_1000_1000.


##################
# DJANGO PROJECT #
##################
Django commands are prefaced with shell vars and the docker command, e.g.

$ HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 \
$ docker-compose run django python3 autograder/manage.py makemigrations

##############
#  TO CLOSE  #
##############
Run docker with command:

$ HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888 \
$ docker-compose down

This should stop and remove the two running docker containers.
