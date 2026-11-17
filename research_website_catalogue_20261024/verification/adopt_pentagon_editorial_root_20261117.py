"""Authenticate three frozen private editorial packets as finite data only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OUT=P/'verification/root-pentagon-full-fifth-torsion-editorial-adoption-20261117.json'
assert not OUT.exists()
specs=[
 ('pentagon-full-fifth-torsion-editorial-sol-20261117','FINAL_MANIFEST.json','e31cdbc3460f63e135e075fbb21bff87e72ae5cbbedb71ce222b822f29645584','0c6838af4b2acf9065b89587f8701b692be78caf974b67e6e5dbb06899a713aa',19,1),
 ('pentagon-full-fifth-torsion-editorial-fact-sol-20261117','MANIFEST.json','0c716dbc8754a9edb056d56f3d9a57209952642b44bcc4ea6dff2d0897cdc685','e1e0e81e40030f4668b6fd00065e381687d1201b34b388ecb06502baea1fe99b',12,0),
 ('pentagon-full-fifth-torsion-legacy-sol-20261117','MANIFEST.json','466ee7fca54912ab7a58eafb913d7634d107855e1a6cd9926697fea3c83dddf6','afcb8766f8d64d0ef24034ad310dce93bcc11854ebaa3386f28bb0fe95420dd1',16,1)]
sha=lambda b:hashlib.sha256(b).hexdigest()
def snapshot(root):
 result={}
 for path in [root]+sorted(root.rglob('*')):
  info=path.lstat();assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
  row={'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,
       'kind':'directory' if path.is_dir() else 'file','empty':not any(path.iterdir()) if path.is_dir() else info.st_size==0}
  if path.is_file():
   b=path.read_bytes();row.update(bytes=len(b),SHA256=sha(b),MD5=hashlib.md5(b).hexdigest())
  result[path.relative_to(root).as_posix()]=row
 return result
packets=[];before={}
for name,mname,msha,fsha,nfiles,ndirs in specs:
 root=P/'verification'/name;actual=snapshot(root);before[name]=actual
 assert actual[mname]['SHA256']==msha and actual['FINAL.json']['SHA256']==fsha
 m=json.loads((root/mname).read_bytes())
 assert m['file_count']==nfiles and m['child_directory_count']==ndirs
 files={k for k,v in actual.items() if v['kind']=='file'}
 dirs={k for k,v in actual.items() if v['kind']=='directory'}
 assert len(files)==nfiles and len(dirs)==ndirs+1
 assert actual['.']['mode']==m['root_mode']
 terminals={r['path']:r for r in m['terminal_pair']}
 assert set(terminals)=={mname,'FINAL.json'}
 assert set(m['payload_files'])|set(terminals)==files
 for rel,row in m['payload_files'].items():
  assert actual[rel]['kind']=='file'
  for k,v in row.items():assert actual[rel][k]==v,(name,rel,k)
 for rel,row in terminals.items():
  assert row['recursive_hash_excluded'] is True
  assert actual[rel]['bytes']==row['bytes'] and actual[rel]['mode']==row['mode']
 assert set(m['directories'])|{'.'}==dirs
 for rel,row in m['directories'].items():
  fields={'mode':row} if isinstance(row,str) else row
  for k,v in fields.items():assert actual[rel][k]==v,(name,rel,k)
 assert sorted(k for k in actual if k!='.' and any(x.startswith('.') for x in Path(k).parts))==sorted(m['hidden_paths'])
 assert sorted(k for k in files if actual[k]['empty'])==sorted(m['empty_files'])
 assert sorted(k for k in dirs if k!='.' and actual[k]['empty'])==sorted(m['empty_directories'])
 packets.append({'path':'verification/'+name,'files':nfiles,'child_directories':ndirs,
                 'external_controls':{mname:msha,'FINAL.json':fsha}})
for name,*unused in specs:assert snapshot(P/'verification'/name)==before[name]
record={'UTC':datetime.now(timezone.utc).isoformat(),'record':'23137834','row':170,
 'status':'ACCEPTED_PRIVATE_EDITORIAL_ONLY','packets':packets,'authenticated_files':47,'child_directories':2,
 'whole_before_after_bytes_individual_modes_topology_exact':True,
 'actual_whole_HTML_MODEL_Bib_writer_fact_legacy_reports_FINALs_personally_read':True,
 'scientific_review':'papers/23137834/reviews/root-continuation-20261117/ROOT_REVIEW.md',
 'scientific_review_SHA256':'acd210977221457737949db0684d2c60c289fef197b6b4dcaa26d87c8aa99599',
 'original_full_claims_abstract_native_assets_and_CC_BY_rights_retained':True,
 'legacy':'No genuine same-work article in physical/native/released fixed collections; no global absence claim',
 'private_copy_percent':100,'follow_up':None,'canonical':None,'AA':None,'redirect':None,
 'publication_certificate':False,'future_action_authority':False,
 'scientific_Git_network_helper_executions_by_this_reader':0}
OUT.write_text(json.dumps(record,indent=2)+'\n')
raw=OUT.read_bytes();print(json.dumps({'files_authenticated':47,'childdirs':2,'bytes':len(raw),'SHA256':sha(raw),'path':str(OUT)}))
