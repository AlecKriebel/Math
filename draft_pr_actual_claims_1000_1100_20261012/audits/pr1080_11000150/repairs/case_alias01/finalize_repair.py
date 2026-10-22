#!/usr/bin/env python3
"""Close only this bounded support workspace; no earlier stage is rewritten."""
import datetime,difflib,hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent;A=W.parents[1];D=A/'preprint_v1_0'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def row(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
if (W/'SEAL.json').exists():raise RuntimeError('Cannot alter a sealed support workspace')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (W/'RESEARCH_LOG.md').open('a') as f:f.write('- '+now+': Complete report and code/prose diff closed; exact before/current/protected/output inventories and separate seal prepared. Bounded physical output repair and terminal handoff 100%; mathematical research estimate 60%. ROOT adoption and NEW independent complete whole03 required; readiness/issues-resolved/publication remain false, services held at PR1032.\n')
patch=[]
for r in obj(W/'BEFORE_COPIES.json')['files']:
 name=r['original_path']
 if name.endswith('.zip'):continue
 patch.extend(difflib.unified_diff((A/r['source_snapshot']).read_text().splitlines(keepends=True),(A/name).read_text().splitlines(keepends=True),fromfile='before/'+name,tofile='after/'+name))
for name in ['preprint_v1_0/CURRENT_CASE_ALIAS_REPAIR01.json','preprint_v1_0/verification_kit/CURRENT_CASE_ALIAS_REPAIR01.json','preprint_v1_0/verification_kit/CASE_ALIAS_HISTORY_RELOCATIONS.json']:
 patch.extend(difflib.unified_diff([],(A/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+name))
for p in sorted(W.glob('*.py')):
 patch.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+p.relative_to(A).as_posix()))
small=['REPORT.md','RESEARCH_LOG.md','ENVIRONMENTAL_ENOSPC_PRE_DRIVER.json','FIRST_ATTEMPT_AND_DIAGNOSTIC.json','AUTHORING_COMPLETE.json','BEFORE_COPIES.json','NEW_COPY_ROWS.json','APPENDED_HISTORY_ROWS.json','SELECTED_CASE_INPUTS.json','REPRODUCTION_SUMMARY.json','FINAL_VERIFICATION.json']
for name in small:
 p=W/name;patch.extend(difflib.unified_diff([],p.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+p.relative_to(A).as_posix()))
(W/'COMPLETE_CODE_PROSE_DIFF.patch').write_text(''.join(patch))
files=[row(p,W) for p in sorted(W.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in {'OUTPUT_PINS.json','SEAL.json'}]
dump(W/'OUTPUT_PINS.json',{'utc':now,'scope':'Every local repair artifact, including complete exact before snapshots and local-only old ZIP, except this inventory and its separate seal. No self-hash.','files':files})
dump(W/'SEAL.json',{'utc':now,'scope':'Separate custody seal binds the complete output inventory, never itself. Not a signature, peer review or final readiness certification.','output_inventory':row(W/'OUTPUT_PINS.json',W),'outputs':len(files),'current_archive':row(D/'verification_kit.zip',D),'current_manifest':row(D/'verification_kit/MANIFEST.json',D),'current_external_binding':row(D/'EXTERNAL_BINDING.json',D),'whole_reviews_completed':2,'minimum_whole_reviews':2,'new_complete_whole03_required':True,'root_repair_adoption_required':True,'root_integrity_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at':1032,'bounded_repair_completion_best_guess_percent':100,'mathematical_research_completion_best_guess_percent':60})
print(json.dumps({'status':'SEALED_BOUNDED_REPAIR_HANDOFF_PENDING_ROOT_ADOPTION_AND_NEW_COMPLETE_WHOLE03','outputs':len(files),'inventory':row(W/'OUTPUT_PINS.json',W),'seal':row(W/'SEAL.json',W)},indent=2))
