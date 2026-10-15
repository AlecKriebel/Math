"""Publish a scoped checkpoint of closed priority audits, preserving shared work."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_priority_025'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(p.read_bytes())
D=P/('private_'+NAME);D.mkdir(exist_ok=False)
def req(c,label):
 if not c:raise RuntimeError(label)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Shared Git writes held')
window();req(git('branch','--show-current')==b'main\n' and not git('diff','--cached','--raw','-z'),'Wrong branch/index')
parent=git('rev-parse','HEAD').decode().strip();req(parent=='7b0175c879e989ea505f6133cc3e6d1f639b12a7','Unexpected native parent')
req(git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Remote differs')
req(load(A/'ROOT_CLOSED_PRIORITY_FAMILIES_AUTHENTICATION_02.json')['status']=='PASS_CLOSED_PRIORITY_FAMILIES_BYTES_MODES_AND_SCIENTIFIC_REPLAYS','Priority authentication missing')
files=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','checkpoint_311_priority_interim_024_receipt.json',Path(__file__).name,
 'root_pause_pr66_math_20261004.py','root_resume_pr66_math_20261004.py','root_resume_pr66_math_20261004_recovery.py','root_resume_pr66_math_20261004_recovery_2.py']]
files += [A/n for n in ['RESEARCH_LOG.md','ROOT_CLOSED_PRIORITY_FAMILIES_AUTHENTICATION_02.json','root_authenticate_priority_families_02.py',
 'READ_ONLY_PRIORITY_CHECKPOINT_02.md','ROOT_PRIORITY_READ_SCOPE_02.json','root_record_priority_read_scope_02.py',
 'ROOT_PRIORITY_ADVERSARY_GATE_03.json','root_release_priority_adversary_03.py']]
F=A/'priority_factorization'; fm=load(F/'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json')
files += [F/x['relative_path'] for x in fm['audit_files'] if not x['private_excluded_from_publication']]
files += [F/'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json',F/'FINAL_SEAL_RECEIPT.json']
C=A/'priority_closure';cm=load(C/'INPUT_OUTPUT_SHA_MANIFEST.json')
files += [C/x['path'] for x in cm['public_outputs_before_seal']]
files += [C/n for n in ['.gitignore','INPUT_OUTPUT_SHA_MANIFEST.json','FINAL_SEAL.json','SELF_SEAL_RECEIPT.json']]
V=A/'closure_priority_adversary/public'
files += [V/n for n in ['source_only_criteria.md','source_only_freeze.json','first_independent_historical_conclusion.md','first_historical_freeze.json','independent_boundary_bridge.md','independent_bridge_freeze.json']]
files=sorted(set(files));allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in files}|{str(allow.relative_to(R))}
req(not any('/private/' in x or '/command_captures/' in x or '/private_sources/' in x or '/streams/' in x for x in paths),'Private sources selected')
def foreign():
 index={};bodies={}
 for item in git('ls-files','--stage','-z').split(b'\0'):
  if item:
   meta,path=item.split(b'\t',1)
   if path.decode() not in paths:index.setdefault(path,[]).append(meta)
 for path in git('diff','--name-only','-z').split(b'\0'):
  if path and path.decode() not in paths:
   p=R/path.decode();bodies[path]=(p.exists(),p.read_bytes() if p.is_file() else None,stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
 return index,bodies
before=foreign();stamp=utc()
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=stamp,descending_git_checkpoint_preparing=True,descending_311_priority_percent=70,
 descending_311_workflow_percent=40,descending_checkpoint_scope='Closed independent priority audits and fresh exact controls; C1 publication judgment pending third fresh adversary.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with p.open('a') as f:
  f.write('\n'+stamp+' — PR311 priority checkpoint: both completed independent families fully body-read and sealed artifacts authenticated (115 factorization files,92 closure files); root fresh exact law and boundary-control replays passed unchanged. Exact Gandolfi–Lenarda2017 C4 priority accepted. Complete KS natural-support contraction/edge-design extension checked, explicitly an audit deduction rather than an earlier published full statement. Third fresh adversary independently derived a facial-lattice bridge before candidate access; frozen criteria, first history and bridge fully read before named release at17:10:32.826356UTC. No C1 final novelty verdict or publication clearance. Math100%, bounded priority70%, workflow40%.\n')
  f.write(stamp+' — Coordination correction: first two PR66 resume operators exited1 at17:00:42.805523 and17:01:19.854125UTC due incorrect bookkeeping-count assertions, BEFORE tracked/status/log or Git changes. Exact held body/mode checks passed. Both failed operators and actual native stderr are preserved; a new third operator proved mandatory protected-set inclusion and complete checked/live inventory, then exited0 at17:02:04.980173UTC. Native main=remote7b0175c879e989ea505f6133cc3e6d1f639b12a7,indexempty,236ascending-owned changedpaths,all8mandatory foreign trackedbody/modespreserved. This is operational ownership checking, not an audit of PR66 mathematics. Shared writes resumed; no outbound other-chat message.\n')
req(all(p.is_file() and not p.is_symlink() for p in files),'Missing selected file')
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=sha(p.read_bytes()),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files},
 math_percent=100,priority_percent=70,workflow_percent=40,publication_clearance=False,active_adversary_namespace_only_early_frozen_artifacts=True),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),('commit',['/usr/bin/git','commit','--only','-m','Checkpoint PR311 exact priority evidence and boundary derivations','--',*sorted(paths)]),('push',['/usr/bin/git','push','origin','main'])]:
 window();req(foreign()==before,'Foreign change before '+phase)
 j=dict(argv=args,cwd=str(R),started_utc=utc(),program_sha256=sha(Path(__file__).read_bytes()))
 (D/(phase+'_preexecution.json')).write_text(json.dumps(j,indent=2)+'\n');r=subprocess.run(args,cwd=R,capture_output=True)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]: (D/(phase+'.'+k)).write_bytes(b)
 j.update(ended_utc=utc(),exit_code=r.returncode,stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr));(D/(phase+'.json')).write_text(json.dumps(j,indent=2)+'\n')
 req(r.returncode==0,phase+' failed');req(foreign()==before,'Foreign change after '+phase)
head=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
req(changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head,'Scope/remote mismatch')
req(all(git('show',head+':'+rel)==(R/rel).read_bytes() for rel in paths),'Published body mismatch')
req(not git('diff','--cached','--raw','-z') and foreign()==before,'Foreign/index mismatch')
j=dict(utc=utc(),status='PASS_PR311_PRIORITY_CHECKPOINT_PUSHED',parent=parent,commit=head,changed_paths=len(changed),allowlist_paths=len(paths),
 entire_index_empty=True,remote_main_exact=True,foreign_index_body_modes_preserved=True,math_percent=100,priority_percent=70,workflow_percent=40,
 priority_complete=False,publication_ready=False,goal_complete=False,captures=str(D))
(P/(NAME+'_receipt.json')).write_text(json.dumps(j,indent=2)+'\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n');print(json.dumps(j,indent=2))
