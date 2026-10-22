"""Sync local five status/log views only from an actually accepted checkpoint."""
from pathlib import Path
import datetime,importlib.util,json,sys,atexit,os
D=Path(__file__).resolve().parent;A=D.parent
sp=importlib.util.spec_from_file_location('current203_checkpoint',D/'checkpoint_math203.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
c,h,rv=v.load();atexit.unregister(h.m.persist_authenticated_tree_cache)
d=D/sys.argv[1];r=v.read(d/'PREPARATION.json');a=v.read(d/'ACCEPTANCE.json')
assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['checkpoint_commit']==r['commit']
root=A.parents[2];rows=[]
for rel in [v.CASE+'CURRENT_CASE_STATUS.json',v.CASE+'RESEARCH_LOG.md',v.PREFIX+'CURRENT_PROGRESS.json',v.PREFIX+'CURRENT_PROGRESS.md',v.PREFIX+'RESEARCH_LOG.md']:
 p=root/rel;post=h.body_at(rel,r['commit']);old=p.read_bytes() if p.exists() else None
 pre=h.body_at(rel,r['expected_main']) if h.lookup(r['parent_tree'],rel) is not None else None
 assert old in [pre,post],'Unexpected local status/log change: '+rel
 assert c.byte_pin(post)==r['selected_files'][rel]
 if old!=post:
  temp=p.with_name(p.name+'.pr203_sync_tmp')
  with temp.open('xb') as out:
   out.write(post);out.flush();os.fsync(out.fileno())
  assert temp.read_bytes()==post
  temp.chmod(0o444);os.replace(temp,p)
 p.chmod(0o444);assert p.read_bytes()==post
 rows.append({'path':rel,'postimage':v.pin(post),'prior_absent_or_exact_prior_or_postimage_guard':True})
j={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'actual_checkpoint':r['commit'],'all_five_local_files_match_accepted_checkpoint':True,'safe_absent_prior_or_postimage_identity_guard':True,'files':rows}
v.save(d/'LOCAL_GLOBAL_FIVE_SYNC.json',v.enc(j));print(json.dumps(j))
