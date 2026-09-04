#!/usr/bin/env python3
import html
import os
import urllib.request
import xml.etree.ElementTree as ET
import re
import sys
import email.utils
from datetime import datetime, timezone

FEED_URL = "https://community.ui.com/rss/releases/UniFi-Network-Application/e6712595-81bb-4829-8e42-9e2630fabcfe"
DOCKERFILE = "Dockerfile"
README = "README.md"
CHANGELOG = "CHANGELOG.md"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (GitHub Actions UniFi Updater)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def parse_rss_latest(feed_bytes):
    """
    Parse the RSS feed and pick the newest release.

    Priority:
    1. Stable (no 'beta', 'rc', or 'release candidate' in title)
    2. RC (no 'beta' in title)
    3. Any entry with a version, as a last resort
    """
    root = ET.fromstring(feed_bytes)
    items = root.findall(".//item")
    if not items:
        raise RuntimeError("No <item> entries in RSS feed")

    releases = []

    for item in items:
        title_el = item.find("title")
        link_el = item.find("link")
        date_el = item.find("pubDate")
        desc_el = item.find("description")

        if title_el is None or link_el is None:
            continue

        title = (title_el.text or "").strip()
        link = (link_el.text or "").strip()
        date_raw = (date_el.text or "").strip() if date_el is not None else ""
        description = (desc_el.text or "").strip() if desc_el is not None else ""

        # Try to extract version like 10.0.160 or 9.5.21
        m = re.search(r"(\d+\.\d+\.\d+)", title)
        if not m:
            # Fallback to 2-part versions like 10.0
            m = re.search(r"(\d+\.\d+)", title)
        if not m:
            continue

        version = m.group(1)

        if date_raw:
            try:
                dt = email.utils.parsedate_to_datetime(date_raw)
                date_str = dt.date().isoformat()
            except Exception:
                date_str = ""
        else:
            date_str = ""

        releases.append(
            {
                "title": title,
                "title_lc": title.lower(),
                "version": version,
                "link": link,
                "date": date_str,
                "description": description,
            }
        )

    if not releases:
        raise RuntimeError("No releases with a recognizable version found in RSS feed")

    # 1. Prefer "stable" (no beta/rc)
    stable = [
        r for r in releases
        if not any(tag in r["title_lc"] for tag in ("beta", " rc", "release candidate"))
    ]
    if stable:
        return stable[0]

    # 2. Fallback: allow RCs but still skip explicit "beta"
    rc = [r for r in releases if "beta" not in r["title_lc"]]
    if rc:
        return rc[0]

    # 3. Last resort: whatever is first in the feed
    return releases[0]


def build_pkgurl(version: str) -> str:
    """
    Construct the expected sysvinit .deb URL from the version.
    Example: 9.5.21 -> https://dl.ui.com/unifi/9.5.21/unifi_sysvinit_all.deb
    """
    return f"https://dl.ui.com/unifi/{version}/unifi_sysvinit_all.deb"


