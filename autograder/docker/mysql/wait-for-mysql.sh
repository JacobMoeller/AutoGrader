#!/bin/sh
# wait-for-mysql.sh

set -e
set -x

host="$1"
shift
cmd="$@"

while ! wget mysql:3306; do sleep 1 done

>&2 echo "Mysql is up - executing command"
exec $cmd