"""Publish only owned PR371 final/readback and PR370 frozen source/proof baseline."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr371_30006025';B=P/'audits/pr370_30004811';paths=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def add(f):
    f=f.resolve();assert f.is_relative_to(P) and f.is_file() and not f.is_symlink()
    assert not {'tmp','private','raw_sources','private_sources','private_replays','__pycache__'}.intersection(f.parts)
    assert f.suffix not in ('.pdf','.png','.jpg','.html')
    paths.add(f.relative_to(R).as_posix())
def manifest(root):
    m=json.loads((root/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
    for e in m['files']:
        p=PurePosixPath(e['path']);assert not p.is_absolute() and '..' not in p.parts and e['path']!='PUBLIC_MANIFEST.json' and e['path'] not in seen;seen.add(e['path'])
        raw=(root/e['path']).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob_sha1'];add(root/e['path'])
    add(root/'PUBLIC_MANIFEST.json');return len(seen)
assert manifest(A/'clean_final_adversary/final_live')==10
assert manifest(A/'clean_final_adversary/post_merge')==7
comparison=json.loads((A/'root_postmerge_comparison.json').read_bytes());assert comparison['status']=='PASS' and comparison['root_checks']==30
actual=json.loads((A/'ACTUAL_MERGE_VERIFICATION.json').read_bytes());assert actual['actual_merge']=='6466f4a301c94d513435401bf772c285bc7b4c42' and actual['workflow_percent']==100
for root in [A,A/'queue_refresh_history/137d5e30efe05bb5f68a5b0bcc4e37480c8a9493']:
    m=json.loads((root/'repaired_snapshot_manifest.json').read_bytes());assert len(m['files'])==47
    for e in m['files']:
        raw=(root/'repaired_snapshot'/e['path']).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'];add(root/'repaired_snapshot'/e['path'])
    for name in ['repaired_snapshot_manifest.json','queue_repair_receipt.json','root_exact_live_receipt.json']:add(root/name)
frozen=json.loads((B/'snapshot_manifest.json').read_bytes());assert frozen['head']=='567c2e493854b32d0cd325ad96e4c5b69c9c1e1b' and len(frozen['files'])==19
for e in frozen['files']:
    raw=(B/'snapshot'/e['path']).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob_sha'];add(B/'snapshot'/e['path'])
source=json.loads((B/'root_source_first_seal.json').read_bytes());math=json.loads((B/'root_mathematical_reconstruction_seal.json').read_bytes())
assert source['sha256']==sha((B/'ROOT_SOURCE_FIRST_BASELINE.md').read_bytes()) and math['math_sha256']==sha((B/'ROOT_MATHEMATICAL_RECONSTRUCTION.md').read_bytes()) and source['utc']<math['utc']
assert source['brief_sibling_findings_exposed_before_seal'] and not source['full_root_independence_from_sibling_findings_claimed']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
criteria=json.loads((A/'acceptance_criteria.json').read_bytes());criteria.update(workflow_completion_percent=100,workflow_percent=100,postmerge_independent_checks=30,postmerge_root_replay_checks=30,postmerge_complete_receipts_equal_except_validated_runtime_leaves=True,postmerge_review_pending=False)
(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_bytes());item=next(x for x in inv['items'] if x['number']==371);item.update(audit_completion_percent=100,audit_workflow_percent=100,audit_disposition='ACCEPTED_ACTUAL_MERGE_AND_POSTMERGE_VERIFIED',general_discovery_completion_percent=0,postmerge_independent_checks=30)
next(x for x in inv['items'] if x['number']==370).update(audit_completion_percent=45,audit_workflow_percent=45,audit_disposition='PRIMARY_SOURCE_AND_UNIVERSAL_MATH_PASS_REPRODUCTION_PENDING',root_brief_sibling_exposure_disclosed=True)
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=f'\n{now}: PR371 final acceptance100% at actual6466f4a; root1829 and freshwhole42 exact-live checks, then independent30 and root30 actual readback checks. Complete receipts agree except five validated runtime leaves. All46 original mathematical targets and113 manifest bindings preserved, wholequeue onlyowncells8/9. Original Question4 resolution0%, unsolved5/5; no paper/Zenodo/DOI/tracker/release. Program18/349=5.1576%. PR370 original19-file freeze plus seven matching source PDF identities and root universal proof45% published. Earlier brief sibling exposure disclosed; root full-independence claim not made.\n'
for f in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'README.md']:
    with f.open('a') as h:h.write(entry)
with (A/'DECISION.md').open('a') as h:h.write('\n## Actual final acceptance\n\n'+entry.strip()+'\n')
for name in ['root_exact_live_gate.py','root_prepare_live.py','root_clean_final_exact_live.json','root_compare_final_live.py','root_final_live_comparison.json','root_compare_postmerge.py','root_postmerge_independent_receipt.json','root_postmerge_comparison.json','virtual_integration_receipt.json','ACTUAL_MERGE_VERIFICATION.json','ACCEPTANCE_DECISION.md','DECISION.md','README.md','RESEARCH_LOG.md','acceptance_criteria.json']:add(A/name)
for name in ['.gitignore','remote_original.json','snapshot_manifest.json','README.md','RESEARCH_LOG.md','root_fetch_primary.py','root_primary_fetch_receipt.json','ROOT_SOURCE_FIRST_BASELINE.md','root_source_first_seal.json','ROOT_MATHEMATICAL_RECONSTRUCTION.md','root_mathematical_reconstruction_seal.json']:add(B/name)
for name in ['root_refresh_queue.py','inventory.json','RESEARCH_LOG.md',Path(__file__).name]:add(P/name)
allow=P/'checkpoint_371_final_370_baseline_public_allowlist.json';paths.add(allow.relative_to(R).as_posix());allow.write_text(json.dumps({'utc':now,'explicit_owned_paths':sorted(paths),'completed_prs':18,'initial_drafts':349,'exclusions':'Every unlisted path, primary source copy, private replay/API and foreign index entry'},indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def foreign_index():
    out={}
    for row in git('ls-files','--stage','-z').split(b'\0'):
        if row:
            meta,path=row.split(b'\t',1)
            if path.decode() not in paths:out.setdefault(path,[]).append(meta)
    return out
assert git('branch','--show-current').strip()==b'main';foreign=foreign_index();parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish actual PR371 acceptance and PR370 source-first baseline','--',*sorted(paths)]),('push',['git','push','origin','main'])]:
    r=subprocess.run(args,cwd=R,capture_output=True);(P/('checkpoint_371_final_370_baseline_'+label+'.stdout')).write_bytes(r.stdout);(P/('checkpoint_371_final_370_baseline_'+label+'.stderr')).write_bytes(r.stderr);assert r.returncode==0,(label,r.stderr)
    assert foreign_index()==foreign,'foreign index changed'
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
print(json.dumps({'status':'PUBLISHED_371_FINAL_370_BASELINE','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_preserved':True},indent=2))
