"""Générateur des définitions d'endpoints /crm21/ (SuperAPP CRM easyspace V2.1).

Usage : python3 -I build_crm21.py  → écrit contracts/endpoints/crm21__<METHODE>_<chemin>.json
Chaque fichier = {"name", "description", "definition"} prêt pour save_endpoint.
"""
import json
import os

DS = "de074ee7-7e90-4df1-bd97-6f53613204bc"
T = {
    "membres": "m3070c01f4ae9eb21",
    "periodes": "m417041728cf6ca7e",
    "verrous": "m5357c4d6f54f2868",
    "oc": "m80adee8ba2348dfe",
    "ob": "m13dd0abc30554ba9",
    "biens": "ma9b9bb062ad8b271",
    "act": "m3573c7a505385e65",
    "contacts": "m4bf4b323ba241e7d",
    "props": "m5ba929066e4852f4",
    "journal": "m638173347625af09",
    "affect": "mf4841a083ad93de7",
}

# Colonnes Opportunités clients
OC = dict(broker="src_c2ljvedgo8rjnjz", prenom="src_c8j7pxeprb45sel", nomf="src_cu4m58kh70jsaas",
          etape="src_ch80mhxt9wmgffa", action="src_cwm9erw27y2a5ax", echeance="src_csdkjyu1i3h2rpd",
          detail="src_caw1n932cne75bt", tel="src_cmt5f5y6apb9n76", prio="src_cp1ak79dze4j7zb",
          quartier="src_crid8q8n1p0n7qe", tx="src_cc9t923zypqax4s", type="src_cqx1ht4dg6mt0gl",
          ville="src_cjuumr2e0utdov7", bl="src_c0qcaxijrq4e44n", ba="src_c8ty9timbln0feq",
          smin="src_cali7clgn81g11x", smax="src_cdivmzu7n1bn63g", ch="src_cj59gxz110km911",
          canal="src_c90ihchqcq0h8hz", criteres="src_csbs48a1es5ynk0", remarques="src_csluzp2qkfjfaw0",
          meuble="src_chjo5jv3sbsxelr", contact="pmv6m9j8dh2qj_contacts_id")
OC_COLS = ["id", "libelle", "updated_at", "crm_cle_creation"] + [v for k, v in OC.items()]

# Colonnes Biens
BI = dict(dispo="src_ckik8lj9kqev9ho", resp="src_c9w1scpswzkjl7g", image="src_ce4lcsor6pndckt",
          nom="src_c30sp73xdb9jdsx", type="src_cy2vb7l7nqcvdec", tx="src_c771ftquhdtvl0r",
          prix="src_c5waewdapjudd8k", surface="src_c4in13ik1q3f1fw", quartier="src_c15ey3zrlrmehdi",
          ville="src_cdespozafnudzr4", ch="src_c16ypivc4c8xya2", sdb="src_co2ku7v5kyzazad",
          etatimg="src_ceni271nn57qrii", gest="src_cv0gxc73awfgmpw", gesttel="src_cmb84pfu1pwkzw5",
          typegest="src_c9vw20gbxhe7cl5", meuble="src_cngnzz2fnhhw2p7", etage="src_csh42ie4h7xo475",
          resume="src_csw28jpixscbfu7", url="src_cx5357kv1ngqndv", cat="src_clwha6vpojuo0p7")
BI_COLS = ["id", "libelle", "statut_brief", "date_confirmation_dispo", "crm_prochaine_action", "crm_echeance",
           "crm_priorite", "crm_notes_suivi", "tat_de_migration_gestionnaire", "affectations_des_gestionnaires_id",
           "annonceurs_immobiliers_id", "updated_at"] + list(BI.values())

# Colonnes Opportunités de biens
OB = dict(statut="src_cey267rja2wv3lq", nom="src_c7a50877zqv8he2", type="src_cd5vgyi78qkg52p",
          prix="src_cwqc3dj4cewpssd", surface="src_cgxt2lkxiqv17wa", quartier="src_cg613eoqivagf9q",
          ville="src_cp1785bk483rstm", tx="src_cjww4qd9gmywdmx", resp="src_cazse08x5syk1gn",
          gest="src_cw8g5cc2gv9f6dz", gesttel="src_c0utrhay1h28b7j", image="src_c17fpsjfd07usk6",
          etatimg="src_cedb9jfgba1ogoj", ch="src_cp4v6o8sxsi64wx", typegest="src_cldjhcgfg5ho2wl",
          resume="src_c7dy2hrzq6flh6y", source="src_cex87mixcqmt60b", notes="src_ckr3g93jwb610nn",
          actionbroker="src_c2vdcfa02rjpqcg")
OB_COLS = ["id", "libelle", "resultat_commercial", "crm_prochaine_action", "crm_echeance", "crm_detail_action",
           "crm_priorite", "crm_notes_suivi", "tat_de_migration_gestionnaire", "affectations_des_gestionnaires_id",
           "pmv6m9j8dh2qj_biens_id", "contacts_id", "updated_at"] + list(OB.values())

# Colonnes Activités
AC = dict(debut="src_cybzjmjoj4zlch0", nature="src_c2xrwp99jzayeub", statut="src_cwtdcarxql2laii")
AC_COLS = ["id", "libelle", "crm_fin", "crm_broker", "crm_etat_visite", "crm_appreciation", "crm_objections",
           "crm_prochaine_etape", "crm_historique_cr", "crm_est_test", "crm_cle_creation", "opportunit_s_clients_id",
           "biens_id", "biens_opportunit_id", "contacts_id"] + list(AC.values())

FR_ETAPES = ["Nouveau", "À qualifier", "Qualifié", "Recherche active", "Biens proposés", "Visite Proposée",
             "RDV Visite Validé", "Visite Effectuée", "Négociation", "Finalisation", "Gagné", "Perdu", "En Pause"]

# ---------------------------------------------------------------- étapes communes


def ds(key, op, params, name=None, run_if=None, on_error=None):
    s = {"key": key, "name": name or key, "type": "datasource",
         "config": {"dataSourceId": DS, "operation": op, "params": params}}
    if run_if:
        s["runIf"] = run_if
    if on_error:
        s["onError"] = on_error
    return s


def tr(key, expr, name=None, run_if=None):
    # JSONata : une suite d'instructions « ; » doit être entourée de parenthèses
    expr = "(\n" + expr.strip() + "\n)"
    s = {"key": key, "name": name or key, "type": "transform", "config": {"expression": expr}}
    if run_if:
        s["runIf"] = run_if
    return s


def respond(key, status, body, run_if=None, name=None):
    s = {"key": key, "name": name or key, "type": "respond",
         "config": {"status": status, "headers": [], "body": body}}
    if run_if:
        s["runIf"] = run_if
    return s


def flt(col, op, value=None, skip=False):
    f = {"column": col, "operator": op}
    if value is not None:
        f["value"] = value
    if skip:
        f["skipIfEmpty"] = True
    return f


IDENT = [
    respond("g401", 401, "{'error':'Session expirée. Reconnectez-vous.'}",
            "$not($exists(auth.claims.email)) or $string(auth.claims.email) = ''", "Session requise"),
    ds("moi", "listRecords", {"table": T["membres"],
                              "filters": [flt("email", "eq", "{{ $lowercase($string(auth.claims.email)) }}")],
                              "columns": ["id", "email", "nom", "role", "broker", "actif"], "limit": 1},
       "Membre CRM21"),
    tr("ident", "($m := steps.moi.rows[0]; $act := $string($m.actif) = 'true'; $r := $string($m.role); "
                "$bk := $exists($m.broker) and $type($m.broker) != 'null' ? $string($m.broker) : ''; "
                "{'email': $lowercase($string(auth.claims.email)), 'nom': $act ? $string($m.nom) : '', "
                "'role': $act ? $r : '', 'admin': $act and $r = 'Admin', 'broker': $act ? $bk : '', "
                "'ok': $act and ($r = 'Admin' or ($r = 'Broker' and $bk != ''))})", "Identité"),
    respond("g403", 403, "{'error':'Votre compte n’est pas encore activé dans le CRM. Contactez l’administrateur.'}",
            "$not(steps.ident.ok)", "Membre actif requis"),
]
ADMIN_ONLY = respond("gadmin", 403, "{'error':'Accès réservé à l’administrateur.'}", "$not(steps.ident.admin)",
                     "Réservé admin")
PER = ds("per", "listRecords", {"table": T["periodes"], "columns": ["debut_utc", "fin_utc", "decalage_min"],
                                "limit": 50}, "Périodes horaires")

# Filtre « mes dossiers » : vide pour l'admin → ignoré ; jamais vide pour un broker (garanti par ident.ok)
MINE = "{{ steps.ident.admin ? '' : steps.ident.broker }}"

# Helpers JSONata partagés (début de chaque transform de mise en forme)
H = r"""
$s := function($v){ ($exists($v) and $type($v) != 'null') ? $replace($string($v), '"', '') : '' };
$n := function($v){ ($x := $s($v); $x != '' and $x != 'null' ? $number($x) : null) };
$b := function($v){ $s($v) = 'true' };
$ms := function($iso){ ($x := $replace($s($iso), /\.[0-9]+/, ''); $x != '' ? $toMillis($x) : null) };
$per := $$.steps.per.rows;
$off := function($t){ ($p := $per[$ms(debut_utc) <= $t and $t < $ms(fin_utc)][0]; $exists($p) ? $n($p.decalage_min) : 60) };
$tzp := function($t){ $off($t) = 0 ? '+0000' : '+0100' };
$loc := function($iso, $pic){ ($t := $ms($iso); $exists($t) ? $fromMillis($t, $pic, $tzp($t)) : '') };
$nowms := $millis();
$today := $fromMillis($nowms, '[Y0001]-[M01]-[D01]', $tzp($nowms));
$tomorrow := $fromMillis($nowms + 86400000, '[Y0001]-[M01]-[D01]', $tzp($nowms + 86400000));
$in7 := $fromMillis($nowms + 7 * 86400000, '[Y0001]-[M01]-[D01]', $tzp($nowms));
$JOURS := ['lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.', 'dim.'];
$MOIS := ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
$jour := function($iso){ $loc($iso, '[Y0001]-[M01]-[D01]') };
$heure := function($iso){ $loc($iso, '[H01]:[m01]') };
$labelJour := function($iso){ ($d := $jour($iso); $d = '' ? '' : ($d = $today ? 'Aujourd’hui' : ($d = $tomorrow ? 'Demain' : $JOURS[$number($loc($iso, '[F1]')) - 1] & ' ' & $loc($iso, '[D1]') & ' ' & $MOIS[$number($loc($iso, '[M1]')) - 1]))) };
$labelDate := function($iso){ ($d := $labelJour($iso); $d = '' ? '' : ($h := $heure($iso); $h = '00:00' ? $d : $d & ' · ' & $h)) };
$dh := function($x){ $exists($x) and $x != null and $x > 0 ? $formatNumber($x, '#,##0', {'grouping-separator': ' '}) & ' DH' : '—' };
$digits := function($t){ $replace($s($t), /[^0-9]/, '') };
$intl := function($t){ ($d := $digits($t); $length($d) < 8 ? '' : ($substring($d, 0, 2) = '00' ? $substring($d, 2) : ($substring($d, 0, 1) = '0' ? '212' & $substring($d, 1) : ($length($d) = 9 ? '212' & $d : $d)))) };
$recette := function($t){ $contains($s($t), '[RECETTE V21]') or $contains($s($t), 'RECETTE CRM1') };
$voirRecette := $$.input.query.recette = '1';
$moi := $$.steps.ident;
"""

