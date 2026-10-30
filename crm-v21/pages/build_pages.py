"""Générateur des pages SuperApp de la V2.1 (JSON du catalogue SuperApp).

Usage : python3 -I build_pages.py → écrit pages/<nom>.json ({title, path, page}).
Vocabulaire : « Opportunité client », « Opportunité de bien », « Catalogue des biens ».
"""
import json
import os

R = "/run/easyspace_schema/crm21"

THEME = {
    "theme": "easyspace",
    "language": "fr",
    "themeTokens": {
        "--background": "#F4F1EA", "--foreground": "#122631",
        "--card": "#FFFFFF", "--card-foreground": "#122631",
        "--popover": "#FFFFFF", "--popover-foreground": "#122631",
        "--primary": "#122631", "--primary-foreground": "#FFFFFF",
        "--muted": "#ECE7DC", "--muted-foreground": "#566D76",
        "--accent": "#F1E8D8", "--accent-foreground": "#122631",
        "--border": "#D8E0E3", "--input": "#D8E0E3", "--ring": "#C7A976",
        "--radius": "12px",
        "--brand-band": "#122631", "--brand-band-foreground": "#FFFFFF", "--brand-band-solid": "#122631",
        "--success": "#1F7A4D", "--warning": "#9A6700", "--danger": "#B42318", "--info": "#2F6F86",
        "--chart-1": "#122631", "--chart-2": "#C7A976", "--chart-3": "#6F8E98", "--chart-4": "#1F7A4D", "--chart-5": "#B4532B",
        "--sans": "Manrope, Inter, system-ui, sans-serif", "--heading": "Manrope, Inter, system-ui, sans-serif",
        "--shadow-soft": "0 1px 2px rgba(18,38,49,0.06)", "--shadow-elegant": "0 6px 20px rgba(18,38,49,0.10)",
    },
}


# ------------------------------------------------------------------ helpers
def n(t, children=None, slot="content", **props):
    node = {"type": t, "props": props}
    if children is not None:
        node["props"][slot] = children
    return node


def stack(children, **p):
    return n("Stack", children, **p)


def row(children, **p):
    p.setdefault("direction", "row")
    p.setdefault("align", "center")
    p.setdefault("gap", "sm")
    return n("Stack", children, **p)


def surf(children, **p):
    p.setdefault("background", "card")
    p.setdefault("radius", "lg")
    p.setdefault("paddingX", "lg")
    p.setdefault("paddingY", "lg")
    p.setdefault("gap", "md")
    p.setdefault("border", "all")
    return n("Surface", children, **p)


def text(t, variant="body", **p):
    return n("Text", text=t, variant=variant, **p)


def badge(label, tone="neutral", **p):
    return n("Badge", label=label, tone=tone, **p)


def btn(label, action, variant="soft", icon="", size="md", **p):
    return n("Button", label=label, action=action, variant=variant, icon=icon, size=size, **p)


def vis(op, path, value=""):
    return {"op": op, "path": path, "value": value}


def nav(to):
    return {"type": "navigate", "to": to}


def call(method, url, body=None, success="Enregistré", body_from=None, extra=None, close=None):
    acts = []
    if close:
        acts.append({"type": "setVariable", "path": close, "value": False})
    acts += [{"type": "refreshData"}, {"type": "showToast", "message": success, "variant": "success"}]
    if extra:
        acts += extra
    a = {"type": "callApi", "method": method, "url": url, "onSuccess": {"type": "sequence", "actions": acts}}
    if body is not None:
        a["body"] = body
    if body_from:
        a["bodyFrom"] = body_from
    return a


def coll(url, item, **p):
    p.setdefault("source", "endpoint")
    p.setdefault("itemsPath", "items")
    p.setdefault("layout", "stack")
    p.setdefault("gap", "sm")
    return n("Collection", item, slot="item", endpointUrl=url, **p)


def record(url, children, **p):
    return n("Record", children, endpointUrl=url, source="endpoint", itemsPath="items", **p)


def modal(state, title, children, description="", size="md"):
    return n("Modal", children, title=title, description=description, statePath=state, size=size)


