# 00 — Audit ciblé SuperAPP CRM easyspace V2.1

Date : 2026-10-30 · Méthode : lectures par les outils MCP (aucune écriture), décompression des maquettes, captures Playwright.
Détails : [00a_audit_maquettes.md](00a_audit_maquettes.md) · [00b_audit_endpoints.md](00b_audit_endpoints.md) · définitions brutes : `contracts/endpoints/crm1__*.json` (31).

## 1. Entrées

| Fichier attendu | État | Effet |
|---|---|---|
| Prototype v2 (mobile) | ✅ `inputs/CRM_EasySpace_Prototype_v2_1.html` | — |
| Mobile Claude Design | ✅ lu depuis l'artifact WSbzKdGLYf5Lf2tDgV4SQ4 | Code identique au prototype (cadre fixe 390×844), **pas responsive** |
| Desktop Claude Design | ✅ lu depuis l'artifact FjZbdoQX48ASCDAskgCiF6 | — |
| Easy_Space_Identite_Visuelle_Fondatrice.pdf | ❌ **absent** | Logo officiel indisponible : emplacement laissé vide. Palette reprise du prompt (identique aux maquettes). |
| Dossier_Livraison_…CRM1_2026-10-30.zip | ❌ **absent** | Remplacé par la lecture directe de l'état réel (endpoints, tables, pages). Limites CRM1 « connues » non lues. |
| PROMPT_DESIGN.md | ⚠️ fourni dans le message, pas en fichier | Utilisé tel quel à l'étape 4. |

