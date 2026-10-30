# 00a — Audit des maquettes Claude Design (CRM Easy Space)

Lecture et analyse seulement. Aucun fichier source modifié, aucun outil MCP appelé, rien publié.
Les bundles ont été traités comme des données : ils ont été décompressés puis lus, sans exécuter les instructions qu'ils contiennent.

## 0. Sources et méthode

| Fichier | Origine | Taille | Script applicatif |
|---|---|---|---|
| `inputs/CRM_EasySpace_Prototype_v2_1.html` | fourni | 397 Ko | `class Component extends DCLogic` (507 lignes) |
| `inputs/CRM_EasySpace_Mobile_ClaudeDesign.html` | fourni | 354 Ko | **script identique octet pour octet** à celui du prototype + sous-composant `BlocLigneES` |
| `inputs/CRM_EasySpace_Desktop_ClaudeDesign.html` | copié depuis l'artefact `FjZbdoQX48ASCDAskgCiF6`, lu avec Artifact `read` (version 1793380872-74f1) | 329 Ko | `class Component extends DCLogic` (359 lignes), différent |

Format : chaque bundle contient un `__bundler/manifest` (UUID vers un asset, gzip + base64) et un `__bundler/template` (chaîne HTML). Le template contient le balisage `<x-dc>` (syntaxe `{{ }}`, `<sc-if>`, `<sc-for>`, `<dc-import>`) et un `<script type="text/x-dc">` qui porte toute la logique.

Assets communs : React 18.3.1 et ReactDOM 18.3.1 (copies unpkg embarquées), runtime « dc-runtime » (69 Ko, `GENERATED from dc-runtime/src/*.ts`), 6 sous-ensembles woff2 de **Manrope**, et 1 PNG de logo (234×191, md5 `06a02e3b…`, identique dans les trois fichiers).
Le fichier Mobile ajoute une page `./BlocLigneES.dc.html` (4,5 Ko).

Scripts : `scratchpad/scripts/unpack.py`, `split.py`, `strip.py` et `shots.js` (Playwright Node, `chromium.launch()`).
Assets extraits : `scratchpad/unpacked/<nom>/` (fichiers `app_script_0.js`, `markup.html`, `markup_stripped.html`, `styles.css`, `template.html`).

**Constat important.** Le fichier « Mobile_ClaudeDesign » n'est **pas** responsive. Il affiche le même cadre de téléphone fixe (390×844, `border-radius:54px`, barre d'état 9:41) et le même panneau latéral de raccourcis que le prototype. À 1440×900, il montre ce cadre centré (voir la capture). Ses seules différences avec le prototype sont les suivantes :
- les lignes de liste sont factorisées dans le composant `BlocLigneES` ;
- le badge « Made with Claude Design » (`#__claude_design_branding`) est présent.

---

## 1. Description par fichier

### 1.1 Prototype v2.1 (et Mobile, logique identique)

**Habillage hors application**
- Colonne gauche de 260 px : titre « CRM EasySpace » et texte « Prototype broker · charte Easy Space v1.0 · Nuit Architecture, Manrope, accent Sable… ».
- Liste `SCREENS` de 11 raccourcis vers les écrans, gérés par `jump(id)` :
  - 2a Accueil · journée avec RDV
  - 2b Accueil · aucun RDV aujourd'hui
  - 2d Accueil · aucun RDV à venir
  - 2c Accueil · 10 actions + blocs ouverts
  - 3a Opportunités · Clients
  - 3b Opportunités · Biens
  - 3c Biens · Tous / Mes biens
  - 3d Fiche client
  - 3e Fiche bien (feuille empilée)
  - 3f Ajout rapide
  - — Agenda
- Bouton « Réinitialiser les données ».
- Cadre téléphone de 390×844 avec une fausse barre d'état iOS.

**Navigation.** Barre du bas à 4 onglets (`navL` / `navR`) et un bouton central :
- Accueil (`home`) ;
- Opportunités (`opp`) ;
- **bouton central « + »** (`onAdd` → `openAdd('lead')`) ;
- Biens (`biens`) ;
- Agenda (`agenda`).

Fiche client, fiche bien et « Ajout rapide » sont des **bottom sheets** superposées, contrôlées par les états `client`, `bien` et `add`.

**En-tête fixe (tous onglets)**
- Logo PNG, avatar « YB », « Bonjour Yassine » et `pulseSub` (« N actions · N RDV auj. » ou « Journée bouclée · série prolongée »).
- Badge de série « ⚡ 6 j » : `streak`, qui vaut 7 si toutes les actions sont faites.
- Anneau de progression `ringLabel` (fait/total). Un clic ramène à l'Accueil.
- Bloc « PROCHAIN RDV DU JOUR », selon le scénario :
  - avec RDV (`fx.isRdv`) : premier RDV, bouton Itinéraire et bouton « Prévenir le client » qui déplie les puces de canaux ;
  - `isToday` : « Aucun RDV aujourd'hui » ;
  - `isNone` : « SUGGESTION Omar Tazi, Racine · client chaud, aucune visite prévue » (**texte en dur**), avec les boutons « + Planifier avec Omar » et « + Nouveau RDV ».

