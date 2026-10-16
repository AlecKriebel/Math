"""Read-only exact-byte/native-original joins for completed second review.

Run normally, never with -O. This checks custody and executed artifacts;
root's independent complete mathematical/prose inspection is separate.
"""
from pathlib import Path
import json, hashlib, base64, datetime, stat, sys
assert not sys.flags.optimize
c=Path(__file__).resolve().parent
d=c/'reviews/whole_package_2'; p=c/'private_sources/whole_package_2'
def h(x): return hashlib.sha256(x).hexdigest()
def oid(k,x): return hashlib.sha1(k.encode()+b' '+str(len(x)).encode()+b'\0'+x).hexdigest()
def get(path): return json.loads(path.read_bytes())
seal_raw=(d/'FINAL_SEAL.json').read_bytes()
assert h(seal_raw)=='d45c7fbcb151dcf2f7335edb293ecaf6df6d495f9c6917a75824c60b504b5d9b'
seal=json.loads(seal_raw); allow=get(d/'PUBLIC_ALLOWLIST.json')
assert h((d/'PUBLIC_ALLOWLIST.json').read_bytes())==seal['public_allowlist_sha256']
assert set(x.name for x in d.iterdir())==set(allow['positive_files'])|{'FINAL_SEAL.json','PUBLIC_ALLOWLIST.json'}
for x in seal['files']:
 f=d/x['path']; raw=f.read_bytes()
 assert len(raw)==x['bytes'] and h(raw)==x['sha256'] and stat.S_ISREG(f.lstat().st_mode) and stat.S_IMODE(f.lstat().st_mode)==0o644
assert len(seal['files'])==seal['payload_count']==23
pins=get(d/'PRIVATE_CUSTODY_PINS.json');actual={}
for x in pins['files']:
 f=c/x['path']; assert f.is_relative_to(c/'private_sources/whole_package_2') and not any(q.is_symlink() for q in [f,*f.parents])
 assert stat.S_ISREG(f.lstat().st_mode)
 raw=f.read_bytes(); assert len(raw)==x['bytes'] and h(raw)==x['sha256']; actual[x['path']]=x['sha256']
assert len(actual)==pins['count']==503
inventory=get(d/'INSPECTION_INVENTORY.json')
for x in inventory['exact_duplicate_groups']:
 for path in x['paths']:
  raw=(c/path).read_bytes(); assert len(raw)==x['bytes'] and h(raw)==x['sha256']
summary=get(d/'REPLAY_SUMMARY.json');runs=get(p/'SIX_GENUINE_REPLAYS.json')['runs']; assert len(runs)==6
for x,y in zip(runs,summary['six_runs']):
 assert x['name']==y['name'] and x['returncode']==y['returncode']==0
 out=(p/(x['name']+'.stdout')).read_bytes(); err=(p/(x['name']+'.stderr')).read_bytes()
 assert h(out)==x['stdout_sha256']==y['stdout_sha256'] and h(err)==x['stderr_sha256']==y['stderr_sha256'] and err==b''
 assert json.loads(out)==x['native_json'] and ('-O' in x['command'])==x['name'].endswith('optimized')
controls=get(p/'controls.stdout'); assert controls['controls']==summary['control_results'] and controls['executions']==38 and controls['all_expectations_matched']
for x in controls['controls']:
 y=get(p/'control_logs'/(x['name']+'__'+('optimized' if x['optimized'] else 'normal')+'.json'))
 assert y['result']==x and h(y['stdout'].encode())==x['stdout_sha256'] and h(y['stderr'].encode())==x['stderr_sha256']
 assert ('-O' in y['command']) is x['optimized'] and x['matched_expectation']
 assert (x['returncode']==0)==(x['expected']=='success')
 if x['diagnostic_required']: assert x['diagnostic_required'] in y['stderr'] or x['diagnostic_required'] in y['stdout']
