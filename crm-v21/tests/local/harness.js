// Banc de test local des transforms JSONata des endpoints /crm21/ (données synthétiques, aucune donnée réelle).
// Usage : NODE_PATH=<dossier jsonata>/node_modules node harness.js <contracts/endpoints> [filtre]
const fs = require('fs'), path = require('path'), jsonata = require('jsonata');
const dir = process.argv[2], only = process.argv[3] || '';
const iso = (d) => new Date(Date.now() + d * 86400000).toISOString().replace('Z', '+00:00');
const oc = (id, o) => Object.assign({ id: String(id), libelle: 'Client ' + id, src_c2ljvedgo8rjnjz: 'Imane', src_ch80mhxt9wmgffa: 'Recherche active',
  src_csdkjyu1i3h2rpd: iso(-1), src_cc9t923zypqax4s: 'Achat', src_c8ty9timbln0feq: '4000000', src_c0qcaxijrq4e44n: null,
  src_crid8q8n1p0n7qe: 'Bourgogne ', src_cqx1ht4dg6mt0gl: 'Appartement', src_cmt5f5y6apb9n76: '0612345678', pmv6m9j8dh2qj_contacts_id: null,
  src_cali7clgn81g11x: '80', src_cj59gxz110km911: '2', updated_at: iso(0) }, o);
const bien = (id, o) => Object.assign({ id: String(id), libelle: 'Bien ' + id, src_ckik8lj9kqev9ho: 'Actif', src_c9w1scpswzkjl7g: 'Imane',
  src_c30sp73xdb9jdsx: 'Appartement Gauthier ' + id, src_cy2vb7l7nqcvdec: 'appartement', src_c771ftquhdtvl0r: 'Vente', src_c5waewdapjudd8k: '3900000',
  src_c4in13ik1q3f1fw: '110', src_c15ey3zrlrmehdi: 'Bourgogne', src_cdespozafnudzr4: 'Casablanca', src_c16ypivc4c8xya2: '3',
  src_ce4lcsor6pndckt: JSON.stringify([{ url: 'https://exemple.ma/p.jpg' }]), date_confirmation_dispo: null, statut_brief: '🟢 À jour',
  crm_echeance: null, tat_de_migration_gestionnaire: 'Validé', src_cv0gxc73awfgmpw: 'Gest', src_cmb84pfu1pwkzw5: '0522000000' }, o);
const ob = (id, o) => Object.assign({ id: String(id), libelle: 'Opp bien ' + id, src_c7a50877zqv8he2: 'Villa ' + id, src_cazse08x5syk1gn: null,
  src_cwqc3dj4cewpssd: '5000000', resultat_commercial: null, crm_echeance: null, pmv6m9j8dh2qj_biens_id: null, tat_de_migration_gestionnaire: 'À confirmer',
  src_c17fpsjfd07usk6: null, src_cjww4qd9gmywdmx: 'Vente' }, o);
const act = (id, o) => Object.assign({ id: String(id), libelle: 'Visite ' + id, src_cybzjmjoj4zlch0: iso(1), crm_fin: null, src_cwtdcarxql2laii: 'Programme',
  crm_etat_visite: null, crm_broker: 'Imane', opportunit_s_clients_id: '1', biens_id: null, crm_appreciation: null, crm_est_test: null }, o);
