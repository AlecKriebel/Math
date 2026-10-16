#!/usr/bin/env python3
"""Close this bounded successor after all writes; later verification is read-only."""
import datetime,difflib,hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0'
def obj(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
if (W/'SEAL.json').exists():raise RuntimeError('Never alter sealed support outputs')
if (W/'scratch').exists():raise RuntimeError('Owned scratch must be pinned and closed first')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (W/'RESEARCH_LOG.md').open('a') as f:f.write('- '+now+': Both qualified READMEs, separate outer/kit three-review accounting, exact-before/source-copy/pointer ledgers, current closed ZIP/binding, 21 actual driver commands, 42 independent semantic commands, full normal/-O mathematical JSON equality with adopted whole03, complete fault suites, 576 guard rejects/273 protected files/12 physical rejects and actual native LOCAL check all pass. Exact scratch pins recorded before owned-only cleanup. Bounded wording repair/handoff completion 100%; mathematical research completion remains 60%. ROOT repair adoption and NEW independent complete whole04 are mandatory; publication_ready/issues_resolved/published remain false and services held at PR1032. Initial read-only Git-status inspection is disclosed in REPORT; no Git mutation or service/outreach occurred.\n')
patch=[]
for r in obj(W/'BEFORE_COPIES.json')['files']:
    n=r['original_path']
    if n.endswith('.zip'):continue
    patch.extend(difflib.unified_diff((A/r['source_snapshot']).read_text().splitlines(keepends=True),(A/n).read_text().splitlines(keepends=True),fromfile='before/'+n,tofile='after/'+n))
copydest={'preprint_v1_0/verification_kit/'+r['destination'] for r in obj(W/'NEW_COPY_ROWS.json')['files']}
for r in obj(W/'CHANGE_ACCOUNTING.json')['new_files']:
    if r['path'] in copydest:continue
    p=A/r['path'];patch.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+r['path']))
for p in sorted(W.iterdir()):
    if p.is_file() and (p.suffix in ['.py','.md'] or p.name in ['BEFORE_COPIES.json','NEW_COPY_ROWS.json','APPENDED_HISTORY_ROWS.json','SELECTED_WHOLE03_INPUTS.json','REPRODUCTION_SUMMARY.json','FINAL_VERIFICATION.json','AUTHORING_COMPLETE.json','PACKAGING_COMPLETE.json']):
        patch.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+p.relative_to(A).as_posix()))
(W/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(patch))
files=[row(p,W) for p in sorted(W.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
dump(W/'OUTPUT_PINS.json',{'utc':now,'scope':'Every local repair artifact, including all exact before snapshots and local-only old ZIP; excludes only this inventory and separate seal. Immutable source-copy additions are enumerated exactly in NEW_COPY_ROWS/CHANGE_ACCOUNTING; operative code/prose is fully diffed. No self-hash.','files':files})
dump(W/'SEAL.json',{'utc':now,'scope':'Separate nonself-hashing custody seal; not a signature, human review, self-adoption or final readiness certification.','output_inventory':row(W/'OUTPUT_PINS.json',W),'outputs':len(files),'current_archive':row(D/'verification_kit.zip',D),'current_manifest':row(D/'verification_kit/MANIFEST.json',D),'current_binding':row(D/'EXTERNAL_BINDING.json',D),'whole_reviews_completed':3,'minimum_whole_reviews':2,'latest_complete_review':'whole03','latest_actionable_counts':{'P0':0,'P1':0,'P2':0,'P3':1},'wording_addressed_pending_ROOT_adoption':True,'required_next_review':'NEW independent complete whole04','root_repair_adoption_required':True,'root_integrity_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'repair_completion_best_guess_percent':100,'mathematical_research_completion_best_guess_percent':60})
print(json.dumps({'status':'SEALED_BOUNDED_WORDING_REPAIR_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE04','outputs':len(files),'inventory':row(W/'OUTPUT_PINS.json',W),'seal':row(W/'SEAL.json',W)},indent=2))
