from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parent
S=AUDIT/'original_source_authentication_20261004'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p,row):
 b=p.read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];return b
manifest=load(S/'ORIGINAL_BLOB_MANIFEST.json')
assert manifest['head']=='78f4a7fadac0fd24e147a617956cb409eb6a579e'
assert manifest['artifact_count']==32
prefix='unsolved_math_prioritization/attempts/10400033/'
rows=[r for r in manifest['artifacts'] if r['path'].startswith(prefix)]
assert len(rows)==25
for r in manifest['artifacts']:
 b=pin(S/r['retained_path'],r)
 assert r['mode']=='100644'
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_SHA1']
commit=(S/'ORIGINAL_GIT_COMMIT_BODY.bin').read_bytes()
assert hashlib.sha1(b'commit '+str(len(commit)).encode()+b'\0'+commit).hexdigest()==manifest['head']
t=load(S/'ORIGINAL_RECURSIVE_TREE.json');children={};expected={'':t['sha']}
assert commit.splitlines()[0]==b'tree '+t['sha'].encode()
by_path={e['path']:e for e in t['tree']}
for r in manifest['artifacts']:
 assert by_path[r['path']]['sha']==r['git_blob_SHA1'] and by_path[r['path']]['mode']==r['mode']

for e in t['tree']:
 parent,_,name=e['path'].rpartition('/');children.setdefault(parent,[]).append((name,e))
 if e['type']=='tree':expected[e['path']]=e['sha']
for directory,target in expected.items():
 entries=sorted(children.get(directory,[]),key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode())
 b=b''.join((e['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(e['sha']) for name,e in entries)
 assert hashlib.sha1(b'tree '+str(len(b)).encode()+b'\0'+b).hexdigest()==target
assert len(expected)==3547 and not t['truncated']
B=S/'original'/prefix
status=load(B/'status.json');ledger=[json.loads(x) for x in (B/'turns.jsonl').read_text().splitlines()]
queue=(S/'original/unsolved_math_prioritization/QUEUE.md').read_text()
q=[x for x in queue.splitlines() if '| 10400033 /' in x]
assert len(q)==1 and q[0].split('|')[8].strip()=='claimed_solved' and q[0].split('|')[9].strip()=='1/5'
assert status['turns_used']==1 and 'turn_limit' not in status
assert len(ledger)==3 and [x['turn'] for x in ledger]==[1,1,1]
commands=[json.loads(x) for x in (S/'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
for row in commands:
 for k in ['stdout','stderr']:
  b=(S/row[k+'_path']).read_bytes();assert len(b)==row[k+'_bytes'] and sha(b)==row[k+'_sha256']
selfmanifest=load(S/'SELF_MANIFEST.json')
for row in selfmanifest['files']:pin(S/row['path'],row)
# Pin the reports and complete READBACK bytes; no execution of sibling code.
gate=load(AUDIT/'ROOT_FULL_MATHEMATICAL_GATE_20261004.json')
for row in gate['reports_read_in_full_by_ROOT']+[gate['ROOT_custody_readback'],gate['ROOT_original_custody_readback'],gate['ROOT_primary_reading_record']]:pin(Path(row['path']),row)
packet=AUDIT/'attributed_prior_result_preparation_20261004';p=load(packet/'DISPOSITION_PROPOSAL.json')
assert p['original_head']==manifest['head'] and p['original_literal_status']=='claimed_solved' and p['original_budget']=='1/5'
assert p['preserve_original_attempt_bodies_modes_blobs']==25 and p['original_turn_events']==3 and p['original_turns_used']==1
assert p['proposed_current_status']=='already_solved' and p['accepted_as']=='attributed_partial_prior_result'
assert not p['paper'] and not p['Zenodo'] and p['new_DOI'] is None and not p['tracker_row']
assert not p['earliest_or_identical_proof_certification'] and not p['exact2000printedbody_read']
assert not p['stronger_prior_p8_extremality_certified'] and not p['merge_clearance'] and not p['native_acceptance_complete']
assert p['novelty_of_additional_proof_or_even_estimate']=='unestablished'
result={'status':'PASS','scope':'snapshot custody and proposal invariants only; not remote ref inspection or native acceptance','original_head':manifest['head'],'original_attempt_files':len(rows),'original_all_manifest_bodies':len(manifest['artifacts']),'original_tree_serializations':len(expected),'all_original_git_blobs_and_commit_digest_verified':True,'all_original_modes':'100644','literal_intake':'claimed_solved','budget':'1/5','turn_events':3,'turns_used':1,'turn_limit':'ABSENT','original_custody_command_streams_verified':len(commands),'original_selfmanifest_members_verified':len(selfmanifest['files']),'root_gate_support_pins_verified':7,'proposal_no_paper_doi_upload_tracker_clearance':True}
(BASE/'CUSTODY_AND_DISPOSITION_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