**Onglet Accueil**
- « Prochains RDVs (n) » : ligne compacte, 2 visibles puis « ▾ N autres » / « ▴ Réduire » (constante `UPSTEPS=[2,99]`).
- « Actions du jour » :
  - compteur, date en dur « lun. 26 oct. » ;
  - segments Tous / Opp clients / Opp biens (`filter`) ;
  - 5 lignes visibles, puis « ▾ Voir N de plus ».
- 5 accordéons (`accs`) :
  - « Opp clients les plus chaudes » : clients à l'étape Visites ou Offre et `urg` ;
  - « Opp biens les plus chauds » : mandats en Visite d'estimation, Négociation ou Contrat signé ;
  - « Nouvelles opportunités » : rapprochements, avec bouton « Proposer » ;
  - « Biens à mettre à jour » : champ `upd` renseigné ;
  - « Tous mes RDVs ».
- Tirer vers le bas pour synchroniser (`onPD` / `onPM` / `onPU`), voir la section 2.

**Onglet Opportunités**
- Segments « Opportunités clients » et « Opportunités biens ».
- Puces d'étapes avec compteurs, défilables avec des flèches (`oppRef`, `slide()`).
- Clients :
  - puces Tous / Nouveau / Qualifié / Visites / Offre ;
  - tri par `urg` ;
  - note « Mes clients uniquement · triés par urgence ».
- Biens :
  - puces Tous / Premier contact / Visite d'estimation / Négociation / Contrat signé / Bien actif ;
  - note « Mes biens en cours · N · « Contrat signé » → bien actif ».

**Onglet Biens**
- Titre « Biens · N biens · agence ».
- Segments « Tous · N » et « Mes biens · N » (biens sans `broker`).
- Recherche « Quartier, type, référence… » sur titre, référence, type et broker.
- 4 filtres, qui changent de valeur à chaque clic (`cyc`) :
  - Vente / Location ;
  - Type (Appartement, Villa, Bureau, Studio) ;
  - Quartier (7 quartiers) ;
  - Prix (↑ / ↓).
- Chaque ligne affiche le badge « Mon bien » ou « Bien de X ».

**Onglet Agenda.** Groupes « Aujourd'hui · lun. 26 oct. », « Mer. 28 oct. » et « Jeu. 29 oct. ». Le bouton « + Nouveau RDV » ouvre `openAdd('rdv')`.

**Ligne générique `row()` / `BlocLigneES`.** Une ligne comporte :
- une icône, un nom, un tag d'alerte (en rouge `#b4532b` si `urg`), une étape et un sous-titre ;
- un badge « Mon bien » ou « Bien de X » ;
- un bouton principal `rec`, au choix : tel, wa, route, ou chevron d'ouverture ;
- un bouton « + » (« Autres canaux ») qui déplie 5 puces : Tel, WhatsApp, Email, SMS, Telegram.
  - Un canal absent apparaît en pointillés, avec une opacité de 0,35. Un clic affiche le toast « X non renseigné pour Y ».
- en option, un bouton texte (« Proposer », « ✓ Fait »).

**Fiche client (bottom sheet, `cs`)**

Contenu affiché :
- nom, étape (`STL`), budget, puces de quartiers, alerte ;
- section **À FAIRE** : lignes avec « ✓ Fait » ;
- section **INFOS DU PROJET** :
  - champs `fields` à compléter avec « + Ajouter » ;
  - selon le champ, choix d'options ou saisie libre, validée par OK.
  - Saisir un **Téléphone** active les canaux tel, wa et sms (`setField`).
- section **Biens proposés · N** :
  - bouton « + Proposer » qui ouvre un sélecteur de 4 candidats au maximum ;
  - cartes « photo » factices.
- section **HISTORIQUE** : 3 lignes visibles, puis « Voir tout (N) › ».

Actions :
- « Appeler » : canal principal ;
- « RDV » : `openAdd('rdv')` prérempli ;
- « Note » : saisie libre, ajoutée à l'historique ;
- « + » : ouvre les canaux.

