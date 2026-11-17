"""Read frozen stage/audit data only; no build, Git or publication action."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V=P/'verification'
OUT=V/'root-gram-thompson-d4-overlay-adoption-20261117.json'
assert not OUT.exists()
specs=[
 ('gram-thompson-d4-overlay-sol-20261117',41,6,{'MANIFEST.json':'1206c4ca98ec65697440130c0b13534291804be09369acb05e7984f67f087fd9','SEAL.json':'8fa752e98d298d35b84f83d36c836e049f3afcbfb4f8987d0d218f36227cc554','FINAL.json':'a8a21cbbd909f13d44dfa1ba35a10758acad996a831eaa756d8f053f1bbd4762'}),
 ('gram-thompson-d4-overlay-audit-sol-20261117',12,0,{'MANIFEST.json':'d403419579bc571f86f821d11f02993cfad2de5de0633d43404649028d019110','FINAL.json':'dd7eae47db1dfb53e788aa60b5853904ec1d885b9a6ca529b25a126379c5395c'}),
 ('gram-thompson-d4-overlay-audit-corrected-sol-20261117',17,0,{'MANIFEST.json':'6bc8e0ed3031c2fc8cdf84ee603c592c27bdb605c26214b48b38636ac9d2dd45','FINAL.json':'c10619359674ceaa599d80dda8d66557d11d5c0e01e8c6855fb1a5d2bf367d7c'})]
sha=lambda b:hashlib.sha256(b).hexdigest()
def snapshot(root):
 d={}
 for p in [root]+sorted(root.rglob('*')):
  s=p.lstat();assert stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode)
  rel=p.relative_to(root).as_posix()
  row={'path':rel,'kind':'directory' if p.is_dir() else 'file','mode':oct(stat.S_IMODE(s.st_mode)),
       'mtime_ns':s.st_mtime_ns,'ctime_ns':s.st_ctime_ns,
       'hidden':any(x.startswith('.') for x in Path(rel).parts if x!='.'),
       'empty':not any(p.iterdir()) if p.is_dir() else s.st_size==0}
  if p.is_file():
   raw=p.read_bytes();row.update(bytes=len(raw),SHA256=sha(raw))
  d[rel]=row
 return d
before={};packets=[]
for name,nfiles,ndirs,pins in specs:
 root=V/name;actual=snapshot(root);before[name]=actual
 assert sum(v['kind']=='file' for v in actual.values())==nfiles
 assert sum(v['kind']=='directory' for v in actual.values())==ndirs+1
 for f,h in pins.items():assert actual[f]['SHA256']==h,(name,f)
 m=json.loads((root/'MANIFEST.json').read_bytes())
 if 'entries' in m:
  rows=m['entries'];excluded=set(m['terminal_content_hash_exclusions_exact'])
  assert excluded=={'MANIFEST.json','SEAL.json'}
  assert {r['path'] for r in rows}==set(actual) and len(rows)==len(actual)
 else:
  rows=m['payload_files']+m['directories'];excluded=set(m['exact_already_created_terminal_recursive_hash_exclusions'])
  assert excluded=={'MANIFEST.json','FINAL.json'} and not m['other_exclusions']
  assert {r['path'] for r in rows}|excluded==set(actual)
  assert len({r['path'] for r in rows})==len(rows)
  for f,mode in m['terminal_modes'].items():assert int(actual[f]['mode'],8)==int(mode,8)
 for row in rows:
  rel=row['path'];a=actual[rel]
  for k,v in row.items():
   if k=='content_hash_exclusion':assert rel in excluded and isinstance(v,str)
   elif k=='mode':assert int(a[k],8)==int(v,8),(name,rel,k)
   else:assert a[k]==v,(name,rel,k)
  if a['kind']=='file' and rel not in excluded:assert isinstance(row['SHA256'],str) and len(row['SHA256'])==64
 packets.append({'path':'verification/'+name,'files':nfiles,'child_directories':ndirs,'external_controls':pins})
for name,*unused in specs:assert snapshot(V/name)==before[name]
f=json.loads((V/specs[2][0]/'FINAL.json').read_bytes())
assert f['reader_exit']==0 and f['reader_invocations']==1 and f['reader_retries']==0
assert f['whole_fixed_before_after_exact'] and f['complete_forward_reverse_buffers_exact']
assert f['whole_projected_files_childdirs_articles_XML']==[816,390,136,137] and f['targets_A_M']==[13,2]
assert f['original_failed_lane']['reader_exit']==1 and f['original_failed_lane']['original_no_closing_guard_or_retro_PASS']
r={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ACCEPTED_PRIVATE_OVERLAY_ONLY','packets':packets,
   'authenticated_files':70,'child_directories':6,'all_payload_bytes_individual_modes_times_topology_exact':True,
   'root_all539producer_source_lines_all3actual_articles_TARGETS_spans_and_new_aggregate_units_personally_read':True,
   'full_corrected_REPORT_FINAL_RESULTS_SCHEMA_DISPOSITION_and_adversarial_review_personally_read':True,
   'original_failed12_packet_preserved_not_retro_PASS':True,'corrected_independent_audit_one_exit0':True,
   'target_changes':[13,2],'projected_files_childdirs_articles_XML':[816,390,136,137],
   'private_stage_percent':100,'full_physical_website_copy':False,'scientific_Git_network_helper_executions':0,
   'publication_certificate':False,'future_action_authority':False,'page_publication_date':None,
   'AA':None,'redirect':None,'follow_up':None}
OUT.write_text(json.dumps(r,indent=2)+'\n')
raw=OUT.read_bytes();print(json.dumps({'authenticated_files':70,'childdirs':6,'bytes':len(raw),'SHA256':sha(raw),'path':str(OUT)}))
