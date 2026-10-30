# Validation des pages CRM Easy Space V2.1 (sans enregistrement)

App : `72fee1ce-3d5a-4f3e-b096-0f79d0a46feb` — date : 2026-10-30. Outils : `validate_page` puis `audit_page` (avec `app`). Aucune écriture (pas de save/publish/patch), fichiers sources non modifiés.

Note : `validate_page` renvoie `ok:true` et `warnings: []` sur les 6 pages (aucune correction signalée). La page renvoyée est seulement normalisée : valeurs égales aux défauts retirées, clés vides ajoutées. Le détail vient d'un diff entrée/sortie, pas d'un message de l'outil. Les erreurs `dead-link` de l'audit viennent du fait que l'app n'a encore aucune page enregistrée : `/`, `/opportunites-clients`, `/biens`, `/agenda` disparaîtront après l'enregistrement ; `/ajout`, `/opportunites-biens` et `/equipe` ne font pas partie des 6 pages testées.

## accueil.json — `/` (Bonjour)

### validate_page
- ok : **true** — nodeCount : 93 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Root `language:"fr"` retiré ; UserMenu vidé (`showName`, `themeChoice`, `logoutLabel`, `items:[]`) ; valeurs par défaut retirées (Surface background card/radius lg/border all, Button variant primary, Text variant body, Stat variant tile, Collection layout grid, `source:"endpoint"`, Grid columns "2", IconTile tone/look/shape, Button `icon:""`) ; Navigation items complétés (`badge/group/parent/iconTone/iconBackground:""`).

### audit_page
- score : **0** — verdict : **needs work** — blocks : 93 — counts : error 19, warn 0, info 1

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | error | dead-link | Stack > Record > Surface > Stack > Button | A navigate action goes to /agenda, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 14 | error | dead-link | Stack > Stack > Button | A navigate action goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 19 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 20 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |

## opportunites-clients.json — `/opportunites-clients` (Opportunités clients)

### validate_page
- ok : **true** — nodeCount : 44 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Mêmes normalisations d'en-tête ; Segmented `size:"sm"` retiré ; TextInput `width:"md"` et `icon:"Search"` retirés ; Collection `layout:"grid"`/`source` retirés (columns:2 conservé) ; Text variant body retiré.

### audit_page
- score : **0** — verdict : **needs work** — blocks : 44 — counts : error 18, warn 0, info 1

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | error | dead-link | Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 14 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 19 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |

## opportunite-client.json — `/opportunite-client` (Opportunité client)

### validate_page
- ok : **true** — nodeCount : 80 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Mêmes normalisations d'en-tête ; Tabs `variant:"underline"` retiré et `tab5:[]`, `tab6:[]` ajoutés ; Modal `size:"md"` (x4) et `description:""` retirés ; Button `size:"md"` (x6) retiré ; Form fields complétés avec ~20 clés vides par champ (placeholder, options, unit, step 1, width "full", multiple false...) ; Form `submitLabel:"Enregistrer"` retiré ; Details rows complétés (`tone:""`, `strong:false`) ; Alert `tone:"info"` retiré ; Timeline `source` retiré.

### audit_page
- score : **0** — verdict : **needs work** — blocks : 80 — counts : error 17, warn 2, info 2

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | warn | grow-in-card-row | Stack > Record > Tabs.tab2 > Collection.item > Surface > Stack | A row with a grow child inside a Collection card collapses to a column when the card is narrow (avatar above the text). | Drop grow and use justify "between", or keep the avatar and text in one inner row. |
| 14 | warn | grow-in-card-row | Stack > Record > Tabs.tab3 > Collection.item > Surface > Stack | A row with a grow child inside a Collection card collapses to a column when the card is narrow (avatar above the text). | Drop grow and use justify "between", or keep the avatar and text in one inner row. |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 19 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 20 | info | breadcrumbs | page | A detail page (reads {{query.*}}) has no Breadcrumbs. | Add Breadcrumbs above the title: Accueil › Liste › {{record.ref}}. |
| 21 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |

## biens.json — `/biens` (Catalogue des biens)

### validate_page
- ok : **true** — nodeCount : 41 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Mêmes normalisations d'en-tête ; Segmented `size:"sm"` et `defaultValue:""` retirés ; TextInput `width`/`icon` retirés ; Collection `layout:"grid"`, `columns:3`, `source` retirés ; Image `fit:"cover"`, `radius:"md"` retirés ; Badge `tone:"success"` retiré.

### audit_page
- score : **0** — verdict : **needs work** — blocks : 41 — counts : error 17, warn 0, info 1

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 14 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |

## bien.json — `/bien` (Fiche bien)

### validate_page
- ok : **true** — nodeCount : 44 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Mêmes normalisations d'en-tête ; Image `fit:"cover"` retiré ; Surface `radius:"lg"` retiré ; Stack `gap:"md"` retiré ; Grid `columns:"2"` retiré (`"3:2"` conservé) ; Button `variant:"primary"`/`size:"md"` retirés ; Modal `size:"md"` retiré ; Form field et Details rows complétés de clés vides.

### audit_page
- score : **0** — verdict : **needs work** — blocks : 44 — counts : error 17, warn 0, info 2

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 14 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | info | breadcrumbs | page | A detail page (reads {{query.*}}) has no Breadcrumbs. | Add Breadcrumbs above the title: Accueil › Liste › {{record.ref}}. |
| 19 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |

## agenda.json — `/agenda` (Agenda)

### validate_page
- ok : **true** — nodeCount : 57 — warnings : `[]` (aucune correction)
- Normalisation silencieuse (diff) : Mêmes normalisations d'en-tête ; Calendar `source:"endpoint"` et `weekStart:"monday"` retirés ; Stack `gap:"md"` retiré ; Surface background/radius/border par défaut retirés ; Badge `tone:"success"` retiré.

### audit_page
- score : **0** — verdict : **needs work** — blocks : 57 — counts : error 17, warn 1, info 1

| # | severity | rule | where | message | fix |
|---|---|---|---|---|---|
| 1 | error | dead-link | Surface > Stack > Stack > Stack > Button | A navigate action goes to /ajout, which is not a page of this app. | Create the page, or point the action at an existing path (list_pages). |
| 2 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 3 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 4 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 5 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 6 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 7 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 8 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 9 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Opportunités de biens" goes to /opportunites-biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 10 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 11 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 12 | error | dead-link | Surface > Stack > Record > Navigation | Navigation item "Équipe" goes to /equipe, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 13 | warn | empty-state | Stack > Calendar | Calendar has no emptyText: the user will read the generic "Aucun élément". | Write what it means and what to do ("Aucune facture échue : rien à relancer"). |
| 14 | error | dead-link | Surface > Navigation | Navigation item "Accueil" goes to /, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 15 | error | dead-link | Surface > Navigation | Navigation item "Clients" goes to /opportunites-clients, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 16 | error | dead-link | Surface > Navigation | Navigation item "Ajouter" goes to /ajout, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 17 | error | dead-link | Surface > Navigation | Navigation item "Biens" goes to /biens, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 18 | error | dead-link | Surface > Navigation | Navigation item "Agenda" goes to /agenda, which is not a page of this app. | Create the page, or point the item at an existing path (list_pages). |
| 19 | info | motion | page | No motion anywhere. | Fine for a work screen. If the page needs one moment (a landing, a first-run), give a single block motion "fade-up"; never every card (reduced-motion users are respected). |