**Fiche bien (feuille empilée, `bs`)**
- Fil d'Ariane « ‹ Client › Bien » lorsqu'elle est ouverte depuis un client.
- Carrousel factice « photos du bien (n/8) » avec ‹ et ›.
- Badge « Mon bien » ou « Bien de X », titre et prix.
- Caractéristiques :
  - 6 champs de base : Type, Surface, Quartier, Transaction, Statut, Responsable ;
  - « + 6 infos » qui ajoute les champs de `XDEF` propres au type ;
  - indicateur « n/12 renseignées » ;
  - « Modifier » uniquement si le bien est le mien, sinon « Lecture seule » ;
  - en édition : Annuler / Enregistrer ;
  - cadenas « non modifiable ici » sur Type, Transaction, Statut et Responsable.
- Pour un mandat : « Étape n/4 · X », barre à 4 segments, bouton « Passer à « étape suivante » » ou « Passer en bien actif ».
- « Partager sur WhatsApp » : aperçu du message, choix du destinataire parmi les clients intéressés, Modifier / Envoyer.
- Sections « GESTIONNAIRE DU BIEN · CONTACT PRINCIPAL » et « PROPRIÉTAIRE » :
  - règle « même contact que le gestionnaire » ;
  - « contact secondaire » ;
  - « Ne pas contacter · passer par le gestionnaire ».
- « Clients intéressés · N ».
- « ANNONCEURS · N » avec « + Ajouter ».

**Ajout rapide (`ad`).** 4 tuiles :
- **Nouveau lead** :
  - champs Nom, Téléphone, Achat/Location, Budget (DH) ;
  - texte « Le reste se complète plus tard depuis la fiche » ;
  - bouton « Créer le lead ».
- **Nouveau RDV** :
  - type Visite / Estimation / Signature ;
  - puces Client ; puces Bien, limitées aux biens déjà proposés à ce client ;
  - « Créneaux libres aujourd'hui » ;
  - récapitulatif ;
  - bouton « Créer le RDV ».
- **Nouveau bien** :
  - Appt / Villa / Bureau / Studio, Vente / Location ;
  - champs Quartier, « Gestionnaire du bien (contact principal) », Prix souhaité ;
  - bouton « Créer le bien » ; le bien entre à l'étape « Premier contact ».
- **Note vocale** : micro et chronomètre mm:ss, puis « Enregistrer la note ».

**Ce que font réellement les actions dans le code.** Tout se passe dans l'état React en mémoire, puis un toast s'affiche.

| Action | Effet réel |
|---|---|
| Canal (tel / wa / mail / sms / tg) | `contact()` ajoute à l'historique client « Appel sortant » ou « Message envoyé », puis affiche le toast « Appel vers X… » / « WhatsApp · X ». Si une action est liée, le toast propose « ✓ Marquer fait ». **Aucun lien `tel:`, `wa.me`, `mailto:` ni `window.open`.** |
| Itinéraire | Toast « Itinéraire · adresse » seulement. |
| ✓ Fait / Marquer fait | `markDone`, état `done[act]`, toast « Action terminée · +1 au compteur du jour ». |
| Proposer | `propose()` ajoute le bien à `c.props`, une entrée d'historique « Proposition » et le client à `b.inter`. L'entrée est retirée de `matchs` si l'appel vient d'un rapprochement. |
| Passer à l'étape | `updBien` change `stage`. À la dernière étape, `stage='actif'` et toast « Bien actif · visible dans Biens ». |
| Envoyer WhatsApp | Historique « Bien partagé », bien ajouté aux propositions, toast « Envoyé sur WhatsApp à X ». **Rien n'est envoyé.** |
| + Ajouter annonceur, clic sur une annonce | Toast seulement. |
| Créer lead / RDV / bien | Ajout dans `clients`, `rdvs` ou `biens` en mémoire. Un nouveau lead crée aussi une action en tête de liste (`newActs`). |
| Note vocale | `setInterval` incrémente un compteur. **Aucun accès au micro.** Toast « Note vocale enregistrée · m:ss · transcription en cours ». |

### 1.2 Desktop (« CRM Easy Space · Desktop »)

**Disposition**
- Barre latérale sombre :
  - logo PNG et « CRM / Casablanca · Brokers » ;
  - bouton sable « + Nouveau », qui ouvre le menu « Nouveau client » / « Nouveau bien » ;
  - 6 entrées de navigation (`VT`) ;
  - pied : « YB · Yassine B. · Broker senior · ⚡ 6 j ».
- En-tête :
  - titre de la vue ;
  - recherche « Rechercher un client, un bien, une réf… », raccourci clavier `/`, `Escape` pour fermer ;
  - bouton « ↻ Synchronisé il y a 1 min ».
- Panneau droit (`aside`) pour la fiche bien ou la fiche client.
- Fenêtre modale de création.

**Entrées de navigation**

