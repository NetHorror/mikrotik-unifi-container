#!/usr/bin/env bash

# fail on error
set -e

# Retry 5 times with a wait of 10 seconds between each retry
tryfail() {
    for i in $(seq 1 5);
        do [ $i -gt 1 ] && sleep 10; $* && s=0 && break || s=$?; done;
    (exit $s)
}

# Try multiple keyservers in case of failure
addKey() {
    for server in $(shuf -e ha.pool.sks-keyservers.net \
        hkp://p80.pool.sks-keyservers.net:80 \
        keyserver.ubuntu.com \
        hkp://keyserver.ubuntu.com:80 \
        pgp.mit.edu) ; do \
        if apt-key adv --keyserver "$server" --recv "$1"; then
            exit 0
        fi
    done
    return 1
}

if [ "x${1}" == "x" ]; then
    echo please pass PKGURL as an environment variable
    exit 0
fi

apt-get update
apt-get install -qy --no-install-recommends \
    binutils \
    ca-certificates \
    curl \
    dirmngr \
    gpg \
    gpg-agent \
    libcap2-bin \
    logrotate \
    openjdk-25-jre-headless \
    procps \
    software-properties-common \
    tzdata

# UniFi 10.1+ requires MongoDB 6.0+ (checked by the .deb package's own dependency resolution).
# mongodb-org-server isn't published for the resolute (26.04) codename yet, only client tools —
# the noble (24.04) arm64/amd64 packages install and run fine on 26.04 (glibc-compatible).
curl -Ls https://www.mongodb.org/static/pgp/server-8.0.asc | gpg --dearmor -o /usr/share/keyrings/mongo.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongo.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list
apt-get update
apt-get install -qy mongodb-org-server

echo 'deb https://www.ui.com/downloads/unifi/debian stable ubiquiti' | tee /etc/apt/sources.list.d/100-ubnt-unifi.list
tryfail apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 06E85760C0A52C50

if [ -d "/usr/local/docker/pre_build/$(dpkg --print-architecture)" ]; then
    find "/usr/local/docker/pre_build/$(dpkg --print-architecture)" -type f -exec '{}' \;
fi

curl -L -o ./unifi.deb "${1}"
apt -qy install ./unifi.deb
rm -f ./unifi.deb
chown -R unifi:unifi /usr/lib/unifi
rm -rf /var/lib/apt/lists/*

rm -rf ${ODATADIR} ${OLOGDIR} ${ORUNDIR} ${BASEDIR}/data ${BASEDIR}/run ${BASEDIR}/logs
mkdir -p ${DATADIR} ${LOGDIR} ${RUNDIR}
ln -s ${DATADIR} ${BASEDIR}/data
ln -s ${RUNDIR} ${BASEDIR}/run
ln -s ${LOGDIR} ${BASEDIR}/logs
ln -s ${DATADIR} ${ODATADIR}
ln -s ${LOGDIR} ${OLOGDIR}
ln -s ${RUNDIR} ${ORUNDIR}
mkdir -p /var/cert ${CERTDIR}
ln -s ${CERTDIR} /var/cert/unifi

rm -rf "${0}"
