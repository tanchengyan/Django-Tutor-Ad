#!/bin/bash
# wait-for-it.sh
# Wait until the service at the given host and port is available.

host="$1"
port="$2"
shift 2
cmd="$@"

while ! nc -z "$host" "$port"; do
  echo "Waiting for $host:$port..."
  sleep 1
done

exec $cmd
