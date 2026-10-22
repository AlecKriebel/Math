"""Direct chunk custody cold replay; no original ZIP ever existed."""
from pathlib import Path
import argparse,datetime,gzip,hashlib,json,os,stat,tempfile,zipfile,re,math
ROOT=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def verify(scratch=None):
 if scratch is None:
  need(not(ROOT/'MANIFEST.json').exists(),'Closed packet requires outside scratch');scratch=ROOT/'private'
 else:
  scratch=Path(scratch).resolve();need(scratch!=ROOT and ROOT not in scratch.parents,'Outside scratch required')
 need(scratch.is_dir(),'Existing scratch directory')
 stats={'cases':0,'physical_files':0,'physical_bytes':0,'directories_including_roots':0,'virtual_paths':0,'virtual_distinct_bodies':set(),'exact_physical_bytes_modes_nsmtimes_closure':True,'original_ZIP_containers_created_or_reconstructed':False,'original_inode_topology_promised':False,'historically_partial_virtual_cases':[],'max_allocated_sample_bytes':0,'semantic_original_checks':[],'volatile_test_spy_omissions_not_reconstructed':[]}
 def sample():
  seen=set();amount=0
  for q in [ROOT,*ROOT.rglob('*')]:
   st=q.lstat();key=st.st_dev,st.st_ino
   if key not in seen:amount+=st.st_blocks*512;seen.add(key)
  stats['max_allocated_sample_bytes']=max(stats['max_allocated_sample_bytes'],amount)
  need(amount<10*1024*1024,'Cold replay physical cap')
  return amount
 sample()
 used=set()
 reader_ns={'__file__':str(ROOT/'chunk_reader17.py'),'__name__':'cold_reader'}
 exec(compile((ROOT/'chunk_reader17.py').read_bytes(),str(ROOT/'chunk_reader17.py'),'exec',dont_inherit=True,optimize=0),reader_ns)
 z=reader_ns['Reader']()
 need(sample()+65536<10*1024*1024,'Preflight scratch allocation cap')
 need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024+65536,'Preflight scratch reserve')
 with tempfile.TemporaryDirectory(prefix='custody17_',dir=scratch)as tmp:
  names=z.keys
  for key in names:need(sha(z.get(key))==key,'Chunk hash')
  def body(pin):
   used.update(pin['chunks']);b=b''.join(z.get(k)for k in pin['chunks'])
   need(len(b)==pin['bytes'],'Body length');return b
  def typed(a,b):
   if type(a)is not type(b):return False
   if type(a)is dict:return set(a)==set(b)and all(typed(a[k],b[k])for k in a)
   if type(a)is list:return len(a)==len(b)and all(typed(x,y)for x,y in zip(a,b))
   if type(a)is float:return math.isfinite(a)and math.isfinite(b)and a==b
   return a==b
  for recipe in sorted((ROOT/'private/case_archives_phase17').glob('*.case.json.gz')):
   index=json.loads(gzip.decompress(recipe.read_bytes()));need(index['direct_custody_no_original_ZIP_created'],'Wrong custody kind')
   if not index.get('historical_virtual_scope_complete',True):stats['historically_partial_virtual_cases'].append({'case':index['case'],'cohort':index.get('cohort'),'scope':'all physical bytes retained; terminated historical process VFS unavailable'})
   files=index['files'];dirs=index['directories'];need('.'in dirs,'Root metadata missing')
   bound=sum(((v['bytes']+4095)//4096)*4096+4096 for v in files.values())+8192*len(dirs)+65536
   need(sample()+bound<10*1024*1024,'Preflight reconstructed case physical cap')
   need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024+bound,'Preflight reconstructed case reserve')
   base=Path(tmp)/'case';base.mkdir()
   for name in sorted(set(dirs)-{'.'},key=lambda n:n.count('/')):
    need(not Path(name).is_absolute()and'..'not in Path(name).parts,'Unsafe directory');(base/name).mkdir()
   for name,pin in files.items():
    need(not Path(name).is_absolute()and'..'not in Path(name).parts,'Unsafe file')
    b=body(pin);need(sha(b)==pin['sha256'],'Physical body hash')
    q=base/name;q.write_bytes(b);os.chmod(q,pin['mode']);os.utime(q,ns=(pin['mtime_ns'],pin['mtime_ns']))
    stats['physical_files']+=1;stats['physical_bytes']+=len(b)
   for name,pin in sorted(dirs.items(),key=lambda x:x[0].count('/'),reverse=True):
    q=base if name=='.'else base/name;os.chmod(q,pin['mode']);os.utime(q,ns=(pin['mtime_ns'],pin['mtime_ns']))
   sample()
   need({q.relative_to(base).as_posix()for q in base.rglob('*')}==set(files)|(set(dirs)-{'.'}),'Restored full namespace')
   for name,pin in files.items():
    q=base/name;s=q.stat();need(sha(q.read_bytes())==pin['sha256']and stat.S_IMODE(s.st_mode)==pin['mode']and s.st_mtime_ns==pin['mtime_ns'],'Physical exact metadata/bytes')
   for name,pin in dirs.items():
    q=base if name=='.'else base/name;s=q.stat();need(stat.S_IMODE(s.st_mode)==pin['mode']and s.st_mtime_ns==pin['mtime_ns'],'Directory/root metadata')
   # Independently compare the complete typed supplied original to its
   # METHOD's physical actor receipt. Earlier identical GETs never satisfy a
   # mutation original. Intentionally held15 baselines must remain missing.
   spy_name='ADVERSARY_ONLY_RETURNED_BODY_SPY.json'
   if spy_name in files:
    def eq(a,b):
     if type(a)is not type(b):return False
     if type(a)is dict:return set(a)==set(b)and all(eq(a[k],b[k])for k in a)
     if type(a)is list:return len(a)==len(b)and all(eq(x,y)for x,y in zip(a,b))
     if type(a)is float:return math.isfinite(a)and math.isfinite(b)and a==b
     return a==b
    label=index['case'];old=label.startswith(('held15_post_fsync_fact_','held16_unicode_'))
    match=re.fullmatch(r'(?:valid_)?original_(create|upload|update|publish)_before_failed_.+',label)
    kind=label.rsplit('_',1)[-1]if old or label.startswith(('after_fsync_','sdk_unicode_'))else match.group(1)if match else None
    need(kind in {'create','upload','update','publish','get'},'Unrecognized semantic original recipe')
    spy=json.loads((base/spy_name).read_bytes());found=[]
    holds=[json.loads((base/n).read_bytes())for n in files if n.startswith(('runtime/CONSUMED_RESPONSE17_HOLD_','runtime/CONSUMED_RESPONSE16_HOLD_'))]
    references={v['path']for h in holds for v in h['all_consumed_response_custody']if v['kind']==kind}
    for name in files:
     if name.startswith('private/service_original_')and name.endswith('.json'):
      value=json.loads((base/name).read_bytes())
      supplied=str(ROOT/'private'/index['cohort']/index['case']/name)
      if value['kind']==kind and eq(value['response'],spy)and(old or supplied in references):found.append((name,value))
    need(len(found)==(0 if old else 1),'Complete method-specific original mismatch')
    detail={'case':label,'kind':kind,'whole_actual_original_matches':len(found),'expected_historical_missing_original':old}
    if not old:
     name,value=found[0];original=str(ROOT/'private'/index['cohort']/index['case']/name)
     holds=[json.loads((base/n).read_bytes())for n in files if n.startswith(('runtime/CONSUMED_RESPONSE17_HOLD_','runtime/CONSUMED_RESPONSE16_HOLD_'))]
     refs=[v for h in holds for v in h['all_consumed_response_custody']if v['path']==original and v['kind']==kind]
     need(refs,'Original receipt missing from persistent HOLD')
     actual={'bytes':len((base/name).read_bytes()),'sha256':sha((base/name).read_bytes())}
     need(all(v['durable_write_returned']is True for v in refs),'Durable first receipt not recorded')
     for v in refs:
      need(type(v['expected_integrity_verified'])is bool,'Invalid integrity status')
      need((v['pin']==actual)==v['expected_integrity_verified'],'Expected-byte integrity status inconsistent')
     if kind!='get':
      fact=value['known_service_fact'];need(fact['kind']==kind and type(fact['requested_or_known_id'])is int and fact['requested_or_known_id']==777,'Combined known identity missing')
      need(fact['sources_sha256']=='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803','Combined known fact source changed')
      need(fact['manifest']==str(ROOT.parent/'operations/proposed/preprint/zenodo-deposit.json'),'Combined canonical manifest changed')
     if label.startswith('sdk_unicode_'):
      raw=(base/name).read_bytes()
      need(raw==(json.dumps(value,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii')and all(b<128 for b in raw),'Unicode original first-receipt bytes not exact ASCII escaped')
      need(all(v['expected_integrity_verified']is True for v in refs),'Unicode byte expectation failed')
     detail.update(first_receipt_referenced=True,combined_known_fact=kind!='get',expected_integrity_verified=refs[0]['expected_integrity_verified'],actual_pin=actual)
    stats['semantic_original_checks'].append(detail)
   component='COMPONENT_ONLY_PARSED_RESPONSE_ASCII.json'
   if component in files:
    supplied=json.loads((base/component).read_bytes());matches=[]
    for name in files:
     if name.startswith('private/service_original_')and name.endswith('.json'):
      value=json.loads((base/name).read_bytes())
      if value['kind']=='create'and typed(value['response'],supplied):matches.append((name,value))
    need(len(matches)==1,'Component original mismatch')
    name,value=matches[0];raw=(base/name).read_bytes()
    need(raw==(json.dumps(value,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii')and all(x<128 for x in raw),'Component actual representation mismatch')
    stats['semantic_original_checks'].append({'case':index['case'],'kind':'component_create','whole_actual_original_matches':1,'phase_invocations':0,'all2056_parser_strings_retained':True})
   for digest,pin in index['virtual_bodies'].items():
    need(sha(body(pin))==digest,'Virtual body hash');stats['virtual_distinct_bodies'].add(digest)
   need(set(index['virtual_paths'].values())==set(index['virtual_bodies']),'Virtual lookup closure')
   for name in sorted(dirs,key=lambda n:n.count('/'),reverse=True):os.chmod(base if name=='.'else base/name,0o700)
   for name in files:(base/name).unlink()
   for name in sorted(set(dirs)-{'.'},key=lambda n:n.count('/'),reverse=True):(base/name).rmdir()
   base.rmdir();stats['cases']+=1;stats['directories_including_roots']+=len(dirs);stats['virtual_paths']+=len(index['virtual_paths'])
   need(os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024,'Free reserve')
  need(used==set(names),'Unreferenced/missing chunk')
 z.close()
 sample()
 stats['virtual_distinct_bodies']=len(stats['virtual_distinct_bodies']);stats['at']=datetime.datetime.now(datetime.timezone.utc).isoformat();stats['verifier_sha256']=sha(Path(__file__).read_bytes());return stats
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--scratch');a=p.parse_args();print(json.dumps(verify(a.scratch),indent=2))