## 2. Règles MCP qui contraignent le projet
- Flux : SmartDB → endpoint API Studio (brouillon → test → publication) → page. Le navigateur appelle `/run/easyspace_schema/<path>` (chemin relatif obligatoire, sinon le jeton utilisateur n'est pas transmis).
- Réponses `{items:[…]}`, clés camelCase plates, nombres en nombres, dates ISO ; connecteur SmartDB renvoie tout en texte → helpers `$s/$n/$b/$d`.
- **La sécurité est dans l'endpoint**, la page ne fait que masquer. `listRecords` lit avec la connexion de service.
- Opérations SmartDB disponibles : `query`, `listRecords`, `getRecord`, `aggregate`, `createRecord`, `updateRecord` (**par id uniquement, sans condition ni nombre de lignes modifiées**), `deleteRecord`. **Pas de SQL ni de transaction** sur SmartDB.
- Base `SuperAPP_easyspace_CRM1` (pmvv68h6de6cr) et base Biens = **Postgres natif** → `smartdb_sync_constraints` (UNIQUE) utilisable.
- Pages : catalogue `get_catalog`, `validate_page` → `audit_page` → `save_page` → `check_page` → `screenshot_page` (seuls les endpoints publiés répondent en capture).

## 3. Existant vérifié
- Workspace 35 « Gestion Biens & CRM » : une seule app, **Easy Space CRM1**. **Aucune app ni endpoint CRM2** (rien à réutiliser d'une tentative précédente).
- Endpoints : 31 `/crm1/` (18 GET, 8 POST, 5 PATCH), 30 publiés, `POST /crm1/fichiers` en brouillon, `problems: []` partout.
- Volumes : Opportunités clients 28 · Biens 43 · Opportunités de biens 33 · Activités 55 · Propositions 1 · Journal 16 · Médias 0.
- Relations doublées : « Contact lié » (historique) **et** « Contact principal CRM1 » sur Opportunités clients ; « Bien lié » **et** « Bien principal CRM1 » sur Opportunités de biens → deux sources possibles pour le même lien, à réconcilier (lecture : principal CRM1 sinon historique).
- n8n : « Telegram — Alertes CRM — V2 » **en production** (envoie toutes les 15 min les alertes « À envoyer »). Aucun workflow d'alerte « modification hors responsable ». Workflows « CRM Mobile — M0/M1 » = recette ancienne, inactifs.

## 4. Comptes et identité (constat bloquant)
| Broker (référentiel) | actif | email_production | Compte plateforme ? |
|---|---|---|---|
| Salma | oui | salmanakra291@gmail.com | ❌ aucun compte |
| Imane Jarmoune | oui | imane.jarmouni@tython.org | ❌ aucun compte |
| Omar Ber | **non** | **vide** | ❌ |
| Majid Benslimane | **non** | majidbens@gmail.com | ❌ (le compte plateforme est majid@tybotflow.com) |

- 9 comptes plateforme + 1 invitation, **tous « Admin Domaine »**. Aucun ne correspond à un broker actif.
- **Faille CRM1** : `/crm1/session` et toutes les gardes considèrent admin quiconque a le rôle `dom-admin`/« Admin Domaine » → en production, **tout utilisateur connecté est admin** et voit tous les dossiers et coordonnées. Le cloisonnement broker ne fonctionne que dans les tests sans rôle.
- Conséquence : V2.1 ne peut **pas** utiliser `auth.claims.roles`. Le rôle doit venir d'un référentiel serveur (email de session → membre → rôle).

## 5. Faiblesses CRM1 (résumé, détail en 00b)
1. Identité/rôle (ci-dessus) — critique.
2. Activités : aucune des 53 lues n'est rattachée à un broker ni à un client → agenda broker vide, PATCH impossible.
3. Écritures multi-tables (lead) non idempotentes (`op.id` = horodatage), contact orphelin possible, pas de dédoublonnage par téléphone.
4. Propositions : anti-doublon par lecture puis écriture (pas sûr en concurrence).
5. « Me l'affecter » : **n'existe pas** ; 10 opportunités de biens sans responsable invisibles aux brokers.
6. Rapprochements : égalité transaction/type seulement ; « Vente » (biens) ≠ « Achat » (clients) → aucun acheteur rapproché ; ni budget ni quartier.
7. Fuseau : `POST /activites` ajoute `+01:00` en dur (faux pendant le Ramadan, où le Maroc est à UTC+0).
8. Journal : `avant/apres` recopient l'enregistrement complet (données personnelles).
9. Données de test : seuls les dossiers « RECETTE CRM1 » sont exclus.
10. `/crm1/fichiers` : non atomique, non journalisé, `clientId` non vérifié ; jamais testé réellement.
11. `/crm1/communications` : journalise « Contact préparé », n'envoie rien (conforme).
12. Biens / opportunités de biens : coordonnées des gestionnaires visibles par tous (acceptable si « partagé », à confirmer).

## 6. Maquettes : réel vs simulé
Tout est simulé (constantes `CLIENTS`, `BIENS`, `ACTIONS`, `MATCHS`, `LEADS`, `TEAM0`, utilisateur « Yassine B. » en dur). Pas de localStorage ; « Réinitialiser » recharge les constantes ; envois WhatsApp/appels = toast ; note vocale = compteur ; créneaux = liste fixe ; suggestion d'attribution = broker du quartier le moins chargé. Étapes : client Nouveau → Qualifié → Visites → Offre ; mandat Premier contact → Visite d'estimation → Négociation → Contrat signé → actif. **Les étapes réelles SmartDB seront relues à l'étape 2** et priment.

## 7. Périmètre retenu (proposition)
Toutes les rubriques de la section 6 du brief : Accueil, Opportunités clients (liste + fiche), Opportunités de biens (liste + fiche + activation contrôlée), Catalogue des biens (liste + fiche + proposer), Agenda (création, annulation, compte rendu), Ajout rapide (lead, RDV, opportunité de bien, note), Vue Équipe admin, page de connexion.
**Masqué / « Bientôt »** jusqu'à preuve de bout en bout : dépôt de document, note vocale + transcription, alertes de modification, partage WhatsApp autre qu'un lien `wa.me` prérempli ouvert par l'utilisateur.

## 8. Stratégie endpoints
Les endpoints `/crm1/` ne doivent pas être modifiés et portent la faille d'identité → **la V2.1 n'appelle que des endpoints `/crm21/`**, qui :
- partagent une même étape d'identité : `auth.claims.email` → table référentiel CRM21 Membres (rôle Broker/Admin, broker lié, actif) ; aucun recours à `auth.claims.roles` ;
- reprennent la logique de lecture CRM1 quand elle est saine (copie adaptée, motif documenté dans docs/01) ;
- corrigent les points 2 à 9 ci-dessus.
Estimation : ~22 GET/écritures, à figer à l'étape 2.

## 9. Améliorations proposées (problème → bénéfice → données)
| # | Problème | Bénéfice | Données / endpoints |
|---|---|---|---|
| A1 | Tout connecté est admin | Cloisonnement réel broker | table CRM21 Membres + garde commune |
| A2 | « Me l'affecter » absent / non atomique | Un seul gagnant garanti | table CRM21 Verrous (UNIQUE `cle`) : insertion = victoire, puis mise à jour du responsable |
| A3 | Doublons de propositions | Une proposition par (client, bien) | UNIQUE sur `cle_proposition` (table Propositions, Postgres) — sinon table de verrous |
| A4 | Lead multi-tables fragile | Reprise sans doublon | clé de requête `idempotencyKey` (envoyée par le formulaire) + recherche préalable contact par téléphone normalisé |
| A5 | Rapprochement vide | Suggestions utiles, méthode affichée | Achat↔Vente, transaction, type, budget ±15 %, quartier ; critères comparés renvoyés et affichés |
| A6 | Fuseau en dur | RDV justes toute l'année | conversion Africa/Casablanca côté serveur avec table des périodes UTC+0 (Ramadan) ; stockage avec décalage explicite ; test à cheval sur minuit |
| A7 | Agenda broker vide | Agenda personnel exact | RDV V2.1 toujours rattachés broker + opportunité ; rattachement de l'existant = migration (GATE 6) |
| A8 | Créneaux libres fictifs | Créneaux réels | calcul depuis les Activités du broker du jour (8h–20h, pas de 30 min) |
| A9 | Photos externes cassées | Pas d'image cassée | URL photo + repli visuel (initiales/type) |
| A10 | Interlocuteurs | « Vérifié » / « À confirmer » visibles | depuis Affectations des gestionnaires (affectation principale vs à confirmer) |
| A11 | Journal trop bavard | Moins de données personnelles copiées | `avant/apres` limités aux champs modifiés |

## 10. Risques
- **R1 bloquant pour la recette réelle** : aucun broker actif n'a de compte plateforme → la V2.1 ne peut être testée qu'avec des claims simulés tant que les comptes ne sont pas créés/rapprochés (action humaine dans Tybot ; l'outil `smartdb_*` ne crée pas de compte).
- R2 Omar : inactif sans email → correction = renseigner son email et créer son compte (GATE 6).
- R3 CRM1 et V2.1 écrivent dans les mêmes tables : chaque écriture documentée avec son effet visible dans CRM1.
- R4 La faille d'identité CRM1 reste active tant que CRM1 n'est pas corrigé (hors périmètre : invariant « ne pas modifier CRM1 ») → **à signaler au responsable**.
- R5 Logo absent ; R6 PDF/ZIP absents ; R7 alertes Telegram en production : jamais alimentées en recette.
- R8 Push GitHub refusé (403) : travail commité localement uniquement.

## 11. Décisions GATE 1 (2026-10-30)
- Rôles : **table CRM21 Membres** (email de session → rôle Broker/Admin, broker lié, actif).
- Endpoints : **tout en /crm21/** ; CRM1 intact.
- Améliorations : aucune préférence exprimée → toutes retenues (A1–A11), car A2–A6 et A9–A10 répondent aux exigences §8 du brief.
- Comptes : **l'utilisateur crée les comptes Tybot des brokers** ; recette en profils simulés en attendant, écarts listés dans docs/02.