def html_to_markdown(raw_html: str) -> str:
    """
    Turn the RSS item's release-notes HTML into readable Markdown.
    Best-effort, regex based (no third-party deps available in the runner).
    """
    text = raw_html

    # Drop the "Checksums" heading and everything after it (hashes aren't
    # relevant to "what's new", and dropping only the <pre> block below would
    # leave a dangling, contentless heading).
    text = re.sub(
        r"<(strong|b|h[1-6])[^>]*>\s*Checksums\s*</(strong|b|h[1-6])>.*$",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Any other <pre> blocks (code samples, etc.) aren't relevant either.
    text = re.sub(r"<pre[^>]*>.*?</pre>", "", text, flags=re.IGNORECASE | re.DOTALL)

    # Drop images (they don't render usefully in a plain changelog file).
    text = re.sub(r"<img[^>]*>", "", text, flags=re.IGNORECASE)

    # Links -> Markdown links
    text = re.sub(
        r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        r"[\2](\1)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Headings
    text = re.sub(r"<h[1-6][^>]*>", "\n### ", text, flags=re.IGNORECASE)
    text = re.sub(r"</h[1-6]>", "\n", text, flags=re.IGNORECASE)

    # Bold (\b prevents "<b...>" from also matching "<br>")
    text = re.sub(r"<(strong|b)\b[^>]*>", "**", text, flags=re.IGNORECASE)
    text = re.sub(r"</(strong|b)\b>", "**", text, flags=re.IGNORECASE)

    # Collapse empty/whitespace-only bold pairs left over from
    # e.g. <p><strong>&nbsp;</strong></p> or <strong><br></strong>
    # (entities aren't unescaped yet at this point, so &nbsp; counts too)
    while True:
        collapsed = re.sub(r"\*\*(?:\s|&nbsp;)*\*\*", "", text)
        if collapsed == text:
            break
        text = collapsed

    # List items
    text = re.sub(r"<li[^>]*>", "- ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?(ul|ol)[^>]*>", "\n", text, flags=re.IGNORECASE)

    # Line breaks / paragraphs
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<p[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)

    # Strip any remaining tags
    text = re.sub(r"<[^>]+>", "", text)

    # Unescape entities (&amp;, &nbsp;, ...)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")

    # Collapse repeated blank lines / trim trailing whitespace per line
    cleaned = []
    blank = False
    for line in (ln.strip() for ln in text.splitlines()):
        if line == "":
            if not blank and cleaned:
                cleaned.append("")
            blank = True
        else:
            cleaned.append(line)
            blank = False

    return "\n".join(cleaned).strip()


def update_dockerfile(url: str) -> None:
    with open(DOCKERFILE, "r", encoding="utf-8") as f:
        src = f.read()

    new_src, subs = re.subn(
        r"ARG\s+PKGURL=.*",
        f"ARG PKGURL={url}",
        src,
        count=1,
    )

    if subs == 0:
        raise RuntimeError("Failed to update PKGURL in Dockerfile")

    if new_src != src:
        with open(DOCKERFILE, "w", encoding="utf-8") as f:
            f.write(new_src)


def update_readme(version: str, date_str: str, link: str) -> None:
    with open(README, "r", encoding="utf-8") as f:
        src = f.read()

    new_row = (
        f"| [`latest` `v{version}`](https://github.com/NetHorror/mikrotik-unifi-container/blob/main/Dockerfile) "
        f"| Current Stable: Version {version} as of {date_str} "
        f"| [Change Log {version}]({link}) |"
    )

    # Replace the first "latest" row in the Current Information table
    new_src, subs = re.subn(
        r"^\| \[`latest` `v[0-9.]+`\]\(.*?\) \| Current Stable: Version [0-9.]+ as of [0-9-]+ \| \[Change Log [0-9.]+\]\(.*?\) \|$",
        new_row,
        src,
        count=1,
        flags=re.MULTILINE,
    )

    if subs == 0:
        raise RuntimeError("Failed to update README row")

    if new_src != src:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_src)


def update_changelog(version: str, date_str: str, link: str, description_html: str) -> None:
    """
    Prepend a "what's new in this version" entry to CHANGELOG.md, sourced from
    the RSS item's own release-notes body. Skips entries already recorded.
    """
    preamble = (
        "# Changelog\n\n"
        "UniFi Network Application release notes, recorded automatically as this "
        "fork's auto-updater (`update.yml`) picks up each new **stable** release "
        "(no betas, no RCs). See [community.ui.com/releases](https://community.ui.com/releases) "
        "for the canonical/official source.\n\n"
    )

    existing = ""
    if os.path.exists(CHANGELOG):
        with open(CHANGELOG, "r", encoding="utf-8") as f:
            existing = f.read()

    if f"## [{version}]" in existing:
        return  # already recorded, nothing to do

    body = html_to_markdown(description_html) if description_html else ""
    entry = f"## [{version}] - {date_str}\n\n[Official release notes]({link})\n\n{body}\n\n"

    if existing:
        marker = "\n## ["
        idx = existing.find(marker)
        if idx == -1:
            new_src = existing.rstrip("\n") + "\n\n" + entry
        else:
            new_src = existing[: idx + 1] + entry + existing[idx + 1 :]
    else:
        new_src = preamble + entry

    with open(CHANGELOG, "w", encoding="utf-8") as f:
        f.write(new_src)


def main() -> None:
    feed = fetch(FEED_URL)
    rel = parse_rss_latest(feed)

    version = rel["version"]
    link = rel["link"]
    date_str = rel["date"] or datetime.now(timezone.utc).date().isoformat()

    pkg_url = build_pkgurl(version)

    update_dockerfile(pkg_url)
    update_readme(version, date_str, link)
    update_changelog(version, date_str, link, rel["description"])

    # Printed so GitHub Actions step can capture it
    print(version)


if __name__ == "__main__":
    main()