def form(fields, submit_label, action, title="", state=None):
    p = dict(fields=fields, submitLabel=submit_label, submitAction=action)
    if title:
        p["title"] = title
    if state:
        p["statePath"] = state
    return n("Form", **p)


def fld(name, label, type_="text", required=False, **p):
    d = {"name": name, "label": label, "type": type_, "required": required}
    d.update(p)
    return d


# ------------------------------------------------------------------ en-tête commun
NAV_ITEMS = [
    {"label": "Accueil", "path": "/", "icon": "House"},
    {"label": "Opportunités clients", "path": "/opportunites-clients", "icon": "Users"},
    {"label": "Opportunités de biens", "path": "/opportunites-biens", "icon": "KeyRound"},
    {"label": "Biens", "path": "/biens", "icon": "Building2"},
    {"label": "Agenda", "path": "/agenda", "icon": "CalendarDays"},
]
NAV_ADMIN = NAV_ITEMS + [{"label": "Équipe", "path": "/equipe", "icon": "UsersRound"}]
NAV_DOCK = [
    {"label": "Accueil", "path": "/", "icon": "House"},
    {"label": "Clients", "path": "/opportunites-clients", "icon": "Users"},
    {"label": "Ajouter", "path": "/ajout", "icon": "CirclePlus"},
    {"label": "Biens", "path": "/biens", "icon": "Building2"},
    {"label": "Agenda", "path": "/agenda", "icon": "CalendarDays"},
]


def header(title, subtitle="", back=None, actions=None):
    left = [row(([btn("Retour", {"type": "goBack"}, "ghost", "ArrowLeft", "sm", iconOnly=True)] if back else []) +
                [text(title, "h1")], gap="sm")]
    if subtitle:
        left.append(text(subtitle, "body", tone="muted"))
    right = actions or []
    brand = row([
        n("IconTile", icon="", text="Easy Space", tone="primary", look="solid", size="sm", shape="rounded"),
        text("Easy Space CRM", "h3"),
    ], gap="sm")
    top = row([brand, row([
        btn("Nouveau", nav("/ajout"), "primary", "Plus", "sm", visibility=vis("truthy", "screen.desktop")),
        n("UserMenu", showName=True, themeChoice=True, logoutLabel="Se déconnecter", items=[]),
    ], gap="sm")], justify="between")
    navs = record(R + "/session", [
        n("Navigation", items=NAV_ITEMS, variant="underline", visibility=vis("falsy", "record.admin")),
        n("Navigation", items=NAV_ADMIN, variant="underline", visibility=vis("truthy", "record.admin")),
    ], emptyText="", visibility=vis("truthy", "screen.desktop"))
    return n("Surface", [
        stack([top, navs], gap="md"),
    ], background="card", border="bottom", radius="none", shadow="none", paddingX="xl", paddingY="md", hideInPrint=True), \
        stack([row(left[:1], gap="sm"), *left[1:]] + ([row(right, gap="sm", wrap=True)] if right else []), gap="xs")


def dock():
    return n("Surface", [n("Navigation", items=NAV_DOCK, variant="dock")], background="card", border="none", radius="none",
             paddingX="none", paddingY="none", visibility=vis("truthy", "screen.phone"))


def page(title, path, body, subtitle="", back=False, actions=None):
    hdr, title_block = header(title, subtitle, back, actions)
    content = [hdr, stack([title_block] + body, padding="xl", gap="xl"), dock()]
    return {"title": title, "path": path, "page": {"root": {"props": THEME}, "content": content}}


PAGES = {}

