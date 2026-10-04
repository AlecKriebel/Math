"""Strict read-only body/full-mode closure contract for the bounded PR52 source preparation."""
from pathlib import Path
import hashlib,json,re,stat
F=Path(__file__).resolve().parent
MF=F/'SELF_MANIFEST.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def read_json(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate JSON key '+k)
   d[k]=v
  return d
 return json.loads(p.read_bytes(),object_pairs_hook=pairs)
def identity(p):
 st=p.lstat();assert stat.S_ISREG(st.st_mode) and not p.is_symlink();b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'sha256':digest(b),'mode':stat.S_IMODE(st.st_mode)}
def row(r,inside=False):
 assert type(r) is dict and set(r)=={'path','bytes','sha256','mode'}
 assert type(r['path']) is str and type(r['bytes']) is int and r['bytes']>=0 and type(r['mode']) is int and 0<=r['mode']<=0o7777
 assert type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256'])
 p=Path(r['path']);assert p.is_absolute() and str(p)==r['path'] and '..' not in p.parts
 if inside:assert F in p.parents
 return p
def inspect(expected_index,expected_ready,closed=False):
 assert all(type(x) is str and re.fullmatch('[0-9a-f]{64}',x) for x in [expected_index,expected_ready])
 ip=F/'INDEX.json';rp=F/'READY.json';assert digest(ip.read_bytes())==expected_index and digest(rp.read_bytes())==expected_ready
 assert identity(ip)['mode']==identity(rp)['mode']==0o444
 index=read_json(ip);ready=read_json(rp)
 assert set(index)=={'schema','created_utc','payload_files','directories','self_exclusions','full_modes_included','source_only'} and index['schema']=='pr52-original-source-payload-index/v1'
 assert index['full_modes_included'] is True and index['source_only'] is True and index['self_exclusions']==['INDEX.json','READY.json','SELF_MANIFEST.json']
 rows=index['payload_files'];assert type(rows) is list and rows and rows==sorted(rows,key=lambda x:x['path']) and len({x['path'] for x in rows})==len(rows)
 expected=set()
 for r in rows:
  p=row(r,True);assert r['mode']==0o444 and identity(p)==r;expected.add(p)
 directories=index['directories'];assert type(directories) is list and directories==sorted(directories,key=lambda x:x['path']);assert len({x['path'] for x in directories})==len(directories)
 dirset=set()
 for r in directories:
  assert set(r)=={'path','mode'} and type(r['path']) is str and type(r['mode']) is int and r['mode']==0o755
  p=Path(r['path']);assert p==F or F in p.parents;assert str(p)==r['path'] and '..' not in p.parts
  st=p.lstat();assert stat.S_ISDIR(st.st_mode) and not p.is_symlink() and stat.S_IMODE(st.st_mode)==r['mode'];dirset.add(p)
 actual_files=set();actual_dirs={F}
 for p in F.rglob('*'):
  st=p.lstat();assert not p.is_symlink()
  if stat.S_ISREG(st.st_mode):actual_files.add(p)
  elif stat.S_ISDIR(st.st_mode):actual_dirs.add(p)
  else:raise ValueError('nonregular node '+str(p))
 permitted=expected|{ip,rp}|({MF} if closed else set());assert actual_files==permitted and actual_dirs==dirset
 assert ready['schema']=='pr52-original-source-ready/v1' and ready['index_sha256']==expected_index and ready['payload_file_count']==len(rows) and ready['complete_prepared_file_count']==len(rows)+2
 assert ready['self_manifest_present_at_preparer_handoff'] is False and ready['root_personal_read_attestation'] is False and ready['native_acceptance_authority'] is False and ready['remote_action_authority'] is False and ready['independent_new_mathematical_verdict'] is False and ready['source_preparation_completion_percent']==100
 refs=read_json(F/'REFERENCE_BINDINGS.json');assert refs['schema']=='pr52-external-reference-categories/v1' and refs['dated_refs_are_observations_not_future_authority'] is True
 allpaths=[]
 for name in ['fixed_upstream_and_stable_reference_rows','dated_derived_cache_rows','dated_mutable_native_rows']:
  group=refs[name];assert type(group) is list and group==sorted(group,key=lambda x:x['path'])
  for r in group:
   p=row(r);assert not (p==F or F in p.parents);allpaths.append(p)
   if name=='fixed_upstream_and_stable_reference_rows':assert identity(p)==r
 assert len(allpaths)==len(set(allpaths))
 return {'index':index,'ready':ready,'file_bindings':rows+[identity(ip),identity(rp)],'directories':directories,'fixed_external_rows_checked':len(refs['fixed_upstream_and_stable_reference_rows']),'dated_mutable_rows_not_future_authority':len(refs['dated_mutable_native_rows']),'dated_derived_cache_rows_not_future_authority':len(refs['dated_derived_cache_rows'])}
