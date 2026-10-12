#!/usr/bin/env python3
"""Collecteur générique de bureaux (Claude Code) — version 1.0.0.

Usage :
  python3 scripts/collecte.py --source-id 6 --transaction LOCATION \
      --ville Casablanca --min 220 --max-exclu 230 --passage EXPERT220229-...

  python3 scripts/collecte.py --preflight            # test d'accès de toutes les sources
  python3 scripts/collecte.py --source-id 6 --transaction VENTE --reprendre ...

Le script :
  1. lit la configuration de la source (scripts/sources/config_sources.json) ;
  2. parcourt la pagination publique de la route propre à la transaction ;
  3. préfiltre les cartes, ouvre chaque fiche candidate, classe la superficie
     (Compatible / À vérifier / Exclu) avec preuves ;
  4. sauvegarde un checkpoint après chaque page et exporte les candidats.
Il n'écrit PAS dans SmartDB : les écritures passent par les outils MCP EasySpace.
Aucun secret n'est lu ni stocké.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.parse

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
sys.path.insert(0, ICI)

from commun import extraction as ex  # noqa: E402
from commun import surface as sf  # noqa: E402
from commun.reseau import ClientHTTP, maintenant, sauver_preuve  # noqa: E402

VERSION = "collecte-bureaux/1.0.0"
CONFIG = os.path.join(ICI, "sources", "config_sources.json")


def charger_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return {str(s["source_id"]): s for s in json.load(f)["sources"]}


# --------------------------------------------------------------------- checkpoint
def chemin_checkpoint(passage: str, source_id: str, transaction: str) -> str:
    return os.path.join(RACINE, "checkpoints", passage, f"source{source_id}_{transaction}.json")


def lire_checkpoint(chemin: str) -> dict | None:
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    return None


def ecrire_checkpoint(chemin: str, cp: dict) -> None:
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    cp["mis_a_jour"] = maintenant()
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cp, f, ensure_ascii=False, indent=1)
    os.replace(tmp, chemin)


# --------------------------------------------------------------------- pagination
def url_page(modele: str, base: str, n: int) -> str:
    if n == 1:
        return base
    return modele.format(url=base, n=n, sep="&" if "?" in base else "?")


def reference(url: str, cfg: dict, page_fiche: str | None = None, donnees: dict | None = None) -> str | None:
    rx = cfg.get("regex_reference")
    if rx:
        m = re.search(rx, url)
        if m:
            return m.group(1)
    if donnees:
        for k in ("sku", "productID", "identifier", "adId", "listId", "reference", "ref", "id"):
            if donnees.get(k):
                return str(donnees[k])
    return None


def cle_annonce(source_id: str, ref: str | None, url: str) -> str:
    if ref:
        return f"SRC{source_id}|REF|{ref}"
    p = urllib.parse.urlsplit(url)
    return f"SRC{source_id}|URL|{p.netloc}{p.path}".rstrip("/")


# --------------------------------------------------------------------- fiche
def transaction_observee(texte: str) -> str | None:
    """LOCATION / VENTE si un seul sens est lisible, sinon None (ambigu ou absent)."""
    bas = texte.lower()
    loc = any(w in bas for w in ("à louer", "a louer", "location", "/louer", "loyer", "-louer", "_louer"))
    ven = any(w in bas for w in ("à vendre", "a vendre", "/vente", "vente ", "-vendre", "_vendre", "acheter"))
    if loc and not ven:
        return "LOCATION"
    if ven and not loc:
        return "VENTE"
    return None


def lire_fiche(client: ClientHTTP, url: str, cfg: dict, args, dossier_preuves: str) -> dict:
    rep = client.get(url)
    sauver_preuve(dossier_preuves, rep, garder_html=args.garder_html)
    fiche = {"url": url, "diagnostic": rep.diagnostic, "statut_http": rep.statut, "date_observation": rep.date}
    if rep.diagnostic != "ok":
        fiche["erreur"] = rep.erreur
        return fiche
    page = rep.texte
    meta = ex.metas(page)
    blocs = ex.jsonld(page)
    nd = ex.next_data(page)
    cles = {"name", "description", "price", "priceCurrency", "floorSize", "value", "unitCode", "addressLocality",
            "streetAddress", "datePosted", "datePublished", "sku", "identifier", "adId", "listId", "size", "surface",
            "area", "neighborhood", "city", "phone", "telephone"}
    donnees = ex.chercher_cles(blocs, cles)
    if nd:
        ex.chercher_cles(nd, cles, trouve=donnees)
    texte = ex.texte_visible(page)
    titre = donnees.get("name") or meta.get("og:title") or meta.get("title") or ""
    description = donnees.get("description") or meta.get("og:description") or meta.get("description") or ""
    corps = texte if args.texte_complet else description
    surf_struct = ex.nombre(donnees.get("floorSize") or donnees.get("size") or donnees.get("surface") or donnees.get("area"))
    trans_obs = transaction_observee(f"{titre} {description} {rep.url_finale}")
    classe = sf.classer(titre, f"{description} {corps}", surf_struct,
                        borne_min=args.min, borne_max_exclue=args.max_exclu,
                        transaction_attendue=args.transaction, transaction_observee=trans_obs)
    ref = reference(url, cfg, page, donnees)
    fiche.update({
        "titre": titre[:300],
        "url_canonique": meta.get("canonical") or rep.url_finale,
        "reference_native": ref,
        "cle_annonce": cle_annonce(args.source_id, ref, meta.get("canonical") or rep.url_finale),
        "prix": ex.nombre(donnees.get("price")),
        "devise": donnees.get("priceCurrency"),
        "quartier": donnees.get("neighborhood") or donnees.get("addressLocality"),
        "adresse": donnees.get("streetAddress"),
        "date_publication_source": donnees.get("datePosted") or donnees.get("datePublished"),
        "surface_structuree": surf_struct,
        "transaction_observee": trans_obs,
        "classement": classe.to_dict(),
        "extrait_description": description[:600],
        "ville_mentionnee": args.ville.lower() in (titre + description + texte[:5000]).lower(),
    })
    return fiche


# --------------------------------------------------------------------- collecte
def collecter(args) -> int:
    cfgs = charger_config()
    cfg = cfgs.get(str(args.source_id))
    if not cfg:
        print(f"Source {args.source_id} absente de la configuration", file=sys.stderr)
        return 2
    routes = cfg.get("routes", {}).get(args.transaction) or []
    cp_path = chemin_checkpoint(args.passage, str(args.source_id), args.transaction)
    cp = lire_checkpoint(cp_path) if args.reprendre else None
    if not routes:
        cp = {"source_id": args.source_id, "transaction": args.transaction, "statut": "Route introuvable",
              "prochaine_action": "Identifier la route publique de cette transaction", "compteurs": {}}
        ecrire_checkpoint(cp_path, cp)
        print(json.dumps(cp, ensure_ascii=False))
        return 3
    if cp is None:
        cp = {
            "passage": args.passage, "version_script": VERSION, "source_id": args.source_id,
            "source": cfg.get("nom"), "mission_id": args.mission_id, "transaction": args.transaction,
            "ville": args.ville, "borne_min": args.min, "borne_max_exclue": args.max_exclu,
            "route_index": 0, "derniere_page": 0, "derniere_url": None,
            "references_traitees": [], "urls_a_verifier": [], "statut": "En cours",
            "compteurs": {"pages": 0, "cartes": 0, "fiches_ouvertes": 0, "compatibles": 0, "a_verifier": 0,
                          "exclus": 0, "erreurs": 0},
            "diagnostics": [], "prochaine_action": "Parcourir la page 1",
        }
    client = ClientHTTP(delai=args.delai, reprises=args.reprises)
    dossier_preuves = os.path.join(RACINE, "preuves", args.passage, f"source{args.source_id}_{args.transaction}")
    sortie = os.path.join(RACINE, "resultats", args.passage, f"source{args.source_id}_{args.transaction}.jsonl")
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    traitees = set(cp["references_traitees"])
    motif = cfg.get("regex_lien_annonce")
    modele = cfg.get("pagination", "{url}{sep}page={n}")
    marge = cfg.get("marge_prefiltre_m2", 60)

    while cp["route_index"] < len(routes):
        base = routes[cp["route_index"]]
        n = cp["derniere_page"] + 1
        vides = 0
        while n <= args.max_pages:
            url = url_page(modele, base, n)
            rep = client.get(url)
            sauver_preuve(dossier_preuves, rep, garder_html=args.garder_html)
            if rep.diagnostic != "ok":
                cp["diagnostics"].append({"url": url, "diagnostic": rep.diagnostic, "statut": rep.statut,
                                          "erreur": rep.erreur, "date": rep.date})
                cp["compteurs"]["erreurs"] += 1
                if n == 1 or rep.diagnostic in ("limitation_outil", "blocage_site_observe", "robots_refuse"):
                    cp["statut"] = {"limitation_outil": "Limitation de l'outil",
                                    "blocage_site_observe": "Blocage du site observé",
                                    "robots_refuse": "Refus robots.txt",
                                    "http_404": "Route obsolète ou introuvable"}.get(rep.diagnostic, "Erreur")
                    cp["prochaine_action"] = f"Reprendre à {url} quand l'accès est rétabli"
                    ecrire_checkpoint(cp_path, cp)
                    print(json.dumps({"statut": cp["statut"], "url": url, "erreur": rep.erreur}, ensure_ascii=False))
                    return 4
                break  # fin de pagination probable (404 au-delà de la dernière page)
            cartes = ex.liens(rep.texte, rep.url_finale, motif)
            nouvelles = [(u, t) for u, t in cartes if cle_annonce(args.source_id, reference(u, cfg), u) not in traitees]
            if not cartes:
                vides += 1
                if vides >= 1:
                    break
            cp["compteurs"]["pages"] += 1
            cp["compteurs"]["cartes"] += len(cartes)
            for u, txt in nouvelles:
                cle = cle_annonce(args.source_id, reference(u, cfg), u)
                traitees.add(cle)
                if not sf.prefiltre_carte(txt or u, args.min, args.max_exclu, marge):
                    continue
                fiche = lire_fiche(client, u, cfg, args, dossier_preuves)
                cp["compteurs"]["fiches_ouvertes"] += 1
                if fiche["diagnostic"] != "ok":
                    cp["urls_a_verifier"].append(u)
                    cp["compteurs"]["erreurs"] += 1
                    continue
                st = fiche["classement"]["statut"]
                if st == sf.EXCLU:
                    cp["compteurs"]["exclus"] += 1
                    continue
                cp["compteurs"]["compatibles" if st == sf.ELIGIBLE else "a_verifier"] += 1
                fiche.update({"passage": args.passage, "source_id": args.source_id, "mission_id": args.mission_id,
                              "transaction": args.transaction})
                with open(sortie, "a", encoding="utf-8") as f:
                    f.write(json.dumps(fiche, ensure_ascii=False) + "\n")
            cp.update({"derniere_page": n, "derniere_url": url, "references_traitees": sorted(traitees),
                       "prochaine_action": f"Parcourir la page {n + 1} de la route {cp['route_index'] + 1}"})
            ecrire_checkpoint(cp_path, cp)
            if not nouvelles and n > 1:
                break  # page déjà vue : pagination bouclée
            n += 1
        cp["route_index"] += 1
        cp["derniere_page"] = 0
        ecrire_checkpoint(cp_path, cp)

    cp["statut"] = "Terminée" if not cp["urls_a_verifier"] and not cp["diagnostics"] else "Partielle"
    cp["prochaine_action"] = "Aucune" if cp["statut"] == "Terminée" else "Revérifier urls_a_verifier"
    ecrire_checkpoint(cp_path, cp)
    print(json.dumps({"statut": cp["statut"], "compteurs": cp["compteurs"]}, ensure_ascii=False))
    return 0


def preflight(args) -> int:
    """Test d'accès (page d'accueil + route de chaque transaction) pour toutes les sources configurées."""
    client = ClientHTTP(delai=0.3, reprises=0, timeout=15, respecter_robots=False)
    lignes = []
    for sid, cfg in charger_config().items():
        urls = [cfg.get("url_principale")] + [r[0] for r in cfg.get("routes", {}).values() if r]
        for u in [x for x in urls if x]:
            rep = client.get(u)
            lignes.append({"source_id": sid, "source": cfg["nom"], "url": u, "statut_http": rep.statut,
                           "diagnostic": rep.diagnostic, "erreur": (rep.erreur or "")[:200], "date": rep.date})
            print(sid, cfg["nom"], u, rep.statut, rep.diagnostic, flush=True)
    out = os.path.join(RACINE, "preuves", args.passage or "preflight", "preflight.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)
    print("->", out)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source-id")
    p.add_argument("--mission-id", type=int)
    p.add_argument("--transaction", choices=["LOCATION", "VENTE"])
    p.add_argument("--ville", default="Casablanca")
    p.add_argument("--min", type=float, default=220.0, help="borne basse incluse (m²)")
    p.add_argument("--max-exclu", type=float, default=230.0, help="borne haute exclue (m²)")
    p.add_argument("--passage", default="")
    p.add_argument("--max-pages", type=int, default=150)
    p.add_argument("--delai", type=float, default=2.0)
    p.add_argument("--reprises", type=int, default=2)
    p.add_argument("--reprendre", action="store_true")
    p.add_argument("--garder-html", action="store_true")
    p.add_argument("--texte-complet", action="store_true", help="classer aussi sur le texte visible complet")
    p.add_argument("--preflight", action="store_true")
    args = p.parse_args(argv)
    if args.preflight:
        return preflight(args)
    if not (args.source_id and args.transaction and args.passage):
        p.error("--source-id, --transaction et --passage sont requis")
    return collecter(args)


if __name__ == "__main__":
    sys.exit(main())
