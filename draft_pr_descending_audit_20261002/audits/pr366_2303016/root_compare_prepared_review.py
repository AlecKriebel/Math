"""Read every full prepared capture and independently reexecute all64 commands."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];F=A/'clean_final_adversary';V=A/'root_live_replay_private';V.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();checks=[];captures=[]
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
o=json.loads((F/'PREPARED_HEAD_RECEIPT.json').read_bytes());ck(o['prepared_head']=='7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8' and o['literal_base_local_remote_main']=='04c40062219cc9fa20834d98db2b270fdad1a848','literal reviewed pair');ck(len(o['commands'])==64,'entire64 command inventory')
def normalize_repos(old,fresh):
 changes=[]
 for side in ['head','base']:
  a,b=old[side]['repo'],fresh[side]['repo'];ck(a['full_name']==b['full_name']=='AlecKriebel/Math','only target repository metadata')
  ck(a['open_issues']==a['open_issues_count'] and b['open_issues']==b['open_issues_count'],'coherent whole repository issue counts')
  for key in ['open_issues','open_issues_count','pushed_at']:
   if a[key]==b[key]:continue
   if key=='pushed_at':
    ck(isinstance(a[key],str) and isinstance(b[key],str),'metadata timestamp type');datetime.fromisoformat(a[key].replace('Z','+00:00'));datetime.fromisoformat(b[key].replace('Z','+00:00'))
   else:ck(type(a[key]) is int and type(b[key]) is int and a[key]>=0 and b[key]>=0,'metadata count type')
   changes.append({'path':side+'.repo.'+key,'previous':a[key],'current':b[key]});b[key]=a[key]
 return changes
for i,c in enumerate(o['commands']):
 old={}
 for stream in ['stdout','stderr']:
  stored=(F/c[stream+'_path']).read_bytes();ck(sha(stored)==c[stream+'_stored_sha256'],'every stored capture '+c['label']+'/'+stream);b=gzip.decompress(stored) if c['compressed'] else stored;ck(len(b)==c[stream+'_bytes'] and sha(b)==c[stream+'_sha256'],'every full logical capture '+c['label']+'/'+stream);old[stream]=b
 ck(c['exit']==0,'old complete exit '+c['label']);z=subprocess.run(c['argv'],cwd=R,capture_output=True);ck(z.returncode==0 and z.stderr==old['stderr'],'fresh full exit/stderr '+c['label']);changes=[]
 if z.stdout!=old['stdout'] and c['argv'][:2]==['gh','api'] and c['argv'][-1]=='repos/AlecKriebel/Math/pulls/366':
  a=json.loads(old['stdout']);b=json.loads(z.stdout);changes=normalize_repos(a,b);ck(a==b,'entire PR objects exact except specified coherent repository metadata')
 else:ck(z.stdout==old['stdout'],'every fresh stdout byte '+c['label'])
 streams={}
 for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=V/(str(i)+'_'+c['label']+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'whole fresh lossless stream '+c['label']+'/'+stream);streams[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'gzip_bytes':p.stat().st_size,'gzip_sha256':sha(p.read_bytes())}
 captures.append({'label':c['label'],'argv':c['argv'],'exit':z.returncode,'only_repository_metadata_changes':changes,**streams})
ck(o['queue']['changed_cells']==[8,9] and o['queue']['line']==406 and o['queue']['whole_non_target_bytes_preserved'] is True,'whole queue contract')
ck(o['test_merge']['parents']==[o['literal_base_local_remote_main'],o['prepared_head']] and o['test_merge']['tree']=='194ef7dbd1f1a0d050400e68a61c6d166a54ef6e','whole prepared actual test merge')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ALL64_PREPARED_CAPTURES_AND_INDEPENDENT_FULL_REEXECUTION','check_count':len(checks),'checks':checks,'captures':captures,'prepared_receipt_sha256':sha((F/'PREPARED_HEAD_RECEIPT.json').read_bytes()),'reviewed_head':o['prepared_head'],'base':o['literal_base_local_remote_main'],'all_math_body_refs_and_scope_literal':True,'only_permitted_normalization':'If changed, six explicitly typed coherent head/base repo open_issues/open_issues_count/pushed_at leaves; full original/fresh objects and streams retained, all remaining fields exact','program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_prepared_comparison_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','reviewed_head','base']},indent=2))
