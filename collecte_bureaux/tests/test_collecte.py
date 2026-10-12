"""Tests hors ligne : règles de superficie + collecte de bout en bout sur un site local factice.

Lancement : python3 -m unittest discover -s tests -v   (depuis collecte_bureaux/)
Le site factice est servi sur 127.0.0.1 ; il ne représente aucune source réelle.
"""
import http.server
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(ICI), "scripts"))

from commun import surface as sf  # noqa: E402

B = dict(borne_min=220, borne_max_exclue=230)


class Bornes(unittest.TestCase):
    def test_exemples_du_bloc(self):
        for v, attendu in [(220, sf.ELIGIBLE), (229, sf.ELIGIBLE), (229.5, sf.ELIGIBLE), (230, sf.EXCLU), (219.9, sf.EXCLU)]:
            c = sf.classer(f"Bureau {str(v).replace('.', ',')} m² à louer Casablanca", "", **B)
            self.assertEqual(c.statut, attendu, v)
            if attendu == sf.ELIGIBLE:
                self.assertEqual(c.superficie_interieure, v)

    def test_terrasse_incluse_pas_compatible(self):
        c = sf.classer("Bureau 225 m² Maarif", "Surface totale de 225 m² dont terrasse de 30 m²", **B)
        self.assertNotEqual(c.statut, sf.ELIGIBLE)

    def test_total_hors_bloc_avec_terrasse_a_verifier(self):
        c = sf.classer("Plateau bureau 260 m²", "260 m² avec terrasse 35 m²", **B)
        self.assertEqual(c.statut, sf.A_VERIFIER)

    def test_interieure_explicite(self):
        c = sf.classer("Plateau 250 m²", "superficie intérieure 224 m², terrasse 26 m²", **B)
        self.assertEqual(c.superficie_interieure, 224)

    def test_plage_et_lots(self):
        self.assertEqual(sf.classer("Bureaux de 200 à 4000 m²", "", **B).statut, sf.A_VERIFIER)
        self.assertEqual(sf.classer("Plateaux bureaux 225 m² divisibles", "", **B).statut, sf.A_VERIFIER)

    def test_coworking_cession(self):
        self.assertEqual(sf.classer("Coworking bureau 225 m²", "", **B).statut, sf.A_VERIFIER)
        self.assertEqual(sf.classer("Cession de bail bureau 222 m2", "", **B).statut, sf.A_VERIFIER)

    def test_milliers_pas_faux_positif(self):
        c = sf.classer("Villa 1 225 m² usage bureau", "", **B)
        self.assertNotEqual(c.statut, sf.ELIGIBLE)

    def test_hors_bloc(self):
        self.assertEqual(sf.classer("Bureau 205 m² à louer", "", **B).statut, sf.EXCLU)

    def test_absent(self):
        self.assertEqual(sf.classer("Bureau à louer Gauthier", "", **B).statut, sf.A_VERIFIER)


PAGES = {
    "/liste": '<a href="/fiche/101">Bureau 224 m²</a><a href="/fiche/102">Bureau 120 m²</a><a href="/liste?page=2">2</a>',
    "/liste?page=2": '<a href="/fiche/103">Plateau</a><a href="/fiche/104">Bureau 240 m² terrasse</a>',
    "/liste?page=3": "<p>aucun résultat</p>",
}
FICHE = """<html><head><title>{t}</title><link rel="canonical" href="http://127.0.0.1:{port}/fiche/{id}">
<script type="application/ld+json">{{"@type":"Offer","name":"{t}","description":"{d}","price":"{p}","priceCurrency":"MAD","sku":"{id}"}}</script>
</head><body>{t} {d}</body></html>"""
FICHES = {
    "101": ("Bureau 224 m² à louer Racine Casablanca", "Bureau de 224 m², 6 bureaux, location", "30000"),
    "102": ("Bureau 120 m² à louer", "location", "9000"),
    "103": ("Plateau bureau à louer Casablanca", "Plateau de 226 m² à louer, open space", "35000"),
    "104": ("Bureau 240 m² à louer Casablanca", "240 m² dont terrasse de 20 m², location", "33000"),
}


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        port = self.server.server_address[1]
        if self.path == "/robots.txt":
            body = "User-agent: *\nAllow: /\n"
        elif self.path in PAGES:
            body = PAGES[self.path]
        elif self.path.startswith("/fiche/") and self.path[7:] in FICHES:
            t, d, p = FICHES[self.path[7:]]
            body = FICHE.format(t=t, d=d, p=p, id=self.path[7:], port=port)
        else:
            self.send_response(404)
            self.end_headers()
            return
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(data)


class BoutEnBout(unittest.TestCase):
    def test_collecte_locale(self):
        import collecte
        srv = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        port = srv.server_address[1]
        tmp = tempfile.mkdtemp()
        cfg = {"sources": [{"source_id": 999, "nom": "Site factice", "url_principale": f"http://127.0.0.1:{port}/",
                            "routes": {"LOCATION": [f"http://127.0.0.1:{port}/liste"], "VENTE": []},
                            "pagination": "{url}{sep}page={n}", "regex_lien_annonce": r"/fiche/\d+",
                            "regex_reference": r"/fiche/(\d+)"}]}
        cfg_path = os.path.join(tmp, "cfg.json")
        with open(cfg_path, "w") as f:
            json.dump(cfg, f)
        anciens = collecte.CONFIG, collecte.RACINE
        collecte.CONFIG, collecte.RACINE = cfg_path, tmp
        try:
            rc = collecte.main(["--source-id", "999", "--transaction", "LOCATION", "--passage", "TEST",
                                "--delai", "0", "--min", "220", "--max-exclu", "230"])
            self.assertEqual(rc, 0)
            lignes = [json.loads(l) for l in open(os.path.join(tmp, "resultats", "TEST", "source999_LOCATION.jsonl"))]
            par_ref = {l["reference_native"]: l["classement"]["statut"] for l in lignes}
            self.assertEqual(par_ref.get("101"), sf.ELIGIBLE)
            self.assertEqual(par_ref.get("103"), sf.ELIGIBLE)       # surface lue dans la fiche
            self.assertEqual(par_ref.get("104"), sf.A_VERIFIER)     # 240 m² terrasse incluse
            self.assertNotIn("102", par_ref)                         # 120 m² écarté au préfiltre
            cp = json.load(open(os.path.join(tmp, "checkpoints", "TEST", "source999_LOCATION.json")))
            self.assertEqual(cp["statut"], "Terminée")
            # Reprise : aucune nouvelle ligne, pas de double comptage
            rc = collecte.main(["--source-id", "999", "--transaction", "LOCATION", "--passage", "TEST",
                                "--delai", "0", "--reprendre"])
            lignes2 = open(os.path.join(tmp, "resultats", "TEST", "source999_LOCATION.jsonl")).read().count("\n")
            self.assertEqual(lignes2, len(lignes))
        finally:
            collecte.CONFIG, collecte.RACINE = anciens
            srv.shutdown()
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