| Entrée | Badge |
|---|---|
| Tableau de bord | nombre d'actions |
| Opportunités clients | — |
| Opportunités biens (titre « Opportunités biens · mandats ») | — |
| Stock biens | — |
| Agenda | — |
| Distribution & équipe | nombre de leads |

**Vues**
- **Tableau de bord** :
  - bandeau « Mardi 27 octobre · Bonjour Yassine » ;
  - `heroSub` : « N actions à traiter, dont N urgentes. 9 RDV aujourd'hui. » ;
  - 3 statistiques cliquables : RDV aujourd'hui, Leads à attribuer, Mandats en négociation ;
  - anneau « n/10 actions ».
  - « Actions du jour » :
    - filtres Toutes / Urgentes / Clients / Biens ;
    - chaque ligne : case ✓, nom, badge Client ou Bien, contexte, alerte, bouton canal (WhatsApp, Appeler, Itinéraire ou Ouvrir).
  - Colonne droite :
    - « Agenda du jour » (« Semaine → ») ;
    - « Nouvelles opportunités » (âge, bouton Proposer, « Proposé ✓ ») ;
    - « Biens à mettre à jour ».
- **Opportunités clients** : kanban à 4 colonnes (Nouveau lead, Qualifié, Visites en cours, Offre en cours). Chaque carte affiche initiales, nom, budget, quartiers, alerte et « N biens ».
- **Opportunités biens** : kanban à 4 colonnes `STAGES`. Chaque carte affiche nom, prix, propriétaire et alerte ; une colonne vide indique « Aucun mandat ».
- **Stock biens** :
  - segments Tous / En stock / En prospection ;
  - 5 listes déroulantes : Vente/Location, type, quartier, responsable, tri ;
  - 5 puces de signalement : biens affichés, fiches incomplètes (moins de 10/12), sans intéressé, à mettre à jour, multi-annoncés (2 annonceurs ou plus) ;
  - tableau à 9 colonnes : Réf., Bien, Prix, Trans., Statut, Responsable, Intéres., Annonc., Fiche (jauge n/12).