# ------------------------------------------------------------------ Accueil
rdv_hero = record(R + "/accueil", [
    surf([
        row([badge("Prochain rendez-vous", "neutral", icon="CalendarClock"),
             badge("{{record.rdvAujourdhui}} aujourd’hui", "warning", visibility=vis("gt", "record.rdvAujourdhui", "0"))],
            justify="between", wrap=True),
        text("{{record.prochainRdv}}", "h2"),
        text("{{record.prochainRdvQuand}}", "body"),
        row([btn("Ouvrir le dossier", nav("{{record.prochainRdvLien}}"), "outline", "FolderOpen", "sm",
                 visibility=vis("truthy", "record.aUnRdv")),
             btn("Voir l’agenda", nav("/agenda"), "ghost", "CalendarDays", "sm")], wrap=True),
    ], background="brand", border="none", shadow="md", paddingX="xl", paddingY="xl"),
    n("Grid", [
        n("Stat", label="Actions du jour", value="{{record.actionsJour}}", detail="échéance aujourd’hui ou passée", tone="primary", icon="ListChecks", variant="tile"),
        n("Stat", label="En retard", value="{{record.retards}}", detail="échéance dépassée", tone="danger", icon="AlarmClock", variant="tile"),
        n("Stat", label="Comptes rendus à faire", value="{{record.crAFaire}}", detail="RDV passés sans retour", tone="warning", icon="NotebookPen", variant="tile"),
        n("Stat", label="RDV cette semaine", value="{{record.rdvSemaine}}", detail="7 prochains jours", tone="info", icon="CalendarRange", variant="tile"),
    ], columns="4", mobileColumns="2", gap="md"),
    row([text("Comment ces chiffres sont calculés", "caption", tone="subtle"), n("InfoTip", text="{{record.regles}}")], gap="xs"),
], emptyText="")

OC_CARD = surf([
    row([row([n("IconTile", icon="", text="{{item.nom}}", tone="primary", look="soft", size="sm", shape="circle"),
              stack([text("{{item.nom}}", "h3"), text("{{item.prochaineAction | default:Pas d’action prévue}}", "caption", tone="muted")], gap="2xs")], gap="sm"),
         badge("{{item.etape}}", "info")], justify="between", align="start"),
    row([badge("En retard", "danger", icon="AlarmClock", visibility=vis("truthy", "item.enRetard")),
         badge("Aujourd’hui", "warning", visibility=vis("truthy", "item.aujourdhui")),
         text("{{item.echeanceLabel}}", "caption", tone="muted"),
         text("{{item.budgetLabel}}", "caption", tone="muted")], wrap=True),
    text("{{item.aCompleter}}", "caption", tone="subtle", visibility=vis("truthy", "item.aCompleter")),
    row([btn("Ouvrir", nav("{{item.lien}}"), "primary", "FolderOpen", "sm"),
         btn("Appeler", nav("{{item.telUrl}}"), "outline", "Phone", "sm", visibility=vis("truthy", "item.telUrl")),
         btn("WhatsApp", nav("{{item.waUrl}}"), "ghost", "MessageCircle", "sm", visibility=vis("truthy", "item.waUrl"))], wrap=True),
], interactive=True, paddingX="md", paddingY="md", gap="sm")

RDV_ROW = surf([
    row([stack([text("{{item.quand}}", "caption", tone="muted"), text("{{item.titre}}", "h3")], gap="2xs"),
         badge("{{item.statut}}", "neutral")], justify="between", align="start"),
    row([btn("Dossier", nav("{{item.lienClient}}"), "outline", "FolderOpen", "sm", visibility=vis("truthy", "item.lienClient"))]),
], paddingX="md", paddingY="sm", gap="xs")

PAGES["accueil"] = page("Bonjour", "/", [
    rdv_hero,
    stack([text("Actions du jour", "h2"),
           coll(R + "/opportunites-clients?vue=actions&limite=6", [OC_CARD], layout="grid", columns=2,
                emptyText="Aucune action à échéance aujourd’hui. Consultez vos opportunités clients pour planifier la suite."),
           btn("Toutes mes opportunités clients", nav("/opportunites-clients"), "link", "", "sm")], gap="md"),
    n("Grid", [
        stack([text("Prochains rendez-vous", "h2"),
               coll(R + "/activites?vue=a-venir&limite=5", [RDV_ROW],
                    emptyText="Aucun rendez-vous à venir. Planifiez une visite depuis une opportunité client.")], gap="md"),
        stack([text("Dossiers chauds", "h2"),
               coll(R + "/opportunites-clients?vue=chauds&limite=5", [OC_CARD],
                    emptyText="Aucun dossier en négociation ou prioritaire pour le moment.")], gap="md"),
    ], columns="2", gap="xl"),
], subtitle="Votre journée en un coup d’œil")

