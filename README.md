# mikrotik-unifi-container

[![Publish Docker image](https://github.com/NetHorror/mikrotik-unifi-container/actions/workflows/docker.yml/badge.svg)](https://github.com/NetHorror/mikrotik-unifi-container/actions/workflows/docker.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE) ![Platform: amd64 | arm64](https://img.shields.io/badge/platform-amd64%20%7C%20arm64-informational) ![Registry: GHCR](https://img.shields.io/badge/registry-ghcr.io-brightgreen)

This repo contains a Dockerized version of [Ubiquiti Network's](https://www.ubnt.com/) UniFi
Network Application, built and published as a **multi-arch (`amd64`/`arm64`) image**.

**Primary target: MikroTik RouterOS on arm64.** This fork exists mainly so the UniFi
controller can run *inside* RouterOS 7's built-in `/container` feature on MikroTik's
arm64-based routers — no separate Docker host, no extra hardware. It's developed against
and tested on a **CCR2116-12G-4S+**, but should run on any arm64 RouterOS device with
enough RAM/storage (RB5009, CCR2004 series, hAP ax³, CHR, etc.). See
[Running on MikroTik RouterOS](#running-on-mikrotik-routeros-arm64) below for the full setup guide.

It also works exactly like any other Docker image on a regular Docker host
(Linux, macOS, Windows via WSL2) — the general instructions in this README
apply there unchanged.

**Why bother?** Using Docker/containers, you can stop worrying about version
hassles and update notices for
UniFi Network Application, Java, _or_ your OS.
A container wraps everything into one well-tested bundle.

To install, a couple lines on the command-line starts the container.
To upgrade, just stop the old container, and start up the new.
It's really that simple.

This project is a fork of [jacobalberty/unifi-docker](https://github.com/jacobalberty/unifi-docker),
rebased on a newer base OS and MongoDB version so it can track the **current stable**
UniFi Network Application release (only stable releases are ever used — no betas, no RCs).

**Latest Version:** The latest version is shown in the first line
of the [Current Information](#current-information) table on this page.

## Setting up, Running, Stopping, Upgrading

First, install Docker on the "Docker host" -
the machine that will run the Docker
and Unifi Controller software.
Use any of the guides on the internet to install on your Docker host.
For Windows, see the [Microsoft guide for installing Docker.](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-containers)

Then use the following steps to set up the directories
and start the Docker container running.

### Setting up directories

_One-time setup:_ create the `unifi` directory on the Docker host.
Within that directory, create two sub-directories: `data` and `log`.

```bash
cd # by default, use the home directory
mkdir -p unifi/data
mkdir -p unifi/log
```

_Note:_ By default, this README assumes you will use the home directory
on Linux, Unix, macOS.
If you create the directory elsewhere, read the
[Options section](#options-on-the-command-line)
below to adjust.)

### Running Unifi-in-Docker

Each time you want to start Unifi, use this command.
Each of the options is [described below.](#options-on-the-command-line)

```bash
docker run -d --init \
   --restart=unless-stopped \
   -p 8080:8080 -p 8443:8443 -p 3478:3478/udp -p 10001:10001/udp \
   -e SYSTEM_IP='<your docker host ip>' \
   -e TZ='Africa/Johannesburg' \
   -v ~/unifi:/unifi \
   --user unifi \
   --name unifi \
   ghcr.io/nethorror/mikrotik-unifi-container
```

In a minute or two, (after Unifi Controller starts up) you can go to
[https://docker-host-address:8443](https://docker-host-address:8443)
to complete configuration from the web (initial install) or resume using Unifi Controller.

**Important:** Two points to be aware of when you're setting up your Unifi Controller:

* When your browser initially connects to the link above, you will
see a warning about an untrusted certificate.
If you are _certain_ that you have typed the address of the
Docker host correctly, agree to the connection.
* See the note below about **Override "Inform Host" IP** so your
Unifi devices can "find" the Unifi Controller.
 
### Stopping Unifi-in-Docker

To change options, stop the Docker container then re-run the `docker run...` command
above with the new options.
_Note:_ The `docker rm unifi` command simply removes the "name" from the previous Docker image.
No time-consuming rebuild is required.

```bash
docker stop unifi
docker rm unifi
```
### Upgrading Unifi Controller

All the configuration and other files created by Unifi Controller
are stored on the Docker host's local disk (`~/unifi` by default.)
No information is retained within the container.
An upgrade to a new version of Unifi Controller simply retrieves a new Docker container,
which then re-uses the configuration from the local disk.
The upgrade process is:

1. **MAKE A BACKUP** on another computer, not the Docker host _(Always, every time...)_
2. Stop the current container (see above)
3. Enter `docker run...` with the newer container tag (see [Current Information](#current-information) section below.)

## Options on the Command Line

The options for the `docker run...` command are:

- `-d` - Detached mode: Unifi-in-Docker runs in the background
- `--init` - Recommended to ensure processes get reaped when they die
- `--restart=unless-stopped` - If the container should stop for some reason,
restart it unless you issue a `docker stop ...`
- `-p ...` - Set the ports to pass through to the container.
`-p 8080:8080 -p 8443:8443 -p 3478:3478/udp -p 10001:10001/udp`
is the minimal set for a working Unifi Controller. 
- `-e SYSTEM_IP=...` - Set ip address that devices will use to reach controller. See [Adopting
Access Points and Unifi Devices](#adopting-access-points-and-unifi-devices) for details.
- `-e TZ=...` - Set an environment variable named `TZ` with the desired time zone.
Find your time zone in this 
[list of timezones.](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- `-e ...` - See the [Environment Variables](#environment-variables)
section for more environment variables.
- `-v ...` - Bind the volume `~/unifi` on the Docker host
to the directory `/unifi`inside the container.
**These instructions assume you placed the "unifi" directory in your home directory.**
If you created the directory elsewhere, modify the `~/unifi` part of this option to match.
See the [Volumes](#volumes) discussion for other volumes used by Unifi Controller.
- `--user unifi` - Run as a non-root user. See the [Run as non-root User](#run-as-non-root-user) discussion below
- `ghcr.io/nethorror/mikrotik-unifi-container` - the name of the container to use.
The image is retrieved from [GitHub Container Registry.](https://github.com/NetHorror/mikrotik-unifi-container/pkgs/container/mikrotik-unifi-container)
The [Current Information](#current-information) section below discusses the versions/tags that are available.

## Current Information

The current tested version of unifi-docker is listed in the table below. 
You can choose the version of Unifi Controller in the `docker run ...` command.
In Docker terminology, these versions are specified by "tags".

For example, in this project the container named `ghcr.io/nethorror/mikrotik-unifi-container`
(with no "tag")
provides the most recent stable release.
The table below lists recent versions.

_Note:_ In Docker, specifying an image with no tag
(e.g., `ghcr.io/nethorror/mikrotik-unifi-container`) gets the "latest" tag.
This always tracks the most recent **stable** UniFi Network Application release —
this fork's auto-updater deliberately never picks up betas or release candidates.

| Tag                                                                                 | Description                                        | Changelog                                                                                                                        |
|--------------------------------------------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| [`latest` `10.6.101`](https://github.com/NetHorror/mikrotik-unifi-container/blob/main/Dockerfile) | Current Stable: Version 10.6.101 as of 2026-08-26 | [Change Log 10.6.101](https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4) |

See [`CHANGELOG.md`](CHANGELOG.md) for the full history of stable releases this fork has
picked up, auto-generated from UniFi's own release notes each time `update.yml` runs.

### multiarch

Images are built for `amd64` and `arm64` (`linux/arm64/v8`). Base OS is Ubuntu 26.04, with
Java 25.

MongoDB is pinned to **4.4.18** instead of the 6.0+ that the `unifi.deb` package normally
depends on. Official MongoDB ARM64 builds from 5.0 onward require ARMv8.1 LSE atomic
instructions, which older ARM64 cores — including the Cortex-A72 used in MikroTik's
CCR2116 — don't implement, so `mongod` crashes with an illegal instruction immediately.
4.4 is the last line built without that requirement, and is the same generation of
MongoDB the router's own stock (non-Docker) UniFi package has run for years without issue.
This is what makes it possible to run a *current* UniFi release on this class of hardware
at all — see [Running on MikroTik RouterOS](#running-on-mikrotik-routeros-arm64) below.

## Running on MikroTik RouterOS (arm64)

This is the main scenario this fork was built for: running the UniFi controller directly
inside a MikroTik router's own RouterOS 7 `/container` feature, on an arm64 board such as
the **CCR2116-12G-4S+**. No separate server, no separate Docker host — the router runs its
own controller for the APs/switches it's already routing traffic for.

**Before you start:**

- Requires **RouterOS 7.x** with the container package, on an **arm64** board.
- Requires attached storage for the container (internal NAND on most boards is far too
  small/slow for a MongoDB-backed app) — a USB drive or an NVMe/SATA disk on boards that
  support one. MikroTik recommends media capable of at least ~100 MB/s sequential and
  ~10K random IOPS; a slow USB stick will make the controller noticeably sluggish.
- Enabling container mode requires physical access to the router (a reset-button
  confirmation or a cold reboot), and on a device already in production this is disruptive.
  **Test this on a spare/test router first** — do not enable/experiment with this on a
  router that's actively serving users.
- Older arm64 cores (e.g. Cortex-A72, as in the CCR2116) lack the ARMv8.1 LSE atomic
  instructions that MongoDB 5.0+ requires — this fork pins MongoDB to 4.4.18 specifically
  so it still runs there (see [multiarch](#multiarch) above). If you're on a newer
  ARMv8.1+ board this doesn't affect you either way.

### 1. Enable container mode

```
/system/device-mode/update container=yes
```
RouterOS will prompt you to confirm by pressing the reset button (or power-cycling,
depending on model) within the next few minutes. `/system/device-mode/print` confirms
once it's active.

### 2. Prepare storage

Format/mount your attached disk (adjust `disk1` to whatever `/disk print` shows for yours),
then point the container subsystem at it:

```
/container/config/set registry-url=https://ghcr.io tmpdir=disk1/pull
```

### 3. Network the container

Simplest option — put the container on its own small subnet, NAT'd out through the router
(the container doesn't need to be directly on the office LAN for the web UI; it only needs
routed reachability, plus `SYSTEM_IP`/Inform-Host set correctly — see
[Adopting Access Points and Unifi Devices](#adopting-access-points-and-unifi-devices)):

```
/interface/bridge/add name=bridge-containers
/ip/address/add address=172.17.0.1/24 interface=bridge-containers

/interface/veth/add name=veth-unifi address=172.17.0.2/24 gateway=172.17.0.1
/interface/bridge/port/add bridge=bridge-containers interface=veth-unifi

/ip/firewall/nat/add chain=srcnat action=masquerade src-address=172.17.0.0/24
```

If you want the controller reachable directly on your existing LAN/VLAN bridge instead
(so `SYSTEM_IP` can just be the router's own LAN address), add `veth-unifi` as a port on
that bridge instead of a dedicated `bridge-containers`, and give it an address in that
subnet.

Forward the ports UniFi devices need to reach the controller (adjust for your topology —
not required if the container sits directly on the same bridge as your APs):

```
/ip/firewall/nat/add chain=dstnat action=dst-nat to-addresses=172.17.0.2 protocol=tcp dst-port=8443 in-interface=<wan-or-lan-if>
/ip/firewall/nat/add chain=dstnat action=dst-nat to-addresses=172.17.0.2 protocol=udp dst-port=3478,10001 in-interface=<wan-or-lan-if>
```

### 4. Environment variables and mounts

```
/container/envs/add list=unifi key=TZ value="Europe/Moscow"
/container/envs/add list=unifi key=SYSTEM_IP value=172.17.0.2
/container/envs/add list=unifi key=DISABLE_UOS_UPGRADE_NAG value=true

/container/mounts/add list=unifi src=disk1/unifi/data dst=/unifi/data
/container/mounts/add list=unifi src=disk1/unifi/log dst=/unifi/log
```

Give the envs/mounts lists (and the container itself, below) the same plain name —
`unifi` is used throughout this guide. Avoid names like `unifi-new`/`unifi-dev` for
anything you intend to keep long-term: they're fine for a temporary side-by-side
container while testing, but renaming a *production* container's own lists later
means recreating it (see [Renaming an existing container's lists](#renaming-an-existing-containers-lists)
below) — better to pick the final name up front. Also worth setting
`DISABLE_UOS_UPGRADE_NAG=true` from the start: without it, every login shows an
"Upgrade to UniFi OS Server" nag modal that doesn't apply to a self-hosted/sysvinit
install like this one (see [Environment Variables](#environment-variables) below).

### 5. Add and start the container

```
/container/add remote-image=ghcr.io/nethorror/mikrotik-unifi-container:latest \
    interface=veth-unifi root-dir=disk1/unifi/root \
    mountlists=unifi envlist=unifi \
    logging=yes start-on-boot=yes

/container/start [find remote-image~"mikrotik-unifi-container"]
```

Give it a couple of minutes on first start (it's initializing MongoDB + the controller),
then check `/container/print` and `/log/print where topics~"container"`. Browse to
`https://<container-or-router-address>:8443` to finish setup.

> **Note on exact command syntax:** MikroTik has renamed a couple of `/container/add`
> parameters across RouterOS versions (e.g. `mounts=`/`mountlists=`, `envlist=`/`envlists=`).
> Run `/container/add ?` on your actual RouterOS version to confirm the exact parameter
> names before pasting these commands. Confirmed on **RouterOS 7.24.2**: the plural
> forms are correct there — `mountlists=` (not `mounts=`) and `envlist=`.

#### Alternative: manual download instead of `remote-image=`

Every [GitHub Release](https://github.com/NetHorror/mikrotik-unifi-container/releases)
also carries a pre-built `mikrotik-unifi-container-<version>-arm64.tar.gz` asset —
the same image published to GHCR, already saved as a plain Docker tarball. Useful if you'd
rather not have the router pull directly from a registry (offline/air-gapped install, or
just a more predictable transfer):

```
# on any machine, then scp/transfer the .tar.gz to the router's storage
gunzip -c mikrotik-unifi-container-<version>-arm64.tar.gz > unifi.tar

/container/add file=disk1/unifi/unifi.tar \
    interface=veth-unifi root-dir=disk1/unifi/root \
    mountlists=unifi envlist=unifi \
    logging=yes start-on-boot=yes
```

Everything else (start, resource limits, updating) works the same either way — the
container object doesn't care whether it was created from `remote-image=` or `file=`.

### 6. Resource limits (recommended on a router)

A router's RAM is shared with routing itself — don't let the controller starve it. Set a
conservative JVM heap via the `unifi` envlist, e.g. `JVM_MAX_HEAP_SIZE=1024M`, then give
`memory-max` **meaningful headroom above that**, not the same value:

```
/container/set [find remote-image~"mikrotik-unifi-container"] memory-max=2684354560
```

`memory-max` is a hard cgroup-style limit — the container is OOM-killed the instant it's
hit, no matter how briefly. `JVM_MAX_HEAP_SIZE` only bounds the JVM heap; the JVM itself
needs extra room beyond that for native/off-heap memory, and `mongod` runs as a separate
process inside the same container with its own memory footprint on top. Setting
`memory-max` equal to (or too close to) `JVM_MAX_HEAP_SIZE` reliably OOM-kills the
container shortly after a healthy-looking start — confirmed in practice: with
`JVM_MAX_HEAP_SIZE=1024M`, `memory-max=1073741824` (1 GiB, i.e. equal to the heap) died
with `killed due to out of memory` in `/container/print`, while real steady-state usage
for this workload sat around 1.8–2.0 GiB. `memory-max=2684354560` (2.5 GiB) runs
healthy with comfortable headroom. If you have more
than a handful of APs, also set `LOTSOFDEVICES=true` (see
[Environment Variables](#environment-variables) below) — it trims a few JVM/UniFi settings
for exactly this kind of memory-constrained deployment.

### 7. Updating

Because RouterOS pulls the image by tag, updating is: stop the container, remove it,
`/container/add` again with the same `remote-image=...:latest` (RouterOS re-pulls), then
start it. Your data lives in the mounted `disk1/unifi/...` paths, so nothing is lost —
same principle as the generic [Upgrading](#upgrading-unifi-controller) section above.

### Renaming an existing container's lists

`/container/envs` and `/container/mounts` are separate named-list tables, not inline
parameters — several containers can share (or each have their own) `list=` name. If you
need to rename an already-running container's envlist/mountlist to tidy things up:

```
/container/stop [find name=unifi]
/container/envs/add list=unifi key=... value=...   ;# repeat for each key you need
/container/mounts/add list=unifi src=... dst=... mode=rw   ;# repeat for each mount
/container/envs/remove [find list=old-list-name]
/container/mounts/remove [find list=old-list-name]
/container/set [find name=unifi] envlist=unifi mountlists=unifi
/container/start [find name=unifi]
```

This is cheap — the container object itself doesn't need to be recreated, and none of
its extracted image layers are touched. **`root-dir` is different:** RouterOS stores a
container's extracted image layers directly under its `root-dir` path, so changing
`root-dir` (e.g. to rename `disk1/unifi-dev-root` → `disk1/unifi/root`) forces a full
re-pull and re-extraction of every image layer from the registry — confirmed in
practice (an ~18-layer, ~2 GB pull from scratch). The mounted data under `/unifi/data`
and `/unifi/log` is untouched either way (it's not under `root-dir`), but budget for the
re-download and don't do this on a whim on a slow link. To rename `root-dir`, you must
`/container/remove` the container object and `/container/add` it again with the new
`root-dir=` — same procedure as [Updating](#7-updating) above, just with a different
`root-dir=` value in the `/container/add` line.

## Adopting Access Points and Unifi Devices

For your Unifi devices to "find" the Unifi Controller running in Docker, you _MUST_ override the
Inform Host IP with the address of the Docker host computer.
(By default, the Docker container usually gets the internal address 172.17.x.x
while Unifi devices connect to the (external) address of the Docker host.)

There are a few ways to do this:

### By setting `SYSTEM_IP` environment variable
Set `SYSTEM_IP` environment variable on the container to the IP devices may use
to reach the controller, eg. your local address. This IP will be used as inform
host during adopting process and used for following communication.

### By overriding Inform Host on device level

* Find **UniFi Devices -> Device Updates and Settings -> Device Settings -> Inform Host Override** in the UniFi Controller web GUI (it's in the middle of that page).
* Check the "Enable" box, and enter the IP address of the Docker host machine. 
* Save settings in Unifi Controller
* Restart UniFi-in-Docker container with `docker stop ...` and `docker run ...` commands.

_Hint: Port 10001 should be forwareded to make it work._

### Other

See [Side Projects](https://github.com/NetHorror/mikrotik-unifi-container/blob/main/Side-Projects.md#other-techniques-for-adoption) for
other techniques to get Unifi devices to adopt your
new Unifi Controller.

## Volumes

Unifi looks for the `/unifi` directory (within the container)
for its special purpose subdirectories:

* `/unifi/data` This contains your UniFi configuration data. (formerly: `/var/lib/unifi`) 

* `/unifi/log` This contains UniFi log files (formerly: `/var/log/unifi`)

* `/unifi/cert` Place custom SSL certs in this directory. 
For more information regarding the naming of the certificates,
see [Certificate Support](#certificate-support). (formerly: `/var/cert/unifi`)

* `/unifi/init.d`
You can place scripts you want to launch every time the container starts in here

* `/var/run/unifi` 
Run information, in general you will not need to touch this volume.
It is there to ensure UniFi has a place to write its PID files

### Legacy Volumes

These are no longer actually volumes, rather they exist for legacy compatibility.
You are urged to move to the new volumes ASAP.

* `/var/lib/unifi` New name: `/unifi/data`
* `/var/log/unifi` New name: `/unifi/log`

## Environment Variables:

You can pass in environment variables using the `-e` option when you invoke `docker run...`
See the `TZ` in the example above.
Other environment variables:

* `SYSTEM_IP`
This is the IP address the controller will use for inform host during adoption.
This should match IP address of the host, reachable from devices (eg. local, not
docker address). If not set, internal docker IP will be used and devices will
most likely to adopt.

* `UNIFI_HTTP_PORT`
This is the HTTP port used by the Web interface. Browsers will be redirected to the `UNIFI_HTTPS_PORT`.
**Default: 8080**

* `UNIFI_HTTPS_PORT`
This is the HTTPS port used by the Web interface.
**Default: 8443** 

* `PORTAL_HTTP_PORT`
Port used for HTTP portal redirection.
**Default: 80** 

* `PORTAL_HTTPS_PORT`
Port used for HTTPS portal redirection.
**Default: 8843** 

* `UNIFI_STDOUT`
Controller outputs logs to stdout in addition to server.log
**Default: unset**

* `SMTP_STARTTLS_ENABLED`
Disable StartTLS for SMTP. Required when the SMTP server do not support encryption
**Default: unset** 

* `TZ`
TimeZone. (i.e America/Chicago)

* `JVM_MAX_THREAD_STACK_SIZE`
Used to set max thread stack size for the JVM
Example:

   ```
   --env JVM_MAX_THREAD_STACK_SIZE=1280k
   ```

   as a fix for [https://community.ubnt.com/t5/UniFi-Routing-Switching/IMPORTANT-Debian-Ubuntu-users-MUST-READ-Updated-06-21/m-p/1968251#M48264](https://community.ubnt.com/t5/UniFi-Routing-Switching/IMPORTANT-Debian-Ubuntu-users-MUST-READ-Updated-06-21/m-p/1968251#M48264)

* `LOTSOFDEVICES`
Enable this with `true` if you run a system with a lot of devices
and/or with a low powered system (like a Raspberry Pi).
This makes a few adjustments to try and improve performance: 

   * enable unifi.G1GC.enabled
   * set unifi.xms to JVM\_INIT\_HEAP\_SIZE
   * set unifi.xmx to JVM\_MAX\_HEAP\_SIZE
   * enable unifi.db.nojournal
   * set unifi.dg.extraargs to --quiet

   See [the Unifi support site](https://help.ui.com/hc/en-us/articles/115005159588-UniFi-How-to-Tune-the-Network-Application-for-High-Number-of-UniFi-Devices)
for an explanation of some of those options.
**Default: unset** 

* `JVM_EXTRA_OPTS`
Used to start the JVM with additional arguments.
**Default: unset** 

* `JVM_INIT_HEAP_SIZE`
Set the starting size of the javascript engine for example: `1024M`
**Default: unset** 

* `JVM_MAX_HEAP_SIZE`
Java Virtual Machine (JVM) allocates available memory. 
For larger installations a larger value is recommended. For memory constrained system this value can be lowered. 
**Default: 1024M** 

* `DISABLE_UOS_UPGRADE_NAG`
Self-hosted installs are shown an "Upgrade to UniFi OS Server" modal after login. If you intend
to keep running the self-hosted/sysvinit controller (e.g. on a MikroTik router), set this to
`true` to have the entrypoint inject a small script into the webapp's `index.html` on startup
that clicks the controller's own **Remind Me Later** button whenever that dialog appears — no
UniFi files are modified beyond that one injected `<script>` tag, and it is a silent no-op if
the dialog's markup ever changes. See [`functions`](functions)'s `patch_uos_nag()`.
**Default: unset**

## Exposed Ports

The Unifi-in-Docker container exposes the following ports.
A minimal Unifi Controller installation requires you
expose the first four with the `-p ...` option.

* 8080/tcp - Device command/control 
* 8443/tcp - Web interface + API 
* 3478/udp - STUN service 
* 10001/udp - Device discovery
* 8843/tcp - HTTPS portal _(optional)_
* 8880/tcp - HTTP portal _(optional)_
* 6789/tcp - Speed Test _(optional)_

See [UniFi - Ports Used](https://help.ubnt.com/hc/en-us/articles/218506997-UniFi-Ports-Used) for more information.

## Run as non-root User

The default container runs Unifi Controller as root.
The recommended `docker run...` command above starts
Unifi Controller so the image runs as `unifi` (non-root)
user with the uid/gid 999/999.
You can also set your data and logs directories to be
owned by the proper gid.

_Note:_ When you run as a non-root user,
you will not be able to bind to lower ports by default.
(This would not necessary if you are using the default ports.)
If you must do this, also pass the 
`--sysctl net.ipv4.ip_unprivileged_port_start=0`
option on the `docker run...` to bind to whatever port you wish.

## Certificate Support

To use custom SSL certs, you must map a volume with the certs to `/unifi/cert`

They should be named:

```shell
cert.pem  # The Certificate
privkey.pem # Private key for the cert
chain.pem # full cert chain
```

If your certificate or private key have different names, you can set the environment variables `CERTNAME` and `CERT_PRIVATE_NAME` to the name of your certificate/private key, e.g. `CERTNAME=my-cert.pem` and `CERT_PRIVATE_NAME=my-privkey.pem`.

For letsencrypt certs, we'll autodetect that and add the needed Identrust X3 CA Cert automatically. In case your letsencrypt cert is already the chained certificate, you can set the `CERT_IS_CHAIN` environment variable to `true`, e.g. `CERT_IS_CHAIN=true`. This option also works together with a custom `CERTNAME`.

### Certificates Using Elliptic Curve Algorithms

If your certs use elliptic curve algorithms, which currently seems to be the default with letsencrypt certs, you might additionally have to set the `UNIFI_ECC_CERT` environment variable to `true`, otherwise clients will fail to establish a secure connection. For example an attempt with `curl` will show:

```shell
% curl -vvv https://my.server.com:8443
curl: (35) error:1404B410:SSL routines:ST_CONNECT:sslv3 alert handshake failure
```

You can check your certificate for this with the following command:

```shell
% openssl x509 -text < cert.pem | grep 'Public Key Algorithm'
         Public Key Algorithm: id-ecPublicKey
```

## License

MIT — see [LICENSE](LICENSE).

If the output contains `id-ec` as shown in the example, then your certificate might be affected.

## Additional Information

This document describes everything you need to get Unifi-in-Docker running.
The [Side Projects and Background Info](https://github.com/NetHorror/mikrotik-unifi-container/blob/main/Side-Projects.md) page
provides more about what we've learned while developing Unifi-in-Docker.

## TODO

This list is empty for now, please [add your suggestions](https://github.com/NetHorror/mikrotik-unifi-container/issues).
