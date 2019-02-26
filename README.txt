Welcome to the Team Deneb README for the AUTOGRADER Assignment.

################################################################################
# DOCKER SET-UP (src: https://cs-devel.potsdam.edu/drbcladd/cis405)
################################################################################

docker-compose.yml requires variables HOST_USER_ID, HOST_GROUP_ID, DJANGO_PORT
to run. These are specified before running any docker-compose commands.

Therefore all commands using docker-compose must be preceded with the following:
    $ HOST_USER_ID=`id --user` HOST_GROUP_ID=`id --group` DJANGO_PORT=8888

To avoid this, you can export these as environmental variables, which
docker-compose.yml will read. See SETUP.txt for further details as needed.

-----

NOTE: Make sure you have the .env file needed first in the same directory as
docker-compose.yml. (You can check that it's working with `docker-compose
config`.)

To build the images, run:
    $ docker-compose build

Launch the containers with command:
    $ docker-compose up db &

Wait for the install to complete. Then exit and execute:
    $ docker-compose up -d
(The optional -d flag will run the containers in the background.)

You should see new repository/images created when using:
    $ docker images

(These include the following: deneb_django, python, deneb_db, mysql.)

You can then see the new repository/images created when using:
    $ docker ps -a

(These include the following: django_####_####, mysql_####_####.)


################################################################################
# WORKING IN DJANGO
################################################################################

Django commands are prefaced with the docker-compose run command, e.g.
    $ docker-compose run django python3 autograder/manage.py makemigrations

################################################################################
# DOCKER CLOSE
################################################################################

Run docker with command:
    $ docker-compose down

This should stop and remove the two running docker containers
(e.g. django_####_####, mysql_####_####).