# ------------------------------------------------------------------ Liste opportunités clients
PAGES["opportunites-clients"] = page("Opportunités clients", "/opportunites-clients", [
    row([n("Segmented", options="actifs:En cours, actions:À faire, retard:En retard, a-completer:À compléter, toutes:Toutes",
           statePath="state.vue", defaultValue="actifs", size="sm"),
         n("TextInput", type="search", placeholder="Nom, quartier, téléphone", statePath="state.q", width="md", icon="Search")],
        justify="between", wrap=True),
    coll(R + "/opportunites-clients?vue={{state.vue}}&q={{state.q}}", [OC_CARD], layout="grid", columns=2,
         emptyText="Aucune opportunité client dans cette vue. Changez de filtre ou ajoutez un lead."),
], subtitle="Votre portefeuille, trié par échéance", actions=[btn("Nouveau lead", nav("/ajout?onglet=1"), "primary", "UserPlus", "sm")])

# ------------------------------------------------------------------ Fiche opportunité client
CID = "{{query.id}}"
PROP_CARD = surf([
    row([n("IconTile", icon="Building2", image="{{item.photo}}", tone="neutral", look="soft", size="md", shape="rounded"),
         stack([text("{{item.nom}}", "h3"), text("{{item.prixLabel}} · {{item.localisation}}", "caption", tone="muted")], gap="2xs", grow=True),
         badge("{{item.statut}}", "info")], align="start"),
    text("Retour : {{item.retour}}", "caption", tone="muted", visibility=vis("truthy", "item.retour")),
    row([btn("Intéressé", {"type": "callApi", "method": "PATCH", "url": R + "/propositions", "body": {"id": "{{item.id}}", "statut": "Intéressé"},
                           "onSuccess": {"type": "sequence", "actions": [{"type": "refreshData"}, {"type": "showToast", "message": "Retour enregistré", "variant": "success"}]}},
             "soft", "ThumbsUp", "sm"),
         btn("Refusé", {"type": "confirm", "title": "Le client refuse ce bien ?", "message": "Précisez la raison pour affiner les prochaines propositions.",
                        "inputLabel": "Raison du refus", "inputRequired": True, "confirmLabel": "Enregistrer",
                        "onConfirm": {"type": "callApi", "method": "PATCH", "url": R + "/propositions",
                                      "body": {"id": "{{item.id}}", "statut": "Refusé", "retour": {"type": "runtime", "path": "payload.input"}},
                                      "onSuccess": {"type": "refreshData"}}}, "ghost", "ThumbsDown", "sm"),
         btn("Visite demandée", {"type": "callApi", "method": "PATCH", "url": R + "/propositions", "body": {"id": "{{item.id}}", "statut": "Visite demandée"},
                                 "onSuccess": {"type": "sequence", "actions": [{"type": "refreshData"}, {"type": "setVariable", "path": "state.rdvOuvert", "value": True}]}},
             "ghost", "CalendarPlus", "sm"),
         btn("Voir le bien", nav("{{item.lienBien}}"), "link", "", "sm")], wrap=True),
], paddingX="md", paddingY="md", gap="sm")

MATCH_CARD = surf([
    row([n("IconTile", icon="Building2", image="{{item.photo}}", tone="neutral", look="soft", size="md", shape="rounded"),
         stack([text("{{item.nom}}", "h3"), text("{{item.prixLabel}} · {{item.surfaceLabel}} · {{item.localisation}}", "caption", tone="muted")], gap="2xs", grow=True)],
        align="start"),
    text("{{item.criteres}}", "caption", tone="success"),
    text("{{item.limites}}", "caption", tone="subtle", visibility=vis("truthy", "item.limites")),
    row([btn("Proposer", call("POST", R + "/propositions", {"clientId": CID, "bienId": "{{item.id}}"}, "Bien proposé au client"), "primary", "Send", "sm"),
         btn("Voir le bien", nav("{{item.lien}}"), "link", "", "sm")], wrap=True),
], paddingX="md", paddingY="md", gap="xs")

