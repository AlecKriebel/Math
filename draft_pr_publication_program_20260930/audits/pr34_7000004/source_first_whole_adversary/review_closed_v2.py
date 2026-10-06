"""Read and actually replay the separately closed procedurally qualified review."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
H=Path(__file__).resolve().parent
P=Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr34_7000004')
S=P/'v2_whole_adversary';D=H/'tmp/second_closed';D.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
want='ab3a780fa3a69ebc786219a1ac021f799d414b6191300a9864fddcb9b6888c75'
assert sha((S/'MANIFEST.json').read_bytes())==want
m=load(S/'MANIFEST.json');rows=[]
for z in m['files']:
 b=(S/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
 method='complete bytes read'
 if '.jsonl' in z['path']:
  for line in b.splitlines():json.loads(line)
  method='all JSONL records parsed'
 elif '.json' in z['path']:json.loads(b);method='complete JSON parsed'
 q=D/z['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 rows.append(dict(z,method=method))
shutil.copyfile(S/'MANIFEST.json',D/'MANIFEST.json')
assert len(rows)==118 and sum(z['bytes'] for z in rows)==360439
assert load(S/'verdict.json')['source_first_order_followed'] is False
assert load(S/'verdict.json')['final_source_first_clean_acceptance_gate'] is False
out=H/'second_closed_actual';out.mkdir(exist_ok=True)
r=subprocess.run(['/usr/bin/python3',str(D/'replay_closed.py'),'--output',str(D/'tmp/actual')],capture_output=True,timeout=600)
(out/'stdout.txt').write_bytes(r.stdout);(out/'stderr.txt').write_bytes(r.stderr)
assert r.returncode==0 and not r.stderr,(r.returncode,r.stderr.decode())
result=load(D/'tmp/actual/ROOT_REPLAY_RESULTS.json')
assert result['closed_audit_manifest_sha256']==want
assert result['historical_metadata_failure_still_recorded_as_failure'] is True
(out/'ROOT_REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
# Execute both unchanged HTTP helpers privately as executable-source coverage;
# actual source bytes, not matching clocks/dynamic redirect strings, are compared.
retrieval_runs=[]
for name,expected in [('retrieve_sources.py','SOURCE_RETRIEVALS.json'),('retrieve_additional.py','ADDITIONAL_SOURCE_RETRIEVALS.json')]:
 r=subprocess.run(['/usr/bin/python3',str(D/name)],capture_output=True,timeout=120)
 (out/(name+'.stdout.txt')).write_bytes(r.stdout);(out/(name+'.stderr.txt')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr
 old=load(S/expected);new=load(D/expected)
 if isinstance(old,dict):old=old['sources'];new=new['sources']
 assert [(z['name'],z['bytes'],z['sha256']) for z in old]==[(z['name'],z['bytes'],z['sha256']) for z in new]
 retrieval_runs.append({'program':name,'implementation_sha256':sha((D/name).read_bytes()),'exit':r.returncode,'all_source_bytes_match_frozen':True})
 (out/expected).write_bytes((D/expected).read_bytes())
# The first complete review's retrieval helper is exactly the second one's code.
assert (P/'current_whole_adversary/retrieve_sources.py').read_bytes()==(S/'retrieve_sources.py').read_bytes()
for z in rows:
 b=(S/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
assert sha((S/'MANIFEST.json').read_bytes())==want
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_second_manifest_sha256':want,'member_count':len(rows),'total_member_bytes':sum(z['bytes'] for z in rows),'complete_read_binding_ledger':rows,'actual_final_closure_replay':result,'actual_HTTP_helper_replays':retrieval_runs,'earlier_HTTP_helper_byte_identical':True,'second_ordering_violation_honestly_preserved':True,'second_review_never_transferred_as_final_gate':True,'all_second_files_unchanged_before_after':True,'scope':'Independent full read/replay of the actual closed second reviewer. Fresh-source clocks and dynamic redirects do not replace original receipts. All writes under this reviewer folder.'}
(H/'SECOND_CLOSED_REVIEW.json').write_text(json.dumps(result,indent=2)+'\n')
print('SECOND REVIEW CLOSED: actual final-closure replay and both unchanged retrieval helpers passed',flush=True)