OC_MAP = r"""
$ETAPES_ACTIVES := ['Nouveau', 'À qualifier', 'Qualifié', 'Recherche active', 'Biens proposés', 'Visite Proposée', 'RDV Visite Validé', 'Visite Effectuée', 'Négociation', 'Finalisation'];
$etapeTone := function($e){ $e = 'Gagné' ? 'success' : ($e = 'Perdu' ? 'danger' : ($e = 'En Pause' ? 'neutral' : ($e in ['Visite Effectuée', 'Négociation', 'Finalisation'] ? 'warning' : 'info'))) };
$ocNom := function($r){ ($l := $s($r.libelle); $l != '' and $l != '[object Object]' ? $l : ($p := $trim($s($r.%(prenom)s) & ' ' & $s($r.%(nomf)s)); $p != '' ? $p : 'Dossier #' & $s($r.id))) };
$oc := function($r){ (
  $e := $s($r.%(etape)s); $ech := $s($r.%(echeance)s); $tx := $s($r.%(tx)s);
  $bud := $tx = 'Location' ? $n($r.%(bl)s) : $n($r.%(ba)s);
  $manque := [($tx = '' ? 'transaction' : null), ($bud = null ? 'budget' : null), ($s($r.%(quartier)s) = '' ? 'quartier' : null), ($s($r.%(type)s) = '' ? 'type de bien' : null), ($s($r.%(contact)s) = '' and $s($r.%(tel)s) = '' ? 'contact' : null)][$ != null];
  $actif := $e in $ETAPES_ACTIVES or $e = '';
  $wa := $intl($r.%(tel)s);
  {
    'id': $n($r.id), 'lien': '/opportunite-client?id=' & $s($r.id), 'nom': $ocNom($r),
    'broker': $s($r.%(broker)s), 'etape': $e = '' ? 'Nouveau' : $e, 'etapeTone': $etapeTone($e),
    'prochaineAction': $s($r.%(action)s), 'detailAction': $s($r.%(detail)s),
    'echeance': $loc($ech, '[Y0001]-[M01]-[D01]T[H01]:[m01]'), 'echeanceJour': $jour($ech),
    'echeanceLabel': $ech = '' ? 'Pas d’échéance' : $labelDate($ech),
    'enRetard': $actif and $ech != '' and $jour($ech) < $today,
    'aujourdhui': $actif and $jour($ech) = $today,
    'priorite': $s($r.%(prio)s) = '' ? 'Normale' : $s($r.%(prio)s),
    'prioriteTone': $s($r.%(prio)s) = 'Urgente' ? 'danger' : ($s($r.%(prio)s) = 'Haute' ? 'warning' : 'neutral'),
    'transaction': $tx, 'typeBien': $s($r.%(type)s), 'quartier': $s($r.%(quartier)s), 'ville': $s($r.%(ville)s),
    'budget': $bud, 'budgetLabel': $dh($bud),
    'telephone': $s($r.%(tel)s), 'telUrl': $wa != '' ? 'tel:+' & $wa : '', 'waUrl': $wa != '' ? 'https://wa.me/' & $wa : '',
    'aCompleter': $count($manque) > 0 ? 'À compléter : ' & $join($manque, ', ') : '', 'nbACompleter': $count($manque),
    'avancee': $e in ['Visite Effectuée', 'Négociation', 'Finalisation'], 'actif': $actif,
    'contactId': $n($r.%(contact)s)
  }
) };
""" % OC

ACT_MAP = r"""
$actTone := function($st, $etat){ $st = 'Annulé' or $etat = 'Annulée' ? 'danger' : ($st in ['Terminé', 'Visité'] or $etat = 'Effectuée' ? 'success' : ($etat = 'Confirmée' ? 'info' : 'warning')) };
$act := function($r){ (
  $d := $s($r.%(debut)s); $st := $s($r.%(statut)s); $etat := $s($r.crm_etat_visite);
  $fini := $st in ['Terminé', 'Visité', 'Annulé'] or $etat in ['Effectuée', 'Annulée'];
  {
    'id': $n($r.id), 'titre': $s($r.libelle) != '' ? $s($r.libelle) : ($s($r.%(nature)s) != '' ? $s($r.%(nature)s) : 'Rendez-vous'),
    'nature': $s($r.%(nature)s) = '' ? 'Visite' : $s($r.%(nature)s),
    'debut': $loc($d, '[Y0001]-[M01]-[D01]T[H01]:[m01]'), 'ts': $ms($d), 'jour': $jour($d), 'heure': $heure($d),
    'fin': $heure($r.crm_fin), 'jourLabel': $labelJour($d), 'quand': $labelDate($d),
    'statut': $etat = 'Annulée' or $st = 'Annulé' ? 'Annulé' : ($fini ? 'Effectué' : ($etat = 'Confirmée' ? 'Confirmé' : 'À confirmer')),
    'statutTone': $actTone($st, $etat), 'aVenir': $not($fini) and $ms($d) >= $nowms,
    'aFaireCR': $not($etat = 'Annulée' or $st = 'Annulé') and $ms($d) < $nowms and $s($r.crm_appreciation) = '',
    'broker': $s($r.crm_broker), 'clientId': $n($r.opportunit_s_clients_id), 'bienId': $n($r.biens_id),
    'lienClient': $s($r.opportunit_s_clients_id) != '' ? '/opportunite-client?id=' & $s($r.opportunit_s_clients_id) : '',
    'appreciation': $s($r.crm_appreciation), 'objections': $s($r.crm_objections), 'prochaineEtape': $s($r.crm_prochaine_etape),
    'test': $b($r.crm_est_test) or $recette($r.libelle)
  }
) };
""" % AC

BI_MAP = r"""
$photo := function($att){ ($a := $type($att) = 'string' ? ($contains($att, '[') ? $eval($att) : []) : $att; $u := [$a.(url ? url : (signedUrl ? signedUrl : path))][0]; $s($u) != '' and $contains($s($u), 'http') ? $s($u) : '' };
$dispoTone := function($d){ $d = 'Actif' ? 'success' : ($d = 'Inactif' ? 'neutral' : 'warning') };
$verif := function($etat){ $etat = 'Validé' ? 'Vérifié' : 'À confirmer' };
$bien := function($r){ (
  $d := $s($r.%(dispo)s); $p := $n($r.%(prix)s); $img := $photo($r.%(image)s);
  $conf := $s($r.date_confirmation_dispo);
  {
    'id': $n($r.id), 'lien': '/bien?id=' & $s($r.id),
    'nom': $s($r.%(nom)s) != '' ? $s($r.%(nom)s) : ($s($r.libelle) != '' ? $s($r.libelle) : 'Bien #' & $s($r.id)),
    'type': $s($r.%(type)s), 'transaction': $s($r.%(tx)s), 'prix': $p, 'prixLabel': $dh($p),
    'surface': $n($r.%(surface)s), 'surfaceLabel': $n($r.%(surface)s) ? $string($n($r.%(surface)s)) & ' m²' : '—',
    'chambres': $n($r.%(ch)s), 'quartier': $s($r.%(quartier)s), 'ville': $s($r.%(ville)s),
    'localisation': $join([$s($r.%(quartier)s), $s($r.%(ville)s)][$ != ''], ', '),
    'dispo': $d = '' ? 'À confirmer' : ($d in ['Actif', 'Inactif'] ? $d : 'À confirmer'), 'dispoTone': $dispoTone($d),
    'responsable': $s($r.%(resp)s), 'mien': $s($r.%(resp)s) = $moi.broker,
    'photo': $img, 'aPhoto': $img != '', 'etatPhotos': $s($r.%(etatimg)s),
    'gestionnaire': $s($r.%(gest)s), 'gestionnaireTel': $s($r.%(gesttel)s),
    'gestionnaireTelUrl': $intl($r.%(gesttel)s) != '' ? 'tel:+' & $intl($r.%(gesttel)s) : '',
    'gestionnaireStatut': $verif($s($r.tat_de_migration_gestionnaire)),
    'gestionnaireTone': $s($r.tat_de_migration_gestionnaire) = 'Validé' ? 'success' : 'warning',
    'provenance': $s($r.%(typegest)s), 'statutBrief': $s($r.statut_brief),
    'dispoConfirmee': $conf = '' ? 'Jamais confirmée' : 'Confirmée le ' & $substring($conf, 0, 10),
    'aActualiser': $d = 'Actif' and ($conf = '' or $ms($conf) < $nowms - 30 * 86400000 or $contains($s($r.statut_brief), '🔴') or $contains($s($r.statut_brief), '🟠') or $contains($s($r.statut_brief), '🟡')),
    'prochaineAction': $s($r.crm_prochaine_action), 'echeanceLabel': $labelDate($r.crm_echeance),
    'resume': $s($r.%(resume)s), 'initiales': $uppercase($substring($s($r.%(type)s), 0, 2))
  }
) };
""" % BI

OB_MAP = r"""
$ob := function($r){ (
  $p := $n($r.%(prix)s); $img := $photo($r.%(image)s); $ech := $s($r.crm_echeance); $resp := $s($r.%(resp)s);
  {
    'id': $n($r.id), 'lien': '/opportunite-bien?id=' & $s($r.id),
    'nom': $s($r.%(nom)s) != '' ? $s($r.%(nom)s) : ($s($r.libelle) != '' ? $s($r.libelle) : 'Opportunité #' & $s($r.id)),
    'statut': $s($r.%(statut)s), 'resultat': $s($r.resultat_commercial) = '' ? 'À qualifier' : $s($r.resultat_commercial),
    'resultatTone': $contains($s($r.resultat_commercial), 'Gagnée') ? 'success' : ($s($r.resultat_commercial) = 'Perdue' ? 'danger' : 'info'),
    'type': $s($r.%(type)s), 'transaction': $s($r.%(tx)s), 'prix': $p, 'prixLabel': $dh($p),
    'surface': $n($r.%(surface)s), 'quartier': $s($r.%(quartier)s), 'ville': $s($r.%(ville)s),
    'localisation': $join([$s($r.%(quartier)s), $s($r.%(ville)s)][$ != ''], ', '),
    'responsable': $resp = '' ? 'Sans responsable' : $resp, 'sansResponsable': $resp = '', 'mien': $resp = $moi.broker,
    'modifiable': $moi.admin or $resp = $moi.broker,
    'gestionnaire': $s($r.%(gest)s), 'gestionnaireTel': $s($r.%(gesttel)s),
    'gestionnaireTelUrl': $intl($r.%(gesttel)s) != '' ? 'tel:+' & $intl($r.%(gesttel)s) : '',
    'gestionnaireStatut': $s($r.tat_de_migration_gestionnaire) = 'Validé' ? 'Vérifié' : 'À confirmer',
    'gestionnaireTone': $s($r.tat_de_migration_gestionnaire) = 'Validé' ? 'success' : 'warning',
    'photo': $img, 'aPhoto': $img != '',
    'prochaineAction': $s($r.crm_prochaine_action), 'echeance': $loc($ech, '[Y0001]-[M01]-[D01]T[H01]:[m01]'),
    'echeanceLabel': $ech = '' ? 'Pas d’échéance' : $labelDate($ech), 'enRetard': $ech != '' and $jour($ech) < $today,
    'aSuivre': $resp = '' or ($ech != '' and $jour($ech) <= $tomorrow),
    'priorite': $s($r.crm_priorite), 'notes': $s($r.crm_notes_suivi), 'resume': $s($r.%(resume)s),
    'bienId': $n($r.pmv6m9j8dh2qj_biens_id), 'lienBien': $s($r.pmv6m9j8dh2qj_biens_id) != '' ? '/bien?id=' & $s($r.pmv6m9j8dh2qj_biens_id) : '',
    'activable': $s($r.pmv6m9j8dh2qj_biens_id) != '' and $contains($s($r.resultat_commercial), 'Gagnée'),
    'test': $recette($r.libelle) or $recette($r.%(nom)s)
  }
) };
""" % OB


def endpoint(name, method, path, steps, query=None, body=None, description=""):
    return {"name": name, "description": description, "definition": {
        "method": method, "path": path, "auth": {"type": "jwt"},
        "input": {"params": [], "query": query or [], "headers": [], "body": body or []},
        "steps": steps, "docs": {"description": description}}}


def q(name, desc=""):
    return {"name": name, "type": "string", "required": False, "description": desc}


def b(name, typ="string", req=False, desc=""):
    return {"name": name, "type": typ, "required": req, "description": desc}


def lr(key, table, cols, filters=None, limit=500, sort=None, name=None, run_if=None):
    p = {"table": table, "columns": cols, "limit": limit}
    if filters:
        p["filters"] = filters
    if sort:
        p["sort"] = sort
    return ds(key, "listRecords", p, name, run_if)


EP = []

# 1. Session
EP.append(endpoint("CRM21 — Session et droits", "GET", "/crm21/session", IDENT + [
    tr("out", "($i := steps.ident; $p := $split($i.nom & ' ', ' ')[0]; {'items':[{'email':$i.email,'nom':$i.nom,"
              "'prenom':$p,'role':$i.role,'admin':$i.admin,'broker':$i.broker,'initiales':$uppercase($substring($i.nom,0,1)),"
              "'salutation':'Bonjour ' & $p}]})")],
    description="Identité V2.1 : email de session → CRM21 Membres. Ne lit jamais auth.claims.roles."))