RDV_FORM = form([
    fld("date", "Date", "date", True, width="half"),
    fld("heure", "Heure", "time", True, width="half", help="Heure de Casablanca"),
    fld("dureeMin", "Durée", "select", False, options="30:30 min, 60:1 h, 90:1 h 30, 120:2 h", defaultValue="60", width="half"),
    fld("nature", "Type", "select", False, options="Visite, Appel, Rendez-vous agence, Signature", defaultValue="Visite", width="half"),
    fld("bienId", "Bien concerné", "select", False, optionsEndpoint=R + "/propositions?clientId=" + CID, valueKey="bienId", labelKey="nom",
        help="Parmi les biens proposés"),
    fld("note", "Note", "textarea", False),
], "Planifier le rendez-vous",
    call("POST", R + "/rdv", {"clientId": CID}, "Rendez-vous enregistré", body_from="payload.values", close="state.rdvOuvert"))

CR_FORM = form([
    fld("id", "Rendez-vous", "select", True, optionsEndpoint=R + "/activites?clientId=" + CID + "&vue=cr", valueKey="id", labelKey="quand"),
    fld("appreciation", "Appréciation du client", "textarea", True),
    fld("objections", "Objections", "textarea", False),
    fld("prochaineEtape", "Prochaine étape", "text", False),
], "Enregistrer le compte rendu",
    call("PATCH", R + "/rdv", {"action": "compte-rendu"}, "Compte rendu enregistré", body_from="payload.values", close="state.crOuvert"))

NOTE_FORM = form([fld("texte", "Note", "textarea", True)], "Ajouter la note",
                 call("POST", R + "/notes", {"clientId": CID}, "Note ajoutée", body_from="payload.values", close="state.noteOuvert"))

SUIVI_FORM = form([
    fld("etape", "Étape", "select", False, optionsEndpoint=R + "/referentiels", options="Nouveau, À qualifier, Qualifié, Recherche active, Biens proposés, Visite Proposée, RDV Visite Validé, Visite Effectuée, Négociation, Finalisation, Gagné, Perdu, En Pause", defaultValue="{{record.etape}}"),
    fld("prochaineAction", "Prochaine action", "select", False, options="Appeler, Demander des informations, Rechercher des biens, Proposer des biens, Planifier une visite, Confirmer le RDV de Visite, Faire le suivi après visite, Proposer une Autre Visite, Proposer Offre Finacière:Proposer une offre financière", defaultValue="{{record.prochaineAction}}"),
    fld("echeanceDate", "Échéance", "date", False, width="half", defaultValue="{{record.echeanceJour}}"),
    fld("echeanceHeure", "Heure", "time", False, width="half"),
    fld("priorite", "Priorité", "radio", False, options="Normale, Haute, Urgente", defaultValue="{{record.priorite}}"),
    fld("budget", "Budget", "money", False, unit="DH", defaultValue="{{record.budget}}", width="half"),
    fld("quartier", "Quartier(s)", "text", False, defaultValue="{{record.quartier}}", width="half"),
], "Enregistrer", call("PATCH", R + "/opportunites-clients", {"id": CID}, "Dossier mis à jour", body_from="payload.values", close="state.suiviOuvert"))
SUIVI_FORM["props"]["fields"][0].pop("optionsEndpoint")

