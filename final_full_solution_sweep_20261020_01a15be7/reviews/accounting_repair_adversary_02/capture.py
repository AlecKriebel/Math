from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
R = Path(__file__).resolve().parent
B = R.parent.parent
P = B/'reviews/completed_publications_accounting_adversary'
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def put(path, value):
    p=R/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(value if isinstance(value,bytes) else (json.dumps(value,indent=2)+'\n').encode())
entries=[]
def capture(src,dst):
    if not src.is_file() or src.is_symlink(): raise RuntimeError(str(src))
    data=src.read_bytes(); put(dst,data)
    entries.append(dict(source=str(src),captured_path=str(dst),captured_at=now(),bytes=len(data),sha256=sha(data)))

put('RESEARCH_LOG.json',[dict(at=now(),completion_estimate_percent=10,event='Bounded independent structural-accounting review started; writes confined to this new review folder. Provider/Git mutations and external outreach excluded.')])
# Immutable old evidence is read and copied, never executed in place or modified.
oldseal=json.loads((P/'OUTPUT_MANIFEST.json').read_text())
bad=[]
for e in oldseal['files']:
    data=(P/e['path']).read_bytes()
    if len(data)!=e['bytes'] or sha(data)!=e['sha256']:bad.append(e['path'])
put('PRE_REPAIR_SEAL_VALIDATION.json',dict(at=now(),files=len(oldseal['files']),mismatches=bad,manifest_sha256=sha((P/'OUTPUT_MANIFEST.json').read_bytes())))
if bad:raise RuntimeError('Pre-repair immutable evidence mismatch')
for src in sorted((P/'inputs/effort').rglob('*')):
    if src.is_file():capture(src,Path('inputs/pre_repair')/src.relative_to(P/'inputs/effort'))
for name in ['REPORT.md','override_controls.py','OVERRIDE_CONTROLS.json','INPUT_MANIFEST.json','OUTPUT_MANIFEST.json','INDEPENDENT_ACCOUNTING.json']:
    capture(P/name,Path('inputs/prior_review')/name)
for name in ['coverage_snapshot.py','STATE.json','rest_inventory.json','dispositions.jsonl','ACCOUNTING_REPAIR_ROOT_REPLAY.json','ROOT_ACCOUNTING_PRE_REPAIR_REVIEW_ACCEPTANCE.json']:
    capture(B/name,Path('inputs/current')/name)
capture(B/'accounting_history/pre_repair_20261021T1704/coverage_snapshot.py',Path('inputs/history/coverage_snapshot.py'))
journal=[json.loads(x) for x in (R/'inputs/current/dispositions.jsonl').read_text().splitlines() if x.strip()]
for e in journal:capture(B/f'PR{e["pr"]:04d}_DISPOSITION.json',Path('inputs/current')/f'PR{e["pr"]:04d}_DISPOSITION.json')
state=json.loads((R/'inputs/current/STATE.json').read_text())
for e in state['reopened_disposition_overrides']:
    capture(B/e['replacement_disposition'],Path('inputs/current')/e['replacement_disposition'])
for e in state['completed_publications']:
    name=e['verification'];capture(B/name,Path('inputs/current')/name)
    proof=json.loads((R/'inputs/current'/name).read_text())
    for rel in proof['evidence'].values():
        p=Path(rel)
        if not p.is_absolute() and (B/p).is_file():capture(B/p,Path('inputs/current')/p)
put('INPUT_MANIFEST.json',dict(at=now(),files=entries,note='Each source was read individually before fixture execution. Canonical STATE/journal may advance later; no globally atomic snapshot or frozen-current-files assertion. Complete recursive old captured inputs retained; current direct evidence captured recursively by original relative path.'))
print(json.dumps(dict(captured_files=len(entries),prior_sealed_files=len(oldseal['files']),prior_seal_mismatches=bad,current_next_pr=state['next_pr'],current_journal_count=len(journal)),indent=2))
