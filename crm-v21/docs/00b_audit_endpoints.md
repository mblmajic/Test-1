# 00b — Audit des endpoints API Studio `/crm1/` (lecture seule)

Date : 2026-10-30. Périmètre : les 31 endpoints `/crm1/` du schéma `easyspace_schema` (data source SmartDB `de074ee7-7e90-4df1-bd97-6f53613204bc`).
Méthode : `list_endpoints`, puis `get_endpoint` sur les 31 (JSON complets dans `crm-v21/contracts/endpoints/crm1__<METHODE>_<chemin>.json`), puis `test_endpoint` **sur les GET uniquement** (`allowWrites:false`, `skipAuth` par défaut). Aucune écriture, aucun `save`/`publish`.
Données personnelles : le rapport ne donne que des comptes et des noms de clés.

Statut : 30 endpoints publiés, 1 brouillon (`POST /crm1/fichiers`). `problems` = `[]` pour les 31, donc aucune erreur bloquante n'est signalée par le Studio.

## 0. Tables SmartDB citées

| Id | Table |
|---|---|
| `mf37113735cdd038b` | Agents brokers internes (garde d'identité) |
| `m80adee8ba2348dfe` | Opportunités Clients (dossiers) |
| `m4bf4b323ba241e7d` | Contacts |
| `ma9b9bb062ad8b271` | Biens |
| `m13dd0abc30554ba9` | Opportunités de biens |
| `m3573c7a505385e65` | Activités (agenda) |
| `m5ba929066e4852f4` | Propositions de biens aux clients |
| `med983146d1970914` | Documents et médias CRM |
| `m638173347625af09` | Journal des événements CRM |
| `mf4841a083ad93de7` | Affectations gestionnaire du bien (lue par les fiches) |
| `mbe5ed5789ee26ddc` | Annonceurs immobiliers (lue par les fiches) |

## 1. Garde d'identité commune (les 31 endpoints)

Les 31 endpoints commencent par les mêmes 3 étapes :

1. `team` : `listRecords` sur `mf37113735cdd038b`, **limit 20**, sans filtre (colonnes `id, broker, actif, email_production, crm_broker_valeur`).
2. `identity` (JSONata) :
   - `email = lowercase(auth.claims.email)` ;
   - `admin = auth.claims.sub = '2ed8af88-0a8d-44dc-9b78-852f3c450cd5'` (UUID codé en dur) **ou** `'dom-admin' in auth.claims.roles` **ou** `'Admin Domaine' in auth.claims.roles` ;
   - `rep` = première ligne dont `lowercase(email_production) = email` et `actif = true|'true'` ;
   - `broker = admin ? 'Majid' : rep.crm_broker_valeur` ; `allowed = admin or exists(rep.id)`.
3. `access` : 403 « Votre compte n'est pas associé à un broker actif… » si `allowed` est faux.

Le filtrage par broker se fait ensuite par égalité de **texte** entre le libellé du broker du dossier et `crm_broker_valeur`.

Ce que les tests ont montré :
- Sans claims : 403. Avec `{"email":"majidbens@gmail.com"}` seul : **403**, parce que la ligne broker « Majid » a `actif=false`. Majid n'est admin que par son `sub` ou par un rôle.
- Avec `sub` admin : 200, `{admin:true, broker:'Majid', email, userId, allowed:true}`.
- Avec `roles:["dom-admin"]` sans email : 200, admin, `email` vide.
- Avec l'email d'un broker actif (simulé) : 200, `admin:false` et le broker associé ; ses listes sont bien filtrées (voir §3).

## 2. Tableau récapitulatif

Légende de la garde : **G** = garde commune ; **G+own** = G plus contrôle de propriété sur le dossier (`getRecord`, puis broker du dossier = broker de l'appelant, ou admin) ; **G+filtre** = G plus `where broker = identity.broker` (sauf admin).
Toutes les écritures ont `problems: []`.

| Méthode | Chemin | Tables (op.) | Garde identité | Filtres (test/visibilité) | Réponse (clés) | Test GET (admin sauf mention) | Faiblesses |
|---|---|---|---|---|---|---|---|
| GET | `/crm1/session` | brokers (list) | G | – | `items[0]{admin,broker,email,userId,allowed}` | 403 sans claims ; 403 email seul ; 200 sub admin ; 200 broker | pas de liste de rôles ; admin → broker « Majid » (inactif) |
| GET | `/crm1/referentiels` | brokers | G | brokers `actif=true` strict | `items[0]{statutsClients[13],typesActivites[5],brokers[{nom,valeur}]}` | 200, 13 statuts, 5 types, 2 brokers | `typesActivites` (Note) ≠ types acceptés par POST activites (Tâche) |
| GET | `/crm1/accueil/synthese` | clients (query) | G+filtre | exclut `nom ^RECETTE CRM1` | `items[0]{opportunites,actions,retards,broker}` | 200 : 27 / 18 / 6 (28 lignes lues) | pageSize 500 sans pagination |
| GET | `/crm1/accueil/actions` | clients (query) | G+filtre | RECETTE ; `action≠''` ; hors Gagné/Perdu/En Pause | `items[]{id,nom,broker,statut,action,echeance,telephone,quartier,typeBien,transaction,budget,contactId,notes,enRetard}` | 200, 18 items | tri `^(<echeance)` sur des chaînes (vides en tête) |
| GET | `/crm1/accueil/dossiers-chauds` | clients (query) | G+filtre | RECETTE ; statuts RDV Visite Validé…Finalisation | idem actions | 200, 1 item | – |
| GET | `/crm1/accueil/biens-a-actualiser` | biens (query) | G (**sans filtre broker**) | `action≠''` ou statut `À confirmer` ; **pas de filtre test** | `items[]{id,nom,broker,statut,typeBien,prix,surface,quartier,ville,adresse,transaction,photos,photoSource,estMonBien,action,echeance,notes}` | 200, 12 items sur 43 biens | tous les biens visibles par tous |
| GET | `/crm1/activites` (Agenda) | activités (query) | G+filtre (`broker` de l'activité) | `test=true` exclu | `items[]{id,nom,broker,date,fin,type,statut,clientId,bienId,appreciation,objections,prochaineEtape}` | admin : 200, 53 items ; broker simulé : **0** | les 53 activités ont `broker` vide et `clientId` null, donc l'agenda d'un broker est vide |
| GET | `/crm1/biens` | biens (query) | G (sans filtre broker) | aucun | mêmes clés que biens-a-actualiser | 200, 43 items (22 Actif / 21 Inactif ; 1 nom RECETTE) | test non filtré ; `photos` exclut les URLs avito mais `photoSource` les expose |
| GET | `/crm1/bien?id=` | biens (query), affectations (get), annonceurs (get) | G (sans own) | – | clés du bien + `gestionnaire,contactGestionnaire,telephoneGestionnaire,emailGestionnaire,etatGestionnaire,roleGestionnaire` | 200, 1 item (id 1), pas d'affectation | coordonnées du gestionnaire visibles par tout broker ; annonceur lu en entier puis jamais utilisé ; le nom du bien contient un téléphone (donnée) |
| GET | `/crm1/opportunites-biens` | opp. biens (query) | G (sans filtre broker) | aucun | clés bien sans `photoSource` | 200, 33 items (10 sans broker ; 1 RECETTE) | `photos` absent du select, donc toujours `[]` ; test non filtré |
| GET | `/crm1/opportunite-bien?id=` | opp. biens, affectations, annonceurs | G (sans own) | – | comme fiche bien | 200, 1 item (id 121) | idem fiche bien |
| GET | `/crm1/opportunites-clients` | clients (query) | G+filtre | RECETTE | `items[],pageInfo` ; item = actions + `waUrl` | admin 200, 27 ; broker simulé 200, 12 | `waUrl` construit côté serveur (préfixe 212) |
| GET | `/crm1/opportunite-client?id=` | clients (query) | G+filtre | RECETTE | idem | 200, 1 item (id 12) | si `id` est absent, la requête renvoie la liste entière (pas de 400) |
| GET | `/crm1/contacts` | clients (query) — **pas la table Contacts** | G+filtre | RECETTE | `items[]{id,nom,telephone,broker,lien}` | 200, 27 items | « contacts » = dossiers ; aucune déduplication par téléphone |
| GET | `/crm1/historique?clientId=` | clients (query, garde), journal (list 500), activités (list 500) | G+filtre (404 si non visible) | `test_crm1`, `crm_est_test` | `items[]{id,date,titre,texte,statut}` | admin id 12 : 200, 0 ; broker id 12 (autre broker) : **404** ; broker id 2 : 200, 0 | ne lit que `type_dossier='client'` (les RDV journalisés en `activite` sont absents) ; pas de tri par date |
| GET | `/crm1/medias?clientId=` | clients (get, own), médias (list 500) | G+own | `test_crm1` | `items[]{id,name,url,type,date,size}` | admin 200, 0 ; broker non propriétaire **403** | URL de fichier renvoyée telle quelle |
| GET | `/crm1/propositions?clientId=` | clients (get, own), propositions (list 500) | G+own | `test_crm1` | `items[]{id,nom,statut,date,retour,bienId}` | admin id 12 : 200, 0 | – |
| GET | `/crm1/rapprochements` | clients (query), biens (query) | G+filtre (clients) | clients RECETTE non filtrés ; biens test non filtrés | `{items[]{id,clientId,client,bienId,bien,prix,quartier,motif}, methode}` | 200, 53 suggestions, 13 biens distincts, `methode` = « Filtre de critères, sans score IA » | voir §4.6 |
| POST | `/crm1/activation-bien` | opp. biens (get/update), biens (update), journal (create/update) | G + **admin seul** | – | 201 `{id,operationId,message}` ; 409 sans bien lié | non testé (écriture) | 2 updates non atomiques |
| POST | `/crm1/activites` | clients (get), journal, activités (create) | G+own (client) | `crm_est_test` | 201 `{id,operationId,message}` | non testé | `jour+heure` concaténés avec **`+01:00` en dur** ; aucune idempotence |
| PATCH | `/crm1/activites` | activités (get/update), journal | G + own (`crm_broker`) | – | 200 `{id,operationId,message}` | non testé | bloqué pour tout non-admin sur les données actuelles (`crm_broker` vide) ; garde `prix` sans objet ici |
| PATCH | `/crm1/biens` | biens (get/update), journal | G + own (`src_c9w1scpswzkjl7g`) | – | 200 | non testé | dernier écrivain gagne ; `echeance` non validée |
| POST | `/crm1/communications` | clients (get), journal (create) | G+own | – | 201 | non testé | **journalisation seule, aucun envoi** (§4.7) |
| POST | `/crm1/fichiers` (**brouillon**) | clients (get), storeFile, médias (create) | G+own | – | 201 `steps.file` | non testé | §4.1 |
| POST | `/crm1/leads` | journal, contacts (create), clients (create), journal | G | – | 201 | non testé | §4.2 |
| POST | `/crm1/notes` | clients (get), journal (create) | G+own | `test_crm1` | 201 | non testé | une seule écriture (correct) |
| POST | `/crm1/opportunites-biens` | journal, opp. biens (create) | G | test → `table_origine='RECETTE_CRM1'` | 201 | non testé | ce marqueur n'est filtré par aucun GET |
| PATCH | `/crm1/opportunites-biens` | opp. biens (get/update), journal | G + own (`src_cazse08x5syk1gn`) | – | 200 | non testé | broker non modifiable (§4.4) |
| PATCH | `/crm1/opportunites-clients` | clients (get/update), journal | G+own | – | 200 | non testé | statut validé, `echeance` et téléphone non validés |
| PATCH | `/crm1/propositions` | propositions (get/update), clients (get), journal (create) | G + own (via le client) | – | 200 `{id,message}` | non testé | écrit **avant** de journaliser ; pas de `operation_id`, `user_id` ni `avant` ; pas de regex sur l'id |
| POST | `/crm1/propositions` | clients, biens (get), propositions (list + create), journal | G+own | `test_crm1` | 201 ; 409 si doublon | non testé | §4.3 |

### Schéma commun aux écritures

Schéma « transaction journalisée » (activation-bien, POST/PATCH activites, PATCH biens, leads, POST/PATCH opportunites-biens, PATCH opportunites-clients, POST propositions) :
1. Après la garde : `op.id = $millis() & '-' & sub`, puis validations.
2. `begin` : `createRecord` dans le journal `m638173347625af09` avec `resultat:'À reprendre'`, `operation_id`, `user_id`, `email_auteur`, `broker`, `type_dossier`, `dossier_id`, `source:'SuperAPP_easyspace_CRM1'`. Les PATCH ajoutent `avant=$string(record)`.
3. `write` : écriture métier.
4. `finish` : `updateRecord` du journal avec `resultat:'Réussi'`, `apres=$string(write)`, et `dossier_id` réécrit (`input.body.clientId` ou `write.id`).
5. `done` : réponse.

Si l'étape 3 échoue, le journal garde « À reprendre ». C'est détectable, mais **rien n'est annulé**.

Exceptions :
- `notes` et `communications` : une seule écriture (dans le journal), donc atomique.
- `PATCH propositions` : écriture puis journal, sans `begin`.
- `fichiers` : aucun journal.

## 3. Résultats de test notables (GET)

- Toutes les requêtes `query` lisent au plus 500 lignes (`pageSize:500`) et toutes ont `hasNextPage:false` aujourd'hui (28 dossiers clients, 43 biens, 33 opportunités de biens, environ 55 activités).
- **Isolation par broker vérifiée** :
  - un broker simulé voit 12 dossiers sur 28 ;
  - il reçoit 404 sur l'historique d'un dossier d'un autre broker, et 403 sur ses médias ;
  - il voit **tous** les biens et toutes les opportunités de biens (aucun filtre).
- L'agenda d'un broker est vide (0), parce qu'aucune activité existante n'a de `broker` ni de `clientId`. L'historique des dossiers testés est vide (0 événement de journal, 0 activité liée).
- Données de test : 1 dossier client `RECETTE CRM1` est bien exclu. En revanche 1 bien et 1 opportunité de bien « RECETTE » restent visibles dans les listes.
- Fuseau en lecture : les datetimes sortent avec un décalage Casablanca correct. On voit `+01:00` en général, et `+00:00` pour une activité de février 2026 (période du Ramadan). Le moteur de requête applique donc bien `Africa/Casablanca`. En base, les valeurs sont en UTC (`…Z`).

## 4. Points examinés spécialement

### 4.1 `POST /crm1/fichiers` (brouillon)
- Étapes : garde → `getRecord` du client par `input.query.clientId` → contrôle de propriété (403) → **`storeFile`** (`field:'file'`, `folder:'crm1'`, `accept:'image/*,application/pdf,audio/*'`, `maxSizeMb:15`) → `createRecord` dans `med983146d1970914` (`storage_key`, `url_fichier`, `nom_fichier`, `mime_type`, `taille_octets`, `categorie` Audio/Photo/Document déduite du MIME, `opportunit_s_clients_id`, `email_auteur`, `date_depot=$now()`, `etat_traitement:'Déposé'`) → 201 avec le corps `steps.file`.
- Statut `draft`, `published:null`, `problems:[]`. Le blocage n'est donc pas technique ; la définition ne dit pas pourquoi l'endpoint est resté en brouillon. Motifs probables visibles dans la définition :
  - (a) pas de validation regex de `clientId` (contrairement aux autres écritures) ;
  - (b) `storeFile` puis `createRecord` ne sont pas atomiques : un fichier orphelin reste stocké si l'insertion échoue ;
  - (c) aucune entrée au journal ni drapeau `test_crm1`, alors que `GET /medias` filtre sur `test_crm1` ;
  - (d) la réponse renvoie l'objet de stockage brut (`key`, `url`) ;
  - (e) le test d'un upload réel exige `allowWrites`, il n'a donc pas été fait.
- Conséquence : la page ne peut pas déposer de fichier aujourd'hui, et `GET /medias` reste vide.

### 4.2 `POST /crm1/leads` (multi-tables, idempotence)
- Ordre : garde → `op` → validations (`nom` 2–150 caractères, `transaction ∈ {Achat, Location}`, `budget` entre 0 et 1e10, `broker` connu si l'appelant est admin) → **journal `begin`** (`À reprendre`, `test_crm1`) → **Contact** `m4bf4b323ba241e7d` (`libelle`, nom, téléphone, `crm_telephone_normalise` = téléphone **brut**, `crm_cle_creation=op.id`) → **Opportunité client** `m80adee8ba2348dfe` (nom, broker = celui de l'appelant ou celui choisi par l'admin, `statut 'Nouveau'`, téléphone, transaction, budget loyer/achat selon la transaction, quartier, lien `pmv6m9j8dh2qj_contacts_id`, `crm_cle_creation`) → journal `finish`.
- **Pas idempotent** :
  - `op.id` est généré par le serveur, pas fourni par le client ;
  - aucune recherche préalable par téléphone ou par `crm_cle_creation` ;
  - un double clic ou une relance réseau crée 2 contacts et 2 dossiers.
- **Pas atomique** : si la création du dossier échoue, le contact reste orphelin et le journal reste « À reprendre ».
- `test=true` n'est enregistré **que dans le journal**. Le contact et le dossier de test ne portent aucun marqueur ni préfixe `RECETTE CRM1`, donc ils apparaîtront comme réels.
- Un admin qui ne choisit pas de broker crée le lead sous « Majid », un broker inactif.

### 4.3 `POST /crm1/propositions` (doublons)
- Clé d'unicité applicative : `cle_proposition = clientId-bienId`. `listRecords limit 1` sur cette clé, puis 409 « déjà proposé ».
- Il s'agit d'une **lecture puis écriture sans verrou** : deux requêtes simultanées passent toutes les deux le contrôle. Il faut une contrainte d'unicité SmartDB sur `cle_proposition` ; sa présence n'a pas pu être vérifiée en lecture seule.
- Une proposition de test (`test_crm1=true`) occupe la même clé et bloque ensuite la vraie.
- Le bien est seulement vérifié comme existant (`getRecord`) : rien sur son statut Actif ni sur la cohérence de la transaction.
- L'écriture renseigne `broker` (= broker du dossier), `email_auteur`, `date_proposition=$now()`, `statut 'Proposé'`, `provenance 'Broker'`, `operation_id`, puis le journal (`type_dossier 'client'`).

### 4.4 « Me l'affecter »
- **Aucun endpoint n'existe pour cela.** `PATCH /crm1/opportunites-biens` ne modifie que `crm_notes_suivi`, `crm_echeance`, `crm_prochaine_action` et `src_cwqc3dj4cewpssd` (prix). La colonne broker `src_cazse08x5syk1gn` n'est pas modifiable.
- La garde `owner` exige `admin` ou `record.broker = identity.broker`. Les **10 opportunités de biens sans broker sur 33** ne sont donc modifiables par aucun broker non-admin.
- `PATCH /opportunites-clients` ne modifie pas non plus le broker.
- Pour mettre en place « Me l'affecter », il faut un endpoint dédié avec écriture **conditionnelle** (`broker IS NULL`). `updateRecord` n'a pas de clause conditionnelle : il faudrait relire après l'écriture, ou utiliser une opération `query` avec un `where`, plus une entrée au journal avec `avant`.

### 4.5 `GET /crm1/contacts`
- Ne lit **pas** la table Contacts : il projette les Opportunités Clients visibles (`id, nom, telephone, broker, lien:'/client?id=<id>'`).
- Filtrage par broker et exclusion RECETTE : corrects (admin 27 items).
- Un même client présent dans plusieurs dossiers apparaît plusieurs fois, sans déduplication par téléphone ni lien vers `contactId`.

### 4.6 `GET /crm1/rapprochements` (méthode)
- Pour chaque dossier non clos (hors Gagné/Perdu/En Pause) visible par l'appelant, l'endpoint retient les biens dont :
  - `lowercase(transaction)` est égal à celle du client ;
  - `lowercase(typeBien)` est égal à celui du client ;
  - `statut` est « Actif » ou « Active ».
- Aucun score, budget, quartier ni surface n'est pris en compte. Le `motif` est fixe : « Type et transaction concordants ; budget et disponibilité à confirmer ». `methode` = « Filtre de critères, sans score IA ».
- Résultat : 53 suggestions sur 13 biens distincts. Certains dossiers reçoivent 9 suggestions identiques par type.
- **Défaut de vocabulaire** :
  - les biens utilisent `Vente`, les clients `Achat`, donc **aucun client acheteur n'est jamais rapproché** ;
  - les types `Local commercial` (client) et `local` / `local commerciale` (bien) ne correspondent pas.
- Les biens déjà proposés au client (table Propositions) ne sont pas exclus. Les biens de test ne sont pas filtrés.

### 4.7 `POST /crm1/communications`
- **Journalisation seule, aucun envoi réel.** Une seule écriture dans le journal : `libelle/type_evenement 'Contact préparé'`, `resume = "<canal> préparé ; envoi ou appel non confirmé."`, `resultat 'Réussi'`, `type_dossier 'client'`.
- Canaux acceptés : Téléphone, WhatsApp, Email, SMS, Telegram.
- L'envoi effectif reste côté client (lien `waUrl` wa.me fourni par les GET de dossiers). L'endpoint ne prend ni le message ni le statut de l'envoi.

### 4.8 `GET /crm1/session`
- Réponse : `{items:[{admin, broker, email, userId, allowed}]}`. Le 403 renvoie `{error}`.
- Côté rôle, il n'y a qu'un **booléen `admin`**. Pas de tableau `roles`, de libellé ni d'id de ligne broker, ni d'`actif`.
- Admin = `sub` codé en dur, ou rôle `dom-admin` / `Admin Domaine`. L'admin est forcé sur `broker:'Majid'`, alors que la ligne Majid est inactive.
- Un admin authentifié par rôle sans email obtient `email:''`, que les écritures recopient ensuite dans `email_auteur`.

## 5. Faiblesses et risques

### Sécurité et confidentialité
0. **CRITIQUE — tout compte connecté est admin.** D'après l'invariant de `crm-v21/CLAUDE.md`, *tous* les comptes plateforme portent le rôle « Admin Domaine ». Or la garde de CRM1 accorde `admin=true` dès que `'Admin Domaine' in auth.claims.roles`.

   En production réelle (JWT avec rôles), chaque broker est donc admin :
   - il voit les 27 dossiers de tous les brokers ;
   - il peut modifier n'importe quel dossier ;
   - il peut activer des biens ;
   - il crée sous le broker « Majid ».

   L'isolation par broker vérifiée au §3 n'a été observée qu'avec des claims simulées **sans** rôle. Elle est sans effet dès que le rôle est présent. Pour la V2.1, il faut déterminer l'admin uniquement via le référentiel brokers (colonne dédiée) rapproché de `auth.claims.email`, jamais via `roles`.
1. **Admin codé en dur** : l'UUID `sub` est recopié dans les 31 définitions, et le broker de l'admin est fixé à « Majid ». Changer d'administrateur impose de republier 31 endpoints. La confiance dans `auth.claims.roles` (`dom-admin`, `Admin Domaine`) dépend entièrement de l'émetteur du JWT.
2. **Identité par email** : l'appariement se fait sur un email en minuscules contre `email_production`. La table brokers est lue avec **limit 20** et sans filtre, donc au-delà de 20 brokers certains seront refusés sans message clair. La propriété des données repose sur l'égalité d'un **libellé texte** de broker (`crm_broker_valeur`) : renommer un broker fait perdre l'accès à ses dossiers.
3. **Pas de cloisonnement des biens** : biens, fiche bien, opportunités de biens et biens à actualiser sont visibles par tous les brokers, y compris le téléphone et l'email du gestionnaire (affectation). La fiche lit aussi l'**annonceur complet** sans l'utiliser.
4. **Le journal contient des données personnelles** : `avant` et `apres` stockent `$string(record)`, c'est-à-dire l'enregistrement complet avec téléphone et notes. Ces données personnelles sont ainsi dupliquées dans le journal.
5. Fiche `opportunite-client` sans `id` : la requête renvoie toute la liste visible, au lieu d'un 400.
6. `POST /fichiers` : URL de stockage renvoyée et lue telle quelle par `GET /medias` ; pas de validation regex de `clientId`.

### Atomicité
7. Les écritures multi-étapes ne sont pas transactionnelles :
   - leads : contact puis dossier ;
   - activation-bien : bien puis opportunité de bien ;
   - fichiers : stockage puis enregistrement.

   Le journal « À reprendre » signale l'échec, mais aucun processus de reprise n'est défini.
8. `PATCH /propositions` écrit avant de journaliser : une écriture réussie suivie d'un journal en échec ne laisse aucune trace.

### Concurrence et idempotence
9. Aucun endpoint n'accepte de clé d'idempotence fournie par le client. `op.id = millis-sub` est unique par milliseconde, mais il est régénéré à chaque relance.
10. Les PATCH suivent la règle du dernier écrivain gagnant (lecture `avant`, puis `updateRecord` sans comparer `updated_at`), donc des mises à jour peuvent se perdre.
11. L'anti-doublon des propositions est une lecture puis écriture qui ne tient pas sous concurrence (voir §4.3). Les leads n'ont aucun anti-doublon.

### Fuseau horaire (Africa/Casablanca)
12. En lecture, le moteur restitue correctement les décalages (`+01:00`, et `+00:00` pendant le Ramadan).
13. `POST /activites` construit `jour + 'T' + heure + ':00+01:00'` avec un décalage **fixe** : un RDV saisi pendant le Ramadan (UTC+0) est décalé d'une heure. `date` peut aussi être fourni tel quel, sans normalisation.
14. Les `echeance` (PATCH clients, biens, opportunités de biens) sont écrites sans validation de format ni de fuseau.
15. Le tri des actions (`^(<echeance)`) se fait sur des chaînes : les échéances vides passent en tête, et des décalages différents peuvent mal ordonner les lignes.

### Données de test et cohérence
16. Les filtres de test ne sont pas homogènes :
    - les dossiers sont filtrés par préfixe de nom `RECETTE CRM1` ;
    - les activités, le journal, les médias et les propositions par un booléen ;
    - les biens et les opportunités de biens ne sont pas filtrés du tout (`table_origine='RECETTE_CRM1'` est ignoré) ;
    - les leads de test ne sont pas marqués.
17. Les référentiels et les validations ne concordent pas :
    - `typesActivites` contient Note mais pas Tâche, alors que POST activites accepte Tâche et refuse Note ;
    - la transaction vaut Vente côté biens et Achat côté clients ;
    - le statut d'activité « Programme » est sans accent.
18. Les données actuelles neutralisent l'agenda et l'historique : les activités n'ont ni broker ni client, donc l'agenda d'un broker est vide et `PATCH /activites` est impossible pour un non-admin. L'historique ne lit que `type_dossier='client'`, alors que les RDV sont journalisés en `activite`.
19. `GET /opportunites-biens` et la fiche correspondante : `photos` n'est pas sélectionné, donc la valeur est toujours vide.
20. Les gardes `prix < 0` présentes dans PATCH activites et PATCH opportunites-clients sont du code mort : ces endpoints n'acceptent pas de champ prix.
