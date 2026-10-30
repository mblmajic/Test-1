# 01 — Contrats de données (V2.1)

Source : `smartdb_list_columns` du 2026-10-30. Les noms `src_…` sont les noms techniques réels utilisés par les endpoints.

## 1. Correspondance des champs

### Opportunités clients — `m80adee8ba2348dfe` (base pmv6m9j8dh2qj)
| Clé API V2.1 | Colonne | Type | Remarque |
|---|---|---|---|
| id | id | ID | |
| nom | libelle / src_c8j7pxeprb45sel + src_cu4m58kh70jsaas | texte | libellé sinon Prénom + Nom |
| broker | src_c2ljvedgo8rjnjz « Agent Broker » | Select | Imane, Salma, Majid, Omar, Non Affectés, Agent IA…, Affectation urgente… → **clé de cloisonnement** |
| etape | src_ch80mhxt9wmgffa « Statut » | Select | Nouveau, À qualifier, Qualifié, Recherche active, Biens proposés, Visite Proposée, RDV Visite Validé, Visite Effectuée, Négociation, Finalisation, Gagné, Perdu, En Pause |
| prochaineAction | src_cwm9erw27y2a5ax | Select | 9 valeurs (Appeler … Proposer Offre Financière) |
| echeance | src_csdkjyu1i3h2rpd | DateTime | « Date prochaine action » |
| detailAction | src_caw1n932cne75bt | LongText | |
| priorite | src_cp1ak79dze4j7zb | Select | Urgente, Haute, Normale |
| telephone | src_cmt5f5y6apb9n76 | Phone | **visible seulement si dossier autorisé** |
| transaction | src_cc9t923zypqax4s | Select | Achat, Location |
| typeBien | src_cqx1ht4dg6mt0gl | Select | Appartement, Villa, Bureau, Local commercial, Terrain, Industriel, Autre, Studio |
| quartiers / ville | src_crid8q8n1p0n7qe / src_cjuumr2e0utdov7 | texte | |
| budget | src_c8ty9timbln0feq (Achat) ou src_c0qcaxijrq4e44n (Loyer) | Currency | selon transaction |
| surfaceMin/Max | src_cali7clgn81g11x / src_cdivmzu7n1bn63g | Number | |
| chambres | src_cj59gxz110km911 | Number | |
| canal | src_c90ihchqcq0h8hz | Select | |
| contactId | pmv6m9j8dh2qj_contacts_id « Contact principal CRM1 » (bt) **sinon** « Contact lié » (mm historique) | lien | règle de lecture : principal CRM1 prioritaire |
| cleCreation | crm_cle_creation | texte | réutilisé comme clé d'idempotence |

### Opportunités de biens — `m13dd0abc30554ba9`
statut `src_cey267rja2wv3lq` · nom `src_c7a50877zqv8he2` · type `src_cd5vgyi78qkg52p` · prix `src_cwqc3dj4cewpssd` · surface `src_cgxt2lkxiqv17wa` · quartier `src_cg613eoqivagf9q` · ville `src_cp1785bk483rstm` · transaction `src_cjww4qd9gmywdmx` (Vente/Location) · **responsable `src_cazse08x5syk1gn` « Broker en Charge »** (Imane, Salma, Majid, IA, Autre, Omar) · gestionnaire `src_cw8g5cc2gv9f6dz` / `src_c0utrhay1h28b7j` · photos `src_c17fpsjfd07usk6` + état `src_cedb9jfgba1ogoj` · résultat `resultat_commercial` · affectation principale (bt) / à confirmer (mm) · état migration gestionnaire `tat_de_migration_gestionnaire` (Gestionnaire inconnu, À confirmer, Conflit, Validé) · bien lié : « Bien principal CRM1 » (bt) sinon « Bien lié » (mm) · suivi `crm_prochaine_action`, `crm_echeance`, `crm_priorite`, `crm_notes_suivi`.

### Biens — `ma9b9bb062ad8b271`
dispo `src_ckik8lj9kqev9ho` (Actif, Inactif, 2 états « en cours de validation ») · responsable `src_c9w1scpswzkjl7g` « Broker Principal » · nom `src_c30sp73xdb9jdsx` · type `src_cy2vb7l7nqcvdec` · transaction `src_c771ftquhdtvl0r` (Vente/Location) · prix `src_c5waewdapjudd8k` · surface `src_c4in13ik1q3f1fw` · quartier `src_c15ey3zrlrmehdi` · ville `src_cdespozafnudzr4` · chambres `src_c16ypivc4c8xya2` · photos `src_ce4lcsor6pndckt` + état `src_ceni271nn57qrii` · gestionnaire `src_cv0gxc73awfgmpw` / `src_cmb84pfu1pwkzw5` · annonceur (bt) · statut brief `statut_brief` · `date_confirmation_dispo` · suivi `crm_*`.

### Activités (RDV) — `m3573c7a505385e65`
début `src_cybzjmjoj4zlch0` (DateTime) · fin `crm_fin` (DateTime ; `src_czeezrk4h82lq7k` est un texte historique) · nature `src_c2xrwp99jzayeub` (texte) · statut `src_cwtdcarxql2laii` (Terminé, Annulé, Visité, Programme) · état visite `crm_etat_visite` · broker `crm_broker` (texte) · opportunité client (bt) · bien (bt) · opportunité de bien (bt) · visiteur/contact (bt) · CR : `crm_appreciation`, `crm_objections`, `crm_prochaine_etape`, `crm_historique_cr` · test `crm_est_test`.

