"""Bind and publish only owned, explicit evidence paths; leave the shared index alone."""
from pathlib import Path
import datetime,hashlib,json,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];R=A.parents[2];C=A/'clean_final_adversary';N=P/'audits/pr373_30004435'
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
mf=json.loads((C/'public/PUBLIC_MANIFEST.json').read_bytes())
paths=set();bindings=[]
for f in mf['files']:
    p=C/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
    assert '/private/' not in str(p) and p.suffix not in ['.pdf','.png','.txt']
    paths.add(p);bindings.append(f)
assert set(mf['explicit_public_allowlist'])=={f['path'] for f in mf['files']}|{'public/PUBLIC_MANIFEST.json'}
paths.add(C/'public/PUBLIC_MANIFEST.json')
codes=json.loads((A/'root_clean_package_reproduction_receipt.json').read_bytes())['code_sha256']
for name,digest in codes.items():assert sha((C/'public/controls'/name).read_bytes())==digest
result={'utc':stamp,'status':'PASS_ALL_FRESH_WHOLE_PUBLIC_BINDINGS','manifest_sha256':sha((C/'public/PUBLIC_MANIFEST.json').read_bytes()),'bound_members':len(bindings),'public_paths_including_manifest':len(paths),'initial_manifest_preserved_as_history':True,'root_mathematical_reproduction':'root_clean_mathematical_reproduction_receipt.json','root_complete_package_reproduction':'root_clean_package_reproduction_receipt.json','source_first_and_mathematical_seals_verified':True,'all_complete_program_streams_exact':True,'whole_prepared_gate_receipt_exact_except_observed_utc':True,'exact_live_body_ready_gate_pending':True,'actual_merge_pending':True}
(A/'root_clean_public_bindings_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
c=json.loads((A/'acceptance_criteria.json').read_text());c.update(workflow_percent=97,fresh_whole_package_review_pending=False,root_fresh_whole_package_reproduction_pending=False,root_whole_public_bindings='root_clean_public_bindings_receipt.json',fresh_whole_manifest_sha256=result['manifest_sha256'],fresh_whole_verdict='PASS_SCOPED_UNSOLVED5/5',exact_live_body_ready_gate_pending=True)
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
(A/'ACCEPTANCE_DECISION.md').write_text(f'''# PR374 proposed acceptance decision

{stamp}: audit workflow97%; unrestricted discovery0%. Accept as unsolved5/5 partial findings only, subject to the final exact live-body/ready/current-main gate and actual merge verification. Root reconstructed all five universal scoped proofs directly and reproduced the original package, three independent mechanism families, and a fresh source-first whole-package adversary. No mandatory mathematical correction remains. No unrestricted profile, novelty, human peer review, or formal proof-assistant certification is claimed.

The all-part multipartite optimum, qualified join replacement and credited triangle-minimizer consequence, qualified L-infinity stability with explicit L1 ties, all weighted-cograph and cograph-sequence limits, and complete measurable rank-one profile are supported. Arbitrary positive-triangle-excess hosts outside these families remain uncontrolled. No paper, Zenodo upload, DOI, tracker row or release is appropriate.

Fresh whole-review manifest SHA256 `{result['manifest_sha256']}` binds {result['bound_members']} members. Root independently reran four new mathematical controls and the entire eight-program publication packet; every full stdout/stderr and mathematical JSON agrees. Root also reran the unchanged prepared gate; its entire receipt matches except its declared observation UTC. All immutable original/refreshed Git/API blobs, historical scopes, five fresh primary PDF inputs, literal queue delta and all-other-main-path preservation pass. Prepared and observed PR bodies remain distinct historical observations; live acceptance and merge are not yet certified.

Refreshed head26df33899c95d860403ab311c568e0328bc87eeb preserves all45 target bytes. Only queue line411/rank400 cells8 and9 change queued0/5 to unsolved5/5. Final metadata mutation must use the exact prepared body and unchanged gate code, with all other shared-main work preserved.
''')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n{stamp}: workflow97%, unrestricted discovery0%. Fresh independent whole-package scoped PASS; root read full report/programs and reproduced four new mathematical controls, all eight packet programs and the unchanged prepared Git/API/body/queue/current-main gate. Entire receipts agree outside only declared timing fields. All {len(bindings)} public manifest members exact. Publish prepared acceptance evidence before sending exact body/ready; final live gate and actual merge remain pending.\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n{stamp}: PR374 audit97%, original discovery0%; all scoped proofs, full original/three-family/fresh-whole replays and prepared merge preservation pass. Acceptance metadata and actual merge pending. Descending14/{len(json.loads((P/"inventory.json").read_text())["items"])} complete. PR373 frozen/source-fetch prep only.\n')
top=['root_clean_mathematical_reproduction.py','root_clean_mathematical_reproduction_receipt.json','root_clean_package_reproduction.py','root_clean_package_reproduction_receipt.json','root_clean_public_bindings_receipt.json','root_prepare_acceptance_checkpoint.py','root_bibliographic_verification.json','acceptance_criteria.json','ACCEPTANCE_DECISION.md','RESEARCH_LOG.md']
paths.update(A/name for name in top)
for directory,names in [('root_clean_math_streams',['source_first_counts','fresh_symbolic','fresh_adversarial','fresh_moments']),('root_clean_package_streams',['package_replay','final_gate_prepared','author_turn1','author_turn2','author_turn3','author_turn4','author_turn5','historical_author_replay','historical_independent','portable_publication'])]:
    paths.update(A/directory/(name+'.'+suffix) for name in names for suffix in ['stdout','stderr'])
for name in ['snapshot_manifest.json','remote_original.json','README.md','RESEARCH_LOG.md','root_fetch_primary.py','root_primary_source_receipt.json','root_freeze_cli_limitation.json']:
    paths.add(N/name)
nmanifest=json.loads((N/'snapshot_manifest.json').read_bytes())
for f in nmanifest['files']:
    p=N/'snapshot'/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'];paths.add(p)
for name in ['freeze_metadata','freeze_files','freeze_fetch']:
    paths.update(N/(name+'.'+suffix) for suffix in ['stdout','stderr'])
for name in ['owr_2020_11.pdf','alnajjar_shmaya_2014.pdf','lemanczyk_thesis.pdf','bressaud_fernandez_galves_1999.pdf']:
    paths.update(N/('root_'+name+'.'+step+'.'+suffix) for step in ['download','extract'] for suffix in ['stdout','stderr'])
paths.update([P/'root_freeze_pr.py',P/'RESEARCH_LOG.md'])
for p in paths:assert p.is_file() and p.is_relative_to(P) and '/private/' not in str(p) and '/raw_sources/' not in str(p) and '/tmp/' not in str(p)
allow=A/'root_prepared_checkpoint_allowlist.json';paths.add(allow)
relative=sorted(str(p.relative_to(R)) for p in paths)
allow.write_text(json.dumps({'utc':stamp,'explicit_owned_paths':relative,'path_count':len(relative),'foreign_index_preserved':True,'no_raw_primary_PDF_text_or_render_paths':True},indent=2)+'\n')
def command(label,args):
    r=subprocess.run(args,cwd=R,capture_output=True)
    (A/('root_prepared_checkpoint_'+label+'.stdout')).write_bytes(r.stdout);(A/('root_prepared_checkpoint_'+label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0,(label,r.stderr.decode());return r.stdout
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
before=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0'))-{''}
foreign=before-set(relative)
command('stage',['git','add','--',*relative])
command('commit',['git','commit','--only','-m','Checkpoint PR374 full independent partial-result audit and freeze PR373', '--',*relative])
after=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).decode().split('\0'))-{''}
assert after==foreign,(after-foreign,foreign-after)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert set(subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],cwd=R).decode().splitlines())<=set(relative)
command('push',['git','push','origin','main'])
print(json.dumps({'status':'PASS_PREPARED_CHECKPOINT_PUBLISHED','commit':commit,'paths':len(relative),'whole_manifest_sha256':result['manifest_sha256'],'foreign_staged_paths_preserved':len(foreign)}))