final=get(p/'FINAL_GATE.json'); assert final['head']==final['independent_ref']=='ff7a7521458c1d2d9ae6f762eac04a3c3d9b9568'
assert final['queue_row']['Status']=='claimed_solved' and final['queue_row']['Turns']=='2/5' and final['state']=='open' and final['draft'] and not final['merged']
raw_by_sha={}
for f in (p/'final_native').iterdir():
 if f.is_file(): raw_by_sha.setdefault(h(f.read_bytes()),[]).append(f)
for x in final['calls']:
 assert x['method']=='GET' and x['returncode']==0 and x['stdout_sha256'] in raw_by_sha and x['stderr_sha256'] in raw_by_sha
 native=get(raw_by_sha[x['stdout_sha256']][0]); route=x['endpoint']
 if route=='pulls/411':
  assert native['head']['sha']==final['head'] and native['state']=='open' and native['draft'] and not native['merged']
  assert h(native['body'].encode())=='959f075e0bfff3fccc2411235000bbefd491177ba078878265182806ca0500a0'
 elif route.startswith('git/ref/'): assert native['object']['sha']==final['head']
 elif route.startswith('git/commits/'): assert native['sha']==final['head'] and native['tree']['sha']=='816a5a7d91a1efbad270da00771c84952a97c8f8'
 elif route.startswith('git/trees/'):
  assert native['truncated'] is False
  serialized=b''
  for t in sorted(native['tree'],key=lambda x:(x['path']+('/' if x['type']=='tree' else '')).encode()):
   serialized+=t['mode'].lstrip('0').encode()+b' '+t['path'].encode()+b'\0'+bytes.fromhex(t['sha'])
  assert oid('tree',serialized)==native['sha']==route.rsplit('/',1)[1]
 elif route.startswith('git/blobs/'):
  raw=base64.b64decode(native['content']); assert len(raw)==native['size'] and oid('blob',raw)==native['sha']==route.rsplit('/',1)[1]
for x in final['files']:
 raw=(c/'prepared_packet'/x['path']).read_bytes(); native=get(p/'final_native'/('blob_'+x['blob']+'.stdout'))
 assert base64.b64decode(native['content'])==raw and len(raw)==native['size']
 assert x['mode']=='100644' and h(raw)==x['sha256'] and oid('blob',raw)==x['blob']
assert len(final['files'])==99
verdict=get(d/'VERDICT.json'); assert verdict['result']=='PASS0' and verdict['finding_count']==0 and not verdict['findings']
assert not get(d/'FINDINGS.json')['findings'] and get(d/'NATIVE_VERDICT.json')['result']=='PASS0'
root_replay=get(c/'private_sources/root_whole2_exact_replay/NATIVE.json')
assert root_replay['returncode']==0 and not base64.b64decode(root_replay['stderr_base64'])
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_CUSTODY_AND_REPLAY_COMPONENT',
 'review_external_seal_sha256':h(seal_raw),'private_originals_verified':503,'positive_outputs_verified':25,
 'byte_duplicate_groups_verified':len(inventory['exact_duplicate_groups']),'fresh_final_GET_calls_joined':len(final['calls']),
 'native_99_blobs_and_immediate_trees_verified':True,'six_actual_replays_command_flags_stdout_JSON_joined':True,
 'controls38_actual_original_logs_and_required_causes_joined':True,'root_independent_exact_replay_sha256':h((c/'private_sources/root_whole2_exact_replay/NATIVE.json').read_bytes()),
 'private_custody_pins_sha256':h((d/'PRIVATE_CUSTODY_PINS.json').read_bytes()),'native_scope_sha256':h((d/'NATIVE_SCOPE_RECEIPTS.json').read_bytes()),
 'setup_correction':'An earlier root one-off join incorrectly expected size on compact FINAL_GATE files and stopped KeyError before any output certificate or mutation. Correct check joins actual native blob size; original tool failure retained.',
 'limitations':'Custody/native joins supplement root full mathematical and report inspection; no novelty or future production certificate.'}
target=c/'ROOT_WHOLE_REVIEW_2_CUSTODY_CHECK.json'
with target.open('x') as f: f.write(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
