#!/usr/bin/env python3
"""Read-only exact package/receipt verifier; does not recertify mathematical proofs.

Run in the existing repository with corrected-head Git objects and repaired_snapshot
present. Downloads, extracted text, rendered sources and private runtime are excluded
from public replay and never loaded by this program. Complete candidate execution
streams are bound records; this verifier checks their contents without rerunning them.
"""
from pathlib import Path
import hashlib,json,subprocess
OWN=Path(__file__).resolve().parent
PARENT=OWN.parent
REPO=OWN.parents[3]
HEAD='420ffdfbb021c5a9378ccbbac198a13a4508dfad'
BASE='8f2b03b15902069ac24c1de59de1bf32b9c22f84'
ORIGINAL='9946a67cf8a1f7e3130d2a12de902db05875283a'
PREFIX='problems/30002762_conjugation_norms/'
PUBLIC_WHITELIST={
 'REPORT.md','RESEARCH_LOG.md','INSPECTION_RECEIPT.json','FINAL_VERDICT.json',
 'OUTPUT_MANIFEST.json','FINAL_SEAL.json','verify_audit.py','verification_output.json',
 'independent_baseline.md','independent_controls.py','independent_controls_output.json',
 'independent_seal.json','initial_mathematical_verdict.json','git_provenance.json',
 'nested_manifest_receipts.json','ancestry_receipts.json','fresh_source_receipts.json',
 'additional_source_receipts.json','source_binding_qualification.json',
 'complete_replay_outputs.json','postseal_adversarial_controls.py',
 'postseal_adversarial_controls_output.json','candidate_boundary_replay_output.json'}
def ck(value):
 if not value:raise AssertionError('audit receipt check failed')