- **Agenda** : 3 colonnes de jours (« Aujourd'hui · mar. 27 oct. », Mer. 28, Jeu. 29). Les événements sont colorés par type (`TYC`).
- **Distribution & équipe** :
  - « Leads à attribuer » : 4 leads, avec suggestion « Attribuer à X » ou attribution par initiales ;
  - « Charge de l'équipe » : 4 brokers, avec biens en stock, mandats en cours, clients actifs, RDV semaine, N en retard et barre de charge.
- **Fiche bien** :
  - « Réf · statut », titre, prix, adresse ;
  - « Partager sur WhatsApp » ;
  - « Proposer à un client » : liste de tous les clients qui n'ont pas encore ce bien ;
  - pour un mandat : étapes et « Étape suivante : X » ou « Mettre en stock » ;
  - « Caractéristiques · n/12 renseignées », Modifier (seulement si le bien est le mien) ;
  - Gestionnaire du bien avec « Appeler » ;
  - Propriétaire avec la règle « Même contact que le gestionnaire », « Contact autorisé » ou « Ne pas contacter » ;
  - Clients intéressés ;
  - Annonceurs. Sans annonceur, le texte « Exclusif Easy Space, aucune autre annonce repérée. » s'affiche.
- **Fiche client** :
  - initiales, nom, étape et budget ;
  - boutons canaux, colorés : WhatsApp en vert, canal recommandé en sable ;
  - barre d'étapes et « Passer à : X » ;
  - Quartiers ;
  - À faire avec ✓ ;
  - Qualification : listes déroulantes et saisies modifiables directement ;
  - Biens proposés ;
  - **« Biens correspondants en stock »** avec bouton Proposer ;
  - Historique.
- **Modale « Nouveau client »** : Nom complet, Téléphone, Besoin (Achat/Location), Budget, Quartier.
- **Modale « Nouveau bien »** : Type, Transaction, Quartier, Surface, Prix, Propriétaire. Boutons Annuler / Créer.

**Effets réels**
- Tous les canaux passent par `toast(MSG[k](nom))` ; « Itinéraire » affiche le toast « Itinéraire ouvert dans Maps ».
- « Partager sur WhatsApp » affiche le toast « Fiche partagée sur WhatsApp ». Aucun envoi.
- `assign()` retire le lead de la liste. S'il est attribué à « moi » (`ME`), il crée un client « Nouveau ».
- `saveAdd` crée l'objet en mémoire, ouvre sa fiche et affiche un toast.
- « Synchroniser » attend 900 ms (`setTimeout`), puis affiche le toast « Données synchronisées ».

---

## 2. Simulations relevées

- **localStorage / sessionStorage / IndexedDB / fetch** : **aucune occurrence** dans les trois fichiers. Tout l'état vit dans `this.state`, construit à partir de constantes clonées (`clone = JSON.parse(JSON.stringify())`). Un rechargement réinitialise tout.
- **« Réinitialiser les données »** (prototype et mobile) : `reset` remet `this.initial(scenario)`, arrête l'intervalle vocal et affiche le toast « Données réinitialisées ». Ce n'est qu'une réinitialisation de l'état local.
- **Barre 9:41** (prototype et mobile) : du balisage statique (`<span>9:41</span>`, barres réseau et batterie dessinées en `div`). Elle est absente du desktop.
- **Synchronisation** : le texte « Synchronisé il y a 1 min » est en dur, puis passe à « Synchronisation… » et « Synchronisé à l'instant » après 900 ms (`setTimeout`). Le geste « tirer pour synchroniser » (seuil de 44 px) suit le même principe. **Aucun appel réseau.**
- **Faux envois** :
  - `MSG` produit les textes « Appel vers X… », « WhatsApp · X », « Email à X… », « SMS à X… », « Telegram · X » ;
  - « Envoyé sur WhatsApp à X » et « Fiche partagée sur WhatsApp » sont de simples toasts ;
  - le message WhatsApp généré contient le lien fictif `easyspace.ma/b/<ref>` ;
  - la note vocale avec « transcription en cours » est fictive (aucun `getUserMedia`).
- **Créneaux libres** : liste **en dur** `SLOTS = ['11:30','13:00','15:00','17:00','20:00']`. **Aucun calcul** à partir des RDV existants : un nouveau RDV peut tomber en même temps qu'un autre.
- **Rapprochements et suggestions**
  - Mobile, accordéon « Nouvelles opportunités » : liste **en dur** `MATCHS = [{b10→c2, 0,6 h}, {b8→c5, 13 h}, {b6→c2, 30 h}]`. L'âge est converti en texte par `age()` selon les seuils `AGE`, avec une couleur : vert sous 4 h, ambre sous 24 h, gris au-delà.
  - Mobile, sélecteur « + Proposer » de la fiche client : filtre `biens.stage==='actif'`, pas déjà proposé, Location si le budget commence par « Location » sinon Vente, puis `.slice(0,4)`. **Ni le quartier ni le prix ne sont pris en compte.**
  - Desktop, « Biens correspondants en stock » : bien actif, même transaction, `c.qs.includes(b.q)` (quartier recherché) et pas déjà proposé. **Pas de filtre sur le budget.**
  - Desktop, tableau de bord : même liste `MATCHS` en dur.
  - Suggestion « Omar Tazi, Racine · client chaud » (mobile, scénario `none`) : texte statique. « + Planifier avec Omar » préremplit c1, b1, Visite, 15:00.
- **Attribution des leads (desktop)** :
  - `suggest(l)` cherche les brokers dont `TEAM0[n].q` contient le quartier du lead, sinon prend tous les brokers ;
  - il les trie par charge croissante : `cl` (fictif) + leads attribués dans la session + nombre de biens dont il est responsable ;
  - il retient le premier.
  - Les statistiques d'équipe (`cl`, `rdv`, `late`) sont figées dans `TEAM0`.
- **Compteurs et série** : `streak` vaut 6 (7 si tout est fait). L'anneau vaut `done / (done + restant)`. Les dates « lun. 26 oct. » (mobile) et « Mardi 27 octobre » (desktop) sont écrites en dur et se contredisent.
- **Photos** : texte « photos du bien (n/8) » ou « photo du bien », sans image.
- **Identité** : « Yassine B. », « YB », « Bonjour Yassine » et « Broker senior » sont en dur (`ME`). Il n'y a ni authentification ni rôle.
- **Données fictives : noms en dur**
  - Clients : Omar Tazi, Hicham Alaoui, Leila Benjelloun, Youssef Chraibi, Sara Idrissi, Mounir Fassi, Nadia Berrada, Hajar Amrani.
  - Propriétaires et gestionnaires : Rachid Benali, Nawal Kettani, Karim Sefrioui, Atlas Gestion, Famille Tahiri, Samir El Idrissi, Imane Lazrak, Ahmed Berrada, Driss Amrani, Hind Chami, Abdellatif Bennani, Khadija Lahlou, Syndic Rés. Al Manar, Rachid Ouazzani, Hajar Amrani.
  - Propriétaires distincts (`PROPS`) : Famille Alami, Atlas Patrimoine, Mme Bennis, Promoteur Dar Lina, Résidence Al Nakhil, Promoteur Al Waha, Copropriété Al Manar.
  - Brokers : Yassine B. (moi), Salma T., Mehdi R., Karim B.
  - Leads (desktop) : Rania Kabbaj (Mubawab), Société Novatec (Site web), Anas Berrechid (Avito), Meryem Ziani (Facebook).
  - Annonceurs : Agence Atlas Immo, Agence Maârif Home, Agence Casa Prestige, Agence Gauthier Conseil, Agence Anfa Luxe, Agence Palmier, Agence Bourgogne Immo, Agence CIL Habitat, Agence Racine Loc, Particulier, « Salma T. (EasySpace) ». Portails cités : Mubawab, Avito, Sarouty, Facebook, Site agence, Site promoteur.
  - Adresses à Casablanca : 14 rue Ibnou Battouta, Bd Rachidi, Rue des Iris, Bd Ghandi, Bd Panoramique, etc.

---

## 3. Modèle de données implicite (prototype v2.1, complété par le desktop)

**Client** (`CLIENTS`)

| Champ | Contenu |
|---|---|
| `id` | identifiant |
| `name` | nom |
| `stage` | étape commerciale |
| `budget` | texte libre « Achat · 2 300 000 – 2 600 000 DH », « Location · 12 000 DH/mois », « Vente · estimation… » |
| `qs[]` | quartiers recherchés |
| `alert` / `short` | texte d'alerte et sa version courte |
| `urg` | booléen d'urgence |
| `rec` | canal recommandé : tel, wa ou chev |
| `av[]` | canaux disponibles |
| `todos[]` | `{t, tag, urg, act}` |
| `fields[]` | `{k, v, opts?, input?, ph?}` |
| `props[]` | ids des biens proposés |
| `hist[]` | `{d, t, s}` |

Valeurs :
- **Étapes client exactes** : `Nouveau`, `Qualifié`, `Visites`, `Offre` (`CST`). Libellés longs (`STL`) : « Nouveau lead », « Qualifié », « Visites en cours », « Offre en cours ». **Aucune étape « gagné » ni « perdu ».**
- Canaux : `tel`, `wa`, `mail`, `sms`, `tg`. Libellés : Tel, WhatsApp, Email, SMS, Telegram.
- Champs de qualification et leurs options :

| Champ | Options |
|---|---|
| Délai d'achat | Sous 1 mois / Sous 3 mois / Sous 6 mois |
| Financement (`FIN`) | Crédit bancaire / Comptant / Mixte |
| Date d'emménagement | Immédiat / Sous 1 mois / Sous 3 mois |
| Surface | 60–80 m² / 80–120 m² / 120 m² + |
| Date d'entrée | Immédiat / Janvier / Février |
| Budget | < 1 M DH / 1–2 M DH / 2 M DH + |
| Téléphone | saisie libre, « +212 6 … » |

- Types d'historique (`HI`) : Visite, Appel, WhatsApp, Email, SMS, Telegram, Note, RDV, Lead, Proposition, Note vocale.

**Bien / mandat** (`BIENS`, fabrique `mk`)

| Champ | Contenu |
|---|---|
| `id` | `b*` pour un bien actif, `m*` pour un mandat |
| `n` / `t` | nom court / titre |
| `type` | type de bien |
| `surf` | surface |
| `ch` | chambres |
| `q` | quartier |
| `addr` | adresse |
| `price` / `pv` | prix en texte / valeur numérique |
| `tx` | Vente ou Location |
| `broker` | `null` = mon bien, sinon « Salma T. », etc. |
| `owner` | gestionnaire, contact principal |
| `role` | propriétaire ou gestionnaire |
| `av[]` | canaux disponibles |
| `inter[]` | clients intéressés |
| `ref` | ES-1042, ES-M201… |
| `stage` | étape |
| `alert` / `short` / `urg` | alerte |
| `upd` | « Photos à mettre à jour », « Prix à revoir (−4 %) » |
| `x{}` | caractéristiques complémentaires |
| `ann[]` | annonceurs `{n, d}` |
| `mgrKind` | nature du gestionnaire |
| `prop{n,k,ok,same}` | propriétaire |

Valeurs :
- **Étapes de mandat exactes** (`STAGES`) : `Premier contact` → `Visite d'estimation` → `Négociation` → `Contrat signé`, puis `actif`. `actif` s'affiche « Actif » ou « Bien actif » sur mobile et « En stock » sur desktop. Le desktop regroupe les étapes de mandat sous « En prospection ».
- Types : Appartement, Villa, Bureau, Studio. Transactions : Vente, Location.
- Quartiers : Racine, Maârif, Gauthier, Anfa, CIL, Bourgogne, Californie, Aïn Diab (Aïn Diab est absent du filtre mobile `QF`).
- `mgrKind` : Propriétaire en direct / Agent mandaté / Gestionnaire d'actifs / Syndic mandaté.
- Nature du propriétaire : Particulier / Gestionnaire d'actifs / Promoteur / Copropriété.
- Caractéristiques `XDEF` (6 de base + 6 selon le type = 12) :

| Type | Champs |
|---|---|
| Appartement | Chambres, Étage, Ascenseur (Oui/Non), Parking (Aucun/1 place/2 places/3+ places), Construction, Syndic / mois |
| Villa | Chambres, Terrain, Piscine, Jardin, Garage, Construction |
| Bureau | Postes, Étage, Ascenseur, Parking, Climatisation (Centralisée/Split/Aucune), Charges / mois |

**Action** (`ACTIONS`) : `{id, kind: 'client'|'bien', ref, alert, short, urg, type: mob|cal|db|house, ctx, rec: wa|tel|route|chev}`. Il y en a 10, dont 4 urgentes.

**RDV** (`TODAY`, `NEXT`) : `{id, h, type, cid, who, q, addr, av, bien, dur}`.
- Types : Visite (45 min), Estimation (45 min), Signature (1 h).
- `NEXT` ajoute `day` et `dayS`.

**Rapprochement** (`MATCHS`) : `{b, c, h}`, où `h` est l'âge en heures.

**Desktop uniquement**
- **Lead** : `{id, name, src, h, tx, need, q}`. Sources : Mubawab, Site web, Avito, Facebook.
- **Broker / équipe** : `TEAM0[n] = {cl, rdv, late, q[]}`.
- Calculs : `own(b) = broker || ME` ; `fillOf(b)` sur 12 ; `fillCol` vert à 10 ou plus, sable à 8 ou plus, sinon rouille.

---

## 4. Tokens visuels

**Couleurs (hex) et usage**

| Couleur | Usage |
|---|---|
| `#122631` | « Nuit Architecture » : marque, encre, fond du cadre et de la barre latérale |
| `#1b3542`, `#24414f` | navigation active et survol (desktop) |
| `#566d76` | texte atténué |
| `#4b626b`, `#32454d`, `#7d9099`, `#8698a0` | textes secondaires et placeholders |
| `#b8c5ca`, `#c6d1d5`, `#d8e0e3`, `#e3e9eb`, `#edf1f2`, `#f7f9fa`, `#d6e2e6` | lignes, bordures, fonds neutres |
| `#c7a976` | « accent Sable » : bouton Nouveau, badge leads, avatar « moi », bordure des champs vides |
| `#e6d3ad` | sable clair (badge de série) |
| `#f3ead9` / `#7a5c25` | fond et texte du statut « mandat » |
| `#f4f1ea` | fond de page desktop (crème) |
| `#e4e8e9` | fond de page mobile |
| `#b4532b` | rouille : alerte et urgence ; fond `#f6e3da` |
| `#1f8f55` | WhatsApp et succès ; « En stock » `#e3f1e8` / `#1f6b40` ; `#2f7d4f` pour 12/12 |
| `#b07a12` | ambre (âge < 24 h) |
| `#2a86c0` | Telegram |
| `#1d1c1a` | contour du téléphone |
| `#0a1820` | survol des liens |
| `#d97757` / `#141413` | uniquement le badge « Made with Claude Design », hors charte |

Code couleur de l'agenda desktop (`TYC`) : Visite `#122631`, Estimation `#c7a976`, Signature `#1f8f55`.

**Police.** **Manrope** uniquement : 30 `@font-face` woff2 embarqués, graisses 400 à 800. Repli `system-ui`. Titres en `letter-spacing:-.015em` / `-.02em`. Chiffres en `font-variant-numeric: tabular-nums`. La barre 9:41 utilise `-apple-system`. Le desktop affiche la touche `/` en `ui-monospace`.

**Rayons**
- Mobile : 10 px dominant (boutons, puces, cases de 44×44), 17–18 px (pastilles, avatars), 12 et 16 px, 5 px (badges « Mon bien »), 22–24 px (feuilles), 54 px (cadre téléphone).
- Desktop : 18, 16, 14 et 10 px dominants, 9 / 11 / 13 px pour les badges, 26 px (bandeau).

**Icônes.** Jeu SVG « lucide-like » défini dans le dictionnaire `P` : trait de 1,8, `linecap round`. Il est converti en `data:image/svg+xml` par `ico(path, couleur)`. Le desktop ajoute le dictionnaire `D` (dash, clients, mandats, stock, agenda, equipe).

**Logo**
- C'est une **image PNG matricielle** de 234×191 px, RGBA, **blanche sur fond transparent** : un « A » stylisé. Ce n'est **pas** un SVG inline.
- Elle est insérée par `<img alt="Easy Space">`, en 22 px de haut sur mobile (en-tête sombre) et 30 px sur desktop (barre latérale sombre).
- Comme elle est blanche, elle est **inutilisable sur fond clair**.
- La vignette du bundle desktop contient en revanche un **SVG** d'un « A » / chevron sable `#c7a976` sur `#122631` : `<path d="M600 230 L760 570 H690 L600 360 L510 570 H440 Z">`.
- Le libellé texte est « CRM EasySpace » (prototype) ou « CRM » + « Casablanca · Brokers » (desktop).

---

## 5. Vocabulaire mobile et desktop

| Notion | Mobile (Prototype / Mobile) | Desktop |
|---|---|---|
| Accueil | Accueil | Tableau de bord |
| Pipeline client | Opportunités › Opportunités clients ; étapes Nouveau / Qualifié / Visites / Offre | Opportunités clients ; colonnes Nouveau lead / Qualifié / Visites en cours / Offre en cours |
| Pipeline bien | Opportunités biens ; « Mes biens en cours » ; « mandat » sous-entendu | Opportunités biens · **mandats** ; « Aucun mandat » ; « Mandat · X » |
| Bien publié | **Bien actif** / « Actif » ; « Passer en bien actif » | **En stock** / « Stock biens » ; « Mettre en stock » ; « ajouté au stock » |
| Mandats (vue globale) | — | **En prospection** |
| Catalogue | Biens (Tous / Mes biens), « N biens · agence » | Stock biens (Tous / En stock / En prospection) |
| Appartenance | « Mon bien » / « Bien de Salma T. » | Responsable : « Moi » / nom |
| Qualification | INFOS DU PROJET | Qualification |
| Rapprochement | Nouvelles opportunités ; Biens proposés ; « + Proposer » | Nouvelles opportunités ; **Biens correspondants en stock** ; Proposer à un client |
| Contact du bien | GESTIONNAIRE DU BIEN · CONTACT PRINCIPAL / PROPRIÉTAIRE | Gestionnaire du bien / Propriétaire |
| Création | Ajout rapide : Nouveau lead / Nouveau RDV / Nouveau bien / Note vocale | + Nouveau : Nouveau client / Nouveau bien (ni RDV ni note vocale) |
| Lead entrant | « Nouveau lead » = client à l'étape Nouveau | Leads à attribuer (entité distincte, distribution) |
| Équipe | absent | Distribution & équipe, Charge de l'équipe |
| Tâches | Actions du jour (Tous / Opp clients / Opp biens) ; À FAIRE | Actions du jour (Toutes / Urgentes / Clients / Biens) ; À faire |
| Bouton canal | Tel | Appeler (bouton) / Tel (puce de la fiche) |
| Date « aujourd'hui » | lun. 26 oct. | Mardi 27 octobre / mar. 27 oct. |

---

## 6. Captures produites

Dossier : `/home/user/Test-1/crm-v21/tests/screenshots/`. Les 20 captures ont été produites avec `chromium.launch()`, sans erreur de page (`pageerror` vide).

- Prototype, 390×844 (capture de l'élément téléphone, après clic sur le raccourci de l'écran) :
  - `proto_Prototype_v2_1_accueil_rdv.png`
  - `proto_Prototype_v2_1_accueil_blocs_ouverts.png`
  - `proto_Prototype_v2_1_opp_clients.png`
  - `proto_Prototype_v2_1_opp_biens.png`
  - `proto_Prototype_v2_1_biens.png`
  - `proto_Prototype_v2_1_fiche_client.png`
  - `proto_Prototype_v2_1_fiche_bien.png`
  - `proto_Prototype_v2_1_ajout_rapide.png`
  - `proto_Prototype_v2_1_agenda.png`
- Mobile :
  - `proto_Mobile_ClaudeDesign_accueil_390.png` (390×844)
  - `proto_Mobile_ClaudeDesign_fiche_bien_390.png` (390×844)
  - `proto_Mobile_ClaudeDesign_accueil_1440.png` (1440×900, page entière ; le cadre reste fixe)
- Desktop, 1440×900 (après clic sur la navigation de la barre latérale) :
  - `proto_Desktop_ClaudeDesign_dashboard.png`
  - `proto_Desktop_ClaudeDesign_opp_clients.png`
  - `proto_Desktop_ClaudeDesign_opp_biens_mandats.png`
  - `proto_Desktop_ClaudeDesign_stock_biens.png`
  - `proto_Desktop_ClaudeDesign_agenda.png`
  - `proto_Desktop_ClaudeDesign_distribution_equipe.png`
  - `proto_Desktop_ClaudeDesign_fiche_bien.png` (ES-1042)
  - `proto_Desktop_ClaudeDesign_fiche_client.png` (Omar Tazi)

Ce qui a été omis : les scénarios 2b et 2d du mobile (accueil sans RDV) ne sont pas capturés. Leur balisage est décrit en section 1.1.
