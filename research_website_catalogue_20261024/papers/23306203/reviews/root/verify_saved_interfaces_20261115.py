#!/usr/bin/env python3
"""Offline read-only saved-interface comparison; never executes scientific code."""
from pathlib import Path
import hashlib,json,stat
P=Path(__file__).resolve().parents[2]
S=P/'sources';C=P/'reviews/scope';A=P/'reviews/adversarial'
nodes=0
def load(q):return json.loads(q.read_bytes())
def pin(q):
 b=q.read_bytes();return {'path':str(q),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def equal(a,b,label):
 global nodes
 nodes+=1
 if type(a) is not type(b):raise ValueError('type differs '+label)
 if isinstance(a,dict):
  if list(a)!=list(b):raise ValueError('ordered keys differ '+label)
  for k in a:equal(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):raise ValueError('length differs '+label)
  for i,(x,y)in enumerate(zip(a,b)):equal(x,y,label+'/'+str(i))
 elif a!=b:raise ValueError('value differs '+label)
def namespace(root,rows,terminals):
 expected=set()
 for e in rows:
  n=Path(e['path'])
  if n.is_absolute() or '..'in n.parts or e['path'] in expected:raise ValueError('unsafe duplicate manifest')
  expected.add(e['path']);q=root/n;b=q.read_bytes()
  if not stat.S_ISREG(q.lstat().st_mode) or len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['SHA256']:raise ValueError('manifest bytes differ')
 actual=set()
 for q in root.rglob('*'):
  mode=q.lstat().st_mode
  if stat.S_ISREG(mode):actual.add(q.relative_to(root).as_posix())
  elif not stat.S_ISDIR(mode):raise ValueError('nonordinary namespace')
 if actual!=expected|set(terminals):raise ValueError('strict root-relative exact namespace differs')
 return {'payloads':len(expected),'root_terminals':len(terminals),'actual_files':len(actual)}
sm=load(S/'SOURCE_READY_MANIFEST.json');cm=load(C/'OWNED_MANIFEST.json');am=load(A/'MANIFEST.json')
spaces={'source':namespace(S,sm['files'],sm['excluded_terminal_files']),'scope':namespace(C,cm['owned_files'],cm['terminal_exclusions']),'adversarial':namespace(A,am['owned_files'],am['excluded_self_and_final_seal_only'])}
ready=load(S/'SOURCE_READY.json');custody=load(A/'SOURCE_CUSTODY.json')
equal(ready,custody['native_whole_source_ready_object'],'whole original READY')
for fn,key in [('ALL_TRANSPORT_RECEIPTS.json','seven_actual_transport_receipts_whole'),('ARCHIVE_CUSTODY.json','whole_original_archive_custody_object'),('NATIVE_SCHEMA_TYPES.json','native_schema_types_whole')]:
 equal(load(S/fn),custody[key],key)
if len(custody['literal_native_copies'])!=21:raise ValueError('native copy count differs')
for e in custody['literal_native_copies']:
 original=Path(e['original_path']);copy=A/e['copy_path'];raw=original.read_bytes()
 if copy.read_bytes()!=raw or len(raw)!=e['bytes'] or hashlib.sha256(raw).hexdigest()!=e['SHA256']:raise ValueError('whole native copy differs')
 try:x=json.loads(raw);y=load(copy)
 except(UnicodeDecodeError,json.JSONDecodeError):continue
 equal(x,y,'whole native copied object')
if not len(ready['whole_native_API_objects'])==len(custody['whole_native_API_objects'])==4:raise ValueError('API count differs')
for e,saved in zip(ready['whole_native_API_objects'],custody['whole_native_API_objects']):
 equal(e,saved['original_custody_object'],'whole API identity')
 equal(load(Path(e['path'])),saved['native_whole_object'],'whole API body')
 equal(e['role'],saved['role'],'API role/order')
package=S/'published-source/asset-001';replay=load(A/'NATIVE_REPLAY.json');expected=(package/'verification/exact_results.json').read_bytes()
equal(json.loads(expected),replay['whole_expected_object'],'entire native expected object')
equal(json.loads(expected),load(C/'SUPPORT_INSPECTION.json')['expected_exact_output'],'entire scope expected object')
if len(expected)!=932 or hashlib.sha256(expected).hexdigest()!=replay['EXPECTED_SHA256']:raise ValueError('expected bytes differ')
equal([x['mode'] for x in replay['runs']],['normal','optimized'],'exact two saved replay modes')
for item in replay['runs']:
 out=(A/('NATIVE_'+item['mode']+'.stdout')).read_bytes();err=(A/('NATIVE_'+item['mode']+'.stderr')).read_bytes()
 if out!=expected or err!=b'' or item['exit_code']!=0 or item['stdout_bytes']!=len(out):raise ValueError('whole recorded streams/exit differ')
 equal(hashlib.sha256(out).hexdigest(),item['stdout_SHA256'],'recorded stdout pin')
 equal(hashlib.sha256(err).hexdigest(),item['stderr_SHA256'],'recorded stderr pin')
for e in replay['whole_isolated_original_payloads']:
 q=package/e['path'];z=A/'native-isolated'/e['path'];b=q.read_bytes()
 if b!=z.read_bytes() or len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['SHA256']:raise ValueError('whole original/isolated payload differs')
print(json.dumps({'status':'PASS_READ_ONLY_WHOLE_TYPED_NATIVE_AND_EXACT_NAMESPACES','typed_nodes':nodes,'closed_namespaces':spaces,'scope_original_basename_exclusion_hole_compensated_by_strict_root_relative_namespace':True,'native_copies_compared_whole':21,'whole_native_API_objects_compared':4,'expected_and_two_saved_stdout_buffers_equal':True,'recorded_exit_codes_zero_and_stderr_empty':True,'all13_original_and_isolated_payload_buffers_equal':True,'expected':pin(package/'verification/exact_results.json'),'root_scientific_execution_import_network_or_writes':False},indent=2))
