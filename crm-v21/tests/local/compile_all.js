// Compile chaque expression JSONata (runIf, transform, respond body, values, modèles {{ }}) de chaque endpoint /crm21/.
const fs = require('fs'), path = require('path'), jsonata = require('jsonata');
const dir = process.argv[2]; let ko = 0, n = 0;
const chk = (f, where, e) => { n++; try { jsonata(e); } catch (x) { ko++; console.log('KO', f, where, x.code, x.message, 'pos', x.position, '«', e.slice(Math.max(0, x.position - 80), x.position + 20), '»'); } };
const walk = (f, steps) => { for (const s of steps) {
  if (s.runIf) chk(f, s.key + '.runIf', s.runIf);
  const c = s.config || {};
  if (s.type === 'transform') chk(f, s.key + '.expr', c.expression);
  if (s.type === 'respond' && c.body) chk(f, s.key + '.body', c.body);
  const p = c.params || {};
  if (typeof p.values === 'string') chk(f, s.key + '.values', p.values);
  for (const v of [p.recordId, ...(p.filters || []).map((x) => x.value)]) if (typeof v === 'string') for (const m of v.matchAll(/\{\{(.*?)\}\}/g)) chk(f, s.key + '.tpl', m[1]);
  if (c.onTrue) walk(f, c.onTrue); if (c.onFalse) walk(f, c.onFalse);
} };
for (const f of fs.readdirSync(dir).filter((x) => x.startsWith('crm21__'))) walk(f, JSON.parse(fs.readFileSync(path.join(dir, f))).definition.steps);
console.log('expressions:', n, 'erreurs:', ko);
