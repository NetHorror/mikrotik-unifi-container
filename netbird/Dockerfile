# UniFi Network Application + NetBird client (separate image, built on top of the main UniFi image).
# NetBird binary and its entrypoint are taken from the official rootless image with COPY only,
# so the build needs no emulation and works for linux/amd64 and linux/arm64.
ARG UNIFI_VERSION=10.6.109
ARG NETBIRD_VERSION=0.83.1

FROM ghcr.io/nethorror/mikrotik-unifi-container:${UNIFI_VERSION} AS unifi
FROM ghcr.io/netbirdio/netbird:${NETBIRD_VERSION}-rootless AS netbird

FROM unifi
COPY --from=netbird /usr/local/bin/netbird /usr/local/bin/netbird
COPY --from=netbird /usr/local/bin/netbird-entrypoint.sh /usr/local/bin/netbird-entrypoint.sh
COPY unifi-nb-entrypoint.sh /usr/local/bin/unifi-nb-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/unifi-nb-entrypoint.sh"]
CMD ["unifi"]