PAGES["opportunite-client"] = page("Opportunité client", "/opportunite-client", [
    record(R + "/opportunite-client?id=" + CID, [
        surf([
            row([stack([text("{{record.nom}}", "h2"), text("{{record.criteresLabel}}", "body", tone="muted")], gap="2xs"),
                 row([badge("{{record.etape}}", "info"), badge("En retard", "danger", visibility=vis("truthy", "record.enRetard")),
                      badge("Priorité {{record.priorite}}", "warning", visibility=vis("neq", "record.priorite", "Normale"))], wrap=True)],
                justify="between", align="start", wrap=True),
            row([text("À faire : {{record.prochaineAction | default:—}} · {{record.echeanceLabel}}", "body")], wrap=True),
            row([btn("Appeler", nav("{{record.telUrl}}"), "primary", "Phone", "md", visibility=vis("truthy", "record.telUrl")),
                 btn("WhatsApp", nav("{{record.waUrl}}"), "outline", "MessageCircle", "md", visibility=vis("truthy", "record.waUrl")),
                 btn("Planifier un RDV", {"type": "setVariable", "path": "state.rdvOuvert", "value": True}, "soft", "CalendarPlus", "md"),
                 btn("Compte rendu", {"type": "setVariable", "path": "state.crOuvert", "value": True}, "soft", "NotebookPen", "md"),
                 btn("Note", {"type": "setVariable", "path": "state.noteOuvert", "value": True}, "ghost", "StickyNote", "md"),
                 btn("Modifier le suivi", {"type": "setVariable", "path": "state.suiviOuvert", "value": True}, "ghost", "Pencil", "md",
                     visibility=vis("truthy", "record.modifiable"))], wrap=True),
            n("Alert", tone="warning", title="Informations à compléter", text="{{record.aCompleter}}", icon="CircleAlert",
              visibility=vis("truthy", "record.aCompleter")),
        ], background="card", shadow="sm", paddingX="xl", paddingY="xl"),
        n("Tabs", variant="underline", queryParam="onglet", tabs="Projet|ClipboardList, Biens proposés|Send, Biens correspondants|Sparkles, Historique|History",
          tab1=[n("Grid", [
              n("Details", rows=[
                  {"label": "Contact", "value": "{{record.contact}}"}, {"label": "Statut du contact", "value": "{{record.contactStatut}}", "tone": "info"},
                  {"label": "Téléphone", "value": "{{record.contactTel | default:—}}"}, {"label": "Broker", "value": "{{record.broker}}"},
                  {"label": "Canal d’entrée", "value": "{{record.canal | default:—}}"}]),
              n("Details", rows=[
                  {"label": "Transaction", "value": "{{record.transaction | default:—}}"}, {"label": "Type de bien", "value": "{{record.typeBien | default:—}}"},
                  {"label": "Budget", "value": "{{record.budgetLabel}}"}, {"label": "Quartier(s)", "value": "{{record.quartier | default:—}}"},
                  {"label": "Surface", "value": "{{record.surfaceLabel}}"}, {"label": "Chambres", "value": "{{record.chambres | default:—}}"},
                  {"label": "Autres critères", "value": "{{record.criteres | default:—}}"}]),
          ], columns="2", gap="lg")],
          tab2=[coll(R + "/propositions?clientId=" + CID, [PROP_CARD],
                     emptyText="Aucun bien proposé. Ouvrez l’onglet Biens correspondants pour en proposer un.")],
          tab3=[n("Alert", tone="info", icon="Info", title="Méthode",
                  text="Biens actifs, transaction et type compatibles, prix au plus 15 % au-dessus du budget, quartier demandé. Les critères vérifiés sont indiqués sur chaque bien ; rien n’est proposé automatiquement."),
                coll(R + "/rapprochements?clientId=" + CID, [MATCH_CARD], layout="grid", columns=2,
                     emptyText="Aucun bien actif ne correspond aux critères. Complétez le budget et le quartier pour élargir la recherche.")],
          tab4=[n("Timeline", source="endpoint", endpointUrl=R + "/historique?clientId=" + CID, itemsPath="items",
                  dateKey="quand", titleKey="titre", textKey="texte", emptyText="Pas encore d’historique sur ce dossier.")]),
        modal("state.rdvOuvert", "Planifier un rendez-vous", [RDV_FORM], "Le rendez-vous est ajouté à l’agenda du broker du dossier."),
        modal("state.crOuvert", "Compte rendu de rendez-vous", [CR_FORM], "Choisissez un rendez-vous passé sans compte rendu."),
        modal("state.noteOuvert", "Ajouter une note", [NOTE_FORM]),
        modal("state.suiviOuvert", "Modifier le suivi", [SUIVI_FORM], "Seuls les champs changés sont enregistrés et tracés."),
    ], emptyText="Dossier introuvable ou non autorisé."),
], back=True)

