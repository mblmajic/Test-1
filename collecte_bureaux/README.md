# Collecte bureaux Casablanca — scripts Claude Code

Collecte des bureaux à louer et à vendre à Casablanca, par bloc de superficie intérieure, sur les sources actives du référentiel SmartDB « Sources Scraping Immobilier » (base `pmu5g6nwuxyez`, table `mc2e82014493678e1`).

Passage initialisé le 2026-10-12 : `EXPERT220229-20261012-143557`, mini-catégorie 3 « 220 à 229 m² ». La règle appliquée est la suivante : superficie intérieure ≥ 220 m² et < 230 m².

## État au 2026-10-12

| Élément | État |
|---|---|
| Missions SmartDB (table `mced928eae13255d4`) | 70 créées, IDs 71 à 140. 71 et 72 « Bloquée », les 68 autres « À lancer » |
| Journaux d'exécution (table `m7babf31a5b306aa7`) | 14 (90HT1U6Q) et 15 (LASTWH2H), MarocImmo LOCATION et VENTE |
| Fiches créées dans « Total Biens 200 à 299m2 » | 0 |
| Cause de l'arrêt | Le proxy sortant de l'environnement Claude Code refuse les 35 domaines sources (`Tunnel connection failed: 403 Forbidden`). C'est une **limitation de l'outil**, pas un blocage des sites. |

## Organisation

```
collecte_bureaux/
  README.md
  requirements.txt            # aucune dépendance externe (bibliothèque standard Python ≥ 3.10)
  scripts/
    collecte.py               # point d'entrée (collecte, reprise, preflight)
    commun/surface.py         # classement Compatible / À vérifier / Exclu
    commun/reseau.py          # HTTP poli : robots.txt, délais, reprises limitées, preuves
    commun/extraction.py      # JSON-LD, __NEXT_DATA__, liens, métadonnées
    sources/config_sources.json  # routes par source et par transaction (non validées)
  tests/test_collecte.py      # tests hors ligne (règles + collecte bout en bout sur un site local factice)
  checkpoints/<passage>/      # un JSON par source et transaction
  preuves/<passage>/          # preuves structurées (URL, date, statut HTTP, empreinte)
  resultats/                  # sorties JSONL par mission, CSV livrables
  etat/                       # instantanés SmartDB lus avant modification
```

## Commandes

```bash
cd collecte_bureaux
python3 -m unittest discover -s tests -v          # tests hors ligne

# Test d'accès à toutes les sources (à lancer en premier dans un nouvel environnement)
python3 scripts/collecte.py --preflight --passage EXPERT220229-20261012-143557

# Collecte d'une mission (les bornes sont des paramètres, réutilisables pour d'autres blocs)
python3 scripts/collecte.py --source-id 6 --mission-id 71 --transaction LOCATION \
  --ville Casablanca --min 220 --max-exclu 230 --passage EXPERT220229-20261012-143557

# Reprise sans doublon à partir du checkpoint
python3 scripts/collecte.py --source-id 6 --mission-id 71 --transaction LOCATION \
  --passage EXPERT220229-20261012-143557 --reprendre
```

Options utiles : `--delai` (2 s par défaut), `--reprises` (2), `--max-pages` (150), `--garder-html` (archive le HTML compressé en preuve), `--texte-complet` (classe aussi sur le texte visible de la fiche).

## Règles de classement (`commun/surface.py`)

- **Compatible** : une seule surface lisible, dans le bloc, sans annexe, plage, lot multiple ni usage douteux.
- **À vérifier** : surface absente ; surface totale avec terrasse ou annexe à déduire ; plage (« de 200 à 4000 m² ») ; plusieurs lots ou surface modulable ; coworking, cession de bail, local commercial, villa ou immeuble ; plusieurs surfaces sans libellé.
- **Exclu** : surface intérieure lisible hors bloc, ou transaction contraire.
- La superficie n'est jamais arrondie. Le séparateur de milliers est géré, pour éviter qu'un « 1 225 m² » soit lu comme 225.

## Ce que le script ne fait pas

- Il n'écrit pas dans SmartDB : les écritures passent par les outils MCP EasySpace, car aucun accès programmatique documenté n'est disponible depuis Python.
- Il ne contourne ni CAPTCHA, ni authentification, ni restriction, et n'appelle aucune API privée. Un blocage observé est enregistré, pas contourné.
- Il ne contient aucun secret.

## Statut de validation (honnête)

| Composant | Statut |
|---|---|
| Règles de superficie, pagination, checkpoint, reprise et dédoublonnage | **Validés hors ligne** : 10 tests, dont une collecte complète sur un site local factice |
| Preflight sur les 35 sources | **Exécuté** le 2026-10-12 à 14:35:57 UTC. Résultat : limitation de l'outil sur les 35 |
| Collecte réelle, source 6 (MarocImmo) LOCATION et VENTE | **Exécutée, en échec** (limitation de l'outil, 0 page lue) |
| Adaptateurs et routes des 34 autres sources | **Proposition non testée** sur site réel |
| Gain par rapport aux méthodes antérieures | **Non mesuré** |

## Débloquer l'accès

Il faut ajouter les domaines des sources à la liste des domaines autorisés de l'environnement : menu de l'environnement cloud dans la barre de titre de la session, puis Modifier, puis Accès réseau. Documentation : <https://code.claude.com/docs/en/cloud-environments#network-access>. On peut aussi exécuter ces scripts sur un poste disposant d'un accès Internet direct.
