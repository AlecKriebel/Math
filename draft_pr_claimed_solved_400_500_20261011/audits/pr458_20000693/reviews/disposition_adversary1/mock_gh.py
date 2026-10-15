#!/usr/bin/env python3
"""Network-free gh test double. Every state write is a private fixture write."""
import base64, hashlib, json, os, sys
from pathlib import Path
HEAD='87a39f7b4e5ef81aacf98464f86586cc95684d7f'
NEW='c'*40
REPO='AlecKriebel/Math'
QUEUE='unsolved_math_prioritization/QUEUE.md'

def main():
 p=Path(os.environ['PRIVATE_GH_STATE']); s=json.loads(p.read_text())
 args=sys.argv[1:]
 if args[:1]!=['api'] or not args[1].startswith('repos/'+REPO+'/'): raise RuntimeError('Unexpected command')
 e=args[1][len('repos/'+REPO+'/'):]; data=None; method='GET'
 if '--input' in args: data=json.loads(sys.stdin.read()); method=args[args.index('--method')+1]
 s['trace'].append({'endpoint':e,'method':method,'payload':data})
 scenario=s.get('scenario',{})
 fail=None
 if e=='pulls/458':
  s['pr_reads']+=1
  out={'state':'open','draft':True,'head':{'sha':HEAD,'ref':'dot/math-20000693','repo':{'full_name':REPO}},'base':{'ref':'main','repo':{'full_name':REPO}}}
  if s['pr_reads']>=scenario.get('change_at_pr_read',1):
   for key,value in scenario.get('pr_changes',{}).items():
    obj=out; parts=key.split('.')
    for part in parts[:-1]: obj=obj[part]
    obj[parts[-1]]=value
 elif e.startswith('git/ref/heads/'):
  s['ref_reads']+=1; out={'object':{'sha':s['ref']}}
  if s['ref_reads']>=scenario.get('change_at_ref_read',1) and 'ref_changed_to' in scenario: out={'object':{'sha':scenario['ref_changed_to']}}
 elif e=='git/commits/'+HEAD: out={'sha':HEAD,'tree':{'sha':'a'*40}}
 elif e=='git/trees/'+'a'*40: out={'tree':[{'path':'unsolved_math_prioritization','mode':'040000','type':'tree','sha':'b'*40}]}
 elif e=='git/trees/'+'b'*40:
  out={'tree':[{'path':'QUEUE.md','mode':scenario.get('queue_mode','100644'),'type':scenario.get('queue_type','blob'),'sha':s['original_blob']}]}
  if scenario.get('duplicate_tree'): out['tree']*=2
 elif e.startswith('git/blobs/'):
  sha=e.rsplit('/',1)[1]; content=s['blobs'][sha]
  if sha!=s['original_blob'] and scenario.get('wrong_blob_readback'): content=base64.b64encode(b'wrong').decode()
  out={'content':content,'encoding':'base64'}
 elif e.startswith('contents/'):
  out={'type':'file','encoding':'base64','path':e[len('contents/'):].split('?ref=')[0],'content':s['synthesis_b64']}
  out.update(scenario.get('contents_changes',{}))
 elif e=='git/blobs' and method=='POST':
  raw=base64.b64decode(data['content'],validate=True); sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
  s['blobs'][sha]=data['content']; s['new_blob']=sha; out={'sha':sha}
 elif e=='git/trees' and method=='POST':
  s['created_tree']=data; out={'sha':'d'*40}
 elif e=='git/commits' and method=='POST':
  s['created_commit']=data; out={'sha':NEW}
 elif e=='compare/'+HEAD+'...'+NEW:
  out={'files':[{'filename':x} for x in scenario.get('comparison_paths',[QUEUE])]}
 elif e.startswith('git/refs/heads/') and method=='PATCH':
  if data!={'sha':NEW,'force':False}: raise RuntimeError('Unexpected ref mutation')
  if scenario.get('patch_updates',True): s['ref']=NEW
  out={'object':{'sha':s['ref']}}
  if scenario.get('patch_error'): fail='simulated uncertain PATCH'
  if scenario.get('patch_bad_json'): s['emit_bad_json']=True
 else: raise RuntimeError('Unmocked endpoint '+e)
 if scenario.get('fail_endpoint')==e: fail='simulated endpoint failure'
 p.write_text(json.dumps(s,indent=2)+'\n')
 if fail: print(fail,file=sys.stderr); return 1
 if s.get('emit_bad_json') and method=='PATCH': print('{');return 0
 print(json.dumps(out)); return 0
if __name__=='__main__': sys.exit(main())
