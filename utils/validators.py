from urllib.parse import urlparse
import ipaddress
import socket
from fastapi import HTTPException

BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]

BLOCKED_HOSTNAMES = {"localhost", "metadata.google.internal", "metadata", "169.254.169.254"}


def validate_url(url: str) -> str:
    # strip whitespace
    url = url.strip()
    # add https:// only when no scheme is present at all (no "://" found)
    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="URL must use http or https scheme. Got: " + parsed.scheme)

    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL: missing domain")

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid URL: cannot extract hostname")

    if hostname.lower() in BLOCKED_HOSTNAMES:
        raise HTTPException(status_code=400, detail="Access to internal/private hosts is not allowed")

    # Check if hostname looks like a raw IP address and block private ranges immediately
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise HTTPException(
                status_code=400,
                detail="Access to private/internal IP addresses is not allowed"
            )
        for network in BLOCKED_NETWORKS:
            if ip in network:
                raise HTTPException(
                    status_code=400,
                    detail="Access to private/internal network is not allowed"
                )
    except HTTPException:
        raise
    except ValueError:
        # Not a raw IP — it's a hostname. Try DNS resolution to catch hostname-based SSRF.
        try:
            resolved_ips = socket.getaddrinfo(hostname, None)
            for result in resolved_ips:
                ip_str = result[4][0]
                try:
                    ip = ipaddress.ip_address(ip_str)
                    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                        raise HTTPException(
                            status_code=400,
                            detail="Access to private/internal IP addresses is not allowed"
                        )
                    for network in BLOCKED_NETWORKS:
                        if ip in network:
                            raise HTTPException(
                                status_code=400,
                                detail="Access to private/internal network is not allowed"
                            )
                except ValueError:
                    pass
        except HTTPException:
            raise
        except socket.gaierror:
            # DNS resolution failed — could be an invalid domain or no network.
            # Allow through; the actual HTTP fetch will fail with a clear error.
            pass
        except Exception:
            pass

    return url
