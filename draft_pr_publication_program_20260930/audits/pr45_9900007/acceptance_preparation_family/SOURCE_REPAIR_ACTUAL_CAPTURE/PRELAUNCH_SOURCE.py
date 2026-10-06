"""Own drafting precision repair; initial proposed source snapshots and full delta remain retained."""
from pathlib import Path
import datetime as dt, difflib, hashlib,json,os
H=Path(__file__).resolve().parent;A=H.parent
names=['pr45_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
initial=H/'INITIAL_GENERATED_SOURCE';initial.mkdir()
patch=[]
for n in names:
 p=H/n;before=p.read_text();(initial/n).write_text(before);after=before
 after=after.replace('exact_original18_and_OBSTRUCTION_unchanged','exact_original18_and_PARTIAL_unchanged')
 after=after.replace('Exactly34 primary completions','Exactly35 primary completions').replace('Exactly34 derived primary completions','Exactly35 derived primary completions').replace('Actual33 prior primaries','Actual34 prior primaries').replace('Require34targets/43turns','Require35targets/43turns').replace('postPR44 native34targets/43turns','postPR44 native35targets/43turns').replace('Exactly35targets/43turns/34primary','Exactly36targets/44turns/35primary').replace('Entire actual43 predecessor references','Entire actual44 predecessor references')
 if n=='pr45_guards.py':
  st=after.index('IMMUTABLE = ');en=after.index('\n',st);after=after[:st]+'IMMUTABLE = '+repr({'PARTIAL.md','SOURCES.md','binary_verification.json','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json','review/submitted_results.json','review/verify_binary_process.py','source_manifest.json','source_record.json','turns.jsonl','verify_binary_process.py'})+after[en:]
  st=after.index('LEGACY_FOREIGN_LOGS_UNUSED = ');en=after.index('\n',st);after=after[:st]+after[en+1:]
  # Fresh protected paths are validated in every gate, including empty/index-clean scopes.
  marker="    snap=load(A/'snapshot_manifest.json');original_native(C/'original_archive')"
  add="    foreign_paths=fresh['protected_foreign_tracked_paths'];require(type(foreign_paths) is list and all(type(n) is str for n in foreign_paths) and foreign_paths==sorted(set(foreign_paths)),'Exact sorted ROOT protected foreign path list')\n    for n in foreign_paths:\n        relative(n);require(n not in NATIVE and not n.startswith(K.relative_to(R).as_posix()+'/') and not n.startswith(A.relative_to(R).as_posix()+'/'),'Foreign exception outside exact owned/native scope')\n"
  after=after.replace(marker,add+marker)
 if before!=after:p.write_text(after);patch.extend(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='INITIAL_GENERATED_SOURCE/'+n,tofile=n))
(H/'SOURCE_REPAIR_DELTA.patch').write_text(''.join(patch))
with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Draft precision repair checkpoint:75% preparation,0% acceptance/discovery. Corrected immutable12 literal PR45 filenames, actual44/35-prior and36-target/44-turn prose and future PARTIAL post flag; preserved every initial source and complete delta. Removed unused inherited foreign exception. No production import/compile/execute.\n')
print(json.dumps({'status':'OWN_SOURCE_PRECISION_REPAIR','actual_pid':os.getpid(),'retained_initial_members':len(names),'production_executed':False,'source_preparation_percent':75}))
