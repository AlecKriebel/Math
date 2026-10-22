"""Caller-pinned read-only closed-package verifier. No network, actor, or file writes."""
from pathlib import Path
import json,hashlib,gzip,stat,sys,os,base64,copy
O=Path(__file__).resolve().parent
SOURCE='5f2a18359d2006783b20650584c2f4560b915f2907c6129b1db4c49488f224c8'
DISCOVERY='11c3a6b59f16f8d2a1d87af3151325f30ca3824a77548b7c5ca15521a4107b4d'
CAPTURE_PINS={}
def sha(b):return hashlib.sha256(b).hexdigest()
def item(p):
 s=p.lstat();v={'kind':'directory'if stat.S_ISDIR(s.st_mode)else'file'if stat.S_ISREG(s.st_mode)else'UNSUPPORTED','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
 assert v['kind']!='UNSUPPORTED','Symlink/unsupported closed member'
 if v['kind']=='file':b=p.read_bytes();v.update(bytes=len(b),sha256=sha(b))
 return v
def closure(root,expected):
 seal=root/'MANIFEST.json';raw=seal.read_bytes();assert sha(raw)==expected,'Externally pinned manifest mismatch';m=json.loads(raw)
 actual={'.'if p==root else str(p.relative_to(root)):item(p)for p in[root,*sorted(root.rglob('*'))]if p!=seal};assert actual==m['entries'],'Closed namespace/bytes/mode/nsmtime/nlink changed'
 sm=item(seal);assert all(sm[k]==v for k,v in m['manifest_metadata'].items()),'Self-reserved manifest metadata changed';return m

def captured(relative,name):
 p=O/relative;b=p.read_bytes();pin=CAPTURE_PINS[relative];assert len(b)==pin['bytes']and sha(b)==pin['sha256']and item(p)==pin,'Captured helper bytes or metadata changed';ns={'__file__':str(p),'__name__':name};exec(compile(b,str(p),'exec',optimize=0),ns);return ns

def verify(expected_manifest):
 m=closure(O,expected_manifest);CAPTURE_PINS.clear();CAPTURE_PINS.update(m['entries']);discovery=O.parent/'existing_publication_remaining_rows_inventory01';closure(discovery,DISCOVERY)
 boot=captured('source/bootstrap.py','_readonly_closed_boot');M,recheck=boot['load_verified'](SOURCE);C=M['ops_core'];P=M['protocol'];G=M['gates'];plan=json.loads((O/'PROPOSAL.json').read_bytes());assert len(P.validate(plan))==34
 gatebytes=gzip.decompress((O/'private/REVIEWED_GATE_PROPOSED.json.gz').read_bytes());assert sha(gatebytes)=='4fbfb0507af3a2a420eba783d6a10057a60d79f74dc5d7fc9eef6e5db33f3a62';gate=json.loads(gatebytes);G.validate_gate(plan,gate);assert len(gate['semantic_decisions'])==3340 and len(gate['intrabatch'])==1122 and len(gate['cross_batch_eleven'])==374 and gate['action_authority']is False and gate['root_action_adopted']is False
 CAS=captured('cas_custody.py','_readonly_closed_cas');index=json.loads((O/'controls/CAS_PACK_INDEX.json').read_bytes());encoded=0
 for name,pin in index['packs'].items():
  b=(O/name).read_bytes();assert sha(b)==pin['sha256']and len(b)==pin['bytes'];pack=json.loads(gzip.decompress(b))
  for relative,e in pack['entries'].items():
   assert index['entries'][relative]['pack']==name;z=CAS['exact_compressed'](relative);assert len(z)==e['exact_compressed_bytes']and sha(z)==e['exact_compressed_sha256'];assert e['original_mode']>=0 and e['original_nlink']>=1 and type(e['original_mtime_ns'])is int;encoded+=1
 names=set(index['entries'])|{str(p.relative_to(O))for p in(O/'controls').glob('*.gz')};custodies=0;fixturefiles=0
 for relative in sorted(names):
  if ('custody'not in Path(relative).name and'CUSTODY'not in Path(relative).name)or not relative.endswith('.gz'):continue
  v=json.loads(CAS['raw'](relative));assert type(v['entries'])is dict
  for n,e in v['entries'].items():
   assert e['kind']in['directory','file']and type(e['mode'])is int and type(e['mtime_ns'])is int and type(e['nlink'])is int and e['nlink']>=1
   if e['kind']=='file':b=CAS['raw'](e['capture']);assert len(b)==e['bytes']and sha(b)==e['sha256'];fixturefiles+=1
  custodies+=1
 histories=0
 for relative in sorted(names):
  if'SOURCE_FREEZE_'not in relative:continue
  v=json.loads(CAS['raw'](relative));manifest=json.loads(v['manifest_raw']);assert manifest==v['manifest'];assert sha(v['manifest_raw'].encode())in relative
  for key,field in [('source_files','source_buffers'),('data_files','data_buffers')]:
   assert set(manifest[key])==set(v[field])
   for n,pin in manifest[key].items():b=v[field][n].encode();assert len(b)==pin['bytes']and sha(b)==pin['sha256']
  histories+=1
 assert histories==4 and custodies>=140
 delta=json.loads(gzip.decompress((O/'private/FAILED_GATE_BUILD01_EXACT_LOSSLESS_DELTA.json.gz').read_bytes()));basis=(O/delta['basis_gzip_path']).read_bytes();assert sha(basis)==delta['basis_gzip_sha256'];old=copy.deepcopy(json.loads(gzip.decompress(basis)))
 for d in delta['old_replacements']:old['semantic_decisions'][d['index']]=d['old']
 raw=(json.dumps(old,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();assert len(raw)==delta['original_raw_bytes']and sha(raw)==delta['original_raw_sha256'];z=gzip.compress(raw,mtime=0);assert len(z)==delta['original_gzip_bytes']and sha(z)==delta['original_gzip_sha256']
 controls=captured('verify_controls.py','_readonly_closed_controls');controls['load_cas']=lambda:CAS;derived=controls['audit']();controls['verify_expected'](derived,json.loads((O/'FINAL_CONTROL_ACCOUNTING.json').read_bytes()))
 active=json.loads((O/'ACTIVE_EXPECTED_OUTPUT_CONTROLS.json').read_bytes());assert len(active['controls'])==4 and active['all_rejected']is True
 for d in active['controls']:
  assert d['rejected']is True
  if'false_envelope'in d:
   try:controls['verify_expected'](derived,d['false_envelope'])
   except AssertionError:pass
   else:raise AssertionError('Hash-consistent false expectation accepted')
  else:
   try:boot['load_verified']('0'*64)
   except RuntimeError as e:assert'Caller-pinned source manifest mismatch'in str(e)
   else:raise AssertionError('Bad external caller hash accepted')
 unit_ns=captured('verify_semantic_and_policy_units.py','_readonly_closed_units');unit_ns['load']=lambda:(M,recheck,SOURCE);units=unit_ns['replay']();assert units==json.loads((O/'SEMANTIC_AND_POLICY_UNIT_RESULTS.json').read_bytes())and units['all_passed']is True and len(units['results'])==9
 initial=json.loads((O/'INITIAL_READONLY_COLLECTION.json').read_bytes());assert initial['columns']==43 and initial['rows']==239 and initial['owned_counts']==[204,204]and initial['owned_two_passes_full_typed_equal']is True and initial['local_count']==250
 closing=json.loads((O/'CLOSING_NUMERIC_READONLY.json').read_bytes());pin=closing['raw_complete'];raw=gzip.decompress((O/pin['path']).read_bytes());assert len(raw)==pin['bytes']and sha(raw)==pin['sha256'];data=json.loads(raw);assert closing['rows']==240 and closing['old_full43_prefix_typed_unchanged']is True and closing['full_metadata_unchanged']is True and len(closing['new_matching_pairs'])==5
 numeric=data['numeric'];assert M['numeric'].target(numeric['metadata'])['sheetId']==1254632077 and C.typed_equal(numeric['value_raw'],numeric['formula_raw'])and len(numeric['values'])==240 and C.typed_equal(numeric['values'],numeric['formulas']);assert len(data['original_raw_cli_transports'])==4
 for r in data['original_raw_cli_transports']:assert r['returncode']==0 and type(base64.b64decode(r['stdout_base64']))is bytes and type(base64.b64decode(r['stderr_base64']))is bytes
 for p in(O/'templates').glob('*.json'):
  t=json.loads(p.read_bytes());assert t['preparation_only']is True and t['valid_until_utc'].startswith('2020-')
  if p.name.startswith('ACTIVATION'):assert t['ready_for_execution']is False
  else:assert t['accepted']is False and t['root_action_adoption']is False and t['independent_whole_review']is False
 outcome=json.loads((O/'OUTCOME.json').read_bytes());assert outcome['action_authority']is False and outcome['readiness']is False and outcome['new_service_effects']==0
 recheck();closure(O,expected_manifest);physical=sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')]);free=os.statvfs(O).f_bavail*os.statvfs(O).f_frsize;assert physical<=10*1024*1024 and free>=150*1024*1024
 return {'verified':True,'source_manifest_sha256':SOURCE,'closed_payload_files':sum(e['kind']=='file'for e in m['entries'].values()),'closed_directories':sum(e['kind']=='directory'for e in m['entries'].values()),'fixture_inventories':custodies,'fixture_file_full_byte_checks':fixturefiles,'exact_virtual_compressed_files':encoded,'historical_source_versions':histories,'final_source_controls':45,'semantic_policy_units':9,'physical_bytes':physical,'free_bytes_at_check':free,'readiness':False,'action_authority':False}
if __name__=='__main__':
 assert len(sys.argv)==2 and len(sys.argv[1])==64,'Supply independently pinned closed manifest SHA256'
 print(json.dumps(verify(sys.argv[1]),sort_keys=True))