# 2. Opportunités clients (liste)
OC_LIST_OUT = H + OC_MAP + r"""
$vue := $s($$.input.query.vue); $qq := $lowercase($s($$.input.query.q));
$all := [$$.steps.rows.rows[$voirRecette or $not($recette(libelle))].$oc($)];
$f := $all[
  ($vue = 'actions' ? (actif and echeanceJour != '' and echeanceJour <= $today) :
  ($vue = 'retard' ? enRetard :
  ($vue = 'avancees' ? (avancee) :
  ($vue = 'a-completer' ? (actif and nbACompleter > 0) :
  ($vue = 'chauds' ? (actif and (avancee or priorite in ['Urgente', 'Haute'])) :
  ($vue = 'toutes' or $s($$.input.query.etape) != '' ? true : actif))))))
  and ($qq = '' or $contains($lowercase(nom & ' ' & quartier & ' ' & telephone & ' ' & typeBien), $qq))
];
$tri := $sort($f, function($a, $b){ ($a.echeance = '' ? '9999' : $a.echeance) > ($b.echeance = '' ? '9999' : $b.echeance) });
$lim := $n($$.input.query.limite);
{'items': $lim ? [$tri[[0..$lim - 1]]] : [$tri], 'total': $count($f)}
"""
EP.append(endpoint("CRM21 — Opportunités clients", "GET", "/crm21/opportunites-clients", IDENT + [
    PER,
    lr("rows", T["oc"], OC_COLS, [flt(OC["broker"], "eq", MINE, True),
                                  flt(OC["etape"], "eq", "{{ input.query.etape }}", True)],
       sort=[{"column": "updated_at", "direction": "desc"}], name="Lecture du portefeuille"),
    tr("out", OC_LIST_OUT, "Mise en forme")],
    query=[q("etape"), q("vue", "actions | retard | avancees | a-completer | chauds | toutes"), q("q"), q("limite"),
           q("recette", "1 = inclure la recette")],
    description="Portefeuille : broker → ses dossiers ; admin → tous. Filtre serveur sur Agent Broker."))

# 3. Fiche opportunité client
OWN_OC = [
    respond("gid", 400, "{'error':'Identifiant de dossier invalide.'}",
            "$not($contains($string(input.query.id), /^[1-9][0-9]{0,9}$/))", "Id valide"),
    lr("rows", T["oc"], OC_COLS, [flt("id", "eq", "{{ input.query.id }}"), flt(OC["broker"], "eq", MINE, True)],
       limit=1, name="Dossier autorisé"),
    respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.rows.rows) = 0",
            "Propriétaire"),
]
EP.append(endpoint("CRM21 — Fiche opportunité client", "GET", "/crm21/opportunite-client", IDENT + [PER] + OWN_OC + [
    lr("contact", T["contacts"], ["id", "libelle", "src_chepoppm9ctk3tm", "src_c2j3fuou3o8taqa"],
       [flt("id", "eq", "{{ $string(steps.rows.rows[0]." + OC["contact"] + ") }}")], limit=1, name="Contact principal",
       run_if="$type(steps.rows.rows[0]." + OC["contact"] + ") in ['number', 'string'] and $string(steps.rows.rows[0]." + OC["contact"] + ") != ''"),
    tr("out", H + OC_MAP + r"""
$r := $$.steps.rows.rows[0]; $c := $$.steps.contact.rows[0]; $x := $oc($r);
{'items': [$merge([$x, {
  'contact': $exists($c) ? ($s($c.libelle) != '' ? $s($c.libelle) : $s($c.src_chepoppm9ctk3tm)) : $x.nom,
  'contactTel': $exists($c) and $s($c.src_c2j3fuou3o8taqa) != '' ? $s($c.src_c2j3fuou3o8taqa) : $x.telephone,
  'contactStatut': $exists($c) ? 'Contact lié' : 'Contact à confirmer',
  'surfaceLabel': ($a := $n($r.""" + OC["smin"] + r"""); $z := $n($r.""" + OC["smax"] + r""");
      $a and $z ? $string($a) & '–' & $string($z) & ' m²' : ($a ? 'dès ' & $string($a) & ' m²' : ($z ? 'jusqu’à ' & $string($z) & ' m²' : '—'))),
  'chambres': $n($r.""" + OC["ch"] + r"""), 'meuble': $s($r.""" + OC["meuble"] + r"""),
  'canal': $s($r.""" + OC["canal"] + r"""), 'criteres': $s($r.""" + OC["criteres"] + r"""),
  'remarques': $s($r.""" + OC["remarques"] + r"""),
  'criteresLabel': $join([$x.transaction, $x.typeBien, $x.quartier, $x.budgetLabel != '—' ? 'budget ' & $x.budgetLabel : null][$ != null and $ != ''], ' · '),
  'modifiable': $moi.admin or $x.broker = $moi.broker
}])]}
""", "Mise en forme")],
    query=[q("id")], description="Fiche : 404 si le dossier n'appartient pas au broker."))

# 4. Propositions d'un dossier
EP.append(endpoint("CRM21 — Biens proposés", "GET", "/crm21/propositions", IDENT + [PER] + [
    respond("gid", 400, "{'error':'Identifiant de dossier invalide.'}",
            "$not($contains($string(input.query.clientId), /^[1-9][0-9]{0,9}$/))", "Id valide"),
    lr("rows", T["oc"], ["id", OC["broker"]], [flt("id", "eq", "{{ input.query.clientId }}"),
                                               flt(OC["broker"], "eq", MINE, True)], limit=1, name="Dossier autorisé"),
    respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.rows.rows) = 0"),
    lr("props", T["props"], ["id", "libelle", "cle_proposition", "statut", "retour_client", "provenance", "broker",
                              "date_proposition", "test_crm1", "pmv6m9j8dh2qj_biens_id"],
       [flt("opportunit_s_clients_id", "eq", "{{ input.query.clientId }}")],
       sort=[{"column": "id", "direction": "asc"}], name="Propositions"),
    lr("biens", T["biens"], BI_COLS, [flt("id", "in", "{{ $join(steps.props.rows.$string(pmv6m9j8dh2qj_biens_id), ',') }}")],
       name="Biens proposés", run_if="$count(steps.props.rows) > 0"),
    tr("out", H + BI_MAP + r"""
$bs := $$.steps.biens.rows;
$ps := $$.steps.props.rows[$voirRecette or $not(test_crm1 = true or $recette(libelle))];
$grp := $ps{ ($s(cle_proposition) != '' ? $s(cle_proposition) : 'id' & $s(id)) : $ };
$uniq := [$each($grp, function($v){ $type($v) = 'array' ? $v[0] : $v })];
$stTone := function($st){ $st in ['Intéressé', 'Visite demandée'] ? 'success' : ($st = 'Refusé' ? 'danger' : 'info') };
{'items': [$uniq.(
  $pr := $; $bid := $n(pmv6m9j8dh2qj_biens_id); $bi := $bs[$n(id) = $bid][0];
  $x := $exists($bi) ? $bien($bi) : {'nom': 'Bien #' & $string($bid), 'prixLabel': '—', 'localisation': '', 'photo': '', 'aPhoto': false};
  {'id': $n($pr.id), 'bienId': $bid, 'lienBien': '/bien?id=' & $string($bid), 'nom': $x.nom, 'prixLabel': $x.prixLabel,
   'localisation': $x.localisation, 'photo': $x.photo, 'aPhoto': $x.aPhoto,
   'statut': $s($pr.statut) = '' ? 'Proposé' : $s($pr.statut), 'statutTone': $stTone($s($pr.statut)),
   'retour': $s($pr.retour_client), 'date': $substring($s($pr.date_proposition), 0, 10),
   'provenance': $s($pr.provenance)}
)]}
""", "Mise en forme")],
    query=[q("clientId"), q("recette")], description="Biens proposés au dossier et retours du client."))

# 5. Agenda
EP.append(endpoint("CRM21 — Agenda", "GET", "/crm21/activites", IDENT + [
    PER,
    lr("mesoc", T["oc"], ["id"], [flt(OC["broker"], "eq", "{{ steps.ident.broker }}")], limit=1000,
       name="Mes dossiers", run_if="$not(steps.ident.admin)"),
    lr("rows", T["act"], AC_COLS, [flt("opportunit_s_clients_id", "eq", "{{ input.query.clientId }}", True),
                                  flt(AC["debut"], "gte", "{{ input.query.du }}", True),
                                  flt(AC["debut"], "lte", "{{ input.query.au }}", True)],
       sort=[{"column": AC["debut"], "direction": "asc"}], limit=1000, name="Activités"),
    tr("out", H + ACT_MAP + r"""
$mine := $$.steps.mesoc.rows.$n(id);
$vue := $s($$.input.query.vue);
$all := [$$.steps.rows.rows[$moi.admin or $s(crm_broker) = $moi.broker or $n(opportunit_s_clients_id) in $mine].$act($)][$voirRecette or $not(test)];
$f := $all[$vue = 'a-venir' ? aVenir : ($vue = 'jour' ? jour = ($s($$.input.query.jour) != '' ? $s($$.input.query.jour) : $today) : ($vue = 'cr' ? aFaireCR : ($vue = 'semaine' ? (jour >= $today and jour <= $in7) : true)))];
$lim := $n($$.input.query.limite);
{'items': $lim ? [$f[[0..$lim - 1]]] : [$f], 'total': $count($f)}
""", "Mise en forme")],
    query=[q("clientId"), q("du", "ISO"), q("au", "ISO"), q("vue", "a-venir | jour | semaine | cr"), q("jour", "YYYY-MM-DD"),
           q("limite"), q("recette")],
    description="Agenda : RDV du broker (Broker visite = lui, ou dossier à lui) ; admin : tous. Heures Africa/Casablanca."))

# 6. Historique
EP.append(endpoint("CRM21 — Historique du dossier", "GET", "/crm21/historique", IDENT + [PER] + [
    respond("gid", 400, "{'error':'Identifiant de dossier invalide.'}",
            "$not($contains($string(input.query.clientId), /^[1-9][0-9]{0,9}$/))"),
    lr("rows", T["oc"], ["id"], [flt("id", "eq", "{{ input.query.clientId }}"), flt(OC["broker"], "eq", MINE, True)],
       limit=1, name="Dossier autorisé"),
    respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.rows.rows) = 0"),
    lr("events", T["journal"], ["id", "date_evenement", "type_evenement", "resume", "resultat", "broker", "test_crm1",
                                "type_dossier", "libelle"],
       [flt("dossier_id", "eq", "{{ input.query.clientId }}"), flt("type_dossier", "in", "client,opportunite-client")],
       sort=[{"column": "id", "direction": "desc"}], limit=100),
    lr("acts", T["act"], AC_COLS, [flt("opportunit_s_clients_id", "eq", "{{ input.query.clientId }}")], limit=200),
    tr("out", H + ACT_MAP + r"""
$ev := [$$.steps.events.rows[($voirRecette or $not(test_crm1 = true)) and $not(type_evenement in ['Refus hors responsable']) and resultat != 'À reprendre'].{
  'id': 'e' & $s(id), 'ts': $ms(date_evenement), 'quand': $labelDate(date_evenement), 'titre': $s(type_evenement),
  'texte': $s(resume), 'auteur': $s(broker), 'icone': type_evenement = 'Note' ? 'sticky-note' : 'history'}];
$ac := [$$.steps.acts.rows.$act($)[$voirRecette or $not(test)].{
  'id': 'a' & $string(id), 'ts': ts, 'quand': quand,
  'titre': nature & ' — ' & statut, 'texte': appreciation, 'auteur': broker, 'icone': 'calendar'}];
{'items': [$sort($append($ev, $ac), function($a, $b){ $a.ts < $b.ts })]}
""", "Mise en forme")],
    query=[q("clientId"), q("recette")], description="Historique : journal (hors refus) + activités, du plus récent au plus ancien."))

# 7. Catalogue des biens
EP.append(endpoint("CRM21 — Catalogue des biens", "GET", "/crm21/biens", IDENT + [
    PER,
    lr("rows", T["biens"], BI_COLS, [flt(BI["tx"], "eq", "{{ input.query.transaction }}", True),
                                     flt(BI["type"], "eq", "{{ input.query.type }}", True),
                                     flt(BI["resp"], "eq", "{{ input.query.mes = '1' ? steps.ident.broker : '' }}", True)],
       sort=[{"column": "updated_at", "direction": "desc"}], name="Biens"),
    tr("out", H + BI_MAP + r"""
$qq := $lowercase($s($$.input.query.q)); $dispo := $s($$.input.query.dispo); $vue := $s($$.input.query.vue);
$pmax := $n($$.input.query.prixMax);
$all := [$$.steps.rows.rows[$voirRecette or $not($recette(libelle) or $recette(src_c30sp73xdb9jdsx))].$bien($)];
$f := $all[($dispo = '' or dispo = $dispo) and ($vue != 'a-actualiser' or aActualiser) and ($pmax = null or (prix != null and prix <= $pmax))
  and ($qq = '' or $contains($lowercase(nom & ' ' & quartier & ' ' & ville & ' ' & type), $qq))];
$lim := $n($$.input.query.limite);
{'items': $lim ? [$f[[0..$lim - 1]]] : [$f], 'total': $count($f)}
""", "Mise en forme")],
    query=[q("q"), q("type"), q("transaction"), q("dispo"), q("mes", "1 = mes biens"), q("vue", "a-actualiser"),
           q("prixMax"), q("limite"), q("recette")],
    description="Catalogue partagé ; « Mes biens » = Broker Principal = moi."))

