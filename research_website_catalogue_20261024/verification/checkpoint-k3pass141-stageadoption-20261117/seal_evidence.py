"""Seal captured own checkpoint evidence only; no Git/network/project execution.
No reads outside this owned lane, no current programme or website comparisons.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/checkpoint-k3pass141-stageadoption-20261117')
PARENT='736c42d516805462cec410ce5ae8366962e38bbe'
COMMIT='15482acd0ef864af280a864758b2ac6aa24dfbe8'
TREE='a775ea5bf0249071756d7142dc11ab1380836cd7'
PREFIX='research_website_catalogue_20261024/'
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(rows):
 d={}
 for k,v in rows:
  assert k not in d
  d[k]=v
 return d
def readj(name): return json.loads((OWN/name).read_bytes(),object_pairs_hook=pairs)
def pin(name):
 p=OWN/name; st=p.lstat(); assert stat.S_ISREG(st.st_mode) and not p.is_symlink()
 b=p.read_bytes(); return dict(bytes=len(b),SHA256=sha(b),mode=format(stat.S_IMODE(st.st_mode),'04o'))
def writej(name,data):
 with (OWN/name).open('x',encoding='utf-8') as f: f.write(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
before,after=readj('GUARDS_BEFORE.json'),readj('GUARDS_AFTER.json')
assert before['repositories']==after['repositories'] and before['public']==after['public']
dry,post=readj('DRY_V2_TREE_AUDIT.json'),readj('POST_V2_TREE_AUDIT.json')
dr,pr=readj('DRY_RUN.receipt.json'),readj('PUSH.receipt.json')
di,pi=readj('DRY_RUN.invocation.json'),readj('PUSH.invocation.json')
assert dr['parent']==pr['parent']==PARENT and pr['commit']==post['commit']==COMMIT and pr['tree']==post['tree']==TREE
assert di['exit_code']==pi['exit_code']==0 and di['helper_unchanged'] and pi['helper_unchanged']
assert di['helper']['SHA256']==pi['helper']['SHA256']==before['helper']['SHA256']==after['helper']['SHA256']=='405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0'
assert dry['changed_paths']==293 and dry['status_counts']=={'M':2,'A':291}
assert post['changed_paths']==294 and post['status_counts']=={'M':3,'A':291}
assert post['fresh_remote_main'].split()[0]==COMMIT
assert dry['sibling_root_entries_preserved']==post['sibling_root_entries_preserved']==159
assert dry['old_root_entries']==post['old_root_entries'] and dry['docs_entry']==post['docs_entry']
assert post['excluded_subtree_leaves_exact_at_parent'] and len(post['excluded_paths'])==3
assert not any(x.startswith('papers/') for x in post['excluded_paths'])
assert all(x['current_file_whole_bytes_equal'] and not x['known_helper_receipt_drift'] for x in post['all_changed_blob_whole_bytes_verified'])
assert len(post['all_changed_blob_whole_bytes_verified'])==294
assert all(x['current_file_whole_bytes_equal'] for x in post['important_committed_blob_identities'])
assert len(post['important_committed_blob_identities'])==21
assert all(x['committed_leaves']==0 for x in post['private_caches'])
oldpaths=(OWN/'DRY_V2_PATHS.txt').read_text().splitlines()
newpaths=(OWN/'POST_V2_PATHS.txt').read_text().splitlines()
assert set(newpaths)-set(oldpaths)=={'M\t'+PREFIX+'verification/checkpoint-subtree-dry-run-20261025.json'} and not set(oldpaths)-set(newpaths)
expected={
 'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md':'726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94',
 'verification/root-clearance-23204176-20261117.json':'ea5472784dffe99ee849d40700541b9453466b2f3edf064a3a02fe091e7f55cd',
 'verification/root-hafnian-retract-corrected-stage-adoption-20261117.json':'6976d6953ce3c10775077257321ae7bdb809a1898d96ef95efadcd3785166dc6',
 'verification/root-hafnian-retract-newhelper-reading-20261117.json':'b99f632c47164518000e32c01c7c5a09345aa2597199d6f5a07b25d418c587eb',
 'papers/23204212/sources/SOURCE_FINAL.json':'b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5',
 'papers/23204810/sources/SOURCE_FINAL.json':'4d62403dbe129bb77393b73492dc92ae8504d5081e84d311cb7905c7323638df',
 'papers/23318851/sources/SOURCE_FINAL.json':'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'}
by={x['path']:x for x in post['important_committed_blob_identities']}
assert all(by[PREFIX+k]['SHA256']==v for k,v in expected.items())
assert (OWN/'DRY_TREE_AUDIT.stdout').read_bytes()==b'' and b"KeyError: 'research_website_catalogue_20261024/RESEARCH_LOG.md'" in (OWN/'DRY_TREE_AUDIT.stderr').read_bytes()
for name in ('DRY_RUN.stderr','PUSH.stderr','DRY_V2_TREE_AUDIT.stderr','POST_V2_TREE_AUDIT.stderr','GUARDS_BEFORE.stderr','GUARDS_AFTER.stderr'): assert (OWN/name).read_bytes()==b''
now=datetime.now(timezone.utc).isoformat()
review_url='https://github.com/AlecKriebel/Math/blob/'+COMMIT+'/'+PREFIX+'papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md'
checks=dict(schema='scoped-checkpoint-complete-captured-postchecks-v1',UTC=now,status='PASS_CHECKPOINT_POSTVERIFIED',commit=COMMIT,parent=PARENT,tree=TREE,dry_paths=293,post_paths=294,status_counts=post['status_counts'],all294current_blobs_and_modes_exact=True,all21important_buffers_exact=True,all159siblings_and_docs_exact=True,all3excluded_trees_exact=True,private_cache_leaves=0,full_native_M_W_and_public_beforeafter_exact=True,protected_equality_capture_UTC=after['UTC'],fresh_remote=post['fresh_remote_main'],commit_headers=post['ordinary_commit_headers'],packet_committed_leaf_counts=post['packet_committed_leaf_counts'],important=post['important_committed_blob_identities'],native_repositories=after['repositories'],public_counts=dict(files=len(after['public']['files']),child_directories=len(after['public']['directories']),root_mode=after['public']['root_mode']),expected_dry_push_delta_only=True,failed_inspector_exit=1,failed_inspector_stderr=pin('DRY_TREE_AUDIT.stderr'),distinct_v2_dry_post_exits=[0,0],helper_dry_push_exits=[0,0],review_url=review_url,current_P_hold_released_after_postchecks=True,no_current_P_W_reads_by_sealer=True,completion_percent=100)
writej('FINAL_CHECKS.json',checks)
attestation=dict(schema='checkpoint-personal-saved-source-reading-v1',UTC=now,helper_lines=94,helper_full_read_before_invocation=True,helper_never_help=True,old_templates_read_only_not_executed=True,new_sources={n:pin(n) for n in ('capture_guards.py','run_helper_once.py','inspect_checkpoint.py','inspect_checkpoint_v2.py','seal_evidence.py')},all_new_saved_sources_personally_fully_read_before_invocation=True,original_inspector_preserved=True,whole293dry_pathlist_personally_read_blocks=['1–100','101–200','201–293'],post_path_delta_only_established_receipt=True,helper_isolated_index_and_ordinary_nonforce_push=True,no_expected_parent_server_lease_claim=True,no_science_source_or_productionhelper_execution=True,no_W_Sheet_release_deploy_AA_redirect_or_outreach=True)
writej('READ_ATTESTATION.json',attestation)
report='Checkpoint '+COMMIT+' was ordinarily pushed and independently postverified at '+after['UTC']+'. Parent '+PARENT+', tree '+TREE+'. All294programme-only paths (291A3M), every changed whole blob/mode and21important buffers matched current files while root held writes. All159siblings, docs and three excluded trees remain exact. The sole dry293→post294 delta is the established dry receipt.\n\nThe K3 root review20893B SHA256726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94 and its bounded-PASS clearance, full stage adoption, oldfailed-audit12/newcontinuation12, preparation11/fullhelper-reading, source192–194 closures and acquisition11 are committed. Native progress140 plus local141pending is preserved; no tracker write occurred. Review: '+review_url+'\n\nComplete native M/W HEAD/index/config/local loose+rawpackedheads and Wpublic781/377/root0750 were unchanged across captured guards. Fetch/remote-tracking/object additions are explicitly outside that equality. No native branch/index/config or website write, release, science/source run, tracker/deploy/AA/redirect/contact occurred.\n\nOne dry helper and one normal push both exited0 with empty stderr. Initial inspector failed1 with literal unchanged-RESEARCH_LOG lookup KeyError,0stdout/369Bstderr. Its code/streams remain exact; separate fully-read165line v2 passed dry and post. No helper retry or silent repair. Private PDFs/compiler caches/whole website clones are uncommitted under actual ignore rules; no paper directory was excluded.\n\nCompletion100% of checkpoint integrity. Root received verified immutable review link and release of current-file hold immediately after postchecks. This seal reads only captured own evidence after that boundary and grants no website or tracker authority.\n'
with (OWN/'REPORT.md').open('x',encoding='utf-8') as f: f.write(report)
rows=[]
for p in sorted(OWN.iterdir()):
 assert p.name not in ('MANIFEST.json','FINAL.json') and p.name not in ('.','..') and '/' not in p.name
 x=pin(p.name); assert x['mode']=='0644'; rows.append(dict(path=p.name,**x,hidden=p.name.startswith('.'),empty=x['bytes']==0))
assert format(stat.S_IMODE(OWN.stat().st_mode),'04o')=='0755'
manifest=dict(schema='finite-scoped-k3pass141-stageadoption-checkpoint-manifest-v1',UTC=now,root=str(OWN),root_mode='0755',regular_files=len(rows)+2,child_directories=0,payload_files=rows,directories=[],exact_already_created_terminal_recursive_hash_exclusions=[str(OWN/'MANIFEST.json'),str(OWN/'FINAL.json')],other_exclusions=[],terminal_modes={'MANIFEST.json':'0644','FINAL.json':'0644'},all_hidden_empty_bytes_modes_topology_included=True,no_future_subtree_or_basename_exclusion=True)
writej('MANIFEST.json',manifest)
final=dict(schema='scoped-k3pass141-stageadoption-checkpoint-FINAL-v1',UTC=now,status='PASS_SCOPED_CHECKPOINT_POSTVERIFIED',completion_percent=100,commit=COMMIT,parent=PARENT,tree=TREE,commit_url='https://github.com/AlecKriebel/Math/commit/'+COMMIT,immutable_K3_review_url=review_url,changed_paths=294,additions=291,modifications=3,all_changed_whole_current_blobs_modes_exact=True,all159siblings_docs_exact=True,all3exclusions_exact_at_parent=True,no_papers_excluded=True,oldfailed_audit12_newcontinuation12_prepare11_acquisition11_committed=True,source192_194_frozen_closures_committed=True,full_native_M_W_HEAD_index_config_localheads_and_public_exact=True,guard_capture_end_UTC=after['UTC'],fresh_remote_exact=True,ordinary_nonforce_single_expected_parent_commit=True,no_expected_parent_server_lease_claim=True,literal_helper_exits=[0,0],literal_inspector_exits=[1,0,0],first_failure_retained=pin('DRY_TREE_AUDIT.stderr'),remaining_checkpoint_gap=None,current_P_hold_released=True,sealer_reads_only_own_captured_evidence=True,own_regular_files=len(rows)+2,own_childdirs=0,root_mode='0755',all_file_modes='0644',hidden_files=sum(x['hidden'] for x in rows),empty_payloads=[x['path'] for x in rows if x['empty']],MANIFEST=pin('MANIFEST.json'),FINAL_CHECKS=pin('FINAL_CHECKS.json'),no_Sheet_W_release_deploy_science_AA_redirect_or_outreach=True,terminal_external_pins_required=True,frozen=True)
writej('FINAL.json',final)
assert len(list(OWN.iterdir()))==len(rows)+2 and all(p.is_file() and not p.is_symlink() for p in OWN.iterdir())
assert all(pin(x['path'])=={k:x[k] for k in ('bytes','SHA256','mode')} for x in rows)
print(json.dumps(dict(status=final['status'],commit=COMMIT,files=len(rows)+2,childdirs=0,FINAL=pin('FINAL.json'),MANIFEST=pin('MANIFEST.json'),completion_percent=100)))
