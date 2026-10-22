#!/usr/bin/env python3
"""Round4 independent hostile selections against exact captured root and kit."""
import builtins,contextlib,copy,hashlib,io,json,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent
p=R/'root_fixture_plumbing.py';raw=p.read_bytes();prefix=raw.split(b'results=[]\nfor ph in')[0]
g={'__file__':str(p),'__name__':'round4_read_source_fixture'}
exec(compile(prefix,str(p),'exec'),g)
need=g['need'];m=g['m'];F=g['F'];K=g['K'];results=[];counter=0

def run(phase='staged'):
 global counter
 counter+=1;g['phase']=phase;receipt=f'ROUND4_{counter:03d}.json';argv=sys.argv;sys.argv=['root_zenodo_readback.py','--phase',phase,'--receipt',receipt]
 try:
  with contextlib.redirect_stdout(io.StringIO()):m.main()
 finally:sys.argv=argv
 return json.loads((F/receipt).read_bytes())
def check(label,fn):fn();results.append({'name':label,'status':'PASS'})
def reject(label,fn):
 try:fn()
 except Exception as exc:
  if not isinstance(exc,(ValueError,KeyError,IndexError)) and type(exc).__name__!='DepositError':raise
  results.append({'name':label,'status':'REJECTED','error_type':type(exc).__name__});return
 raise RuntimeError('hostile accepted '+label)
first=run();(F/'ZENODO_STAGED_NATIVE_READBACK.json').write_text(json.dumps(first))
check('entire_staged_path_stale_pyc_ignored',lambda:need(first['id']==g['RID'] and not first['published'] and first['files']==g['original']['files'],'staged path'))
second=run('published');check('entire_published_path',lambda:need(second['published'] and second['all_supplied_metadata_fields_verified']==11,'published path'))
original_native=g['native']
for label,mut in [('wrong_native_id',lambda n:n.update(id='999999992')),('wrong_phase',lambda n:n.update(is_published=True)),('title',lambda n:n['metadata'].update(title='Other')),('ORCID',lambda n:n['metadata']['creators'][0]['person_or_org']['identifiers'][0].update(identifier='0000-0000-0000-0000')),('access',lambda n:n['access'].update(files='restricted')),('description_double_escape',lambda n:n['metadata'].update(description=n['metadata']['description'].replace('&gt;','&amp;gt;'))),('extra_file',lambda n:n['files']['entries'].update({'ghost.txt':{}})),('file_size',lambda n:next(iter(n['files']['entries'].values())).update(size=1)),('file_checksum',lambda n:next(iter(n['files']['entries'].values())).update(checksum='md5:'+'0'*32))]:
 def changed(mut=mut):n=original_native();mut(n);return n
 g['native']=changed;reject('native_'+label,run);g['native']=original_native
Client=g['Client'];old_get=Client.get
for label,mut in [('legacy_submitted_phase',lambda n:n.update(submitted=True)),('legacy_unknown_norm_description',lambda n:n['metadata'].update(description=n['metadata']['description']+' altered')),('legacy_missing_field',lambda n:n['metadata'].pop('license'))]:
 def changed(self,rid,mut=mut):n=old_get(self,rid);mut(n);return n
 Client.get=changed;reject(label,run);Client.get=old_get
Conn=g['Conn'];old_response=Conn.getresponse
for label,body,status in [('HTTP_redirect',b'',302),('HTTP_auth',b'',403),('same_length_changed_binary',None,200),('oversize_binary',b'x'*10000001,200)]:
 def response(self,body=body,status=status):
  data=body
  if data is None:
   data=(g['P']/self.name).read_bytes();data=bytes([data[0]^1])+data[1:]
  return types.SimpleNamespace(status=status,read=lambda limit:data)
 Conn.getresponse=response;reject(label,run);Conn.getresponse=old_response
# Hash the exact captured bytes and execute them, despite a file swap after capture.
source=K.read_bytes();original_exec=m.exec
def swapping_exec(code,ns):
 K.write_bytes(b"raise RuntimeError('SWAPPED_SOURCE_MUST_NOT_EXECUTE')\n")
 original_exec(code,ns)
m.exec=swapping_exec
try:out=run();check('source_swap_after_capture_executes_only_captured_verified_bytes',lambda:need(out['files']==first['files'],'source capture'))
finally:K.write_bytes(source);m.exec=original_exec
K.write_bytes(source+b'\n# tampered before capture\n')
try:reject('kit_source_change_before_capture_rejected',run)
finally:K.write_bytes(source)
# Published path must preserve staged native metadata, even for a field the
# supplied-field normalization intentionally omits (an extra native marker).
native_before=json.loads((F/'ZENODO_STAGED_NATIVE_READBACK.json').read_bytes())
native_before['native_metadata']['extra_stage_marker']='a';(F/'ZENODO_STAGED_NATIVE_READBACK.json').write_text(json.dumps(native_before))
reject('published_native_full_metadata_change_since_stage',lambda:run('published'))
print(json.dumps({'schema':'pr681-round4-new-root-readback-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','count':len(results),'controls':results,'root_source_sha256':hashlib.sha256(g['root_source']).hexdigest(),'kit_source_sha256':hashlib.sha256(K.read_bytes()).hexdigest(),'fixture_source_sha256':hashlib.sha256(raw).hexdigest(),'token_HTTP_transports_fully_intercepted':True,'real_credentials_network_or_external_mutations':0,'mock_calls':g['calls']},indent=2,sort_keys=True))
