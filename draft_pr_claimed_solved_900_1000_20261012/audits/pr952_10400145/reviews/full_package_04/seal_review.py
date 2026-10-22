from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parent
# Deliberately public authored metadata/source/raw finite receipts. No recursive
# traversal of private, fixtures, render, caches or primary-body directories.
selected=[q for q in R.iterdir() if q.is_file() and q.name!='MANIFEST.json' and q.suffix in ('.md','.json','.py','.raw')]
selected += list((R/'sources').glob('*RETRIEVAL.json'))
for d in R.iterdir():
 if d.is_dir() and d.name.startswith('observations_'):selected += list(d.glob('*.json'))
records={}
for q in sorted(selected):
 name=q.relative_to(R).as_posix()
 if name in records:raise RuntimeError('duplicate allowlist')
 b=q.read_bytes();records[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json'}
if not mandatory<=set(records):raise RuntimeError('missing mandatory records')
manifest={'schema':'pr952-full-package-review-public-seal-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_agent_id':'/root/pr952_full_package_04','files':records,'explicit_public_allowlist':list(records),'excluded_private_material':'Private primary bodies/text extracts/images, caches, mutable fixtures, downloaded HTML/PDF bodies, temporary cold/operations files and private raw preflight output remain preserved but excluded. Authentication maps and actual observation receipts are deliberately public metadata. MANIFEST self-excluded.','derived_code_note':'run_cold/run_suites/run_additional_replays/inspect_closures/inspect_originals reuse explicitly labeled authenticated earlier orchestration/checklists with own-path or numbered-history adaptations; new cyclotomic and marker case designs are own04. Original v1 math source and observed outputs retained before integer-sign correction.','authority':'No acceptance, publication or service/Git mutation authority.'}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print('SEALED',len(records),hashlib.sha256((R/'MANIFEST.json').read_bytes()).hexdigest())