# 8. Fiche bien
EP.append(endpoint("CRM21 — Fiche bien", "GET", "/crm21/bien", IDENT + [PER] + [
    respond("gid", 400, "{'error':'Identifiant de bien invalide.'}", "$not($contains($string(input.query.id), /^[1-9][0-9]{0,9}$/))"),
    lr("rows", T["biens"], BI_COLS, [flt("id", "eq", "{{ input.query.id }}")], limit=1),
    respond("g404", 404, "{'error':'Bien introuvable.'}", "$count(steps.rows.rows) = 0"),
    lr("props", T["props"], ["id", "statut", "opportunit_s_clients_id", "test_crm1", "libelle"],
       [flt("pmv6m9j8dh2qj_biens_id", "eq", "{{ input.query.id }}")], limit=200, name="Clients intéressés"),
    tr("out", H + BI_MAP + r"""
$x := $bien($$.steps.rows.rows[0]);
$ps := $$.steps.props.rows[$not(test_crm1 = true or $recette(libelle))];
{'items': [$merge([$x, {'nbPropositions': $count($ps), 'nbInteresses': $count($ps[statut in ['Intéressé', 'Visite demandée']]),
  'interessesLabel': $count($ps) = 0 ? 'Pas encore proposé' : $string($count($ps)) & ' proposition(s), ' & $string($count($ps[statut in ['Intéressé', 'Visite demandée']])) & ' intéressé(s)'}])]}
""", "Mise en forme")],
    query=[q("id")], description="Fiche bien partagée ; nombre de clients intéressés sans leurs coordonnées."))

# 9. Rapprochements pour un dossier
EP.append(endpoint("CRM21 — Biens correspondants", "GET", "/crm21/rapprochements", IDENT + [PER] + [
    respond("gid", 400, "{'error':'Identifiant de dossier invalide.'}",
            "$not($contains($string(input.query.clientId), /^[1-9][0-9]{0,9}$/))"),
    lr("rows", T["oc"], OC_COLS, [flt("id", "eq", "{{ input.query.clientId }}"), flt(OC["broker"], "eq", MINE, True)],
       limit=1, name="Dossier autorisé"),
    respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.rows.rows) = 0"),
    lr("biens", T["biens"], BI_COLS, [flt(BI["dispo"], "eq", "Actif")], limit=1000, name="Biens actifs"),
    lr("props", T["props"], ["pmv6m9j8dh2qj_biens_id"], [flt("opportunit_s_clients_id", "eq", "{{ input.query.clientId }}")],
       limit=500, name="Déjà proposés"),
    tr("out", H + OC_MAP + BI_MAP + r"""
$c := $oc($$.steps.rows.rows[0]); $r := $$.steps.rows.rows[0];
$deja := $$.steps.props.rows.$n(pmv6m9j8dh2qj_biens_id);
$TX := {'Achat': 'Vente', 'Location': 'Location'};
$TYPES := {'Appartement': ['appartement', 'studio'], 'Studio': ['studio', 'appartement'], 'Villa': ['villa'], 'Bureau': ['bureau'],
  'Local commercial': ['local commerciale', 'magasin', 'local'], 'Terrain': ['terrain'], 'Industriel': ['local'], 'Autre': []};
$txb := $lookup($TX, $c.transaction); $types := $lookup($TYPES, $c.typeBien);
$quartiers := [$split($lowercase($c.quartier), /[,;\/]| et /).$trim($)][$ != ''];
$smin := $n($r.""" + OC["smin"] + r"""); $ch := $n($r.""" + OC["ch"] + r""");
$cands := [$$.steps.biens.rows[$not($recette(libelle)) and $not($n(id) in $deja)].$bien($)];
$scored := [$cands[($not($exists($txb)) or transaction = $txb) and ($count($types) = 0 or type in $types)].(
  $bi := $;
  $okBudget := $c.budget = null or $bi.prix = null ? null : $bi.prix <= $c.budget * 1.15;
  $okQuartier := $count($quartiers) = 0 ? null : $count($quartiers[$contains($lowercase($bi.quartier), $)]) > 0;
  $okSurface := $smin = null or $bi.surface = null ? null : $bi.surface >= $smin * 0.9;
  $okCh := $ch = null or $bi.chambres = null ? null : $bi.chambres >= $ch;
  $crit := [($exists($txb) ? 'Transaction' : null), ($count($types) > 0 ? 'Type' : null), ($okBudget = true ? 'Budget ≤ +15 %' : null),
    ($okQuartier = true ? 'Quartier' : null), ($okSurface = true ? 'Surface' : null), ($okCh = true ? 'Chambres' : null)][$ != null];
  $manq := [($okBudget = null ? 'budget inconnu' : null), ($okQuartier = null ? 'quartier non précisé' : null)][$ != null];
  $okBudget = false or $okQuartier = false ? null : $merge([$bi, {'score': $count($crit), 'criteres': 'Critères vérifiés : ' & $join($crit, ', '),
    'limites': $count($manq) > 0 ? 'Non vérifié : ' & $join($manq, ', ') : '', 'clientId': $c.id}])
)][$ != null];
$lim := $n($$.input.query.limite) ? $n($$.input.query.limite) : 10;
$tri := $sort($scored, function($a, $b){ $a.score < $b.score });
{'items': [$tri[[0..$lim - 1]]], 'methode': 'Biens actifs, transaction et type compatibles, prix ≤ budget + 15 %, quartier demandé ; triés par nombre de critères vérifiés.'}
""", "Rapprochement")],
    query=[q("clientId"), q("limite")],
    description="Suggestions transparentes : critères comparés renvoyés par bien. Rien n'est écrit."))

# 10. Référentiels
EP.append(endpoint("CRM21 — Référentiels", "GET", "/crm21/referentiels", IDENT + [
    lr("membres", T["membres"], ["nom", "broker", "role", "actif"], [flt("actif", "eq", "true")], limit=50,
       run_if="steps.ident.admin"),
    tr("out", r"""
$opt := function($a){ [$a.{'label': $, 'value': $}] };
{'items': [{
  'etapes': $opt(%s),
  'actions': $opt(['Appeler', 'Demander des informations', 'Rechercher des biens', 'Proposer des biens', 'Planifier une visite', 'Confirmer le RDV de Visite', 'Faire le suivi après visite', 'Proposer une Autre Visite', 'Proposer Offre Finacière']),
  'priorites': $opt(['Urgente', 'Haute', 'Normale']),
  'transactions': $opt(['Achat', 'Location']),
  'typesClient': $opt(['Appartement', 'Studio', 'Villa', 'Bureau', 'Local commercial', 'Terrain', 'Industriel', 'Autre']),
  'typesBien': $opt(['appartement', 'studio', 'villa', 'bureau', 'local commerciale', 'magasin', 'terrain', 'local']),
  'natures': $opt(['Visite', 'Appel', 'Rendez-vous agence', 'Signature']),
  'statutsProposition': $opt(['Proposé', 'Intéressé', 'Refusé', 'Visite demandée']),
  'brokers': steps.ident.admin ? [steps.membres.rows[role = 'Broker' or broker].{'label': nom, 'value': broker}] : [{'label': steps.ident.nom, 'value': steps.ident.broker}]
}]}
""" % json.dumps(FR_ETAPES, ensure_ascii=False))],
    description="Listes de choix pour les formulaires."))

# 11. Créneaux libres
EP.append(endpoint("CRM21 — Créneaux libres", "GET", "/crm21/creneaux", IDENT + [
    PER,
    respond("gjour", 400, "{'error':'Date invalide (AAAA-MM-JJ).'}",
            "$exists(input.query.jour) and input.query.jour != '' and $not($contains(input.query.jour, /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/))"),
    lr("rows", T["act"], ["id", AC["debut"], "crm_fin", "crm_broker", AC["statut"], "crm_etat_visite"],
       [flt("crm_broker", "eq", "{{ steps.ident.broker }}")], limit=1000, name="Mes RDV"),
    tr("out", H + r"""
$j := $s($$.input.query.jour) != '' ? $s($$.input.query.jour) : $today;
$tz := $tzp($toMillis($j & 'T12:00:00+01:00'));
$tzi := $substring($tz, 0, 3) & ':' & $substring($tz, 3);
$occ := $$.steps.rows.rows[$s(src_cwtdcarxql2laii) != 'Annulé' and $s(crm_etat_visite) != 'Annulée' and $jour(src_cybzjmjoj4zlch0) = $j].{
  'a': $ms(src_cybzjmjoj4zlch0), 'b': $s(crm_fin) != '' ? $ms(crm_fin) : $ms(src_cybzjmjoj4zlch0) + 3600000};
$slots := [9..19].(
  $h := $; $hh := $h < 10 ? '0' & $string($h) : $string($h);
  [{'h': $hh & ':00'}, {'h': $hh & ':30'}]
);
$libres := $slots[(
  $t := $toMillis($j & 'T' & h & ':00' & $tzi);
  $t > $nowms and $count($occ[a < $t + 3600000 and b > $t]) = 0
)];
{'items': [$libres.{'label': h, 'value': $j & 'T' & h}], 'methode': 'Créneaux d’une heure entre 9 h et 20 h sans RDV existant du broker (hors annulés).'}
""", "Calcul")],
    query=[q("jour")], description="Créneaux libres calculés depuis les RDV réels du broker."))


# ---------------------------------------------------------------- lectures (suite)

# 12. Opportunités de biens (liste partagée)
EP.append(endpoint("CRM21 — Opportunités de biens", "GET", "/crm21/opportunites-biens", IDENT + [
    PER,
    lr("rows", T["ob"], OB_COLS, [flt(OB["tx"], "eq", "{{ input.query.transaction }}", True)],
       sort=[{"column": "updated_at", "direction": "desc"}], name="Opportunités de biens"),
    tr("out", H + BI_MAP + OB_MAP + r"""
$vue := $s($$.input.query.vue); $qq := $lowercase($s($$.input.query.q));
$all := [$$.steps.rows.rows.$ob($)][$voirRecette or $not(test)];
$f := $all[($vue = 'mes' ? mien : ($vue = 'sans-responsable' ? sansResponsable : ($vue = 'a-suivre' ? aSuivre : true)))
  and ($qq = '' or $contains($lowercase(nom & ' ' & quartier & ' ' & ville & ' ' & gestionnaire), $qq))];
$tri := $sort($f, function($a, $b){ ($a.echeance = '' ? '9999' : $a.echeance) > ($b.echeance = '' ? '9999' : $b.echeance) });
$lim := $n($$.input.query.limite);
{'items': $lim ? [$tri[[0..$lim - 1]]] : [$tri], 'total': $count($f)}
""", "Mise en forme")],
    query=[q("vue", "mes | sans-responsable | a-suivre"), q("q"), q("transaction"), q("limite"), q("recette")],
    description="Opportunités de biens partagées entre brokers ; « modifiable » indique si l'appelant est responsable."))

# 13. Fiche opportunité de bien
EP.append(endpoint("CRM21 — Fiche opportunité de bien", "GET", "/crm21/opportunite-bien", IDENT + [PER] + [
    respond("gid", 400, "{'error':'Identifiant invalide.'}", "$not($contains($string(input.query.id), /^[1-9][0-9]{0,9}$/))"),
    lr("rows", T["ob"], OB_COLS, [flt("id", "eq", "{{ input.query.id }}")], limit=1),
    respond("g404", 404, "{'error':'Opportunité de bien introuvable.'}", "$count(steps.rows.rows) = 0"),
    tr("out", H + BI_MAP + OB_MAP + r"""
$x := $ob($$.steps.rows.rows[0]);
{'items': [$merge([$x, {'responsableLabel': $x.sansResponsable ? 'Sans responsable — attribution par l’administrateur' : 'Suivi par ' & $x.responsable,
  'activationLabel': $x.activable ? 'Le bien lié peut être activé' : ($x.bienId = null ? 'Aucun bien lié : activation impossible' : 'Activation possible quand le résultat est « Gagnée »')}])]}
""", "Mise en forme")],
    query=[q("id")], description="Fiche partagée ; badge gestionnaire vérifié / à confirmer d'après l'état de migration."))