# ------------------------------------------------------------------ Catalogue des biens
BIEN_CARD = surf([
    n("Image", src="{{item.photo}}", alt="Photo du bien {{item.nom}}", ratio="video", fit="cover", radius="md", visibility=vis("truthy", "item.aPhoto")),
    n("Surface", [row([n("IconTile", icon="Building2", tone="neutral", look="soft", size="lg"), text("Photo indisponible", "caption", tone="muted")], justify="center")],
      background="muted", radius="md", paddingY="2xl", visibility=vis("falsy", "item.aPhoto")),
    row([badge("{{item.dispo}}", "success", visibility=vis("eq", "item.dispo", "Actif")),
         badge("{{item.dispo}}", "neutral", visibility=vis("eq", "item.dispo", "Inactif")),
         badge("{{item.dispo}}", "warning", visibility=vis("eq", "item.dispo", "À confirmer")),
         badge("{{item.transaction}}", "neutral"), badge("Mon bien", "primary", visibility=vis("truthy", "item.mien"))], wrap=True),
    text("{{item.nom}}", "h3"),
    text("{{item.prixLabel}} · {{item.surfaceLabel}} · {{item.localisation}}", "caption", tone="muted"),
    btn("Voir la fiche", nav("{{item.lien}}"), "outline", "", "sm"),
], interactive=True, paddingX="md", paddingY="md", gap="sm")

PAGES["biens"] = page("Catalogue des biens", "/biens", [
    row([n("Segmented", options=":Tous les biens, 1:Mes biens", statePath="state.mes", defaultValue="", size="sm"),
         n("Segmented", options=":Toutes, Vente, Location", statePath="state.tx", defaultValue="", size="sm"),
         n("Select", options="appartement:Appartement, studio:Studio, villa:Villa, bureau:Bureau, local commerciale:Local commercial, magasin:Magasin, terrain:Terrain",
           allLabel="Tous types", statePath="state.type", width="sm"),
         n("TextInput", type="search", placeholder="Quartier, nom", statePath="state.q", width="md", icon="Search")], wrap=True),
    coll(R + "/biens?mes={{state.mes}}&transaction={{state.tx}}&type={{state.type}}&q={{state.q}}&dispo=Actif", [BIEN_CARD],
         layout="grid", columns=3, limit=24, loadMore=True,
         emptyText="Aucun bien disponible avec ces filtres. Élargissez la recherche."),
], subtitle="Biens disponibles, partagés entre brokers")

# ------------------------------------------------------------------ Fiche bien
PROPOSER_FORM = form([
    fld("clientId", "Opportunité client", "select", True, optionsEndpoint=R + "/opportunites-clients", valueKey="id", labelKey="nom"),
], "Proposer ce bien", call("POST", R + "/propositions", {"bienId": "{{query.id}}"}, "Bien proposé", body_from="payload.values", close="state.proposerOuvert"))

PAGES["bien"] = page("Fiche bien", "/bien", [
    record(R + "/bien?id={{query.id}}", [
        n("Grid", [
            stack([
                n("Image", src="{{record.photo}}", alt="Photo du bien {{record.nom}}", ratio="wide", fit="cover", radius="lg", visibility=vis("truthy", "record.aPhoto")),
                n("Surface", [n("EmptyState", icon="ImageOff", title="Photo indisponible", text="Le lien de la photo n’est pas accessible. Demandez une photo au gestionnaire.", framed=False)],
                  background="muted", radius="lg", visibility=vis("falsy", "record.aPhoto")),
            ], gap="md"),
            stack([
                row([badge("{{record.dispo}}", "success", visibility=vis("eq", "record.dispo", "Actif")),
                     badge("{{record.dispo}}", "warning", visibility=vis("neq", "record.dispo", "Actif")),
                     badge("{{record.transaction}}", "neutral"), badge("Mon bien", "primary", visibility=vis("truthy", "record.mien"))], wrap=True),
                text("{{record.nom}}", "h2"),
                text("{{record.prixLabel}}", "h3"),
                text("{{record.surfaceLabel}} · {{record.chambres | default:—}} ch. · {{record.localisation}}", "body", tone="muted"),
                row([btn("Proposer à un client", {"type": "setVariable", "path": "state.proposerOuvert", "value": True}, "primary", "Send", "md"),
                     btn("Appeler le gestionnaire", nav("{{record.gestionnaireTelUrl}}"), "outline", "Phone", "md", visibility=vis("truthy", "record.gestionnaireTelUrl"))], wrap=True),
            ], gap="sm"),
        ], columns="3:2", gap="xl"),
        n("Grid", [
            n("Details", rows=[
                {"label": "Gestionnaire", "value": "{{record.gestionnaire | default:—}}"},
                {"label": "Interlocuteur", "value": "{{record.gestionnaireStatut}}", "tone": "info"},
                {"label": "Provenance", "value": "{{record.provenance | default:—}}"},
                {"label": "Responsable", "value": "{{record.responsable | default:—}}"}]),
            n("Details", rows=[
                {"label": "Disponibilité", "value": "{{record.dispoConfirmee}}"},
                {"label": "Clients", "value": "{{record.interessesLabel}}"},
                {"label": "Prochaine action", "value": "{{record.prochaineAction | default:—}}"},
                {"label": "Échéance", "value": "{{record.echeanceLabel | default:—}}"}]),
        ], columns="2", gap="lg"),
        n("Markdown", text="{{record.resume}}", visibility=vis("truthy", "record.resume")),
        modal("state.proposerOuvert", "Proposer ce bien", [PROPOSER_FORM], "Seules vos opportunités clients sont listées."),
    ], emptyText="Bien introuvable."),
], back=True)

