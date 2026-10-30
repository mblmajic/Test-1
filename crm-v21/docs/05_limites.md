# 05 — Limites restantes

| # | Limite | Cause exacte | Impact | Prochaine action |
|---|---|---|---|---|
| L1 | Pas d'écriture conditionnelle atomique | SmartDB `updateRecord` = par id, sans condition ni nb de lignes ; pas de SQL ; `smartdb_create_table` ignore `pk:true` sur une colonne texte (colonne `cle` créée non-PK) ; `createRecord` avec `id` explicite → `BAD_REQUEST "Column \"Id\" is read-only"` (API Studio) et id ignoré (outil MCP) ; aucun paramètre UNIQUE dans `smartdb_create_column`/`update_column` ; `smartdb_sync_constraints` → « Column … not found in Postgres — skipping » pour toutes les colonnes | « Me l'affecter » et anti-doublon des propositions ne peuvent pas être garantis en concurrence | voir décision GATE 2b |
| L2 | Comptes brokers absents | Salma, Imane sans compte plateforme ; Omar inactif sans email | Recette broker uniquement par claims simulés | L'utilisateur invite les comptes dans Tybot |
| L3 | Dates du Ramadan 2027 approximatives | dates officielles non publiées | décalage horaire faux ±1 jour en bordure | saisir les dates officielles dans CRM21 Périodes horaires (`confirme`) |
| L4 | Faille d'identité CRM1 | rôle « Admin Domaine » = admin dans /crm1/ | tout utilisateur CRM1 voit tout | hors périmètre (invariant), à corriger par le responsable CRM1 |
| L5 | Logo officiel absent | PDF de charte non fourni | emplacement vide | fournir le PDF |
| L6 | Push GitHub refusé (403) | accès GitHub de la session | travail commité localement | reconnecter GitHub |
| L7 | Brouillon de test `POST /crm21/test-verrou` | outils de suppression désactivés | aucun (jamais publié) | supprimer dans API Studio |