# 14. Accueil (un seul enregistrement d'indicateurs)
EP.append(endpoint("CRM21 — Accueil", "GET", "/crm21/accueil", IDENT + [
    PER,
    lr("oc", T["oc"], OC_COLS, [flt(OC["broker"], "eq", MINE, True)], limit=1000, name="Portefeuille"),
    lr("acts", T["act"], AC_COLS, [flt(AC["debut"], "gte", "{{ $fromMillis($millis() - 7 * 86400000) }}")],
       sort=[{"column": AC["debut"], "direction": "asc"}], limit=1000, name="Activités récentes et à venir"),
    lr("ob", T["ob"], OB_COLS, limit=1000, name="Opportunités de biens"),
    lr("biens", T["biens"], BI_COLS, [flt(BI["dispo"], "eq", "Actif")], limit=1000, name="Biens actifs"),
    tr("out", H + OC_MAP + ACT_MAP + BI_MAP + OB_MAP + r"""
$ocs := [$$.steps.oc.rows[$not($recette(libelle))].$oc($)];
$mineIds := $ocs.id;
$acts := [$$.steps.acts.rows.$act($)][$not(test) and ($moi.admin or broker = $moi.broker or clientId in $mineIds)];
$prochains := [$acts[aVenir]];
$p := $prochains[0];
$obs := [$$.steps.ob.rows.$ob($)][$not(test)];
$bs := [$$.steps.biens.rows[$not($recette(libelle))].$bien($)];
{'items': [{
  'salutation': 'Bonjour ' & $split($moi.nom & ' ', ' ')[0],
  'dateLabel': $labelJour($fromMillis($nowms)),
  'role': $moi.role,
  'prochainRdv': $exists($p) ? $p.titre : 'Aucun rendez-vous à venir',
  'prochainRdvQuand': $exists($p) ? $p.quand : 'Planifiez une visite depuis une opportunité client',
  'prochainRdvLien': $exists($p) and $p.lienClient != '' ? $p.lienClient : '/agenda',
  'aUnRdv': $exists($p),
  'rdvSemaine': $count($prochains[jour <= $in7]),
  'rdvAujourdhui': $count($prochains[jour = $today]),
  'crAFaire': $count($acts[aFaireCR]),
  'actionsJour': $count($ocs[actif and echeanceJour != '' and echeanceJour <= $today]),
  'retards': $count($ocs[enRetard]),
  'aCompleter': $count($ocs[actif and nbACompleter > 0]),
  'avancees': $count($ocs[avancee]),
  'dossiersActifs': $count($ocs[actif]),
  'obASuivre': $count($obs[aSuivre]),
  'obSansResponsable': $count($obs[sansResponsable]),
  'biensAActualiser': $count($bs[aActualiser and ($moi.admin or responsable = $moi.broker)]),
  'regles': 'Actions : échéance aujourd’hui ou passée. Retards : échéance avant aujourd’hui. Avancées : Visite effectuée, Négociation, Finalisation. Biens à actualiser : disponibilité non confirmée depuis 30 jours ou brief à reprendre.'
}]}
""", "Indicateurs")],
    description="Indicateurs d'accueil calculés sur données réelles ; règles renvoyées dans 'regles'."))

# 15. Vue Équipe (admin)
EP.append(endpoint("CRM21 — Équipe (admin)", "GET", "/crm21/equipe", IDENT + [
    ADMIN_ONLY, PER,
    lr("membres", T["membres"], ["nom", "broker", "role", "actif"], [flt("actif", "eq", "true")], limit=50),
    lr("oc", T["oc"], OC_COLS, limit=1000),
    lr("ob", T["ob"], OB_COLS, limit=1000),
    lr("biens", T["biens"], ["id", "libelle", BI["dispo"], BI["resp"]], [flt(BI["dispo"], "eq", "Actif")], limit=1000),
    lr("acts", T["act"], ["id", "crm_broker", AC["debut"], AC["statut"], "crm_etat_visite", "crm_est_test", "libelle"],
       [flt(AC["debut"], "gte", "{{ $now() }}")], limit=1000),
    tr("out", H + OC_MAP + r"""
$ocs := [$$.steps.oc.rows[$not($recette(libelle))].$oc($)];
$brokers := $$.steps.membres.rows[$s(broker) != ''];
$vue := $s($$.input.query.vue);
$vue = 'leads' ? {'items': [$ocs[actif and ($not(broker in $brokers.broker))]]} :
{'items': [$brokers.(
  $bk := $s(broker);
  {'broker': $bk, 'nom': $s(nom), 'role': $s(role),
   'clientsActifs': $count($ocs[broker = $bk and actif]),
   'retards': $count($ocs[broker = $bk and enRetard]),
   'mandatsEnCours': $count($$.steps.ob.rows[$s(src_cazse08x5syk1gn) = $bk and $s(resultat_commercial) in ['', 'À qualifier', 'En cours', 'Disponible pour affectation']]),
   'biensEnStock': $count($$.steps.biens.rows[$s(src_c9w1scpswzkjl7g) = $bk]),
   'rdvSemaine': $count($$.steps.acts.rows[$s(crm_broker) = $bk and $s(src_cwtdcarxql2laii) != 'Annulé' and $s(crm_etat_visite) != 'Annulée' and $jour(src_cybzjmjoj4zlch0) <= $in7 and $not(crm_est_test = true)])}
)]}
""", "Charge")],
    query=[q("vue", "leads = leads à attribuer")], description="Réservé admin (CRM21 Membres). Charge par broker ou leads à attribuer."))

# ---------------------------------------------------------------- écritures

OP = tr("op", "{'id': $exists(input.body.cle) and $string(input.body.cle) != '' ? 'v21-' & $string(input.body.cle) : 'v21-' & $string($millis()) & '-' & $substring($string(auth.claims.sub), 0, 8), 'date': $now()}", "Identifiant d'opération")


def journal(key, type_dossier, dossier_expr, type_ev, resume_expr, apres_expr="''", test_expr="false", run_if=None):
    vals = ("{'libelle': %s, 'operation_id': steps.op.id, 'date_evenement': $now(), 'user_id': $string(auth.claims.sub), "
            "'email_auteur': steps.ident.email, 'broker': steps.ident.broker, 'type_dossier': '%s', 'dossier_id': $string(%s), "
            "'type_evenement': '%s', 'resume': $substring($string(%s), 0, 2000), 'apres': $substring($string(%s), 0, 2000), "
            "'resultat': 'Réussi', 'source': 'SuperAPP_CRM_V21', 'test_crm1': %s}") % (
        "'%s'" % type_ev, type_dossier, dossier_expr, type_ev, resume_expr, apres_expr, test_expr)
    return ds(key, "createRecord", {"table": T["journal"], "values": vals}, "Journal", run_if)


def own_oc_body(field="clientId"):
    return [
        respond("gid", 400, "{'error':'Dossier manquant ou invalide.'}",
                "$not($contains($string(input.body.%s), /^[1-9][0-9]{0,9}$/))" % field, "Id valide"),
        lr("oc", T["oc"], OC_COLS, [flt("id", "eq", "{{ $string(input.body.%s) }}" % field), flt(OC["broker"], "eq", MINE, True)],
           limit=1, name="Dossier autorisé"),
        respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.oc.rows) = 0", "Propriétaire"),
    ]


OCNAME = "($r := steps.oc.rows[0]; $l := $string($r.libelle); $l != '' and $l != 'null' ? $l : 'Dossier #' & $string($r.id))"
RECETTE_OC = "$contains(" + OCNAME + ", '[RECETTE V21]')"

# local 'YYYY-MM-DDTHH:mm' → ISO avec décalage Casablanca
TOISO = r"""
$s := function($v){ ($exists($v) and $type($v) != 'null') ? $string($v) : '' };
$ms := function($iso){ ($x := $replace($s($iso), /\.[0-9]+/, ''); $x != '' ? $toMillis($x) : null) };
$per := $$.steps.per.rows;
$off := function($t){ ($p := $per[$ms(debut_utc) <= $t and $t < $ms(fin_utc)][0]; $exists($p) ? $number($string($p.decalage_min)) : 60) };
$iso := function($local){ $s($local) = '' ? null : ($g := $toMillis($local & ':00+01:00'); $off($g) = 0 ? $local & ':00+00:00' : $local & ':00+01:00') };
"""

NATURES = "['Visite', 'Appel', 'Rendez-vous agence', 'Signature']"

# W1. Créer un RDV
EP.append(endpoint("CRM21 — Créer un rendez-vous", "POST", "/crm21/rdv", IDENT + [PER, OP] + [
    respond("gdeb", 400, "{'error':'Date et heure obligatoires (AAAA-MM-JJTHH:MM).'}",
            "$not($contains($string(input.body.debut), /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$/))"),
    respond("gdur", 400, "{'error':'Durée entre 15 et 480 minutes.'}",
            "$exists(input.body.dureeMin) and $string(input.body.dureeMin) != '' and ($number($string(input.body.dureeMin)) < 15 or $number($string(input.body.dureeMin)) > 480)"),
    respond("gnat", 400, "{'error':'Type de rendez-vous inconnu.'}",
            "$exists(input.body.nature) and $string(input.body.nature) != '' and $not(input.body.nature in " + NATURES + ")"),
    respond("gnote", 400, "{'error':'Note trop longue (2000 caractères max).'}", "$length($string(input.body.note)) > 2000"),
] + own_oc_body() + [
    lr("bien", T["biens"], ["id", BI["nom"], "libelle"], [flt("id", "eq", "{{ $string(input.body.bienId) }}")], limit=1,
       run_if="$exists(input.body.bienId) and $string(input.body.bienId) != ''", name="Bien"),
    respond("gbien", 400, "{'error':'Bien introuvable.'}",
            "$exists(input.body.bienId) and $string(input.body.bienId) != '' and $count(steps.bien.rows) = 0"),
    lr("deja", T["act"], ["id", AC["debut"]], [flt("crm_cle_creation", "eq", "{{ steps.op.id }}")], limit=1, name="Reprise"),
    respond("dejafait", 200, "{'items':[{'id': steps.deja.rows[0].id, 'message':'Rendez-vous déjà enregistré.', 'reprise': true}]}",
            "$count(steps.deja.rows) > 0", "Idempotence"),
    tr("t", TOISO + r"""
$d := $iso($$.input.body.debut); $dur := $s($$.input.body.dureeMin) != '' ? $number($string($$.input.body.dureeMin)) : 60;
$finMs := $ms($d) + $dur * 60000; $fo := $off($finMs);
{'debut': $d, 'debutMs': $ms($d), 'finMs': $finMs, 'fin': $fromMillis($finMs, '[Y0001]-[M01]-[D01]T[H01]:[m01]:[s01]', $fo = 0 ? '+0000' : '+0100') & ($fo = 0 ? '+00:00' : '+01:00')}
""", "Fuseau Africa/Casablanca"),
    respond("gpasse", 400, "{'error':'Ce créneau est déjà passé.'}", "steps.t.debutMs < $millis() - 300000"),
    lr("agenda", T["act"], ["id", AC["debut"], "crm_fin", AC["statut"], "crm_etat_visite", "libelle"],
       [flt("crm_broker", "eq", "{{ $string(steps.oc.rows[0].%s) }}" % OC["broker"]),
        flt(AC["debut"], "gte", "{{ $fromMillis(steps.t.debutMs - 8 * 3600000) }}"),
        flt(AC["debut"], "lte", "{{ $fromMillis(steps.t.finMs) }}")], limit=50, name="Chevauchements"),
    tr("chev", r"""
$ms := function($iso){ ($x := $replace($string($iso), /\.[0-9]+/, ''); $x != '' and $x != 'null' ? $toMillis($x) : null) };
$c := $$.steps.agenda.rows[$string(src_cwtdcarxql2laii) != 'Annulé' and $string(crm_etat_visite) != 'Annulée' and
  $ms(src_cybzjmjoj4zlch0) < $$.steps.t.finMs and ($exists(crm_fin) and $string(crm_fin) != 'null' ? $ms(crm_fin) : $ms(src_cybzjmjoj4zlch0) + 3600000) > $$.steps.t.debutMs];
{'conflit': $count($c) > 0, 'avec': $string($c[0].libelle)}
""", "Contrôle"),
    respond("g409", 409, "{'error':'Créneau déjà occupé dans l’agenda (' & steps.chev.avec & '). Choisissez un autre horaire.'}",
            "steps.chev.conflit and $not(input.body.forcer = true or input.body.forcer = 'true')"),
    ds("write", "createRecord", {"table": T["act"], "values":
        "{'libelle': ($exists(input.body.nature) and input.body.nature != '' ? input.body.nature : 'Visite') & ' — ' & " + OCNAME + ", "
        "'" + AC["debut"] + "': steps.t.debut, 'crm_fin': steps.t.fin, "
        "'" + AC["nature"] + "': $exists(input.body.nature) and input.body.nature != '' ? input.body.nature : 'Visite', "
        "'" + AC["statut"] + "': 'Programme', 'crm_etat_visite': 'À confirmer', "
        "'crm_broker': $string(steps.oc.rows[0]." + OC["broker"] + "), 'opportunit_s_clients_id': $number($string(input.body.clientId)), "
        "'biens_id': $exists(input.body.bienId) and $string(input.body.bienId) != '' ? $number($string(input.body.bienId)) : null, "
        "'crm_historique_cr': $exists(input.body.note) and input.body.note != '' ? 'Note à la création : ' & input.body.note : null, "
        "'crm_cle_creation': steps.op.id, 'crm_est_test': " + RECETTE_OC + "}"}, "Création du RDV"),
    journal("j", "client", "input.body.clientId", "RDV planifié", "'RDV ' & steps.t.debut", "{'rdv': steps.write.id, 'debut': steps.t.debut, 'fin': steps.t.fin}", RECETTE_OC),
    respond("done", 201, "{'items':[{'id': steps.write.id, 'debut': steps.t.debut, 'fin': steps.t.fin, 'message':'Rendez-vous enregistré.'}]}"),
], body=[b("clientId", "any", True), b("debut", "string", True, "heure locale AAAA-MM-JJTHH:MM"), b("dureeMin", "any"),
         b("nature"), b("bienId", "any"), b("note"), b("cle", "string", False, "clé d'idempotence"), b("forcer", "any")],
    description="RDV rattaché au dossier et à son broker ; heure locale convertie côté serveur ; refus si chevauchement ; idempotent par clé."))

