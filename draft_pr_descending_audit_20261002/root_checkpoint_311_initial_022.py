"""Publish an explicitly scoped provisional mathematical checkpoint on main."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr311_30005303'
NAME='checkpoint_311_initial_022'
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def req(c,label):
    if not c:raise RuntimeError(label)
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def window():req(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],'Shared window paused')
window();req(not (P/(NAME+'_receipt.json')).exists(),'Already checkpointed')
req(git('branch','--show-current')==b'main\n','Not main')
req(not git('diff','--cached','--raw','-z'),'Index not empty')
parent=git('rev-parse','HEAD').decode().strip()
req(git('ls-remote','origin','refs/heads/main').decode().split()[0]==parent,'Remote differs')
original=load(A/'snapshot_manifest.json')
req(original['head']=='895f2ba037e71bac054b58f1a4be7bb4d5dbd53a' and len(original['files'])==30,'Source snapshot mismatch')
replay=load(A/'ROOT_INDEPENDENT_CONTROL_REPLAYS.json')
req(replay['status']=='PASS_THREE_SOURCE_FIRST_INDEPENDENT_CONTROLS_REPRODUCED_BYTE_IDENTICALLY','Independent reproduction missing')
stamp=utc()
(A/'README.md').write_text('''# Provisional descending audit: PR311 / 30005303

Original submitted head895f2ba037e71bac054b58f1a4be7bb4d5dbd53a is claimed_solved, author2/5. The source asks two finite binary graphical-model questions: closure of MTP2 edge-factorizing laws, and clique factorization of all global-Markov MTP2 laws. The separate Gaussian conjecture is outside this entry. Original30 Git/API/disk objects and four manifests agree. Original EMS pages3125–3127 were visually read; primary copyrighted files remain private.

Root analytical review provisionally finds a valid C4 counterexample to the second conjecture and a finite real max-flow/residual-factor compactness proof of the first. Two independent source-first families froze their own criteria and separate controls before reading candidate prose; both first assessments pass. Their final author-code consistency reports remain pending. A later extra summary read by the lattice reviewer is transparently disclosed, after its independent first verdict and controls were frozen; inherited aggregate claims are excluded from its evidence.

Root reproduced all564189 author assertions and89324 inherited assertions byte-identically. Three independently designed source/prose programs also reproduce exactly, including C6 global independence, support reconstruction, equality aggregation, isolated/empty cases, normalization bounds and ordinary non-MTP2 closure countercontrols. Exact finite checks supplement analytical proofs. Evidence and contemporaneous actual command-stream hashes are recorded in the bound receipts.

Mathematical audit estimate70%, workflow25%; mathematical acceptance, priority audit and publication clearance remain pending. No merge, preprint, Zenodo record, DOI, tracker row or GitHub release. The overall persistent goal remains active. Only submitted claimed_solved draft PRs are processed; PR315–312 were skipped by status alone, and PR8 is excluded. No outside individual was contacted.
''')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp,descending_active_pr=311,descending_311_mathematical_verification_percent=70,
    descending_311_workflow_percent=25,descending_311_priority_complete=False,descending_311_preprint_ready=False,
    descending_git_checkpoint_preparing=True,descending_checkpoint_scope='PR311 source/proof/provisional independent review and unchanged exact replays only; no mathematical/priority/publication acceptance.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
inv=load(P/'inventory.json');item=next(x for x in inv['items'] if x['number']==311)
item.update(audit_started_utc='2026-10-04T15:48:28.224387+00:00',audit_workflow_percent=25,
    mathematical_verification_percent=70,mathematical_acceptance=False,priority_acceptance=False,
    original_submitted_status='claimed_solved',original_author_turns='2/5',publication_ready=False,
    disposition='source_and_proof_provisional_pass_final_fresh_consistency_reviews_pending')
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=stamp+' — PR311 provisional checkpoint: exact original30 paths, source-first root/two-family criteria, both independent first verdicts, complete root proofs and unchanged author/inherited/three fresh exact replays. Math70%, workflow25%, priority0%; no acceptance/promotion. Original author2/5 preserved. Shared ascending integration release independently verified; only owned audit/status files published.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write('\n'+entry)
owned=[P/n for n in ['CURRENT_SCOPE.json','RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','STATUS_FILTER_LEDGER.json','inventory.json',
    'checkpoint_316_disposition_021_receipt.json','root_resume_pr65_attributed_20261004.py',Path(__file__).name]]
owned += [A/n for n in ['README.md','RESEARCH_LOG.md','root_source_intake.py','root_source_intake_recovery.py',
    'root_run.py','root_authenticate_initial_inputs.py','root_family_first_gate_and_replay.py','snapshot_manifest.json',
    'ROOT_SOURCE_INTAKE.json','ROOT_SOURCE_CRITERIA.md','ROOT_SOURCE_CRITERIA_FREEZE.json','ROOT_FAMILY_SOURCE_GATE.json',
    'ROOT_FAMILY_FIRST_CANDIDATE_GATE.json','ROOT_PROOF_AUDIT.md','ROOT_PROOF_AUDIT_CHECKPOINT.json',
    'ROOT_INITIAL_INPUT_BINDINGS.json','ROOT_INDEPENDENT_CONTROL_REPLAYS.json']]
owned += [A/'snapshot'/x['path'] for x in original['files']]
for family in ['lattice_factorization','markov_closure']:
    owned += [A/family/n for n in ['INDEPENDENT_SOURCE_CRITERIA.md','INDEPENDENT_SOURCE_CRITERIA.sha256',
        'FIRST_CANDIDATE_ASSESSMENT.md','FIRST_CANDIDATE_ASSESSMENT.sha256']]
owned += [A/'lattice_factorization'/n for n in ['source_control_exact.py','source_control_result.json','prose_controls_exact.py','prose_controls_result.json']]
owned += [A/'markov_closure'/n for n in ['independent_controls.py','INDEPENDENT_CONTROLS_RESULT.json']]
req(all(p.is_file() and not p.is_symlink() for p in owned),'Owned file missing')
req(not any(p.suffix in {'.pdf','.png','.bin'} or 'private' in str(p.relative_to(P)) for p in owned),'Private binary selected')
allow=P/(NAME+'_allowlist.json');paths={str(p.relative_to(R)) for p in owned}|{str(allow.relative_to(R))}
def foreign():
    index={};bodies={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,path=item.split(b'\t',1)
            if path.decode() not in paths:index.setdefault(path,[]).append(meta)
    for path in git('diff','--name-only','-z').split(b'\0'):
        if path and path.decode() not in paths:
            p=R/path.decode();bodies[path]=(p.exists(),p.read_bytes() if p.is_file() else None,p.stat().st_mode&0o7777 if p.exists() else None)
    return index,bodies
before=foreign()
pins={rel:dict(bytes=(R/rel).stat().st_size,sha256=sha((R/rel).read_bytes())) for rel in sorted(paths) if rel!=str(allow.relative_to(R))}
allow.write_text(json.dumps(dict(utc=utc(),paths=sorted(paths),pins=pins,math_percent=70,workflow_percent=25,
    mathematical_acceptance=False,priority_clearance=False,publication_ready=False),indent=2)+'\n')
for phase,args in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),
    ('commit',['/usr/bin/git','commit','--only','-m','Checkpoint PR311 source-first mathematical audit and independent exact controls','--',*sorted(paths)]),
    ('push',['/usr/bin/git','push','origin','main'])]:
    window();req(foreign()==before,'Foreign state changed before '+phase)
    spec=dict(argv=args,cwd=str(R),started_utc=utc(),operator_sha256=sha(Path(__file__).read_bytes()))
    (P/(NAME+'_'+phase+'_preexecution.json')).write_text(json.dumps(spec,indent=2)+'\n')
    run=subprocess.run(args,cwd=R,capture_output=True)
    for k,b in [('stdout',run.stdout),('stderr',run.stderr)]: (P/(NAME+'_'+phase+'.'+k)).write_bytes(b)
    spec.update(ended_utc=utc(),exit_code=run.returncode,stdout_sha256=sha(run.stdout),stderr_sha256=sha(run.stderr))
    (P/(NAME+'_'+phase+'.json')).write_text(json.dumps(spec,indent=2)+'\n')
    req(run.returncode==0,phase+' failed');req(foreign()==before,'Foreign state changed after '+phase)
head=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines())
req(changed<=paths and git('ls-remote','origin','refs/heads/main').decode().split()[0]==head,'Checkpoint scope/remote mismatch')
req(all(git('show',head+':'+rel)==(R/rel).read_bytes() for rel in paths),'Published body mismatch')
req(foreign()==before and not git('diff','--cached','--raw','-z'),'Final foreign/index mismatch')
receipt=dict(utc=utc(),status='PASS_PR311_PROVISIONAL_CHECKPOINT_PUSHED',parent=parent,commit=head,allowlist_paths=len(paths),
    changed_paths=len(changed),remote_main_exact=True,index_empty=True,foreign_index_and_body_modes_preserved=True,
    math_percent=70,workflow_percent=25,priority_percent=0,mathematical_acceptance=False,publication_ready=False,goal_complete=False)
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=head,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — PR311 provisional checkpoint pushed '+head+'; exact remote/owned bytes and empty index verified, foreign work preserved. Math70%, workflow25%; goal active.\n')
print(json.dumps(receipt,indent=2))
