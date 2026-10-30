# 02 — Droits et sécurité (V2.1)

## Identité (toutes les routes /crm21/)
1. `auth.claims.email` (minuscules). Absent → 401.
2. Lecture `CRM21 Membres` filtrée sur cet email **dans l'étape de lecture** (pas de `skipIfEmpty`). Aucune ligne active → 403 « Votre compte n'est pas encore activé dans le CRM. Contactez l'administrateur. »
3. `role` ∈ {Broker, Admin} et `broker` (valeur du select « Agent Broker ») viennent de cette ligne. **`auth.claims.roles` n'est jamais lu** (tous les comptes sont « Admin Domaine »). Aucun paramètre navigateur ne peut fixer rôle ou broker.

## Matrice rôle × ressource × action
| Ressource | Broker | Admin | Contrôle serveur |
|---|---|---|---|
| Opportunités clients — liste/fiche | les siennes (broker = le sien) | toutes | filtre broker dans la lecture ; fiche d'un autre → 404 |
| Coordonnées client (téléphone, contact) | si dossier autorisé | toutes | champ omis sinon |
| Opp. client — créer (lead) | broker = lui-même | broker au choix | broker imposé serveur pour Broker |
| Opp. client — modifier étape/échéance/critères | les siennes | toutes | vérif. propriétaire avant écriture ; journal |
| Opp. client — réattribuer | ✗ | ✓ | garde Admin |
| Opportunités de biens — lire | toutes (partagé) | toutes | coordonnées gestionnaire visibles (partagé) |
| Opp. bien — modifier suivi | si responsable = lui ou vide | toutes | **hors responsable : refus 403** (verrouillage) + journal de la tentative ; alerte « Bientôt » |
| Opp. bien — « Me l'affecter » | si responsable vide | ✓ | verrou atomique (CRM21 Verrous) |
| Opp. bien — activation du bien | si responsable = lui | ✓ | conditions métier + journal |
| Biens — lire, « Mes biens » | tous | tous | |
| Biens — modifier suivi | si Broker Principal = lui | tous | |
| Proposer un bien | à ses opp. clients | toutes | propriétaire + verrou anti-doublon |
| Agenda — lire | ses RDV (crm_broker = lui ou opp. client à lui) | tous | |
| Agenda — créer / annuler / CR | sur ses dossiers | tous | propriétaire |
| Journal — lire | historique de ses dossiers (résumé) | tout | |
| Vue Équipe (leads à attribuer, charge) | ✗ (403) | ✓ | garde Admin |
| CRM21 Membres — gérer | ✗ | ✓ | garde Admin |

## Modification hors responsable
V2.1 **verrouille** (403) plutôt que d'autoriser avec alerte : l'alerte n'est pas opérationnelle (le seul canal existant, « Telegram — Alertes CRM — V2 », est en production et n'a pas de type d'alerte prévu pour ce cas). Chaque refus est tracé dans le Journal (`type_evenement = Refus hors responsable`). Limite documentée en docs/05.

## Comptes réels nécessaires (état au 2026-10-30)
| Personne | Rôle V2.1 | Email référentiel | Compte plateforme | Action |
|---|---|---|---|---|
| Salma | Broker | salmanakra291@gmail.com | ❌ | **utilisateur : inviter dans Tybot** |
| Imane Jarmoune | Broker | imane.jarmouni@tython.org | ❌ | **utilisateur : inviter dans Tybot** |
| Omar Ber | Broker | (vide), inactif | ❌ | fournir email, réactiver (GATE 6), inviter |
| Majid | Admin | majid@tybotflow.com (compte) ≠ majidbens@gmail.com (référentiel) | ✅ majid@tybotflow.com | Membre CRM21 avec l'email du compte |
Tant que ces comptes n'existent pas, les tests broker se font par `claims` simulés (limite signalée en docs/04 et 05).

## Tests obligatoires par route
Admin (200, tout) · Broker A (ses lignes) · Broker B (lignes différentes) · email non membre (403) · sans email (401) · appel direct avec l'id d'un dossier d'un autre broker (404/403).