# W2. Modifier un RDV : compte rendu, confirmation, annulation, déplacement
EP.append(endpoint("CRM21 — Suivi d'un rendez-vous", "PATCH", "/crm21/rdv", IDENT + [PER, OP] + [
    respond("gid", 400, "{'error':'Rendez-vous manquant.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("gact", 400, "{'error':'Action inconnue.'}", "$not(input.body.action in ['compte-rendu', 'confirmer', 'annuler', 'deplacer'])"),
    respond("gcr", 400, "{'error':'Le compte rendu doit contenir l’appréciation du client.'}",
            "input.body.action = 'compte-rendu' and $length($trim($string(input.body.appreciation))) < 2"),
    respond("glen", 400, "{'error':'Texte trop long (4000 caractères max).'}",
            "$length($string(input.body.appreciation)) > 4000 or $length($string(input.body.objections)) > 4000 or $length($string(input.body.prochaineEtape)) > 4000"),
    respond("gdeb", 400, "{'error':'Nouvelle date obligatoire (AAAA-MM-JJTHH:MM).'}",
            "input.body.action = 'deplacer' and $not($contains($string(input.body.debut), /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$/))"),
    lr("rdv", T["act"], AC_COLS, [flt("id", "eq", "{{ $string(input.body.id) }}")], limit=1),
    respond("g404", 404, "{'error':'Rendez-vous introuvable.'}", "$count(steps.rdv.rows) = 0"),
    lr("oc", T["oc"], ["id", "libelle", OC["broker"]], [flt("id", "eq", "{{ $string(steps.rdv.rows[0].opportunit_s_clients_id) }}")],
       limit=1, run_if="$exists(steps.rdv.rows[0].opportunit_s_clients_id) and $string(steps.rdv.rows[0].opportunit_s_clients_id) != 'null'"),
    respond("gown", 403, "{'error':'Ce rendez-vous n’est pas dans votre agenda.'}",
            "$not(steps.ident.admin or $string(steps.rdv.rows[0].crm_broker) = steps.ident.broker or $string(steps.oc.rows[0]." + OC["broker"] + ") = steps.ident.broker)"),
    tr("t", TOISO + r"""
$a := $$.input.body.action; $r := $$.steps.rdv.rows[0];
$d := $a = 'deplacer' ? $iso($$.input.body.debut) : null;
$dur := ($ms($r.crm_fin) and $ms($r.src_cybzjmjoj4zlch0)) ? $ms($r.crm_fin) - $ms($r.src_cybzjmjoj4zlch0) : 3600000;
$finMs := $d ? $ms($d) + $dur : null;
$stamp := $fromMillis($millis(), '[D01]/[M01]/[Y0001] [H01]:[m01]', $off($millis()) = 0 ? '+0000' : '+0100');
$hist := $s($r.crm_historique_cr);
$a = 'compte-rendu' ? {'crm_appreciation': $$.input.body.appreciation, 'crm_objections': $$.input.body.objections, 'crm_prochaine_etape': $$.input.body.prochaineEtape,
   'crm_etat_visite': 'Effectuée', 'src_cwtdcarxql2laii': 'Terminé',
   'crm_historique_cr': $trim($hist & '\n[' & $stamp & ' — ' & $$.steps.ident.nom & '] ' & $$.input.body.appreciation)} :
($a = 'confirmer' ? {'crm_etat_visite': 'Confirmée', 'crm_confirmation_client': true} :
($a = 'annuler' ? {'crm_etat_visite': 'Annulée', 'src_cwtdcarxql2laii': 'Annulé',
   'crm_historique_cr': $trim($hist & '\n[' & $stamp & '] Annulé' & ($s($$.input.body.motif) != '' ? ' : ' & $$.input.body.motif : ''))} :
{'src_cybzjmjoj4zlch0': $d, 'crm_fin': $fromMillis($finMs, '[Y0001]-[M01]-[D01]T[H01]:[m01]:[s01]', $off($finMs) = 0 ? '+0000' : '+0100') & ($off($finMs) = 0 ? '+00:00' : '+01:00'),
   'crm_etat_visite': 'À confirmer', 'src_cwtdcarxql2laii': 'Programme'}))
""", "Valeurs"),
    respond("gpasse", 400, "{'error':'Impossible : ce rendez-vous est annulé.'}",
            "input.body.action in ['compte-rendu', 'confirmer', 'deplacer'] and $string(steps.rdv.rows[0].crm_etat_visite) = 'Annulée'"),
    ds("write", "updateRecord", {"table": T["act"], "recordId": "{{ $string(input.body.id) }}", "values": "steps.t", "failIfNotFound": True},
       "Mise à jour"),
    journal("j", "client", "steps.rdv.rows[0].opportunit_s_clients_id", "RDV — ' & input.body.action & '", "input.body.action",
            "$keys(steps.t)", "steps.rdv.rows[0].crm_est_test = true"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'action': input.body.action, 'message': input.body.action = 'compte-rendu' ? 'Compte rendu enregistré.' : (input.body.action = 'annuler' ? 'Rendez-vous annulé.' : (input.body.action = 'confirmer' ? 'Rendez-vous confirmé.' : 'Rendez-vous déplacé.'))}]}"),
], body=[b("id", "any", True), b("action", "string", True), b("appreciation"), b("objections"), b("prochaineEtape"),
         b("motif"), b("debut")],
    description="Compte rendu, confirmation, annulation ou déplacement ; propriétaire contrôlé ; historique horodaté."))

# W3. Proposer un bien
EP.append(endpoint("CRM21 — Proposer un bien", "POST", "/crm21/propositions", IDENT + [OP] + own_oc_body() + [
    respond("gbid", 400, "{'error':'Bien manquant.'}", "$not($contains($string(input.body.bienId), /^[1-9][0-9]{0,9}$/))"),
    lr("bien", T["biens"], ["id", "libelle", BI["nom"], BI["dispo"]], [flt("id", "eq", "{{ $string(input.body.bienId) }}")], limit=1),
    respond("gbien", 404, "{'error':'Bien introuvable.'}", "$count(steps.bien.rows) = 0"),
    tr("k", "{'cle': $string(input.body.clientId) & '-' & $string(input.body.bienId)}", "Clé"),
    lr("deja", T["props"], ["id"], [flt("cle_proposition", "eq", "{{ steps.k.cle }}")], limit=1, name="Déjà proposé ?"),
    respond("g409", 409, "{'error':'Ce bien est déjà proposé à ce client.'}", "$count(steps.deja.rows) > 0"),
    ds("write", "createRecord", {"table": T["props"], "values":
        "{'libelle': ($b := steps.bien.rows[0]; $n := $string($b." + BI["nom"] + "); ($n != '' and $n != 'null' ? $n : 'Bien #' & $string($b.id))) & ' → ' & " + OCNAME + ", "
        "'cle_proposition': steps.k.cle, 'statut': 'Proposé', 'provenance': input.body.provenance = 'Suggestion automatique' ? 'Suggestion automatique' : 'Broker', "
        "'broker': $string(steps.oc.rows[0]." + OC["broker"] + "), 'email_auteur': steps.ident.email, 'date_proposition': $now(), "
        "'operation_id': steps.op.id, 'test_crm1': " + RECETTE_OC + ", "
        "'opportunit_s_clients_id': $number($string(input.body.clientId)), 'pmv6m9j8dh2qj_biens_id': $number($string(input.body.bienId))}"},
       "Création"),
    lr("apres", T["props"], ["id"], [flt("cle_proposition", "eq", "{{ steps.k.cle }}")], limit=10,
       sort=[{"column": "id", "direction": "asc"}], name="Relecture anti-doublon"),
    ds("annule", "deleteRecord", {"table": T["props"], "recordId": "{{ $string(steps.write.id) }}", "failIfNotFound": False},
       "Compensation (doublon concurrent)", run_if="$number($string(steps.apres.rows[0].id)) != $number($string(steps.write.id))"),
    respond("g409b", 409, "{'error':'Ce bien vient d’être proposé à ce client par une autre session.'}",
            "$number($string(steps.apres.rows[0].id)) != $number($string(steps.write.id))"),
    journal("j", "client", "input.body.clientId", "Bien proposé", "steps.k.cle", "{'proposition': steps.write.id, 'bien': input.body.bienId}", RECETTE_OC),
    respond("done", 201, "{'items':[{'id': steps.write.id, 'message':'Bien proposé au client.'}]}"),
], body=[b("clientId", "any", True), b("bienId", "any", True), b("provenance"), b("cle")],
    description="Une proposition par (client, bien) : contrôle préalable + relecture après insertion, la ligne la plus récente se retire en cas de doublon concurrent."))

# W4. Retour client sur une proposition
EP.append(endpoint("CRM21 — Retour sur une proposition", "PATCH", "/crm21/propositions", IDENT + [OP] + [
    respond("gid", 400, "{'error':'Proposition manquante.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("gst", 400, "{'error':'Statut inconnu.'}", "$not(input.body.statut in ['Proposé', 'Intéressé', 'Refusé', 'Visite demandée'])"),
    respond("glen", 400, "{'error':'Retour trop long (2000 caractères max).'}", "$length($string(input.body.retour)) > 2000"),
    lr("prop", T["props"], ["id", "opportunit_s_clients_id", "test_crm1", "statut", "retour_client"], [flt("id", "eq", "{{ $string(input.body.id) }}")], limit=1),
    respond("g404", 404, "{'error':'Proposition introuvable.'}", "$count(steps.prop.rows) = 0"),
    lr("oc", T["oc"], ["id", OC["broker"]], [flt("id", "eq", "{{ $string(steps.prop.rows[0].opportunit_s_clients_id) }}"),
                                             flt(OC["broker"], "eq", MINE, True)], limit=1),
    respond("gown", 404, "{'error':'Proposition introuvable ou non autorisée.'}", "$count(steps.oc.rows) = 0"),
    ds("write", "updateRecord", {"table": T["props"], "recordId": "{{ $string(input.body.id) }}", "failIfNotFound": True,
                                 "values": "{'statut': input.body.statut, 'retour_client': $exists(input.body.retour) ? input.body.retour : steps.prop.rows[0].retour_client}"}),
    journal("j", "client", "steps.prop.rows[0].opportunit_s_clients_id", "Retour client", "input.body.statut & ($exists(input.body.retour) and input.body.retour != '' ? ' : ' & input.body.retour : '')",
            "{'statut': [steps.prop.rows[0].statut, input.body.statut]}", "steps.prop.rows[0].test_crm1 = true"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'statut': input.body.statut, 'message':'Retour enregistré.'}]}"),
], body=[b("id", "any", True), b("statut", "string", True), b("retour")], description="Statut et retour du client ; propriétaire du dossier contrôlé."))

# W5. Modifier une opportunité client
OC_EDIT = {"etape": OC["etape"], "prochaineAction": OC["action"], "detailAction": OC["detail"], "priorite": OC["prio"],
           "quartier": OC["quartier"], "typeBien": OC["type"], "transaction": OC["tx"]}