const steps = {
  moi: { rows: [{ id: 3, email: 'imane@exemple.ma', nom: 'Imane Test', role: 'Broker', broker: 'Imane', actif: true }] },
  ident: { email: 'imane@exemple.ma', nom: 'Imane Test', role: 'Broker', admin: false, broker: 'Imane', ok: true },
  per: { rows: [{ debut_utc: '2027-02-07T02:00:00+00:00', fin_utc: '2027-03-14T03:00:00+01:00', decalage_min: '0' }] },
  rows: { rows: [oc(1), oc(2, { src_csdkjyu1i3h2rpd: null, src_ch80mhxt9wmgffa: null, libelle: null, src_c8ty9timbln0feq: null }), oc(3, { src_cc9t923zypqax4s: 'Location', src_c0qcaxijrq4e44n: '8000', src_ch80mhxt9wmgffa: 'Négociation' })] },
  contact: { rows: [{ id: 5, libelle: 'Contact', src_c2j3fuou3o8taqa: '0600000000' }] },
  props: { rows: [{ id: 1, cle_proposition: '1-9', statut: 'Proposé', pmv6m9j8dh2qj_biens_id: '9', test_crm1: false, date_proposition: iso(-2) },
                  { id: 2, cle_proposition: '1-9', statut: 'Proposé', pmv6m9j8dh2qj_biens_id: '9', test_crm1: false }] },
  biens: { rows: [bien(9), bien(10, { src_c5waewdapjudd8k: null, src_ce4lcsor6pndckt: null, date_confirmation_dispo: '2026-01-01' }), bien(11, { src_c771ftquhdtvl0r: 'Location' })] },
  events: { rows: [{ id: 1, date_evenement: iso(-1), type_evenement: 'Note', resume: 'Texte', resultat: 'Réussi', test_crm1: false }] },
  acts: { rows: [act(1), act(2, { src_cybzjmjoj4zlch0: null }), act(3, { src_cybzjmjoj4zlch0: iso(-3) })] },
  mesoc: { rows: [{ id: '1' }] },
  oc: { rows: [oc(1), oc(2, { src_csdkjyu1i3h2rpd: null })] },
  ob: { rows: [ob(1), ob(2, { src_cazse08x5syk1gn: 'Imane', crm_echeance: iso(0), resultat_commercial: 'Gagnée — commercialisation autorisée', pmv6m9j8dh2qj_biens_id: '9' })] },
  membres: { rows: [{ nom: 'Imane', broker: 'Imane', role: 'Broker', actif: true }, { nom: 'Majid', broker: 'Majid', role: 'Admin', actif: true }] },
};
const variants = [{}, { vue: 'actions' }, { vue: 'toutes' }, { vue: 'a-venir' }, { vue: 'leads' }, { vue: 'a-actualiser' }, { vue: 'sans-responsable' }, { mes: '1', q: 'bour' }];
(async () => {
  let ko = 0;
  for (const f of fs.readdirSync(dir).filter((x) => x.startsWith('crm21__GET_') && x.includes(only))) {
    const def = JSON.parse(fs.readFileSync(path.join(dir, f))).definition;
    for (const v of variants) {
      const st = JSON.parse(JSON.stringify(steps));
      if (f.includes('acti')) st.rows = st.acts;           // agenda : rows = activités
      if (f.includes('biens') && !f.includes('opportunites')) st.rows = st.biens;
      if (f.includes('GET_bien.')) st.rows = { rows: [bien(9)] };
      if (f.includes('opportunite')) {} 
      if (f.includes('opportunites-biens') || f.includes('opportunite-bien')) st.rows = st.ob;
      if (f.includes('creneaux')) st.rows = st.acts;
      const ctx = { input: { query: Object.assign({ id: '1', clientId: '1' }, v), body: {}, params: {} }, auth: { claims: { email: 'imane@exemple.ma', sub: 'x' } }, steps: st, now: new Date().toISOString() };
      for (const s of def.steps) {
        try {
          if (s.runIf) await jsonata(s.runIf).evaluate(ctx);
          if (s.type === 'transform') {
            const out = await jsonata(s.config.expression).evaluate(ctx);
            if (s.key !== 'out') { ctx.steps[s.key] = out; continue; }
            const it = (out && out.items) || [];
            if (JSON.stringify(v) === '{}') console.log('OK', f, 'items=' + it.length, JSON.stringify(it[0] || {}).slice(0, 700));
          }
        } catch (e) { ko++; console.log('KO', f, JSON.stringify(v), s.key, e.code, e.message, 'pos', e.position); break; }
      }
    }
  }
  console.log('erreurs:', ko);
})();