def sha(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads(p.read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def blob(ref,path):return git('show',ref+':'+path)
# Bounded public envelope, hash graph, no accidental private artifacts.
ck({p.name for p in OWN.iterdir() if p.is_file()}==PUBLIC_WHITELIST)
ck(all(p.is_file() or p.name in {'raw_sources','tmp'} for p in OWN.iterdir()))
m=readj(OWN/'OUTPUT_MANIFEST.json');seal=readj(OWN/'FINAL_SEAL.json')
ck(m['head']==seal['head']==HEAD)
ck(sha((OWN/'OUTPUT_MANIFEST.json').read_bytes())==seal['output_manifest_sha256'])
ck(sha((OWN/'REPORT.md').read_bytes())==seal['report_sha256'])
ck({e['path'] for e in m['files']}==PUBLIC_WHITELIST-{'OUTPUT_MANIFEST.json','FINAL_SEAL.json'})
ck(len(m['files'])==len(PUBLIC_WHITELIST)-2)
for e in m['files']:
 b=(OWN/e['path']).read_bytes();ck(len(b)==e['bytes'] and sha(b)==e['sha256'])
for p in OWN.glob('*.json'):readj(p)
ind=readj(OWN/'independent_seal.json')
ck(ind['before_candidate_read'])
for name,h in ind['files'].items():ck(sha((OWN/name).read_bytes())==h)
# Snapshot manifest and direct Git bytes/blob IDs; original target preservation.
snapshot=PARENT/'repaired_snapshot'
frozen=readj(PARENT/'repaired_snapshot_manifest.json')
provenance=readj(OWN/'git_provenance.json')
ck(frozen['head']==HEAD and frozen['base']==BASE and len(frozen['files'])==44)
by_path={e['path']:e for e in provenance['files']}
for e in frozen['files']:
 p=e['path'];b=(snapshot/p).read_bytes();g=blob(HEAD,p)
 ck(b==g and len(b)==e['bytes'] and sha(b)==e['sha256'])
 ck(git('rev-parse',HEAD+':'+p).decode().strip()==by_path[p]['git_blob'])
 if p.startswith(PREFIX):ck(g==blob(ORIGINAL,p))
q='unsolved_math_prioritization/QUEUE.md'
a=blob(BASE,q).splitlines(keepends=True);b=blob(HEAD,q).splitlines(keepends=True)
ck(len(a)==len(b));ck([i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y]==[417])
ck(a[416].replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |')==b[416])
changed=git('diff','--name-status',BASE,HEAD).decode().splitlines()
ck(changed==provenance['direct_changed_paths_against_base'])
# Recompute all nested records from candidate manifests, including lengths.
nested=0;links=0;historical=0
problem=snapshot/PREFIX
for name in [*(f'TURN_{i}_MANIFEST.json' for i in range(1,6)), 'FINAL_AUTHOR_MANIFEST.json','review/REVIEW_MANIFEST.json']:
 mp=problem/name;nm=readj(mp)
 for e in nm['files']:
  rb=(mp.parent/e['path']).read_bytes();ck(len(rb)==e['bytes'] and sha(rb)==e['sha256']);nested+=1
 if 'previous_manifest_sha256' in nm:
  i=int(name.split('_')[1]);ck(sha((problem/f'TURN_{i-1}_MANIFEST.json').read_bytes())==nm['previous_manifest_sha256']);links+=1
ck(nested==66 and links==4)
for i in range(1,5):
 r=readj(problem/f'TURN_{i}_REMOTE_RECEIPT.json')
 for e in r['files']:
  p=PREFIX+e['path'];rb=blob(r['head'],p)
  ck(len(rb)==e['size']);ck(git('rev-parse',r['head']+':'+p).decode().strip()==e['sha'])
  ck(rb==blob(HEAD,p));historical+=1
ck(historical==64)
review=readj(problem/'review/REVIEW_MANIFEST.json')
ck(sha((problem/'FINAL_AUTHOR_MANIFEST.json').read_bytes())==review['author_manifest_sha256'])
ancestry=readj(OWN/'ancestry_receipts.json')
for ref,expected in ancestry['ancestry'].items():
 ck(expected);ck(subprocess.run(['git','merge-base','--is-ancestor',ref,HEAD],cwd=REPO).returncode==0)
for name in ancestry['author_wip_file_matches']:ck(blob(ancestry['author_wip'],PREFIX+name)==(problem/name).read_bytes())
ck(blob(ancestry['author_wip'],PREFIX+'FINAL_AUTHOR_MANIFEST.json')==(problem/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
# Complete execution records and exact author/old output bindings, without source loading.
runs=readj(OWN/'complete_replay_outputs.json')
ck(len(runs)==8)
expected=[f'check_turn_{i}.py' for i in range(1,6)]+['REPLAY_ALL.py','review/independent_check.py','verify_publication.py']
ck([r['program'] for r in runs]==expected)
for r in runs:ck(r['exit_code']==0 and r['stderr']=='' and r['elapsed_seconds']>=0)
for i in range(1,6):ck(runs[i-1]['stdout']==(problem/f'TURN_{i}_CHECKS.json').read_text())
ck(runs[6]['stdout']==(problem/'review/INDEPENDENT_CHECKS.json').read_text())
author=json.loads(runs[5]['stdout']);publication=json.loads(runs[7]['stdout'])
ck(author=={'all_receipts_byte_exact':True,'assertions':345888,'manifest_entries':62,'source_bindings_checked':0})
ck(publication=={'author_assertions':345888,'independent_assertions':47964,'source_bindings_checked':0,'source_omission_explicit':True,'status':'PASS'})
post=readj(OWN/'postseal_adversarial_controls_output.json');ck(post['status']=='PASS' and post['assertions']==251278)
verdict=readj(OWN/'FINAL_VERDICT.json')
ck(verdict['verdict']=='SCOPED PASS' and verdict['head']==HEAD and not verdict['mandatory_repairs'])
ck(verdict['original_problem_status']=='unresolved' and verdict['audit_completion_percent']==100)
print(json.dumps({'status':'PASS','head':HEAD,'public_whitelist_files':len(PUBLIC_WHITELIST),'direct_git_snapshot_files':44,'original_target_files_preserved':43,'nested_bindings':nested,'previous_links':links,'historical_git_bindings':historical,'ancestry_refs':len(ancestry['ancestry']),'complete_execution_streams_bound':8,'candidate_free_baseline_hashes_intact':True,'queue_change_line':417,'all_other_queue_bytes_preserved':True,'private_source_bindings_loaded':0,'scope':'Read-only exact package and receipt verification; mathematical PASS rests on the written proof audit and inspected primary sources.'},indent=2,sort_keys=True))