EP.append(endpoint("CRM21 — Modifier une opportunité client", "PATCH", "/crm21/opportunites-clients", IDENT + [PER, OP] + [
    respond("gid", 400, "{'error':'Dossier manquant.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("get", 400, "{'error':'Étape inconnue.'}", "$exists(input.body.etape) and $not(input.body.etape in " + json.dumps(FR_ETAPES, ensure_ascii=False) + ")"),
    respond("gpr", 400, "{'error':'Priorité inconnue.'}", "$exists(input.body.priorite) and $not(input.body.priorite in ['Urgente', 'Haute', 'Normale'])"),
    respond("gtx", 400, "{'error':'Transaction inconnue.'}", "$exists(input.body.transaction) and $not(input.body.transaction in ['Achat', 'Location'])"),
    respond("gech", 400, "{'error':'Échéance invalide (AAAA-MM-JJTHH:MM).'}",
            "$exists(input.body.echeance) and input.body.echeance != '' and $not($contains($string(input.body.echeance), /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$/))"),
    respond("gbud", 400, "{'error':'Budget invalide.'}", "$exists(input.body.budget) and input.body.budget != '' and ($type($number($string(input.body.budget))) != 'number' or $number($string(input.body.budget)) < 0 or $number($string(input.body.budget)) > 1000000000)"),
    respond("gbk", 403, "{'error':'Seul l’administrateur peut réattribuer un dossier.'}", "$exists(input.body.broker) and $not(steps.ident.admin)"),
    respond("gbk2", 400, "{'error':'Broker inconnu.'}", "$exists(input.body.broker) and $not(input.body.broker in ['Imane', 'Salma', 'Majid', 'Omar'])"),
    respond("glen", 400, "{'error':'Texte trop long.'}", "$length($string(input.body.detailAction)) > 4000 or $length($string(input.body.quartier)) > 200"),
] + [
    lr("oc", T["oc"], OC_COLS, [flt("id", "eq", "{{ $string(input.body.id) }}"), flt(OC["broker"], "eq", MINE, True)], limit=1),
    respond("g404", 404, "{'error':'Dossier introuvable ou non autorisé.'}", "$count(steps.oc.rows) = 0"),
    tr("v", TOISO + r"""
$B := $$.input.body; $r := $$.steps.oc.rows[0];
$MAP := """ + json.dumps(OC_EDIT, ensure_ascii=False) + r""";
$base := $merge([$keys($MAP)[$exists($lookup($B, $))].{$lookup($MAP, $): $lookup($B, $)}]);
$tx := $exists($B.transaction) ? $B.transaction : $string($r.""" + OC["tx"] + r""");
$bud := $exists($B.budget) ? ($B.budget = '' ? {} : ($tx = 'Location' ? {'""" + OC["bl"] + r"""': $number($string($B.budget))} : {'""" + OC["ba"] + r"""': $number($string($B.budget))})) : {};
$ech := $exists($B.echeance) ? {'""" + OC["echeance"] + r"""': $B.echeance = '' ? null : $iso($B.echeance)} : {};
$bk := $exists($B.broker) ? {'""" + OC["broker"] + r"""': $B.broker} : {};
$v := $merge([$base, $bud, $ech, $bk]);
{'values': $v, 'avant': $merge([$keys($v).{$: $lookup($r, $)}]), 'n': $count($keys($v))}
""", "Champs autorisés"),
    respond("gvide", 400, "{'error':'Aucune modification.'}", "steps.v.n = 0"),
    ds("write", "updateRecord", {"table": T["oc"], "recordId": "{{ $string(input.body.id) }}", "values": "steps.v.values", "failIfNotFound": True}),
    journal("j", "client", "input.body.id", "Modification du dossier", "$join($keys(steps.v.values), ', ')",
            "{'avant': steps.v.avant, 'apres': steps.v.values}", RECETTE_OC),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'message':'Dossier mis à jour.'}]}"),
], body=[b("id", "any", True), b("etape"), b("prochaineAction"), b("echeance"), b("detailAction"), b("priorite"), b("budget", "any"),
         b("quartier"), b("typeBien"), b("transaction"), b("broker")],
    description="Liste fermée de champs ; réattribution réservée à l'admin ; journal limité aux champs modifiés."))

# W6. Note
EP.append(endpoint("CRM21 — Ajouter une note", "POST", "/crm21/notes", IDENT + [OP] + own_oc_body() + [
    respond("gtx", 400, "{'error':'La note est vide ou trop longue (5000 caractères max).'}",
            "$length($trim($string(input.body.texte))) < 2 or $length($string(input.body.texte)) > 5000"),
    lr("deja", T["journal"], ["id"], [flt("operation_id", "eq", "{{ steps.op.id }}")], limit=1, name="Reprise"),
    respond("dejafait", 200, "{'items':[{'id': steps.deja.rows[0].id, 'message':'Note déjà enregistrée.', 'reprise': true}]}", "$count(steps.deja.rows) > 0"),
    journal("write", "client", "input.body.clientId", "Note", "input.body.texte", "''", RECETTE_OC),
    respond("done", 201, "{'items':[{'id': steps.write.id, 'message':'Note ajoutée.'}]}"),
], body=[b("clientId", "any", True), b("texte", "string", True), b("cle")], description="Note rattachée au dossier, visible dans l'historique."))

# W7. Nouveau lead (contact + opportunité), idempotent
EP.append(endpoint("CRM21 — Nouveau lead", "POST", "/crm21/leads", IDENT + [OP] + [
    respond("gnom", 400, "{'error':'Nom obligatoire (2 à 150 caractères).'}",
            "$length($trim($string(input.body.nom))) < 2 or $length($string(input.body.nom)) > 150"),
    respond("gtel", 400, "{'error':'Téléphone invalide.'}",
            "$exists(input.body.telephone) and input.body.telephone != '' and $length($replace($string(input.body.telephone), /[^0-9]/, '')) < 9"),
    respond("gtx", 400, "{'error':'Choisissez Achat ou Location.'}", "$not(input.body.transaction in ['Achat', 'Location'])"),
    respond("gbud", 400, "{'error':'Budget invalide.'}",
            "$exists(input.body.budget) and input.body.budget != '' and ($type($number($string(input.body.budget))) != 'number' or $number($string(input.body.budget)) < 0 or $number($string(input.body.budget)) > 1000000000)"),
    respond("gbk", 400, "{'error':'Broker inconnu.'}", "steps.ident.admin and $exists(input.body.broker) and input.body.broker != '' and $not(input.body.broker in ['Imane', 'Salma', 'Majid', 'Omar'])"),
    tr("tel", "($d := $replace($string(input.body.telephone), /[^0-9]/, ''); {'norm': $length($d) < 9 ? '' : ($substring($d, 0, 2) = '00' ? '+' & $substring($d, 2) : ($substring($d, 0, 1) = '0' ? '+212' & $substring($d, 1) : ($length($d) = 9 ? '+212' & $d : '+' & $d)))})", "Téléphone normalisé"),
    lr("deja", T["oc"], ["id", OC["broker"]], [flt("crm_cle_creation", "eq", "{{ steps.op.id }}")], limit=1, name="Reprise (même clé)"),
    respond("dejafait", 200, "{'items':[{'id': steps.deja.rows[0].id, 'lien': '/opportunite-client?id=' & $string(steps.deja.rows[0].id), 'message':'Lead déjà enregistré.', 'reprise': true}]}",
            "$count(steps.deja.rows) > 0"),
    lr("contact", T["contacts"], ["id"], [flt("crm_telephone_normalise", "eq", "{{ steps.tel.norm }}")], limit=1,
       name="Contact existant", run_if="steps.tel.norm != ''"),
    lr("doublon", T["oc"], ["id", OC["broker"], OC["etape"]], [flt(OC["contact"], "eq", "{{ $string(steps.contact.rows[0].id) }}")], limit=5,
       name="Dossier ouvert pour ce contact", run_if="$count(steps.contact.rows) > 0"),
    respond("g409", 409, "steps.ident.admin or steps.doublon.rows[0].src_c2ljvedgo8rjnjz = steps.ident.broker ? {'error':'Un dossier existe déjà pour ce numéro.', 'lien': '/opportunite-client?id=' & $string(steps.doublon.rows[0].id)} : {'error':'Ce numéro est déjà suivi dans le CRM. Contactez l’administrateur.'}",
            "$count(steps.doublon.rows[$not($string(src_ch80mhxt9wmgffa) in ['Gagné', 'Perdu'])]) > 0"),
    ds("newcontact", "createRecord", {"table": T["contacts"], "values":
        "{'libelle': $trim(input.body.nom), 'src_chepoppm9ctk3tm': $trim(input.body.nom), 'src_c2j3fuou3o8taqa': input.body.telephone, "
        "'crm_telephone_normalise': steps.tel.norm, 'crm_cle_creation': steps.op.id}"}, "Création du contact",
       run_if="$count(steps.contact.rows) = 0"),
    ds("write", "createRecord", {"table": T["oc"], "values":
        "($bud := $exists(input.body.budget) and input.body.budget != '' ? $number($string(input.body.budget)) : null; "
        "{'libelle': $trim(input.body.nom), '" + OC["prenom"] + "': $trim(input.body.nom), "
        "'" + OC["broker"] + "': steps.ident.admin and $exists(input.body.broker) and input.body.broker != '' ? input.body.broker : steps.ident.broker, "
        "'" + OC["etape"] + "': 'Nouveau', '" + OC["action"] + "': 'Appeler', '" + OC["tel"] + "': steps.tel.norm != '' ? steps.tel.norm : null, "
        "'" + OC["tx"] + "': input.body.transaction, '" + OC["bl"] + "': input.body.transaction = 'Location' ? $bud : null, "
        "'" + OC["ba"] + "': input.body.transaction = 'Achat' ? $bud : null, '" + OC["quartier"] + "': input.body.quartier, "
        "'" + OC["type"] + "': input.body.typeBien in ['Appartement', 'Villa', 'Bureau', 'Local commercial', 'Terrain', 'Industriel', 'Autre', 'Studio'] ? input.body.typeBien : null, "
        "'" + OC["canal"] + "': input.body.canal in ['WhatsApp', 'Meta Ads', 'Agent / recommandation', 'Site web', 'Téléphone', 'Autre'] ? input.body.canal : null, "
        "'" + OC["contact"] + "': $count(steps.contact.rows) > 0 ? steps.contact.rows[0].id : steps.newcontact.id, "
        "'crm_cle_creation': steps.op.id})"}, "Création de l'opportunité"),
    journal("j", "client", "steps.write.id", "Création lead", "'Lead ' & input.body.transaction",
            "{'contact': $count(steps.contact.rows) > 0 ? 'existant' : 'créé', 'cle': steps.op.id}", "$contains(input.body.nom, '[RECETTE V21]')"),
    respond("done", 201, "{'items':[{'id': steps.write.id, 'lien': '/opportunite-client?id=' & $string(steps.write.id), 'message':'Lead créé.'}]}"),
], body=[b("nom", "string", True), b("telephone"), b("transaction", "string", True), b("budget", "any"), b("quartier"), b("typeBien"),
         b("canal"), b("broker"), b("cle", "string", False, "clé d'idempotence fournie par le formulaire")],
    description="Ordre : reprise par clé → contact existant par téléphone normalisé → contact → opportunité → journal. Relance avec la même clé = aucun doublon."))

# W8. Nouvelle opportunité de bien
EP.append(endpoint("CRM21 — Nouvelle opportunité de bien", "POST", "/crm21/opportunites-biens", IDENT + [OP] + [
    respond("gnom", 400, "{'error':'Nom du bien obligatoire (3 à 150 caractères).'}",
            "$length($trim($string(input.body.nom))) < 3 or $length($string(input.body.nom)) > 150"),
    respond("gtx", 400, "{'error':'Choisissez Vente ou Location.'}", "$not(input.body.transaction in ['Vente', 'Location'])"),
    respond("gty", 400, "{'error':'Type de bien inconnu.'}",
            "$exists(input.body.type) and input.body.type != '' and $not(input.body.type in ['appartement', 'studio', 'villa', 'local commerciale', 'magasin', 'bureau', 'terrain', 'local'])"),
    respond("gpx", 400, "{'error':'Prix invalide.'}",
            "$exists(input.body.prix) and input.body.prix != '' and ($type($number($string(input.body.prix))) != 'number' or $number($string(input.body.prix)) < 0)"),
    lr("deja", T["journal"], ["id", "dossier_id"], [flt("operation_id", "eq", "{{ steps.op.id }}"), flt("type_evenement", "eq", "Création opportunité de bien")],
       limit=1, name="Reprise"),
    respond("dejafait", 200, "{'items':[{'id': $number(steps.deja.rows[0].dossier_id), 'lien': '/opportunite-bien?id=' & steps.deja.rows[0].dossier_id, 'message':'Opportunité déjà enregistrée.', 'reprise': true}]}",
            "$count(steps.deja.rows) > 0"),
    ds("write", "createRecord", {"table": T["ob"], "values":
        "{'libelle': $trim(input.body.nom), '" + OB["nom"] + "': $trim(input.body.nom), '" + OB["tx"] + "': input.body.transaction, "
        "'" + OB["type"] + "': input.body.type != '' ? input.body.type : null, "
        "'" + OB["prix"] + "': $exists(input.body.prix) and input.body.prix != '' ? $number($string(input.body.prix)) : null, "
        "'" + OB["quartier"] + "': input.body.quartier, '" + OB["gest"] + "': input.body.gestionnaire, '" + OB["gesttel"] + "': input.body.gestionnaireTel, "
        "'" + OB["resp"] + "': steps.ident.broker, 'resultat_commercial': 'À qualifier', 'tat_de_migration_gestionnaire': 'À confirmer', "
        "'crm_prochaine_action': 'Qualifier le bien avec le gestionnaire', 'table_origine': 'SuperAPP CRM V2.1'}"}, "Création"),
    journal("j", "opportunite-bien", "steps.write.id", "Création opportunité de bien", "input.body.nom", "{'cle': steps.op.id}",
            "$contains(input.body.nom, '[RECETTE V21]')"),
    respond("done", 201, "{'items':[{'id': steps.write.id, 'lien': '/opportunite-bien?id=' & $string(steps.write.id), 'message':'Opportunité de bien créée.'}]}"),
], body=[b("nom", "string", True), b("transaction", "string", True), b("type"), b("prix", "any"), b("quartier"),
         b("gestionnaire"), b("gestionnaireTel"), b("cle")],
    description="Créée avec le broker appelant comme responsable ; gestionnaire « À confirmer »."))

