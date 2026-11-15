#!/bin/sh
# Start NetBird client in background (state in /unifi/data/netbird, persisted with UniFi data), then hand over to UniFi entrypoint.
set -e
mkdir -p /unifi/data/netbird /var/log/netbird
if [ ! -L /var/lib/netbird ]; then rm -rf /var/lib/netbird; ln -s /unifi/data/netbird /var/lib/netbird; fi
if [ "${NB_ENABLE:-1}" = "1" ]; then
  /usr/local/bin/netbird-entrypoint.sh >>/var/log/netbird/entrypoint.log 2>&1 &
fi
exec /usr/local/bin/docker-entrypoint.sh "$@"
