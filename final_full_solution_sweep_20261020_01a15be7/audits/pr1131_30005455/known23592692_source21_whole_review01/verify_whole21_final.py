"""Read-only independent whole21 enclosure verifier.
External caller must hash THIS complete file, then supply manifest hash/nsmtime.
No services, imports of actors, action/authority creation or filesystem writes.
"""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode)or sys.flags.optimize:raise RuntimeError('use isolated -I -S -B optimize0')
from pathlib import Path
import argparse,base64,hashlib,json,stat
W=Path(__file__).resolve().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def unique(pairs):
  d={}
  for k,v in pairs:need(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(b,object_pairs_hook=unique,parse_constant=lambda _:need(False,'nonfinite JSON'))
def metadata(p):
 s=p.lstat();return {'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'inode':s.st_ino,'device':s.st_dev}
def filepin(p):
 need(stat.S_ISREG(p.lstat().st_mode)and not p.is_symlink(),'regular nonsymlink file '+str(p));b=p.read_bytes()
 return {**metadata(p),'bytes':len(b),'sha256':sha(b)}
def tree(root,exclude=()):
 need(root.is_dir()and not root.is_symlink(),'regular root')
 files={};dirs={'.':metadata(root)}
 for q in sorted(root.rglob('*')):
  rel=str(q.relative_to(root));need(not q.is_symlink(),'symlink in closed namespace')
  if q.is_dir():dirs[rel]=metadata(q)
  elif rel not in exclude:files[rel]=filepin(q)
 return {'files':files,'directories':dirs}
def readpin(x):
 p=Path(x['path']);need(p.is_absolute()and not any(q.is_symlink()for q in[p,*p.parents]),'absolute no-symlink input')
 actual=filepin(p);need(actual=={k:v for k,v in x.items()if k!='path'},'external complete bytes/metadata drift '+str(p));return p.read_bytes()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--manifest-nsmtime',required=True,type=int);a=ap.parse_args()
 p=W/'MANIFEST_WHOLE21.json';raw=p.read_bytes();need(sha(raw)==a.manifest_sha256 and p.stat().st_mtime_ns==a.manifest_nsmtime,'externally caller-pinned manifest')
 m=strict(raw);need(m['schema']=='independent-known23592692-whole21-review-1'and m['status']=='CLEAN_BOUNDED_REVIEW_NO_ACTION_AUTHORITY','complete independent review required')
 need(tree(W,('MANIFEST_WHOLE21.json',))==m['own_namespace'],'complete own namespace bytes/mode/nsmtime/nlink/inode/device')
 need(metadata(p)==m['manifest_metadata_except_mtime']|{'mtime_ns':a.manifest_nsmtime},'manifest inode/mode/link identity')
 for x in m['external_files']:readpin(x)
 for x in m['external_trees']:
  need(tree(Path(x['path']))==x['namespace'],'entire external closed namespace '+x['path'])
 need(m['actual_effects']==0 and m['actual_action_authority']is False,'review grants no actual action')
 inputs=strict((W/'FINAL_C64_SOURCE_AND_REPAIRED_CONTROLLER_INPUTS.json').read_bytes())
 expected={'source21/SOURCE_MANIFEST21.json':'c64fae35c2ea0ebd7213e0791559f3cb5eba9f87a5b6fa8a0fc2038af2da9670','source21/overlay21.py':'b766a845f624a788e69fee8b435ffa0fde24aa3b337ced43b34296798b48ad13','entry21.py':'694fb1692a0d30c5f4d7ea3e782887a88070ec3a980869717a8f5f025d8663ea','native_step21.py':'ca513166da9a72098891b90d44175d2a547c1a530e68595222e5ba8f426b9f7f'}
 for key,x in inputs.items():
  b=base64.b64decode(x['full_source_base64'],validate=True);need(len(b)==x['bytes']and sha(b)==x['sha256']and Path(x['path']).read_bytes()==b,'exact final captured candidate remains actual')
  if key in expected:need(x['sha256']==expected[key],'final explicit source pin')
 mf=strict(base64.b64decode(inputs['source21/SOURCE_MANIFEST21.json']['full_source_base64'],validate=True))
 need(set(mf)=={'overlay21.py','DATA_CONTRACT21.json','SOURCE19_OVERLAY_REPLACEMENTS.json'},'complete finite source21')
 for key,spec in mf.items():
  x=inputs['source21/'+key];need(spec=={'bytes':x['bytes'],'sha256':x['sha256']},'manifest/source consistency')
 for name,count in [('FINAL_GRANT_WIRE_FALSIFIERS01_RESULTS.json',44),('FINAL_C64_CONSTRUCTOR_BINDINGS01_RESULTS.json',46)]:
  r=strict((W/name).read_bytes());need(r['status']=='PASS'and r['count']==count and len(r['checks'])==count and r['actual_effects']==0,'complete final own controls')
  need(r['source21_sha256']==expected['source21/SOURCE_MANIFEST21.json']and r['overlay21_sha256']==expected['source21/overlay21.py'],'final controls/source linkage')
 parent=strict((W/'ROOT_PARENT03_CUSTODY_RESULTS.json').read_bytes());need(parent['status']=='PASS','outer-parent custody model')
 controller=strict((W/'FINAL_CONTROLLER_SAME_BUFFER_RESULTS01.json').read_bytes())
 need(controller['status']=='PASS'and controller['count']==5 and len(controller['checks'])==5 and controller['actual_effects']==0,'four final controller controls plus historical reproducer')
 need(controller['final_controller_sha256']==expected['native_step21.py']and controller['checks'][0]['historical_gap_reproduced']is True,'final controller/source linkage')
 # Every original child result preserves complete binary stdout/stderr first.
 native_count=0
 for q in W.glob('*_ORIGINAL_NATIVE.json'):
  v=strict(q.read_bytes());prefix=q.name.removesuffix('_ORIGINAL_NATIVE.json')
  for role in ['STDOUT','STDERR']:
   b=(W/(prefix+'_'+role+'.bin')).read_bytes();need(v[role]=={'bytes':len(b),'sha256':sha(b)},'original transport bytes '+prefix)
  need(type(v['returncode'])is int and len(v['argv'])>=5 and v['argv'][1:4]==['-I','-S','-B'],'complete native argv/return code')
  need('started_at'in v and 'finished_at'in v,'aware UTC native chronology')
  native_count+=1
 need(native_count==m['original_native_count'],'all original native envelopes retained')
 prep=m['preparation'];need(prep['source21_sha256']==expected['source21/SOURCE_MANIFEST21.json'],'sealed preparation source')
 cold=strict((W/prep['cold_native']).read_bytes());need(cold['returncode']==0,'actual cold native success')
 cb=(W/prep['cold_stdout']).read_bytes();cr=strict(cb);need(cr['status']=='PASS','read-only final preparation cold result')
 need(cr==prep['cold_result'],'complete cold result adopted')
 print(json.dumps({'status':'PASS','manifest_sha256':sha(raw),'files':len(m['own_namespace']['files']),'directories':len(m['own_namespace']['directories']),'external_files':len(m['external_files']),'external_trees':len(m['external_trees']),'own_final_controls':90,'parent_custody_controls':5,'controller_final_controls':4,'original_native_envelopes':native_count,'actual_effects':0,'actual_action_authority':False},sort_keys=True))
if __name__=='__main__':main()
