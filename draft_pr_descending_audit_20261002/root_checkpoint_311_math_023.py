"""Publish completed mathematics and source-first priority gates, preserving other work."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,stat
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303';NAME='checkpoint_311_math_023'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def req(c,label):
    if not c:raise RuntimeError(label)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Shared window paused')
window();req(not (P/(NAME+'_receipt.json')).exists(),'Checkpoint exists')
req(git('branch','--show-current')==b'main\n','Not main');req(not git('diff','--cached','--raw','-z'),'Index nonempty')
parent=git('rev-parse','HEAD').decode().strip();req(git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Remote differs')
accept=load(A/'ROOT_MATHEMATICAL_ACCEPTANCE.json');req(accept['status']=='PASS_BOTH_EXACT_SOURCE_MATHEMATICAL_ANSWERS_ACCEPTED','Math not accepted')
req(accept['original_head']=='895f2ba037e71bac054b58f1a4be7bb4d5dbd53a' and not accept['publication_ready'],'Wrong source or premature clearance')
owned=[P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json','checkpoint_311_initial_022_receipt.json',Path(__file__).name]]
owned += [A/n for n in ['.gitignore','README.md','RESEARCH_LOG.md','PRIORITY_AUDIT_PLAN.md','ROOT_MATHEMATICAL_ACCEPTANCE.md','ROOT_MATHEMATICAL_ACCEPTANCE.json',
    'ROOT_MARKOV_FINAL_ARTIFACT_AUTHENTICATION.json','ROOT_LATTICE_FINAL_ARTIFACT_AUTHENTICATION.json',
    'root_validate_markov_final.py','root_validate_lattice_final.py','root_accept_mathematics.py',
    'ROOT_PRIORITY_SOURCE_GATE.json','root_release_priority_candidates.py','ROOT_PRIORITY_SOURCE_RETRIEVAL.json','root_fetch_priority_sources.py',
    'ROOT_PRIORITY_FOLLOWUP_RETRIEVAL.json','root_fetch_priority_followups.py','ROOT_PRIORITY_CITATION_CHAIN_RETRIEVAL.json','root_fetch_priority_citation_chains.py']]
for family in ['markov_closure','lattice_factorization']:
    F=A/family;mf=load(F/'FINAL_AUDIT_MANIFEST.json');auth=load(A/('ROOT_'+('MARKOV' if family=='markov_closure' else 'LATTICE')+'_FINAL_ARTIFACT_AUTHENTICATION.json'))
    for rel,expected in auth['final_pins'].items():req(sha((F/rel).read_bytes())==expected,'Changed final '+rel)
    for item in mf.get('artifacts',mf.get('files',[])):
        if item.get('local_source_verification_only'):continue
        p=F/item['relative_path'];req(sha(p.read_bytes())==item['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Changed sealed member')
        owned.append(p)
    owned += [F/'FINAL_AUDIT_MANIFEST.json',F/'FINAL_SEAL_RECEIPT.json']
    if family=='markov_closure':owned.append(F/'FINAL_AUDIT_MANIFEST.sha256')
owned += [A/'priority_factorization'/n for n in ['.gitignore','source_only_comparison_criteria.md','source_only_checkpoint.json','source_only_freeze_manifest.json']]
owned += [A/'priority_closure'/n for n in ['.gitignore','SOURCE_ONLY_COMPARISON_CRITERIA.md','SOURCE_ONLY_FREEZE_SEAL.json']]
req(all(p.is_file() and not p.is_symlink() for p in owned),'Missing selected file')
req(not any(p.suffix in {'.pdf','.png','.bin'} or '_private' in str(p.relative_to(P)) for p in owned),'Private source selected')
stamp=utc()
(A/'README.md').write_text('''# Descending audit: PR311 / 30005303

The original submitted head895f2ba037e71bac054b58f1a4be7bb4d5dbd53a is claimed_solved, author2/5. Its original30 objects and four manifests are authenticated and preserved. The exact source asks two finite binary graphical-model questions; its separate Gaussian conjecture is outside this entry.

Root and both fresh source-first mathematical families have accepted the two answers: finite edge-factor closure under MTP2, and a global-Markov MTP2 C4 counterexample to clique factorization (also refuting the stronger lattice-support statement). Root read and authenticated the complete proofs, code, input bindings, sealed final reports and execution streams. All564189 author and89324 inherited assertions and three fresh independent control programs reproduced byte-identically. The fresh lattice family also supplied a separate support/log-design closure proof. Its later extra summary exposure is disclosed and excluded from evidence; its initial verdict and controls were frozen first.

This accepts mathematical correctness only. Two new independent primary-source priority families are active. Each froze source-only comparison criteria before candidate access; the factorization family also froze its first historical finding independently. Root fully read and authenticated both criteria before a named release of candidate prose. Potential qualifying prior counterexamples are under comparison. No priority verdict or publication clearance is granted by this checkpoint. Primary copyrighted PDFs, text, page images and private native captures are excluded from publication.

Best estimates: mathematics100%, workflow35%, historical-priority audit20%. No merge, paper, Zenodo upload, DOI, tracker row or GitHub release for PR311. The persistent goal remains active. The current goal processes only originally submitted claimed_solved draft PRs in descending order, excluding PR8; other statuses are skipped by status alone. No outside individual was contacted.
''')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=stamp,descending_active_pr=311,descending_311_mathematical_verification_percent=100,
    descending_311_mathematical_verification_complete=True,descending_311_workflow_percent=35,descending_311_priority_percent=20,
    descending_311_priority_complete=False,descending_311_preprint_ready=False,descending_git_checkpoint_preparing=True,
    descending_checkpoint_scope='PR311 complete accepted mathematics and frozen source-first priority criteria; historical verdict/publication pending.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
inv=load(P/'inventory.json');item=next(x for x in inv['items'] if x['number']==311)
item.update(audit_workflow_percent=35,mathematical_verification_percent=100,mathematical_acceptance=True,
    priority_acceptance=False,priority_audit_percent=20,original_submitted_status='claimed_solved',original_author_turns='2/5',
    publication_ready=False,disposition='mathematics_accepted_fresh_source_first_priority_audit_active')
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=stamp+' — PR311 mathematical checkpoint: both complete fresh families closed, all proofs/code/manifests/native streams read and authenticated; exact two source answers accepted. New independent priority criteria fully root-read before named candidate release. Potential qualifying prior witnesses being checked, no historical verdict. Math100%, workflow35%, priority20%; original author2/5 untouched, no publication/merge.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write('\n'+entry)
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in owned}|{str(allow.relative_to(R))}
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
before=foreign();pins={rel:dict(bytes=(R/rel).stat().st_size,sha256=sha((R/rel).read_bytes())) for rel in sorted(paths) if rel!=str(allow.relative_to(R))}
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins=pins,math_percent=100,workflow_percent=35,
    priority_percent=20,mathematical_acceptance=True,priority_clearance=False,publication_ready=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),
    ('commit',['/usr/bin/git','commit','--only','-m','Accept PR311 mathematics and checkpoint independent priority intake','--',*sorted(paths)]),
    ('push',['/usr/bin/git','push','origin','main'])]:
    window();req(foreign()==before,'Foreign state changed before '+phase)
    spec=dict(argv=args,cwd=str(R),started_utc=utc(),operator_sha256=sha(Path(__file__).read_bytes()))
    (P/(NAME+'_'+phase+'_preexecution.json')).write_text(json.dumps(spec,indent=2)+'\n')
    run=subprocess.run(args,cwd=R,capture_output=True)
    for k,b in [('stdout',run.stdout),('stderr',run.stderr)]: (P/(NAME+'_'+phase+'.'+k)).write_bytes(b)
    spec.update(ended_utc=utc(),exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr))
    (P/(NAME+'_'+phase+'.json')).write_text(json.dumps(spec,indent=2)+'\n')
    req(run.returncode==0,phase+' failed');req(foreign()==before,'Foreign state changed after '+phase)
head=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
req(changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head,'Scope/remote mismatch')
req(all(git('show',head+':'+rel)==(R/rel).read_bytes() for rel in paths),'Published bytes differ')
req(foreign()==before and not git('diff','--cached','--raw','-z'),'Final foreign/index mismatch')
receipt=dict(utc=utc(),status='PASS_PR311_MATHEMATICAL_ACCEPTANCE_CHECKPOINT_PUSHED',parent=parent,commit=head,
    allowlist_paths=len(paths),changed_paths=len(changed),remote_main_exact=True,index_empty=True,foreign_index_and_body_modes_preserved=True,
    math_percent=100,workflow_percent=35,priority_percent=20,mathematical_acceptance=True,priority_clearance=False,publication_ready=False,goal_complete=False)
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR311 mathematics checkpoint pushed '+head+'; exact remote/owned bytes and empty index verified; foreign work preserved. Math100%, workflow35%, priority20%; goal active.\n')
print(json.dumps(receipt,indent=2))
