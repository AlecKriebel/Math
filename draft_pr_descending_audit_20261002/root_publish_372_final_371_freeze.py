"""Publish only explicitly owned final PR372 and initial PR371 audit artifacts."""
from pathlib import Path
import datetime,hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parent;A=P/'audits/pr372_9700034';N=P/'audits/pr371_30006025';paths=set()
def sha(b):return hashlib.sha256(b).hexdigest()
def add(f):
    f=f.resolve();assert f.is_relative_to(P) and f.is_file()
    assert not any(x in f.parts for x in ['tmp','raw_sources','private_api','private_git','private_live','private_sources','private_replay','__pycache__'])
    assert f.suffix not in ['.pdf','.png','.jpg','.html'];paths.add(str(f.relative_to(R)))
for name in ['DECISION.md','ACCEPTANCE_DECISION.md','acceptance_criteria.json','accepted_pr_body.txt','merge_body.txt','queue_repair_receipt.json','repaired_snapshot_manifest.json','ACTUAL_MERGE_VERIFICATION.json','virtual_integration_receipt.json','root_clean_historical_full_receipt.json','root_clean_historical_comparison.json','root_compare_live_receipts.py','root_exact_live_full_receipt.json','root_live_full_comparison_receipt.json','root_live_full_difference_inventory.json','root_live_raw_pr_difference_inventory.json','root_final_review_manifest_verification.json','root_merge_helper_guard_addendum.json','README.md','RESEARCH_LOG.md']:
    add(A/name)
for manifest,root in [(A/'repaired_snapshot_manifest.json',A/'repaired_snapshot'),(A/'clean_final_adversary/PUBLIC_MANIFEST.json',A/'clean_final_adversary'),(A/'clean_final_adversary/final_live/PUBLIC_MANIFEST.json',A/'clean_final_adversary'),(A/'clean_final_adversary/post_merge/PUBLIC_MANIFEST.json',A/'clean_final_adversary'),(N/'snapshot_manifest.json',N/'snapshot')]:
    add(manifest)
    for e in json.loads(manifest.read_bytes())['files']:
        f=root/e['path'];b=f.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];add(f)
for name in ['README.md','RESEARCH_LOG.md','.gitignore','root_primary_fetch_receipt.json','root_primary_render_receipt.json','bgl2025-published_fresh_receipt.json','philippe2008-journal_fresh_receipt.json']:
    add(N/name)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (P/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n{now}: Publish final PR372 audit100%, actual merge329e7303d4616ebcf060a3c8731bd62ed1fa339a; root and fresh whole final/actual-merge checks pass with all sealed proofs and46? No:48 target files preserved. Original general discovery0%;17/349=4.8711% descending acceptance. PR371 immutable47paths/46target freeze and fresh primary metadata published at source-first audit15%; original resolution0%. No papers/DOIs/releases. All foreign index entries preserved.\n'.replace('46? No:48','48'))
for name in ['RESEARCH_LOG.md','inventory.json','root_integrate_reviewed_pr.py',Path(__file__).name]:add(P/name)
report=P/'checkpoint_372_final_371_freeze_public_allowlist.json';paths.add(str(report.relative_to(R)))
report.write_text(json.dumps({'utc':now,'checkpoint':'PR372 accepted final audit100%; PR371 frozen source-first15%','explicit_owned_paths':sorted(paths),'exclusions':'All unlisted foreign paths, source PDFs/text/renders, raw API/Git and private execution copies','program_completed':17,'program_total':349,'original_discovery_percent':0},indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def indexmap():
    out={}
    for x in git('ls-files','--stage','-z').split(b'\0'):
        if x:
            meta,path=x.split(b'\t',1);out.setdefault(path,[]).append(meta)
    return out
assert git('branch','--show-current').strip()==b'main';initial=indexmap();foreign={k:v for k,v in initial.items() if k.decode() not in paths};parent=git('rev-parse','HEAD').decode().strip()
for label,args in [('stage',['git','add','--',*sorted(paths)]),('commit',['git','commit','--only','-m','Publish accepted PR372 audit and freeze PR371 source-first review','--',*sorted(paths)])]:
    r=subprocess.run(args,cwd=R,capture_output=True);(P/f'checkpoint_372_final_371_freeze_{label}.stdout').write_bytes(r.stdout);(P/f'checkpoint_372_final_371_freeze_{label}.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr
commit=git('rev-parse','HEAD').decode().strip();changed=set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines());assert changed<=paths
assert {k:v for k,v in indexmap().items() if k.decode() not in paths}==foreign,'foreign index changed'
r=subprocess.run(['git','push','origin','main'],cwd=R,capture_output=True);(P/'checkpoint_372_final_371_freeze_push.stdout').write_bytes(r.stdout);(P/'checkpoint_372_final_371_freeze_push.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr
print(json.dumps({'status':'PUBLISHED_EXPLICIT_OWN_FINAL_372_INITIAL_371','commit':commit,'parent':parent,'changed_owned_paths':len(changed),'foreign_index_unchanged':True,'completed':17,'total':349}))
