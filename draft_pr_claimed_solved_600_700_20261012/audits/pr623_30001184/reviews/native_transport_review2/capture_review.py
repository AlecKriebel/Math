from pathlib import Path
import hashlib, json, datetime

ROOT = Path('/Users/alec/Documents/Math')
AUDIT = ROOT/'draft_pr_claimed_solved_600_700_20261012/audits/pr623_30001184'
HERE = AUDIT/'reviews/native_transport_review2'
SNAP = HERE/'tmp/inputs'
SNAP.mkdir(parents=True, exist_ok=True)

files = list((AUDIT/'reviews/native_transport_author').glob('*'))
files = [p for p in files if p.is_file()]
files += [ROOT/'zenodo_deposit_tool/zenodo.py']
files += list((AUDIT/'reviews/native_transport_review1').glob('*'))
files = [p for p in files if p.is_file()]
files += [AUDIT/n for n in ['FINAL_PUBLICATION_GATE.json','NATIVE_PUBLISHED_API_CALIBRATION.json','NATIVE_PUBLISHED_CONTENT_CALIBRATION.json','NATIVE_PUBLISHED_CONTENT_WILDCARD_CALIBRATION.json','PR_METADATA.json','ROOT_REPAIRED_ARCHIVE_BINDING.json']]
gate_bytes = (AUDIT/'FINAL_PUBLICATION_GATE.json').read_bytes()
gate = json.loads(gate_bytes)
files += [AUDIT/n for n in gate['reviewed_inputs']]
files += [AUDIT/n for n in gate['final_repair_pins']]
receipts = {}
for p in dict.fromkeys(files):
    data = gate_bytes if p == AUDIT/'FINAL_PUBLICATION_GATE.json' else p.read_bytes()
    rel = p.relative_to(ROOT)
    q = SNAP/rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(data)
    receipts[str(rel)] = {'size': len(data), 'sha256':hashlib.sha256(data).hexdigest(), 'snapshot': str(q)}
checks = {}
for rel, v in gate['reviewed_inputs'].items():
    checks[rel] = receipts[str((AUDIT/rel).relative_to(ROOT))]['sha256'] == v['sha256'] and receipts[str((AUDIT/rel).relative_to(ROOT))]['size'] == v['size']
assert all(checks.values())
result = {'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':receipts,'gate45':checks,'gate45_count':len(checks),'native29_count':sum(n.startswith('native/') for n in checks)}
(HERE/'INPUT_BINDING.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'captured':len(receipts),'gate45':len(checks),'native29':result['native29_count'],'all_match':all(checks.values())}))
