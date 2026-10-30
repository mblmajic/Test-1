# SuperAPP CRM easyspace V2.1 — invariants (à relire au début de chaque session)

- Ne jamais modifier les pages, la configuration ni les endpoints /crm1/ de « Easy Space CRM1 » (id ed144d14-f98f-4a42-b2e1-c7f8764cb6ef).
- Ne jamais supprimer de donnée réelle. Les données de recette sont préfixées « [RECETTE V21] » et consignées dans tests/recette_registry.json dès leur création.
- Ne jamais envoyer de message réel (WhatsApp, email, SMS, Telegram) à un client ou un broker pendant les essais. Le workflow n8n « Telegram — Alertes CRM — V2 » est EN PRODUCTION : ne jamais lui fournir de ligne « À envoyer » en recette.
- Ne jamais demander de mot de passe ni de clé secrète. Utiliser uniquement les credentials référencés par les outils.
- L'identité et le rôle viennent de la session authentifiée (auth.claims.email) rapprochée du référentiel serveur (Agents brokers internes mf37113735cdd038b), jamais d'un paramètre envoyé par le navigateur. Tous les comptes plateforme ont le rôle « Admin Domaine » : auth.claims.roles ne distingue PAS broker et admin.
- Une fonction non opérationnelle n'apparaît pas comme active : masquée ou marquée « Bientôt ».
- Source de vérité : état réel lu par les outils > documents > prompt.
- Toute nouvelle table va dans SuperAPP_easyspace_CRM1 (pmvv68h6de6cr, Postgres natif), préfixée « CRM21 ». Jamais de nouvelle base.
- Préfixe endpoints : /crm21/. App : « SuperAPP CRM easyspace V2.1 », workspace 35. Source SmartDB API Studio : de074ee7-7e90-4df1-bd97-6f53613204bc. Pages : chemins relatifs /run/easyspace_schema/…
- Points d'arrêt : GATE 1 audit · GATE 2 schéma · GATE 3 publish_endpoint · GATE 4 publish_page/app · GATE 5 accès/adresse · GATE 6 données réelles/migration/suppression.