### Propositions — `m5ba929066e4852f4` (base CRM1)
`cle_proposition` (« oppClientId-bienId ») · statut (À proposer, Proposé, Intéressé, Refusé, Visite demandée) · `retour_client` · provenance (Broker, Suggestion automatique) · `broker`, `email_auteur`, `date_proposition`, `operation_id`, `test_crm1` · liens opportunité client (bt) et bien (bt).

### Journal — `m638173347625af09`
`type_evenement`, `type_dossier`, `dossier_id`, `libelle`, `resume`, `avant`, `apres`, `resultat`, `broker`, `email_auteur`, `user_id`, `operation_id`, `source`, `date_evenement`, `test_crm1`.

## 2. Règles de calcul (Accueil)
| Indicateur | Règle | Données |
|---|---|---|
| Prochain RDV | 1re activité du périmètre, statut ∉ {Annulé, Terminé}, début ≥ maintenant, triée par début | Activités |
| RDV à venir | idem, 7 jours glissants | Activités |
| Actions prioritaires | opportunités clients du périmètre avec échéance ≤ fin du jour, étape ∉ {Gagné, Perdu, En Pause}, triées priorité puis échéance | Opp. clients |
| Retards | échéance < début du jour (Africa/Casablanca) | Opp. clients |
| Informations à compléter | budget vide **ou** quartier vide **ou** transaction vide **ou** contact absent | Opp. clients |
| Opp. clients avancées | étape ∈ {Visite Effectuée, Négociation, Finalisation} | Opp. clients |
| Opp. de biens à suivre | `crm_echeance` ≤ J+2 ou responsable vide | Opp. biens |
| Biens à actualiser | dispo Actif et (`date_confirmation_dispo` vide ou > 30 j) ou `statut_brief` ∈ {🔴, 🟠, 🟡} | Biens |
| Suggestions | voir §3 | |
Toutes les dates sont calculées en Africa/Casablanca (§4). Les données de recette (`[RECETTE V21]`, `RECETTE CRM1`, `test_crm1`, `crm_est_test`) sont exclues.

## 3. Rapprochement (méthode affichée)
Bien candidat si : dispo = Actif ; transaction compatible (Achat↔Vente, Location↔Location) ; type compatible (table de correspondance client→bien, ex. Appartement→appartement/studio, Local commercial→local commerciale/magasin/local) ; prix ≤ budget × 1,15 (si budget connu) ; quartier du bien contenu dans « Quartier(s) » du client (si renseigné). Score = nombre de critères satisfaits parmi budget, quartier, surface, chambres. Chaque suggestion renvoie `criteres: ["Transaction", "Type", "Budget ≤ +15 %", …]` et `manquants`. Aucune suggestion n'est écrite automatiquement.

## 4. Fuseau Africa/Casablanca
Décision : **stockage en ISO avec décalage explicite** (`2026-10-30T23:30:00+01:00`), calculé côté serveur. UTC+1 par défaut ; UTC+0 pendant les périodes de la table `CRM21 Périodes horaires` (Ramadan, dates officielles à saisir chaque année). Lecture : conversion vers l'heure locale avant tout regroupement par jour. Test obligatoire : RDV 23:30 → 00:30.

## 5. Inventaire des endpoints CRM1 → verdict V2.1
Tous **remplacés** par un équivalent `/crm21/` (décision GATE 1 : faille d'identité, voir 00_audit §4). Logique de lecture reprise quand elle est saine.

| Endpoint CRM1 | Besoin V2.1 | Verdict | Motif |
|---|---|---|---|
| GET session | identité | remplacé | rôle via CRM21 Membres |
| GET referentiels | listes | remplacé | incohérence Note/Tâche corrigée |
| GET accueil/* (4) | accueil | remplacé, fusionné en 1 | une seule lecture, règles §2 |
| GET opportunites-clients / opportunite-client | liste, fiche | remplacé | cloisonnement réel |
| GET opportunites-biens / opportunite-bien | liste, fiche | remplacé | photos, badges vérifié/à confirmer, filtres recette |
| GET biens / bien | catalogue, fiche | remplacé | « Mes biens », repli photo |
| GET activites | agenda | remplacé | fuseau, rattachement broker |
| GET historique | fiche | remplacé | |
| GET rapprochements | suggestions | remplacé | méthode §3 |
| GET contacts | — | non repris | la fiche porte son contact |
| GET propositions, medias | fiche | remplacé | |
| POST leads | ajout rapide | remplacé | idempotence, dédoublonnage téléphone |
| POST opportunites-biens | ajout rapide | remplacé | idempotence |
| POST activites / PATCH activites | RDV, CR, annulation | remplacé | fuseau, broker rattaché |
| POST notes | note | remplacé | |
| POST propositions / PATCH propositions | proposer, retour | remplacé | verrou anti-doublon |
| POST communications | journal « contact préparé » | remplacé | |
| POST fichiers (brouillon) | document | **masqué « Bientôt »** tant que non vérifié | |
| POST activation-bien | activation contrôlée | remplacé | |
| PATCH opportunites-clients / biens / opportunites-biens | édition | remplacé | champs autorisés, journal minimal |
| — | « Me l'affecter » | **nouveau** | verrou atomique |
| — | vue Équipe | **nouveau** | admin seulement |

## 6. Effets des écritures sur CRM1
À compléter endpoint par endpoint (tables, champs, effet visible dans CRM1) lors de la création des brouillons.
