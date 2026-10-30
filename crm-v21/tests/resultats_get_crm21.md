# Résultats des tests GET CRM21 — passe 2 (2026-10-30, ~19:00)

Mêmes règles : brouillons uniquement (save_endpoint upsert), test_endpoint skipAuth sans allowWrites, aucune publication ni écriture.
Appelants : admin (Majid), Imane (broker « Imane »), Salma (broker « Salma »), non-membre.
Ids : dossier 23 (Imane), dossier 6 (Salma, contact lié), bien 9.

## Passe arrêtée : nouvelle erreur bloquante commune

Les parenthèses et la garde `contact` sont bien corrigées (problems = [] à l'enregistrement). Mais **toutes** les expressions `out` qui appellent `$dh(x)` avec un montant > 0 échouent à l'exécution :

- step `out`, 422, `EXPRESSION_ERROR` — « Expression failed: The sub-picture must not contain a passive character that is preceded by an active character and that is followed by another active character » (D3086, token `formatNumber`, position 4899 dans opportunites-clients, 4824 dans opportunite-client).
- Cause : `$formatNumber($x, '#,##0', {'grouping-separator': ' '})`. Quand le séparateur de groupes devient l'espace, la virgule du motif n'est plus un séparateur et devient un caractère passif placé entre deux caractères actifs.
- Correctif possible : `$formatNumber($x, '# ##0', {'grouping-separator': ' '})`, ou plus sûr `$replace($formatNumber($x, '#,##0'), ',', ' ')`.
- `$dh` est défini dans le préambule commun des 13 expressions `out` (tous les GET sauf session et referentiels). Il est appelé via `$oc` (budgetLabel) et `$bien` (prixLabel). Il échoue dès qu'un dossier ou un bien a un montant positif.
- Comme le préambule doit être corrigé dans les 13 fichiers puis ré-enregistré, la suite de la passe n'a pas été lancée (les 422 auraient été identiques).

## Enregistrements effectués (problems)

| endpoint | id | problems |
|---|---|---|
| GET /crm21/session | f9e520db-8c1d-4b8d-9061-408ab3258557 | aucun |
| GET /crm21/referentiels | 3adc338f-4f95-40ba-9976-ed60772ace44 | aucun |
| GET /crm21/opportunites-clients | 2f777bfd-880f-440c-ad3a-73e55f9497a9 | aucun |
| GET /crm21/opportunite-client | de5113ec-d1ea-4e34-b716-09a94fa878f3 | aucun |
| propositions, historique, rapprochements, biens, bien, creneaux, activites | (ids inchangés, cf. crm21_ids.json) | non ré-enregistrés dans cette passe : la version de l'API Studio est encore celle de la passe 1 |
| opportunites-biens, opportunite-bien, accueil, equipe | — | non enregistrés |

Note : le dossier contient 15 fichiers crm21__GET_*.json, et non 19.

## GET /crm21/referentiels

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | 200, 1 item | 13 étapes, 9 actions, 3 priorités ; brokers = 3 (Majid, Salma, Imane). Majid (rôle Admin) figure dans la liste car `role = 'Broker' or broker` retient tout membre dont le champ broker est rempli |
| Imane | 200 | 200, 1 item | brokers = 1 (Imane) ; `membres` skipped |

## GET /crm21/opportunites-clients

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin vue=toutes | 200 | **422** | rows=28 ; `out` : D3086 formatNumber (ci-dessus) |
| admin vue=actions | 200 | **422** | rows=28 ; même erreur |
| Imane | 200 | **422** | rows=12 (filtre serveur Imane OK) ; même erreur |
| Salma | 200 | **422** | rows=13 ; même erreur |
| non-membre | 403 | non relancé | 403 `g403` en passe 1 (étape inchangée) |

## GET /crm21/opportunite-client

| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin id=23 | 200 | **422** | `contact` désormais **skipped** (garde corrigée, OK) ; `out` : D3086 formatNumber (budget 4 000 000) |
| Salma id=6 | 200 | **200**, 1 item | etape=Biens proposés, etapeTone=info, echeanceLabel=« mer. 4 nov. · 15:00 », enRetard=false, budgetLabel=« — » (budget null, d'où l'absence d'appel à formatNumber), aCompleter=« À compléter : budget », contactStatut=« Contact lié », surfaceLabel=« — », chambres=null, modifiable=true. L'échéance stockée 14:00Z s'affiche 15:00 (UTC+1) : cohérent |
| Imane id=23 / Imane id=6 | 200 / 404 | non relancé | le 404 `g404` d'Imane sur le dossier 6 était validé en passe 1 |

## Endpoints non relancés dans cette passe

propositions, historique, rapprochements, activites, biens, bien, creneaux, opportunites-biens, opportunite-bien, accueil, equipe : à relancer après la correction de `$dh`.