# ------------------------------------------------------------------ Agenda
AG_ROW = surf([
    row([stack([text("{{item.jourLabel}} · {{item.heure}}", "caption", tone="muted"), text("{{item.titre}}", "h3")], gap="2xs"),
         row([badge("{{item.statut}}", "success", visibility=vis("eq", "item.statut", "Effectué")),
              badge("{{item.statut}}", "danger", visibility=vis("eq", "item.statut", "Annulé")),
              badge("{{item.statut}}", "info", visibility=vis("eq", "item.statut", "Confirmé")),
              badge("{{item.statut}}", "warning", visibility=vis("eq", "item.statut", "À confirmer"))])], justify="between", align="start"),
    row([btn("Dossier", nav("{{item.lienClient}}"), "outline", "FolderOpen", "sm", visibility=vis("truthy", "item.lienClient")),
         btn("Confirmer", call("PATCH", R + "/rdv", {"id": "{{item.id}}", "action": "confirmer"}, "Rendez-vous confirmé"), "soft", "Check", "sm",
             visibility=vis("eq", "item.statut", "À confirmer")),
         btn("Compte rendu", nav("{{item.lienClient}}"), "soft", "NotebookPen", "sm", visibility=vis("truthy", "item.aFaireCR")),
         btn("Annuler", {"type": "confirm", "title": "Annuler ce rendez-vous ?", "message": "Le client n’est pas prévenu automatiquement.",
                         "inputLabel": "Motif", "inputRequired": False, "variant": "danger", "confirmLabel": "Annuler le RDV",
                         "onConfirm": {"type": "callApi", "method": "PATCH", "url": R + "/rdv",
                                       "body": {"id": "{{item.id}}", "action": "annuler", "motif": {"type": "runtime", "path": "payload.input"}},
                                       "onSuccess": {"type": "refreshData"}}},
             "ghost", "X", "sm", visibility=vis("truthy", "item.aVenir"))], wrap=True),
], paddingX="md", paddingY="sm", gap="xs")

PAGES["agenda"] = page("Agenda", "/agenda", [
    n("Calendar", source="endpoint", endpointUrl=R + "/activites", itemsPath="items", dateKey="debut", titleKey="titre", statusKey="statut",
      badgeTones="À confirmer:warning, Confirmé:info, Effectué:success, Annulé:danger", views="month, week, day", defaultView="week",
      hours="8-21", weekStart="monday", visibility=vis("truthy", "screen.desktop")),
    stack([text("À venir", "h2"),
           coll(R + "/activites?vue=a-venir", [AG_ROW], emptyText="Aucun rendez-vous à venir. Planifiez-en un depuis une opportunité client.")], gap="md"),
    stack([text("Comptes rendus à faire", "h2"),
           coll(R + "/activites?vue=cr&limite=10", [AG_ROW], emptyText="Tous les rendez-vous passés ont leur compte rendu.")], gap="md"),
], subtitle="Heures de Casablanca")


def write_all(outdir):
    for k, p in PAGES.items():
        with open(os.path.join(outdir, k + ".json"), "w") as f:
            json.dump(p, f, ensure_ascii=False, indent=1)
        print(k, len(json.dumps(p)))


if __name__ == "__main__":
    write_all(os.path.dirname(os.path.abspath(__file__)))
