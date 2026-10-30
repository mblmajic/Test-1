# 04 — Plan et résultats de tests

Format : cas | attendu | obtenu | preuve. Détail brut des GET : `tests/resultats_get_crm21.md`.

## Identité et droits (GET /crm21/session) — brouillon
| Cas | Attendu | Obtenu | Preuve |
|---|---|---|---|
| Broker membre (Imane, claims avec rôle dom-admin) | 200, role Broker, admin false | 200, Broker, broker Imane | test_endpoint 2026-10-30 |
| Admin membre (majid@tybotflow.com) | 200, admin true | 200 | test_endpoint |
| Compte « Admin Domaine » non membre (othmane@) | 403 | 403 « Votre compte n'est pas encore activé… » | test_endpoint |
| Sans email | 401 | 401 | test_endpoint |

## Cloisonnement des lectures (filtre serveur Agent Broker)
| Cas | Attendu | Obtenu | Preuve |
|---|---|---|---|
| Admin, portefeuille | tous (28) | step rows = 28 | trace SQL sans filtre |
| Imane | ses dossiers | 12, SQL `where src_c2ljvedgo8rjnjz = 'Imane'` | trace |
| Salma | ses dossiers | 13 | trace |
| Imane → fiche/propositions/historique/rapprochements du dossier 6 (Salma) | 404 | 404 g404 | test_endpoint |

## Atomicité (L1)
| Cas | Attendu | Obtenu | Preuve |
|---|---|---|---|
| Colonne texte en clé primaire | création PK | ignoré (`cle` non PK) | smartdb_list_columns |
| createRecord avec id explicite (API Studio) | rejet doublon | `BAD_REQUEST Column "Id" is read-only` | test_endpoint /crm21/test-verrou |
| smartdb_sync_constraints | contrainte UNIQUE | « Column … not found in Postgres — skipping » | réponse outil |

## À venir
Lectures (après correctif), écritures sur données [RECETTE V21], concurrence propositions, fuseau (RDV 23:30 → 00:30), formulaires invalides, pages mobile/desktop.
