#!/usr/bin/env python3
"""Read-only comparison of original native interfaces and recorded sole-owner outputs."""
from pathlib import Path
import hashlib,json,stat
P=Path(__file__).resolve().parents[2]
S=P/'sources'; A=P/'reviews/adversarial'; C=P/'reviews/scope'
count=0
def equal(a,b,label):
 global count
 count+=1
 if type(a) is not type(b): raise ValueError('type differs: '+label)
 if isinstance(a,dict):
  if set(a)!=set(b): raise ValueError('keys differ: '+label)
  for k in a:equal(a[k],b[k],label+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):raise ValueError('length differs: '+label)
  for i,(x,y) in enumerate(zip(a,b)):equal(x,y,label+'/'+str(i))
 elif a!=b:raise ValueError('value differs: '+label)
def load(q):return json.loads(q.read_bytes())
def pin(q):
 b=q.read_bytes();return {'path':str(q),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def namespace(root,rows,excluded):
 expected=set()
 for row in rows:
  q=root/row['path']
  if row['path'] in expected or Path(row['path']).is_absolute() or '..' in Path(row['path']).parts:raise ValueError('unsafe or duplicate manifest')
  expected.add(row['path']); b=q.read_bytes()
  if not stat.S_ISREG(q.lstat().st_mode) or len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['SHA256']:raise ValueError('whole manifest member differs')
 actual=set()
 for q in root.rglob('*'):
  mode=q.lstat().st_mode
  if stat.S_ISREG(mode):actual.add(q.relative_to(root).as_posix())
  elif not stat.S_ISDIR(mode):raise ValueError('nonordinary namespace node')
 if actual!=expected|set(excluded):raise ValueError('closed exact relative namespace differs')
 return {'payload_files':len(expected),'terminal_files':len(excluded),'actual_files':len(actual)}
ready=load(S/'SOURCE_READY.json');native=load(A/'FINAL_NATIVE_INPUTS.json');scope=load(C/'CUSTODY_BINDING.json')
equal(ready,native['whole_original_SOURCE_READY'],'whole READY')
equal(ready,load(A/'SOURCE_NATIVE_MANIFEST.json')['whole_original_SOURCE_READY'],'whole manifest READY')
for row,saved in zip(ready['whole_native_API_objects'],native['whole_native_API_objects']):
 equal(row,saved['original_identity'],'API identity')
 equal(load(Path(row['path'])),saved['whole_original_object'],'whole API body')
equal(ready['whole_native_API_objects'],scope['whole_native_API_objects'],'scope whole API identities')
equal(ready['all_native_assets_in_original_order'],scope['whole_assets_in_literal_order'],'scope whole ordered native assets')
for name,field in [('ALL_TRANSPORT_RECEIPTS.json','whole_original_transport_receipts'),('NATIVE_SCHEMA_TYPES.json','whole_original_NATIVE_SCHEMA_TYPES'),('QUEUE_BINDING.json','whole_original_QUEUE_BINDING'),('ARCHIVE_CUSTODY.json','whole_original_ARCHIVE_CUSTODY')]:
 equal(load(S/name),native[field],field)
for name,value in scope['historical_source_flags'].items():equal(ready[name],value,'scope historical flag '+name)
sm=load(S/'SOURCE_READY_MANIFEST.json');cm=load(C/'OWNED_MANIFEST.json');am=load(A/'OWNED_MANIFEST.json')
namespaces={'source':namespace(S,sm['files'],sm['excluded_terminal_files']),'scope':namespace(C,cm['files'],['OWNED_MANIFEST.json','CLOSURE.json','SEAL.json']),'adversarial':namespace(A,am['files'],am['excluded_final_control_files'])}
package=S/'published-source/asset-001/supported_cycle_verification'
expected=(package/'verification/EXPECTED.json').read_bytes(); replay=load(A/'NATIVE_SELECTED_REPLAY.json')
equal(load(package/'SOURCE_MANIFEST.json'),native['whole_original_source_file_manifest'],'whole authored manifest')
equal(load(package/'ORIGINAL_BINDING.json'),native['whole_original_original_binding'],'whole original binding')
code=pin(package/'verification/exact_checks.py');equal(code['SHA256'],replay['selected_source_code_SHA256'],'native code pin')
if replay['reproduce_or_package_builder_executed'] is not False or replay['source_files_unchanged']!=77:raise ValueError('replay scope differs')
for mode,rec in zip(['normal','optimized','double-optimized'],replay['receipts']):
 out=A/('native-'+mode+'.stdout.json');err=A/('native-'+mode+'.stderr')
 equal(rec['mode'],mode,'native replay mode')
 if out.read_bytes()!=expected or err.read_bytes()!=b'' or rec['returncode']!=0 or rec['stdout_bytes']!=len(expected):raise ValueError('whole actual recorded output differs')
 equal(hashlib.sha256(expected).hexdigest(),rec['stdout_SHA256'],'recorded output pin')
print(json.dumps({'UTC_comparison_scope':'durable saved bytes only; no scientific execution/import/network/writes','status':'PASS','whole_typed_nodes_compared':count,'closed_namespaces':namespaces,'selected_code':code,'expected_stdout':pin(package/'verification/EXPECTED.json'),'whole_expected_and_three_recorded_stdout_buffers_equal':True,'stderr_empty_and_all_three_recorded_exit_codes_zero':True,'actual_interpreter_in_sole_owner_receipt':replay['python'],'root_replayed_science':False},indent=2))
