from __future__ import annotations

import re
from typing import List

from urllib.parse import urlparse

from loguru import logger


def normalize_url(url: str) -> str:
    """Normalize URL: lowercase, remove scheme and fragment, keep query."""
    url = url.strip().lower()
    url = re.sub(r"^https?://", "", url)
    if "#" in url:
        url = url.split("#", 1)[0]
    return url
TOKEN_SPLIT_PATTERN = re.compile(r"[./_\-?=&]+")


def tokenize_url(url: str) -> List[str]:
    """Tokenize URL using common URL separators."""
    norm = normalize_url(url)
    tokens = [t for t in TOKEN_SPLIT_PATTERN.split(norm) if t]
    return tokens

def get_hostname_and_path(url: str) -> tuple[str, str]:
    """Return hostname and path-part of URL (after scheme)."""
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = parsed.hostname or ""
    path = parsed.path or ""
    if parsed.query:
        path = path + "?" + parsed.query
    return host, path
