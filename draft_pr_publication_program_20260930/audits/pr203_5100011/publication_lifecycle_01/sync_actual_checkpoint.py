"""Synchronize five local status/log views only after actual remote acceptance."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys,os
if sys.flags.optimize:raise RuntimeError('Publication operations require ordinary Python; optimization removes assertions')
A=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('finish203_sync',A/'publication_lifecycle_01/finish203.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
c,h,rv,n=v.load();m=v.m
d=A/sys.argv[1];r=m.read(d/'PREPARATION.json');a=m.read(d/'ACCEPTANCE.json')
assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit']
root=A.parents[2];rows=[]
for rel in [m.CASE+'CURRENT_CASE_STATUS.json',m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.json',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:
 p=root/rel;pre=h.body_at(rel,r['expected_main']);post=h.body_at(rel,r['commit']);old=p.read_bytes()
 assert old in [pre,post],'Unexpected local status/log change: '+rel
 assert c.byte_pin(post)==r['selected_files'][rel]
 if old!=post:
  tmp=p.with_name(p.name+'.pr203_sync_tmp')
  with tmp.open('xb') as out:out.write(post);out.flush();os.fsync(out.fileno())
  assert tmp.read_bytes()==post
  tmp.chmod(0o444);os.replace(tmp,p)
 p.chmod(0o444);assert p.read_bytes()==post
 rows.append({'path':rel,'postimage':m.pin(post),'prior_or_postimage_guard':True})
j={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'actual_checkpoint':r['commit'],'all_five_local_files_match_accepted_checkpoint':True,'safe_prior_or_postimage_identity_guard':True,'files':rows}
p=d/'LOCAL_GLOBAL_FIVE_SYNC.json'
with p.open('x') as out:json.dump(j,out,indent=2);out.write('\n')
p.chmod(0o444);print(json.dumps(j))
