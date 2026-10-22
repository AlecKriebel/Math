#!/usr/bin/env python3
"""Install only the externally authorized exact core; retain before/after pins."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145';W=A/'publication/workflow';D=A/'preprint'
OLD='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8';NEW='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';AUTH='88c70b6d71f2674fa5593a70c2924a949408fadd6b36f731127db1aaef469063';READY='14bd1137e83f974e7dbf8153614533d72b5fe93d6382cea33e220580e396d603'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):
 path=Path(path);parts=path.relative_to(ROOT).parts
 for i in range(len(parts)+1):need(not ROOT.joinpath(*parts[:i]).is_symlink(),'no linked input')
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':sha(b),'mode':format(path.stat().st_mode,'06o')}
def save_new(name,value):
 with (OWN/name).open('x') as stream:json.dump(value,stream,indent=2,ensure_ascii=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
started=now();authorization=A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json';need(pin(authorization)['sha256']==AUTH,'external root authorization before reading');auth=json.loads(raw(authorization));need(auth['authorized_new_core_sha256']==NEW and auth['old_installed_core_sha256']==OLD and auth['readiness_sha256']==READY,'exact root authorized transition')
readiness=raw(OWN/'PROPOSAL_READINESS.json');need(sha(readiness)==READY,'external immutable proposal readiness');doc=json.loads(readiness)
for name,item in doc['files'].items():need(pin(ROOT/name)==item,'proposal closure changed before installation '+name)
core=P/'accept_pr952.py';proposed=raw(OWN/'PROPOSED_accept_pr952.py');need(pin(core)['sha256']==OLD and sha(proposed)==NEW,'exact old/new core bytes')
paths=[P/name for name in ['merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py','CURRENT_STATE.json','inventory.json','RESEARCH_LOG.md']]+[ROOT/'zenodo_deposit_tool/zenodo.py',A/'RESEARCH_LOG.md',A/'source_record_private.txt',A/'ORIGINAL_FILE_RECORDS.json',A/'operations_engineering_03/MANIFEST.json']
for directory in [W,D,A/'original']:
 paths.extend(path for path in directory.rglob('*') if path.is_file())
paths.extend(ROOT/name for name in ['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/catalog.json','unsolved_math_prioritization/review_v2/related_target_groups.json','unsolved_math_prioritization/cache/catalog.sqlite'])
protected={path.relative_to(ROOT).as_posix():pin(path) for path in sorted(set(paths))}
save_new('INSTALL_BEFORE_PROTECTED_SNAPSHOT.json',{'utc':now(),'path_base':'repository_root','files':protected,'file_count':len(protected),'scope':'Exact noncore shared paths observed before authorized installation; pin metadata only, no private contents copied.'})
intent={'schema':'pr952-engineering04-exact-core-install-intent-v1','started_utc':started,'root_authorization_path':authorization.relative_to(ROOT).as_posix(),'root_authorization_sha256':AUTH,'proposal_readiness_sha256':READY,'target':core.relative_to(ROOT).as_posix(),'before':pin(core),'approved_after':pin(OWN/'PROPOSED_accept_pr952.py'),'sole_shared_mutation':'replace exact accept_pr952.py bytes','remote_mutation_authorized':False,'acceptance_authority':False}
save_new('INSTALL_INTENT.json',intent)
info=core.stat();need(info.st_nlink==1 and stat.S_IMODE(info.st_mode)==0o644,'core single-link644')
temporary=OWN/'INSTALL_CORE_APPROVED.tmp';fd=os.open(temporary,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
try:
 with os.fdopen(fd,'wb') as stream:
  os.fchmod(stream.fileno(),0o644);need(stream.write(proposed)==len(proposed),'complete approved byte write');stream.flush();os.fsync(stream.fileno())
 need(raw(temporary)==proposed and pin(core)['sha256']==OLD,'temporary/new and fresh old pins')
 os.replace(temporary,core)
 directory=os.open(P,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(directory)
 finally:os.close(directory)
finally:
 if temporary.exists():temporary.unlink()
need(raw(core)==proposed,'installed exact approved readback')
for name,item in protected.items():need(pin(ROOT/name)==item,'protected shared file changed during installation '+name)
save_new('INSTALL_ACTION_RECEIPT.json',{**intent,'completed_utc':now(),'installed':pin(core),'protected_noncore_file_count':len(protected),'all_noncore_protected_files_exact':True,'actual_service_Git_or_remote_mutations':0,'workflow_science_state_inventory_logs_edits':0,'installed_tests_pending':True,'status':'EXACT_AUTHORIZED_CORE_INSTALLED_WAITING_INERT_VALIDATION'})
with (OWN/'INSTALL_RESEARCH_LOG.md').open('x') as stream:stream.write('# PR952 authorized installation engineering log\n\n'+now()+' — External root authorization88c70b... and prior399-file readiness14bd... authenticated before installation. Installed ONLY exact14ac4e... core atomically with readback; '+str(len(protected))+' other shared paths unchanged. Original proposal research log/399 closure retained byte-exact; this separate installation log records new work. Installation-validation estimate25%; no acceptance/service authority.\n')
print(json.dumps({'status':'EXACT_AUTHORIZED_CORE_INSTALLED','sha256':sha(raw(core)),'protected_shared_files':len(protected),'receipt_sha256':sha(raw(OWN/'INSTALL_ACTION_RECEIPT.json'))}))
