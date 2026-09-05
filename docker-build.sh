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

# EXPERIMENTAL (branch experiment/mongo44-cortex-a72): pinned to MongoDB 4.4 instead of the
# usual 6.0+ requirement. Official MongoDB ARM64 builds from 5.0 onward are compiled requiring
# ARMv8.1 LSE atomics, which older ARM64 cores (e.g. Cortex-A72, as used in MikroTik CCR2116)
# don't implement — mongod hits SIGILL immediately. 4.4 is the last line built without that
# requirement. See project memory unifi-container-arm64-mongodb-incompatibility for details.
curl -Ls https://www.mongodb.org/static/pgp/server-4.4.asc | gpg --dearmor -o /usr/share/keyrings/mongo.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongo.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
apt-get update
apt-get install -qy mongodb-org-server=4.4.18 mongodb-org-shell=4.4.18

echo 'deb [signed-by=/usr/share/keyrings/unifi.gpg] https://www.ui.com/downloads/unifi/debian stable ubiquiti' | tee /etc/apt/sources.list.d/100-ubnt-unifi.list
tryfail curl -fsSL https://dl.ui.com/unifi/unifi-repo.gpg -o /tmp/unifi-repo.gpg
gpg --dearmor -o /usr/share/keyrings/unifi.gpg /tmp/unifi-repo.gpg
rm -f /tmp/unifi-repo.gpg

if [ -d "/usr/local/docker/pre_build/$(dpkg --print-architecture)" ]; then
    find "/usr/local/docker/pre_build/$(dpkg --print-architecture)" -type f -exec '{}' \;
fi

curl -L -o ./unifi.deb "${1}"
# unifi.deb declares a hard Depends on mongodb-org (>=6.0) at the packaging-metadata level;
# --force-depends skips only that check (postinst still runs normally). Do NOT follow this with
# `apt-get install -f` — it would "fix" the unmet dependency by pulling MongoDB 6+ back in.
dpkg -i --force-depends ./unifi.deb
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
