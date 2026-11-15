# UniFi Network Application + NetBird client (a variant of the main image, same repository).
# NetBird binary and its entrypoint are taken from the official rootless image with COPY only,
# so the build needs no emulation and works for linux/amd64 and linux/arm64.
ARG UNIFI_VERSION=10.6.111
ARG NETBIRD_VERSION=0.83.1

FROM ghcr.io/nethorror/mikrotik-unifi-container:${UNIFI_VERSION} AS unifi
FROM ghcr.io/netbirdio/netbird:${NETBIRD_VERSION}-rootless AS netbird

FROM unifi

# NetBird defaults that keep the client in userspace (netstack) mode, so it does not change
# the container's routes or DNS. Without these the kernel-mode client broke its own DNS on RouterOS.
ENV NB_ENABLE=1 \
    NB_USE_NETSTACK_MODE=true \
    NB_DISABLE_DNS=true \
    NB_DISABLE_CUSTOM_ROUTING=true \
    NB_USE_LEGACY_ROUTING=true \
    NB_ENABLE_NETSTACK_LOCAL_FORWARDING=true

COPY --from=netbird /usr/local/bin/netbird /usr/local/bin/netbird
COPY --from=netbird /usr/local/bin/netbird-entrypoint.sh /usr/local/bin/netbird-entrypoint.sh
COPY unifi-nb-entrypoint.sh /usr/local/bin/unifi-nb-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/unifi-nb-entrypoint.sh"]
CMD ["unifi"]
