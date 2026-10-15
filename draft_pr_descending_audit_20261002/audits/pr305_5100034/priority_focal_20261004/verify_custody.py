from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
errors=[]; resolved=[]; receipts=0; artifacts=0
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((ROOT/'CRITERIA_FREEZE.json').read_text())
if sha(ROOT/'FROZEN_ACCEPTANCE_CRITERIA.md')!=freeze['sha256']: errors.append('Frozen criteria mismatch')
for p in sorted((ROOT/'receipts').glob('*.json')):
    r=json.loads(p.read_text());receipts+=1
    for kind in ['stdout','stderr']:
        q=Path(r[kind+'_file'])
        if not q.exists() or sha(q)!=r[kind+'_sha256']:errors.append(str(p.name)+' '+kind+' mismatch')
    for a in r['artifacts']:
        artifacts+=1;q=Path(a['path'])
        if q.exists() and sha(q)==a['sha256'] and q.stat().st_size==a['bytes']:continue
        if p.name=='classical_boundary_control.json' and q.name=='classical_boundary_control.py':
            archived=ROOT/'classical_boundary_control_initial.py'
            if archived.exists() and sha(archived)==a['sha256'] and archived.stat().st_size==a['bytes']:
                resolved.append({'receipt':str(p.relative_to(ROOT)),'archived_bytes':str(archived.relative_to(ROOT))});continue
        errors.append(str(p.name)+' artifact mismatch '+a['path'])
c=json.loads((ROOT/'SOURCE_CUSTODY.json').read_text())
for a in c['all_private_evidence_files']:
    q=ROOT/a['path']
    if not q.exists() or sha(q)!=a['sha256'] or q.stat().st_size!=a['bytes']:errors.append('custody mismatch '+a['path'])
if len(c['sources'])!=23:errors.append('source count')
report=(ROOT/'FOCAL_PRIORITY_COMPARISON.md').read_text()
for s in c['sources']:
    if s['id'] not in report:errors.append('missing report source '+s['id'])
if '\n\n| S22' in report:errors.append('broken comparison table')
if 'C|M|' in report:errors.append('unescaped table pipe')
for line in report.splitlines():
    if line.startswith('|') and line.count('|')!=4:errors.append('invalid table row delimiters')
out={'criteria_hash':freeze['sha256'],'receipt_count':receipts,'artifact_bindings_checked':artifacts,
     'private_files_checked':len(c['all_private_evidence_files']),
     'historical_resolution':resolved,'errors':errors,'passed':not errors}
print(json.dumps(out,indent=2));raise SystemExit(bool(errors))
