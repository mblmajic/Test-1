"""Extraction de données publiques intégrées aux pages (JSON-LD, __NEXT_DATA__, liens)."""
from __future__ import annotations

import html
import json
import re
import urllib.parse
from html.parser import HTMLParser

RE_JSONLD = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S | re.I)
RE_NEXT = re.compile(r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(.*?)</script>', re.S | re.I)
RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
RE_META = re.compile(r'<meta[^>]+(?:property|name)=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\']', re.I)
RE_CANON = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I)


def jsonld(page: str) -> list:
    blocs = []
    for brut in RE_JSONLD.findall(page):
        try:
            d = json.loads(html.unescape(brut.strip()))
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and "@graph" in d:
            blocs.extend(d["@graph"])
        elif isinstance(d, list):
            blocs.extend(d)
        else:
            blocs.append(d)
    return blocs


def next_data(page: str) -> dict | None:
    m = RE_NEXT.search(page)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def metas(page: str) -> dict:
    out = {k.lower(): html.unescape(v) for k, v in RE_META.findall(page)}
    t = RE_TITLE.search(page)
    if t:
        out["title"] = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()
    c = RE_CANON.search(page)
    if c:
        out["canonical"] = c.group(1)
    return out


class _Liens(HTMLParser):
    def __init__(self):
        super().__init__()
        self.liens: list[tuple[str, str]] = []
        self._pile: list[list] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._pile.append([dict(attrs).get("href") or "", ""])

    def handle_data(self, data):
        for item in self._pile:
            item[1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self._pile:
            href, txt = self._pile.pop()
            self.liens.append((href, re.sub(r"\s+", " ", txt).strip()))


def liens(page: str, base: str, motif: str | None = None) -> list[tuple[str, str]]:
    p = _Liens()
    try:
        p.feed(page)
    except Exception:
        pass
    vus, out = set(), []
    rx = re.compile(motif) if motif else None
    for href, txt in p.liens:
        absolu = urllib.parse.urljoin(base, href.split("#")[0])
        if rx and not rx.search(absolu):
            continue
        if absolu not in vus:
            vus.add(absolu)
            out.append((absolu, txt))
    return out


def texte_visible(page: str, limite: int = 20000) -> str:
    page = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<[^>]+>", " ", page)
    return re.sub(r"\s+", " ", html.unescape(page)).strip()[:limite]


def chercher_cles(obj, cles: set[str], profondeur: int = 0, trouve: dict | None = None) -> dict:
    """Parcourt un JSON et collecte la première valeur rencontrée pour chaque clé demandée."""
    trouve = {} if trouve is None else trouve
    if profondeur > 12:
        return trouve
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in cles and k not in trouve and not isinstance(v, (dict, list)):
                trouve[k] = v
            chercher_cles(v, cles, profondeur + 1, trouve)
    elif isinstance(obj, list):
        for v in obj:
            chercher_cles(v, cles, profondeur + 1, trouve)
    return trouve


def nombre(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d[\d   .]*(?:,\d+)?", str(v))
    if not m:
        return None
    s = re.sub(r"[   ]", "", m.group(0))
    if s.count(".") >= 1 and "," not in s and re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None
