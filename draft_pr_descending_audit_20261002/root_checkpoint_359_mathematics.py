#!/usr/bin/env python3
"""Publish owned review findings on main, preserving every foreign staged entry."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr359_30001370'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
assert json.loads((A/'ROOT_FAMILY_CLOSURE_VERIFICATION.json').read_bytes())['status']=='PASS_ALL_THREE_CLOSED_FAMILIES_PARENT_VERIFIED'
assert json.loads((A/'ROOT_SOURCE_MANIFEST_REPLAY_RECEIPT.json').read_bytes())['status']=='PASS_ALL_THREE_ORIGINAL_SOURCE_PAYLOADS_AND_SOURCE_ENABLED_REPLAY'
assert json.loads((A/'ROOT_CANDIDATE_REPLAY_RECEIPT.json').read_bytes())['status']=='PASS_COMPLETE_CANDIDATE_REPLAY'
paths=set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    rel=p.relative_to(P)
    assert not any(x=='private' or x.endswith('_private') or x.startswith('private_') or x=='__pycache__' for x in rel.parts[:-1])
    assert p.suffix not in {'.pdf','.zip','.png'}
    paths.add(str(p.relative_to(R)))
for p in A.iterdir():
    if p.is_file() and (p.suffix in {'.py','.md','.json','.txt'} or p.name=='.gitignore'):add(p)
for p in (A/'snapshot').rglob('*'):
    if p.is_file():add(p)
for family in ['algebra_certificate_review','topology_density_review','backward_feedback_review']:
    for p in (A/family/'public').rglob('*'):
        if p.is_file():add(p)
    for p in (A/family).iterdir():
        if p.is_file() and p.suffix=='.json':add(p)
for n in ['RESEARCH_LOG.md','inventory.json','STATUS_FILTER_LEDGER.json','SHARED_GIT_WINDOW_STATUS.json',
          'root_filter_next_claimed.py',Path(__file__).name,'checkpoint_364_zenodo_publication_receipt.json']:
    add(P/n)
add(P/'audits/pr364_30004048/GIT_ZENODO_PUBLICATION_READBACK.json')
allow=P/'checkpoint_359_mathematics_allowlist.json';paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc':utc(),'explicit_owned_paths':sorted(paths),'mathematical_audit_percent':100,
                            'publication_workflow_percent':45,'priority_pending':True,'preprint_pending':True,
                            'scope':'Frozen eligible PR359 mathematical evidence plus status-only skipping ledger and own PR364 accepted-publication readback. No excluded PR substantive processing or candidate promotion.'},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def window():assert not json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
assert git('branch','--show-current')==b'main\n'
assert not git('diff','--name-only','--diff-filter=U')
assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,capture_output=True).returncode!=0
def foreign():
    out={}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta,name=item.split(b'\t',1)
            if name.decode() not in paths:out.setdefault(name,[]).append(meta)
    return out
before=foreign();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','-f','--',*sorted(paths)]),
                   ('commit',['git','commit','--only','-m','Audit exact full L1 common basin boundaries with three independent mathematical families','--',*sorted(paths)]),
                   ('push',['git','push','origin','main'])]:
    window();start=utc();p=subprocess.run(args,cwd=R,capture_output=True);end=utc()
    (P/('checkpoint_359_mathematics_'+label+'.stdout')).write_bytes(p.stdout)
    (P/('checkpoint_359_mathematics_'+label+'.stderr')).write_bytes(p.stderr)
    rec={'argv':args,'cwd':str(R),'started_utc':start,'completed_utc':end,'exit_code':p.returncode,
         'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)}
    (P/('checkpoint_359_mathematics_'+label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert p.returncode==0,(label,p.stderr.decode(errors='replace'))
    assert foreign()==before,'Foreign staged entries changed.'
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
assert changed<=paths
remote=git('ls-remote','origin','refs/heads/main').decode().split()[0]
assert remote==commit
for rel in paths:
    assert git('show',commit+':'+rel)==(R/rel).read_bytes(),rel
receipt={'utc':utc(),'status':'OWNED_MATHEMATICS_CHECKPOINT_PUSHED_AND_FULL_BYTES_READ_BACK',
         'commit':commit,'parent':parent,'changed_owned_paths':len(changed),'allowlist_paths':len(paths),
         'foreign_staged_entries_preserved':True,'remote_main_exact':True,'all_allowlisted_git_disk_bytes_equal':True,
         'mathematical_audit_percent':100,'publication_workflow_percent':45,
         'priority_preprint_integration_publication_pending':True,'pr359_mutation_performed':False,
         'scope':'Only submitted claimed_solved PR359 mathematical review and own ongoing goal evidence.'}
(P/'checkpoint_359_mathematics_publication_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
