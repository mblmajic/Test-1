# Résultats des tests GET CRM21 — passe 3 (2026-10-30, ~19:03)

Règles : brouillons uniquement (save_endpoint upsert), test_endpoint skipAuth sans allowWrites, aucune publication ni écriture SmartDB.
Appelants : admin (Majid), Imane, Salma, non-membre. Ids de test : dossier 23 (Imane, budget 4 000 000), dossier 6 (Salma), bien 9.

## 1. Nouvelle erreur commune (bloquante pour l'admin et pour toute date vide)

- **opportunites-clients**, admin vue=toutes **et** admin vue=actions : 422, step `out`, `EXPRESSION_ERROR` — « Expression failed: The expressions either side of operator "<=" must evaluate to numeric or string values » (T2010, token `<=`, position 4898, c'est-à-dire l'appel `$oc($)`).
- Cause : `$loc` teste `$exists($t)`. Pour une date vide, `$ms('')` renvoie `null`, et en JSONata `$exists(null)` vaut **true**. `$tzp(null)` appelle alors `$off(null)`, qui évalue `$ms(debut_utc) <= null` et échoue (T2010).
  - Le portefeuille admin contient au moins un dossier sans échéance.
  - Les portefeuilles d'Imane et de Salma n'en contiennent aucun, d'où leurs 200.
- Correctif proposé (préambule commun des 13 `out`) : `$loc := function($iso, $pic){ ($t := $ms($iso); $type($t) = 'number' ? $fromMillis($t, $pic, $tzp($t)) : '') };`. Garder éventuellement aussi `$type($t) = 'number'` dans `$off`.
- Endpoints exposés (appel de `$jour`, `$heure` ou `$labelDate` sur une date pouvant être vide) :
  - opportunites-clients, opportunite-client et rapprochements (échéance) ;
  - biens, bien, propositions, rapprochements et opportunites-biens (`crm_echeance` des biens, nulle par exemple pour le bien 9) ;
  - activites et historique (`crm_fin`, toujours nulle sur les activités historiques) ;
  - accueil et equipe (à vérifier).

## 2. Enregistrements (problems)

| endpoint | id | problems | version enregistrée |
|---|---|---|---|
| GET /crm21/session | f9e520db-8c1d-4b8d-9061-408ab3258557 | aucun | identique au fichier (inchangé depuis la passe 2) |
| GET /crm21/referentiels | 3adc338f-4f95-40ba-9976-ed60772ace44 | aucun | identique au fichier (inchangé depuis la passe 2) |
| GET /crm21/opportunites-clients | 2f777bfd-880f-440c-ad3a-73e55f9497a9 | aucun | passe 3 ($dh corrigé) |
| GET /crm21/opportunite-client | de5113ec-d1ea-4e34-b716-09a94fa878f3 | aucun | passe 3 ($dh corrigé) |
| propositions, historique, rapprochements, biens, bien, creneaux, activites | ids de la passe 1 (crm21_ids.json) | — | **pas encore ré-enregistrés** (l'API Studio contient la version de la passe 1) |
| opportunites-biens, opportunite-bien, accueil, equipe | — | — | **pas encore enregistrés** |

Passe interrompue après ces 4 endpoints : le correctif de `$loc` modifie à nouveau le préambule des 13 fichiers, qui devront donc tous être ré-enregistrés.

## 3. Tests

### referentiels (passe 2, version identique)
| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin | 200 | 200, 1 item | 13 étapes ; brokers = 3 (Majid, Admin, inclus car son champ broker est rempli) |
| Imane | 200 | 200, 1 item | brokers = 1 (Imane) |

### opportunites-clients
| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin vue=toutes | 200 | **422** | rows=28 ; `out` T2010 « <= » pos 4898 (cf. §1) |
| admin vue=actions | 200 | **422** | idem |
| Imane | 200 | 200, 4 items, total 4 | 1er item : etape=Nouveau, etapeTone=info, echeanceLabel=« mar. 6 oct. · 13:03 », enRetard=true, budgetLabel=« — », aCompleter=« À compléter : budget ». Le dossier 23 donne budgetLabel=« 4 000 000 DH » (formatNumber OK) et echeanceLabel=« Aujourd’hui · 10:15 » |
| Salma | 200 | 200, 12 items, total 12 | 1er item : etape=Visite Proposée, etapeTone=info, echeanceLabel=« mar. 3 nov. · 16:00 », enRetard=false, budgetLabel=« 8 000 DH », aCompleter=« », priorite=Haute. Valeurs vides : budget null ×3, contactId null ×4, téléphone vide ×1 |
| non-membre | 403 | 403 | `g403` |

Remarques :
- Le dossier id 18 (Imane) a une étape vide en base ; elle est affichée « Nouveau ».
- Imane voit 4 dossiers sur 12, car la vue par défaut exclut Perdu, Gagné et En Pause.
- quartier/ville contiennent des espaces de fin (« Bourgogne  », « Casablanca  »), visibles dans criteresLabel : « Bourgogne  · budget ».

### opportunite-client
| cas | attendu | obtenu | détail |
|---|---|---|---|
| admin id=23 | 200 | 200, 1 item | etape=Recherche active, etapeTone=info, echeanceLabel=« Aujourd’hui · 10:15 », enRetard=false, budgetLabel=« 4 000 000 DH », aCompleter=« », contactStatut=« Contact à confirmer », surfaceLabel=« — », chambres=null, criteres=« », modifiable=true. `contact` skipped (garde corrigée OK) |
| Imane id=6 | 404 | 404 | `g404` |
| Imane id=23 | 200 | non relancé | même chemin que l'admin |
| Salma id=6 | 200 | 200 (passe 2) | etape=Biens proposés, budgetLabel=« — », contactStatut=« Contact lié » ; pas d'appel à `$dh`, résultat inchangé attendu |

### Autres endpoints
Pas encore relancés (cf. §2) : propositions, historique, rapprochements, activites, biens, bien, creneaux, opportunites-biens, opportunite-bien, accueil, equipe.
