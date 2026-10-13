# Changelog

UniFi Network Application release notes, recorded automatically as this
fork's auto-updater (`update.yml`) picks up each new **stable** release
(no betas, no RCs). See [community.ui.com/releases](https://community.ui.com/releases)
for the canonical/official source.

## [11.0.83] - 2026-10-12

[Official release notes](https://community.ui.com/releases/UniFi-Network-Application-11-0-83/d6940379-cd5a-4e61-8596-7e22d647a4ea)

### Overview
UniFi Network Application 11.0.83 requires UniFi OS 6.0 or newer. The upgrade may take up to 20 minutes.

**Improved Application Stability**

- Migrated the application database to PostgreSQL.
- Introduced a new, more scalable statistics engine.
- Existing statistics history is cleared and starts fresh after the update.
- Removed USG gateway support.
- Network Application 10.6 is the last version supporting USG.
- Removed Network Application Server support.
- Upgrade to UniFi OS Server, the official replacement.
- All sites are automatically migrated to the Zone-Based Firewall.

**Live Flows**

View active flows on the gateway while they are in progress and terminate them on demand.

- Supported on UDM-Pro, UDM-SE, UDM-Pro-Max, UDW, EFG, EF-Core, UDM-Beast, UCG-Fiber, UCG-Max, UXG-Max, UXG-Fiber, UXG-Pro, and UXG-Enterprise.
- Requires UniFi OS 6.0.10 or newer.

**External Network Lists**

Added an External source option to Network Lists to import domain or IP lists from external sources.

- Requires UniFi OS 6.0.10 or newer.

**WiFi Uplink**

Connect your gateway to a nearby WiFi network to use as an internet backup.

- Supported on UDR-7, UDR-5G-Max, Express 7, and UCG-Industrial.
- Requires UniFi OS 6.0.10 or newer.

**Matter Thread Device Monitoring**

Commission Matter Thread devices to monitor their status and connectivity.

- Requires UniFi OS Gateway 6.0.10 or newer.
- mDNS must be enabled.
- IPv6 must be enabled on the network hosting the Thread Border Routers.

### Improvements

- Added an option to generate client device icons.
- Added a new client connection alarm.
- Added Battery Self-Test for UPS devices.
- Added bulk editing for clients, including removal and blocking.
- Added a country selection dropdown to Channel Plan.
- Added support for Subnet Overlap System Logs.
- Added Time Machine to the Topology page.
- Added IPIP WAN support for Japanese IPv4 over IPv6 services.
- Added a Packet Capture option to the Radio side panel.
- Added Remote Power Cycle support for UPS 2U Pro.
- Added a USB-C option for EAV-Bridge.
- Added SD-WAN Policies for destination- and performance-based routing across selected spokes, with configurable hub selection, WAN priorities, and tunnel health thresholds for packet loss, latency, and jitter.
- Requires Site Manager 5.10.2 or newer.
- Improved traffic animations in Topology.
- Improved guest authorization latency through the API.
- Improved switch stacking stability.
- Improved the 802.1X and RADIUS settings user experience.
- Improved Channel AI.
- Improved IGMP Snooping settings validation.
- Improved the firmware Revert experience with a feedback form.
- Improved the Deep Inspection settings user experience.
- Improved Port Manager default columns and filters.
- Improved Time Machine loading performance on large sites.
- Improved the VPN settings user experience.
- Improved availability detection for Virtual Network Override.
- Improved the Routing settings user experience.
- Increased the VLAN limit when no gateway is adopted.
- Time Machine now remembers whether it was open or closed.
- Updated Site-to-Site OpenVPN encryption options with AES-192-CBC and AES-128-CBC support.
- Removed System Settings when using Site Manager.
- Language and Time settings are now managed through the Site Manager header and synchronized across UniFi applications.
- Country selection is now available in WiFi Channel settings.
- NTP settings are now available in the Site Gateway side panel.
- The Professional Installer section has been removed, with Extend 6 GHz Non-PSC Channel Use now available in Global WiFi settings.
- System Settings remain available in the Local Portal for Language and Time configuration.

**Flows**

- Added Firewall Policy names for Allow actions in Traffic Flows.
- Requires UniFi OS 6.0.10 or newer.
- Added Application Column/Filter in Traffic Flows.
- Requires UniFi OS 6.0.10 or newer.
- Added a Flows Logging option to Firewall Policies.
- Improved Traffic Flows reporting.
- Local DNS queries are now identified as DNS in Traffic Flows.

### Bugfixes

- Fixed an issue where Channel AI could suggest channels unavailable to outdoor access points.
- Fixed an issue where disabling the display on a meshed Express 7 could fail.
- Fixed a rare issue where Alarm Manager emails could be sent unexpectedly.
- Fixed an issue where Firewall Policies referencing SD-WAN hub-spoke tunnels could stop working after WAN interface changes.
- Fixed missing System Log events for unauthorized Hotspot guests.
- Fixed a rare issue where hostname and IPv6 address information could fluctuate.
- Fixed an issue where an incorrect parent device could be offered when adopting a UniFi Device Bridge.
- Fixed a rare issue where leaving a web session open for an extended period could cause the browser to crash.
- Fixed an issue where L2TP VPN appeared as a Content Filtering source option.
- Fixed a rare issue where devices could appear twice in the Devices list.
- Fixed a rare issue where guest voucher authorization could report success without providing internet access.
- Fixed a rare issue where Hotspot guests could be required to reauthorize when roaming between access points.
- Fixed a rare issue where SD-WAN tunnels could fail to establish between sites.
- Fixed an issue where Isolated Networks did not isolate traffic to the VPN zone.
- Fixed a rare issue where IPv6 IPS threats did not appear in Traffic Flows.
- Fixed an issue where Site Manager could fail to display statistics for multi-site hosts with a large number of sites.

### Additional information

**Self-Hosted UniFi Deployments**

For self-hosted deployments, we recommend upgrading to [UniFi OS Server](https://ui.com/download/releases/unifi-os-server). It provides the full UniFi OS Platform experience, ensuring you receive the latest features, improvements, and integrations.

UniFi Cloud Gateways remain our recommended solution for deployments that do not require self-hosting.

## [10.6.106] - 2026-09-10

[Official release notes](https://community.ui.com/releases/UniFi-Network-Application-10-6-106/f206c01d-3f73-471b-b4a5-2da48f157ea6)

### Improvements

- Added MLO STR Mesh support for WiFi 7 Access Points.
- Requires UAP 8.8 or newer.
- Improved Application stability.
- Improved Observability resiliency.

### Bugfixes

- Fixed a rare issue where WiFi clients using MLO could display an incorrect IP address.
- Fixed an issue where WiFi Broadcast could fail on UDR7 and UDR-5G when using MLO STR.
- Fixed inaccurate Port Lock events in Port Manager Time Machine.
- Fixed an issue where Site Admins could fail to open Settings in multi-site deployments.
- Fixed a rare issue where network configuration changes could fail to save.
- Fixed a rare issue where the Client Session widget was not displayed in the Client panel.

### Additional information

**UniFi OS Server**

Going forward, we recommend users upgrade to [UniFi OS Server](https://ui.com/download/releases/unifi-os-server) for all self-hosted deployments. It provides the full UniFi OS Platform experience, ensuring you receive the latest features, improvements, and integrations.

**UniFi Network Native Application for UniFi OS**

Compatible with UDM, UDR, UDR7, UDR 5G Max, Express, Express 7, and UCG models (Ultra, Max, Fiber, and Industrial) on UniFi OS 3.1.6 or later. UDM-Pro, UDM-SE, and UDW have been using it since UniFi OS 5.1.5.

- The UniFi OS update utilizes the application version compatible with your console.
- The manual update process via SSH requires a compatible package. Incompatible packages will be rejected on installation.
- Older UniFi OS versions (prior to UniFi OS 3.1.6) on the UDM and UDR continue to utilize the standard UniFi Network Application for UniFi OS.

## [10.6.101] - 2026-08-26

[Official release notes](https://community.ui.com/releases/UniFi-Network-Application-10-6-101/05283624-0980-4dd7-b8d6-9fa5c4e28da4)

### Overview
UniFi Network Application 10.6.101 adds Drift Inspector, Topology Spotlight, and expanded Safe Ops features, along with the improvements and bug fixes listed below.

**Added Drift Inspector to Blueprints in Site Manager**

- Make local changes to sites using Blueprint orchestrations, with a clear view of configuration drift and an easy way to resolve it.

**Added Topology Spotlight**

- Quickly highlight and filter selected devices for easier navigation and troubleshooting in large topologies.

**Improved SafeOps features**

- Expanded Test & Confirm support to VPN and Management networks.
- Added Nightly Channel AI Optimization with configurable radio selection and an improved optimization algorithm.

**Improved Time Machine Experience**

- Added Time Machine for Radios to review radio usage metrics, configuration changes, and radio events from the past 24 hours.
- Expanded Port Manager Time Machine to All Ports, making it easier to identify and troubleshoot problematic network segments.

### Improvements

- Added a flapping devices filter to Port Manager Time Machine for clients with frequent reconnections.
- Added the Reduced Firewall State Timeouts profile for EFG, EF-Core, and UXG-Enterprise.
- Added a confirmation prompt when updating all devices from the Devices filter side panel.
- Added sorting to Network Lists and descriptions on hover.
- Added column sorting to tables in Settings Overview.
- Added an Allow Empty Password option for RADIUS MAC Authentication.
- Added the ability to disable the LCM screen on meshed UX7 devices.
- Added Sort by Topology to the Devices page.
- Added a notice for unsupported devices in Test & Confirm settings.
- Added a disabled port filter to Port Manager.
- Added an Additional Labels option to Infrastructure Topology.
- Added a warning in Topology when Sonos devices with mixed wired and wireless connections are detected.
- Added validation to prevent OpenVPN Server and Site-to-Site VPNs from using the same UDP port.
- Added a Spotlight selection option in Topology.
- Added the ability to disable insecure OpenVPN compression.
- Added Multicast Suppressor support.
- Requires UAP 8.8 or newer.
- Added a Lock Port to UniFi Device option to Port Manager.
- Requires Switch firmware version 7.6 or newer.
- Added support for adopting multiple U5G devices on the same site over LAN.
- Added support for using Domain Network Lists in QoS Policies.
- Added support for customizing WAN interfaces used for Automatic Speed Tests.
- Added Bulk Update Management to the Devices page.
- Improved Device Auto-Recovery stability.
- Improved Data Plane Protection resiliency.
- Improved Traffic Activity Statistics accuracy.
- Improved the Observability section.
- Improved the device revert experience by allowing easy reversion for all devices with the same Device model and version.
- Improved DHCP Options validation.
- Improved the Dynamic DNS settings user experience.
- Improved RADIUS settings validation.
- Improved Virtual Network management in Topology.
- Improved the AV Manager user experience.
- Improved Honeypot validation.
- Improved the display of unstable links in Infrastructure Topology.
- Improved network subnet validation against static route destinations.
- Improved Port Profiles management in Port Manager.
- Improved Port Manager by automatically opening Time Machine.
- Improved the Device Update confirmation screen by showing the number of connected devices that might be interrupted.
- Improved OpenVPN server configuration files by removing periodic TLS key renegotiation.
- Requires UniFi OS 5.1 or newer
- Improved VPN Server settings validation.
- Improved application startup resiliency.
- Improved the Port Forwarding table user experience.
- Removed the Network Override option for WAN-adopted U5G devices.
- Removed the STP Edge note from Port Manager when Auto STP Edge is disabled.
- Separated the Reset Stats and Clear Last Seen Device actions in Port Manager.
- Enabled DHCP Guarding by default on new networks.

### Bugfixes

- Fixed an issue where client devices with a configured Power Source could be automatically enrolled in Device Auto-Recovery.
- Fixed an issue where the AP Stopped Mesh system log could be generated repeatedly after an AP switched to a wired uplink.
- Fixed an issue where the High Traffic alarm incorrectly reported wireless client downloads as uploads.
- Fixed an issue where SD-WAN Mesh VPN tunnels could remain after the configuration was removed.
- Fixed an issue where the client count in the WiFi Broadcast overview was incorrect when MLO clients were connected.
- Fixed an issue where filter counters could flicker on the Connectivity page in rare cases.
- Fixed an issue where the hostname was not set correctly for a UX7 connected via mesh.
- Fixed an issue where a custom APN could be lost after moving a SIM between slots on a U5G.
- Fixed an issue where the UX7 did not display connected wireless clients in the Devices list.
- Fixed a rare issue where opening Client Observability could impact system stability.
- Fixed an issue where DAS/DAC (CoA) was unavailable when using Open security with RADIUS MAC Authentication.
- Fixed an issue where MC-LAG configurations could be lost after restoring a backup.
- Fixed an issue where the Connectivity page was missing some roaming events.
- Fixed a rare issue where adopting an LTE device could cause a gateway configuration error.

### Additional information

**UniFi OS Server**

Going forward, we recommend users upgrade to [UniFi OS Server](https://ui.com/download/releases/unifi-os-server) for all self-hosted deployments. It provides the full UniFi OS Platform experience, ensuring you receive the latest features, improvements, and integrations.

**UniFi Network Native Application for UniFi OS**

Compatible with UDM, UDR, UDR7, UDR 5G Max, Express, Express 7, and UCG models (Ultra, Max, Fiber, and Industrial) on UniFi OS 3.1.6 or later. UDM-Pro, UDM-SE, and UDW have been using it since UniFi OS 5.1.5.

- The UniFi OS update utilizes the application version compatible with your console.
- The manual update process via SSH requires a compatible package. Incompatible packages will be rejected on installation.
- Older UniFi OS versions (prior to UniFi OS 3.1.6) on the UDM and UDR continue to utilize the standard UniFi Network Application for UniFi OS.

## [10.0] - Genesis: what changed since 9.x

> **Note:** this fork's changelog only starts tracking releases from UniFi Network 10.x
> onward. This entry is a **synthesized summary** (not an official verbatim UniFi
> announcement) compiled from Ubiquiti's own "Introducing UniFi Network 10.x" blog posts
> and public release notes, to give new readers context for what changed relative to 9.x.
> For the authoritative, version-by-version detail see the linked posts below.

UniFi Network 10 was a major version bump that, across its 10.0-10.6 minor releases,
reworked several core parts of the product:

- **Legacy Web UI removed.** The old (pre-redesign) web interface was fully removed as of
  10.0.140/10.0.160 — the modern UI is now the only option for self-hosted installs.
- **Redesigned High Availability setup** (10.1) that lowers the barrier to true redundancy,
  plus WiFi Doctor for automatic detection/resolution of common connectivity problems, and
  the first Early Access of UniFi Site Manager for centralized, multi-site "Fabric"
  management. ([Introducing UniFi Network 10.1](https://blog.ui.com/article/introducing-unifi-network-10-1))
- **Time Machine and Infrastructure Topology** (10.2): historical, timeline-style visibility
  into switch port state changes, a digital-twin rack view for infrastructure, and support
  for Enhanced Open (OWE) WiFi for better privacy/anti-deauth protection.
  ([Introducing UniFi Network 10.2](https://blog.ui.com/article/introducing-unifi-network-10-2))
- **eBGP and expanded IPv6** (10.4): enterprise-grade eBGP peering with upstream ISPs built
  directly into the platform, automatic ISP dual-stack detection, WireGuard VPN over IPv6,
  and Teleport VPN for dependable remote access behind CG-NAT.
  ([Introducing UniFi Network 10.4](https://blog.ui.com/article/introducing-unifi-network-10-4))
- **Safe Ops and license-free Building Bridges** (10.5): Test & Confirm holds configuration
  changes as provisional until devices confirm connectivity (with automatic rollback if it's
  lost), Time Machine extends into troubleshooting from the client's perspective, and
  license-free UniFi Building Bridges extend trunk connectivity across campuses.
  ([Introducing UniFi Network 10.5](https://blog.ui.com/article/introducing-network-10-5))
- **Drift Inspector and Topology Spotlight** (10.6): configuration drift detection/resolution
  for Blueprint-orchestrated sites, spotlight-style filtering for large topologies, and
  further expansion of the Safe Ops and Time Machine features introduced in 10.5.
  ([Introducing UniFi Network 10.6](https://blog.ui.com/article/introducing-unifi-network-10-6))

Throughout 10.x, Ubiquiti has also been steering self-hosted deployments (like this fork)
toward [UniFi OS Server](https://ui.com/download/releases/unifi-os-server) as the
recommended path going forward, while continuing to ship and support the sysvinit package
this image is built from. See [`DISABLE_UOS_UPGRADE_NAG`](README.md#environment-variables)
in the README if you'd like to suppress the in-app upgrade reminder.