# W9. Suivi d'une opportunité de bien (verrouillé hors responsable)
EP.append(endpoint("CRM21 — Suivi opportunité de bien", "PATCH", "/crm21/opportunites-biens", IDENT + [PER, OP] + [
    respond("gid", 400, "{'error':'Opportunité manquante.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("gres", 400, "{'error':'Résultat inconnu.'}",
            "$exists(input.body.resultat) and $not(input.body.resultat in ['À qualifier', 'Disponible pour affectation', 'En cours', 'Gagnée — commercialisation autorisée', 'Perdue'])"),
    respond("gpr", 400, "{'error':'Priorité inconnue.'}", "$exists(input.body.priorite) and $not(input.body.priorite in ['Urgente', 'Haute', 'Normale'])"),
    respond("gech", 400, "{'error':'Échéance invalide (AAAA-MM-JJTHH:MM).'}",
            "$exists(input.body.echeance) and input.body.echeance != '' and $not($contains($string(input.body.echeance), /^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$/))"),
    respond("glen", 400, "{'error':'Texte trop long.'}", "$length($string(input.body.notes)) > 4000 or $length($string(input.body.prochaineAction)) > 300"),
    lr("ob", T["ob"], ["id", "libelle", OB["resp"], "crm_notes_suivi", "crm_prochaine_action", "crm_echeance", "crm_priorite", "resultat_commercial"],
       [flt("id", "eq", "{{ $string(input.body.id) }}")], limit=1),
    respond("g404", 404, "{'error':'Opportunité introuvable.'}", "$count(steps.ob.rows) = 0"),
    journal("refus", "opportunite-bien", "input.body.id", "Refus hors responsable", "'Tentative de modification par ' & steps.ident.broker", "''", "false",
            run_if="$not(steps.ident.admin or $string(steps.ob.rows[0]." + OB["resp"] + ") = steps.ident.broker)"),
    respond("gown", 403, "{'error':'Seul le responsable (' & $string(steps.ob.rows[0]." + OB["resp"] + ") & ') ou l’administrateur peut modifier ce suivi.'}",
            "$not(steps.ident.admin or $string(steps.ob.rows[0]." + OB["resp"] + ") = steps.ident.broker)"),
    tr("v", TOISO + r"""
$B := $$.input.body; $r := $$.steps.ob.rows[0];
$v := $merge([
  $exists($B.prochaineAction) ? {'crm_prochaine_action': $B.prochaineAction} : {},
  $exists($B.priorite) ? {'crm_priorite': $B.priorite} : {},
  $exists($B.resultat) ? {'resultat_commercial': $B.resultat} : {},
  $exists($B.echeance) ? {'crm_echeance': $B.echeance = '' ? null : $iso($B.echeance)} : {},
  $exists($B.notes) and $B.notes != '' ? {'crm_notes_suivi': $trim($s($r.crm_notes_suivi) & '\n[' & $substring($now(), 0, 10) & ' — ' & $$.steps.ident.nom & '] ' & $B.notes)} : {}
]);
{'values': $v, 'n': $count($keys($v))}
""", "Champs autorisés"),
    respond("gvide", 400, "{'error':'Aucune modification.'}", "steps.v.n = 0"),
    ds("write", "updateRecord", {"table": T["ob"], "recordId": "{{ $string(input.body.id) }}", "values": "steps.v.values", "failIfNotFound": True}),
    journal("j", "opportunite-bien", "input.body.id", "Suivi opportunité de bien", "$join($keys(steps.v.values), ', ')", "steps.v.values",
            "$contains($string(steps.ob.rows[0].libelle), '[RECETTE V21]')"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'message':'Suivi mis à jour.'}]}"),
], body=[b("id", "any", True), b("prochaineAction"), b("echeance"), b("priorite"), b("resultat"), b("notes")],
    description="Modification réservée au responsable ou à l'admin ; toute tentative refusée est tracée dans le journal."))

# W10. Activation contrôlée du bien lié
EP.append(endpoint("CRM21 — Activer le bien lié", "POST", "/crm21/activation-bien", IDENT + [OP] + [
    respond("gid", 400, "{'error':'Opportunité manquante.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    lr("ob", T["ob"], ["id", "libelle", OB["resp"], "resultat_commercial", "pmv6m9j8dh2qj_biens_id"], [flt("id", "eq", "{{ $string(input.body.id) }}")], limit=1),
    respond("g404", 404, "{'error':'Opportunité introuvable.'}", "$count(steps.ob.rows) = 0"),
    respond("gown", 403, "{'error':'Activation réservée au responsable ou à l’administrateur.'}",
            "$not(steps.ident.admin or $string(steps.ob.rows[0]." + OB["resp"] + ") = steps.ident.broker)"),
    respond("glien", 409, "{'error':'Aucun bien lié : rattachez d’abord le bien.'}",
            "$not($exists(steps.ob.rows[0].pmv6m9j8dh2qj_biens_id)) or $string(steps.ob.rows[0].pmv6m9j8dh2qj_biens_id) = 'null'"),
    respond("gres", 409, "{'error':'Activation possible seulement quand le résultat est « Gagnée — commercialisation autorisée ».'}",
            "$not($contains($string(steps.ob.rows[0].resultat_commercial), 'Gagnée'))"),
    ds("write", "updateRecord", {"table": T["biens"], "recordId": "{{ $string(steps.ob.rows[0].pmv6m9j8dh2qj_biens_id) }}", "failIfNotFound": True,
                                 "values": "{'" + BI["dispo"] + "': 'Actif', 'date_confirmation_dispo': $substring($now(), 0, 10)}"}, "Bien actif"),
    journal("j", "opportunite-bien", "input.body.id", "Activation du bien lié", "'Bien ' & $string(steps.ob.rows[0].pmv6m9j8dh2qj_biens_id) & ' activé'",
            "{'bien': steps.ob.rows[0].pmv6m9j8dh2qj_biens_id, 'dispo': 'Actif'}", "$contains($string(steps.ob.rows[0].libelle), '[RECETTE V21]')"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'lienBien': '/bien?id=' & $string(steps.ob.rows[0].pmv6m9j8dh2qj_biens_id), 'message':'Bien activé dans le catalogue.'}]}"),
], body=[b("id", "any", True)], description="Active le bien lié si le dossier est gagné ; responsable ou admin."))

# W11. Suivi d'un bien (disponibilité)
EP.append(endpoint("CRM21 — Suivi d'un bien", "PATCH", "/crm21/biens", IDENT + [PER, OP] + [
    respond("gid", 400, "{'error':'Bien manquant.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("gdis", 400, "{'error':'Disponibilité inconnue.'}", "$exists(input.body.dispo) and $not(input.body.dispo in ['Actif', 'Inactif'])"),
    respond("glen", 400, "{'error':'Texte trop long.'}", "$length($string(input.body.notes)) > 4000"),
    lr("bien", T["biens"], ["id", "libelle", BI["resp"], "crm_notes_suivi"], [flt("id", "eq", "{{ $string(input.body.id) }}")], limit=1),
    respond("g404", 404, "{'error':'Bien introuvable.'}", "$count(steps.bien.rows) = 0"),
    respond("gown", 403, "{'error':'Seul le broker principal du bien ou l’administrateur peut le modifier.'}",
            "$not(steps.ident.admin or $string(steps.bien.rows[0]." + BI["resp"] + ") = steps.ident.broker)"),
    tr("v", r"""
$B := $$.input.body; $r := $$.steps.bien.rows[0];
$v := $merge([
  $B.confirmerDispo = true or $B.confirmerDispo = 'true' ? {'date_confirmation_dispo': $substring($now(), 0, 10), '""" + BI["dispo"] + r"""': 'Actif'} : {},
  $exists($B.dispo) ? {'""" + BI["dispo"] + r"""': $B.dispo} : {},
  $exists($B.prochaineAction) ? {'crm_prochaine_action': $B.prochaineAction} : {},
  $exists($B.notes) and $B.notes != '' ? {'crm_notes_suivi': $trim(($exists($r.crm_notes_suivi) and $type($r.crm_notes_suivi) != 'null' ? $string($r.crm_notes_suivi) : '') & '\n[' & $substring($now(), 0, 10) & '] ' & $B.notes)} : {}
]);
{'values': $v, 'n': $count($keys($v))}
""", "Champs autorisés"),
    respond("gvide", 400, "{'error':'Aucune modification.'}", "steps.v.n = 0"),
    ds("write", "updateRecord", {"table": T["biens"], "recordId": "{{ $string(input.body.id) }}", "values": "steps.v.values", "failIfNotFound": True}),
    journal("j", "bien", "input.body.id", "Suivi du bien", "$join($keys(steps.v.values), ', ')", "steps.v.values",
            "$contains($string(steps.bien.rows[0].libelle), '[RECETTE V21]')"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'message':'Bien mis à jour.'}]}"),
], body=[b("id", "any", True), b("confirmerDispo", "any"), b("dispo"), b("prochaineAction"), b("notes")],
    description="Confirmer la disponibilité, changer le statut ou ajouter une note ; broker principal ou admin."))

# W12. Attribution par l'admin
EP.append(endpoint("CRM21 — Attribuer (admin)", "PATCH", "/crm21/attribution", IDENT + [ADMIN_ONLY, OP] + [
    respond("gty", 400, "{'error':'Type inconnu.'}", "$not(input.body.type in ['client', 'bien'])"),
    respond("gid", 400, "{'error':'Identifiant manquant.'}", "$not($contains($string(input.body.id), /^[1-9][0-9]{0,9}$/))"),
    respond("gbk", 400, "{'error':'Broker inconnu.'}", "$not(input.body.broker in ['Imane', 'Salma', 'Majid', 'Omar'])"),
    ds("wc", "updateRecord", {"table": T["oc"], "recordId": "{{ $string(input.body.id) }}", "failIfNotFound": True,
                              "values": "{'" + OC["broker"] + "': input.body.broker}"}, "Dossier client", run_if="input.body.type = 'client'"),
    ds("wb", "updateRecord", {"table": T["ob"], "recordId": "{{ $string(input.body.id) }}", "failIfNotFound": True,
                              "values": "{'" + OB["resp"] + "': input.body.broker}"}, "Opportunité de bien", run_if="input.body.type = 'bien'"),
    journal("j", "attribution", "input.body.id", "Attribution", "input.body.type & ' → ' & input.body.broker", "{'broker': input.body.broker}",
            "$contains($string(steps.wc.libelle) & $string(steps.wb.libelle), '[RECETTE V21]')"),
    respond("done", 200, "{'items':[{'id': $number($string(input.body.id)), 'broker': input.body.broker, 'message':'Attribué à ' & input.body.broker & '.'}]}"),
], body=[b("type", "string", True), b("id", "any", True), b("broker", "string", True)],
    description="Attribution d'un dossier client ou d'une opportunité de bien ; un seul écrivain (admin)."))


def write_all(outdir):
    os.makedirs(outdir, exist_ok=True)
    for e in EP:
        d = e["definition"]
        fn = "crm21__%s_%s.json" % (d["method"], d["path"].replace("/crm21/", "").replace("/", "_"))
        with open(os.path.join(outdir, fn), "w") as f:
            json.dump(e, f, ensure_ascii=False, indent=1)
        print(fn, len(json.dumps(e)))


if __name__ == "__main__":
    write_all(os.path.join(os.path.dirname(os.path.abspath(__file__)), "endpoints"))
