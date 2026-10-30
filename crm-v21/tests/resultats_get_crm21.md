# Résultats des tests GET CRM21 (brouillons API Studio) — 2026-10-30

Méthode : `save_endpoint` (brouillon, upsert méthode+chemin) avec name/description/definition copiés tels quels depuis `contracts/endpoints/crm21__GET_*.json`, puis `test_endpoint` (skipAuth, sans allowWrites). Aucune publication ni écriture.
Appelants simulés : **admin** (Majid, rôle Admin), **Imane** (broker « Imane »), **Salma** (broker « Salma », sans roles), **non-membre** (absent de CRM21 Membres).
Ids utilisés : dossier **23** (broker Imane, étape « Recherche active », sans contact lié), dossier **6** (broker Salma, contact lié) = dossier d'un autre broker pour Imane ; bien **9** (Actif).
Les ids de dossier proviennent de la trace du step `rows` de opportunites-clients (vue=toutes), car le body admin est en erreur 422.

## Cause commune (bloquante)

Les 10 steps `out` sauf session (`referentiels`, puis tous ceux commençant par `$s := function…`) sont une suite d'instructions `;` **non entourée de parenthèses**. JSONata refuse : `save_endpoint.problems` = `Syntax error: ";" (at character 99)` (55 pour referentiels) et chaque test qui atteint `out` renvoie **422** :
`out` → `EXPRESSION_ERROR` — `Invalid expression: Syntax error: ";"` (S0201, position 99 ; position 55 pour referentiels).
Correctif attendu : envelopper toute l'expression dans `( … )` (comme `ident` et `session.out`).

Conséquence : aucun item mis en forme n'a pu être observé (clés/valeurs du 1er item indisponibles) hors session. Les gardes (401/403/400/404) et les filtres serveur sont en revanche vérifiables et sont reportés ci-dessous.

## GET /crm21/session — f9e520db-8c1d-4b8d-9061-408ab3258557 — problems : aucun

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | 200, 1 item | clés : email, nom, prenom, role, admin, broker, initiales, salutation ; role=Admin, admin=true, broker=Majid |
| Imane | 200 | 200, 1 item | role=Broker, admin=false, broker=Imane (claims.roles dom-admin ignorés : OK) |
| non-membre | 403 | 403 | répondu par `g403` : « Votre compte n’est pas encore activé dans le CRM. Contactez l’administrateur. » |

## GET /crm21/referentiels — 3adc338f-4f95-40ba-9976-ed60772ace44 — problems : `out` Syntax error ";" (char 55)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | **422** | `membres` OK (3 membres actifs) ; `out` : Invalid expression: Syntax error: ";" (pos 55) |
| Imane | 200 | **422** | `membres` skipped (non admin, OK) ; `out` même erreur |

## GET /crm21/opportunites-clients — 2f777bfd-880f-440c-ad3a-73e55f9497a9 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, vue=toutes | 200 | **422** | `rows` = 28 dossiers (aucun filtre broker : OK) ; `out` : Syntax error ";" (pos 99) |
| admin, vue=actions | 200 | **422** | idem, `rows` = 28 ; `out` même erreur |
| Imane (sans vue) | 200 | **422** | `rows` = 12, SQL `where src_c2ljvedgo8rjnjz = 'Imane'` : filtre serveur OK ; `out` même erreur |
| Salma (sans vue) | 200 | **422** | `rows` = 13, filtre `= 'Salma'` OK ; `out` même erreur |
| non-membre | 403 | 403 | `g403` |

Remarque données : 1 dossier sans broker (id 35) et 1 dossier broker « Omar » (non membre) ne sont visibles que de l'admin.

## GET /crm21/opportunite-client — de5113ec-d1ea-4e34-b716-09a94fa878f3 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, id=23 | 200 | **400** | step `contact` : INVALID_VALUE « A value does not match the type of its column » — cause « invalid input syntax for type bigint: "null" » |
| Imane, id=23 (le sien) | 200 | **400** | même erreur au step `contact` |
| Imane, id=6 (Salma) | 404 | 404 | `g404` « Dossier introuvable ou non autorisé. » |
| Salma, id=6 (le sien) | 200 | **422** | `rows`=1, `contact` OK (1 ligne) ; `out` : Syntax error ";" (pos 99) |

Bug 2 : le `runIf` de `contact` (`$exists(...contacts_id) and $string(...) != ''`) est vrai quand `contacts_id` vaut `null` ($exists(null)=true, $string(null)="null"), d'où le filtre `id = "null"`. 14 dossiers sur 28 n'ont pas de contact lié.

## GET /crm21/propositions — eb230b7f-2109-4490-abe0-cd3b0f7eb306 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, clientId=6 | 200 | **422** | `rows`=1, `props`=0 (aucune proposition), `biens` skipped ; `out` Syntax error ";" (pos 99) |
| Imane, clientId=23 | 200 | **422** | `props`=0 ; `out` même erreur |
| Imane, clientId=6 | 404 | 404 | `g404` |

## GET /crm21/historique — 58c3ad63-676c-4dd4-9eb9-9a1d30883a9a — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, clientId=23 | 200 | **422** | `events`=0, `acts`=0 ; `out` Syntax error ";" (pos 99) |
| Imane, clientId=23 | 200 | **422** | idem |
| Imane, clientId=6 | 404 | 404 | `g404` |

## GET /crm21/rapprochements — ccb4c0f4-9455-4c5f-9752-7a1d7da87542 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, clientId=23 | 200 | **422** | `rows`=1, `biens` actifs=22, `props`=0 ; `out` Syntax error ";" (pos 99) |
| Imane, clientId=23 | 200 | **422** | idem |
| Imane, clientId=6 | 404 | 404 | `g404` |

## GET /crm21/biens — 09736918-6f90-467a-949a-e23e7ebfbf2c — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | **422** | `rows`=43 biens ; `out` Syntax error ";" (pos 99) |
| Imane | 200 | **422** | `rows`=43 (catalogue partagé, OK) ; `out` même erreur |

## GET /crm21/bien — 80209b05-5ef3-4f1c-b2c2-a7f3267da967 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin, id=9 | 200 | **422** | `rows`=1 (bureau, Location, Actif, 5 photos avec url http), `props`=0 ; `out` Syntax error ";" (pos 99) |
| Imane, id=9 | 200 | **422** | idem |

## GET /crm21/creneaux — b08bb832-00dd-47d7-9506-f7d94c9c3ee5 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin (sans jour) | 200 | **422** | `rows`=2 RDV broker Majid ; `out` Syntax error ";" (pos 99) |
| Imane (sans jour) | 200 | **422** | `rows`=0 ; `out` même erreur |

## GET /crm21/activites — 498fedaf-5b14-4203-91f3-3443dfc685f4 — problems : `out` Syntax error ";" (char 99)

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | **422** | `mesoc` skipped, `rows`=55 activités ; `out` Syntax error ";" (pos 99) |
| Imane | 200 | **422** | `mesoc`=12 dossiers, `rows`=55 ; `out` même erreur |
| Salma | 200 | **422** | `mesoc`=12 dossiers, `rows`=55 ; `out` même erreur |

Remarque : `rows` lit toute la table Activités sans filtre broker (le cloisonnement se fait seulement dans `out`). Les activités historiques ont `crm_broker` et `opportunit_s_clients_id` vides : un broker en verra probablement 0 une fois `out` corrigé.

## Données de période horaire

`per` renvoie 1 seule ligne (2027-02-07 → 2027-03-14, décalage 0) ; hors de cette plage le décalage par défaut est +60 min (UTC+1), cohérent avec Africa/Casablanca.
