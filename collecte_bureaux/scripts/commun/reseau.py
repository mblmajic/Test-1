"""Accès HTTP public, poli et traçable (bibliothèque standard uniquement).

- respecte robots.txt (refus => on n'insiste pas) ;
- délai entre requêtes et nombre de reprises limités ;
- aucune tentative de contourner CAPTCHA, authentification ou blocage ;
- chaque réponse est résumée en preuve (URL, date, statut, empreinte).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) CollecteBureauxCasablanca/1.0 (+usage interne, cadence lente)"
SIGNES_BLOCAGE = ("captcha", "cf-challenge", "access denied", "attention required", "are you a robot", "datadome")


def maintenant() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Reponse:
    url: str
    url_finale: str
    statut: int | None
    texte: str
    erreur: str | None
    date: str
    empreinte: str
    diagnostic: str  # ok | http_<code> | blocage_site_observe | limitation_outil | robots_refuse | erreur_reseau

    def preuve(self) -> dict:
        return {
            "url": self.url,
            "url_finale": self.url_finale,
            "statut_http": self.statut,
            "date_observation": self.date,
            "sha256_16": self.empreinte,
            "diagnostic": self.diagnostic,
            "erreur": self.erreur,
        }


class ClientHTTP:
    def __init__(self, delai: float = 2.0, reprises: int = 2, timeout: float = 25.0, respecter_robots: bool = True):
        self.delai = delai
        self.reprises = reprises
        self.timeout = timeout
        self.respecter_robots = respecter_robots
        self._dernier = 0.0
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}

    def _attendre(self) -> None:
        reste = self.delai - (time.monotonic() - self._dernier)
        if reste > 0:
            time.sleep(reste)
        self._dernier = time.monotonic()

    def robots_autorise(self, url: str) -> bool:
        if not self.respecter_robots:
            return True
        p = urllib.parse.urlsplit(url)
        base = f"{p.scheme}://{p.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                r = self._brut(base + "/robots.txt")
                rp.parse(r[2].splitlines() if r[0] == 200 else [])
                self._robots[base] = rp
            except Exception:
                self._robots[base] = None  # robots illisible : on reste prudent mais on n'interdit pas
        rp = self._robots[base]
        return True if rp is None else rp.can_fetch(USER_AGENT, url)

    def _brut(self, url: str) -> tuple[int, str, str]:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        })
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = resp.read()
            enc = resp.headers.get("Content-Encoding", "")
            if enc == "gzip":
                data = gzip.decompress(data)
            elif enc == "deflate":
                data = zlib.decompress(data)
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.status, resp.geturl(), data.decode(charset, errors="replace")

    def get(self, url: str) -> Reponse:
        date = maintenant()
        if not self.robots_autorise(url):
            return Reponse(url, url, None, "", "robots.txt interdit cette URL", date, "", "robots_refuse")
        derniere_erreur = None
        for essai in range(self.reprises + 1):
            self._attendre()
            try:
                statut, finale, texte = self._brut(url)
                emp = hashlib.sha256(texte.encode()).hexdigest()[:16]
                bas = texte[:20000].lower()
                diag = "blocage_site_observe" if any(s in bas for s in SIGNES_BLOCAGE) else "ok"
                return Reponse(url, finale, statut, texte, None, date, emp, diag)
            except urllib.error.HTTPError as e:
                corps = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
                if e.code in (403, 429) and any(s in corps.lower() for s in SIGNES_BLOCAGE):
                    return Reponse(url, url, e.code, corps, str(e), date, "", "blocage_site_observe")
                if e.code in (404, 410):
                    return Reponse(url, url, e.code, corps, str(e), date, "", f"http_{e.code}")
                derniere_erreur = (e.code, str(e), corps)
                if e.code not in (429, 500, 502, 503, 504):
                    break
                time.sleep(self.delai * (essai + 2))
            except urllib.error.URLError as e:
                raison = str(e.reason)
                # Tunnel refusé par le proxy sortant de l'environnement : ce n'est pas le site.
                if "Tunnel connection failed" in raison or "403" in raison and "CONNECT" in raison.upper():
                    return Reponse(url, url, None, "", raison, date, "", "limitation_outil")
                derniere_erreur = (None, raison, "")
                time.sleep(self.delai * (essai + 1))
            except Exception as e:  # timeouts, SSL...
                derniere_erreur = (None, repr(e), "")
                time.sleep(self.delai * (essai + 1))
        code, msg, corps = derniere_erreur or (None, "inconnue", "")
        diag = f"http_{code}" if code else "erreur_reseau"
        return Reponse(url, url, code, corps, msg, date, "", diag)


def sauver_preuve(dossier: str, reponse: Reponse, garder_html: bool = False) -> str:
    import os
    os.makedirs(dossier, exist_ok=True)
    nom = hashlib.sha1(reponse.url.encode()).hexdigest()[:12]
    chemin = os.path.join(dossier, f"{nom}.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(reponse.preuve(), f, ensure_ascii=False, indent=1)
    if garder_html and reponse.texte:
        with open(os.path.join(dossier, f"{nom}.html.gz"), "wb") as f:
            f.write(gzip.compress(reponse.texte.encode()))
    return chemin
