#!/usr/bin/env python3
"""Private network-free GitHub model with independently recorded requests."""
import base64,hashlib,json,os,sys
from pathlib import Path
HEAD='87a39f7b4e5ef81aacf98464f86586cc95684d7f';NEW='c'*40;REPO='AlecKriebel/Math';QUEUE='unsolved_math_prioritization/QUEUE.md'
p=Path(os.environ['REVIEW_PRIVATE_STATE']);s=json.loads(p.read_text());a=sys.argv[1:]
if len(a)<2 or a[0]!='api' or not a[1].startswith('repos/'+REPO+'/'):raise RuntimeError('Unmocked command')
e=a[1][len('repos/'+REPO+'/'):];method='GET';data=None
if '--input' in a:
 method=a[a.index('--method')+1];data=json.loads(sys.stdin.read())
s['requests'].append({'endpoint':e,'method':method,'payload':data});cfg=s['config'];rc=0;raw=None
if e=='pulls/458':
 s['pr_reads']+=1;o={'state':'open','draft':True,'head':{'sha':HEAD,'ref':'dot/math-20000693','repo':{'full_name':REPO}},'base':{'ref':'main','repo':{'full_name':REPO}}}
 if s['pr_reads']>=cfg.get('pr_stage',99):
  x=o;parts=cfg['pr_field'].split('.')
  for k in parts[:-1]:x=x[k]
  x[parts[-1]]=cfg['pr_value']
elif e.startswith('git/ref/heads/'):
 s['ref_reads']+=1;o={'object':{'sha':s['ref']}}
 if s['ref_reads']>=cfg.get('ref_stage',99):o['object']['sha']='e'*40
elif e=='git/commits/'+HEAD:o={'sha':HEAD,'tree':{'sha':'a'*40}}
elif e=='git/trees/'+'a'*40:o={'tree':[{'path':'unsolved_math_prioritization','type':'tree','mode':'040000','sha':'b'*40}]}
elif e=='git/trees/'+'b'*40:
 o={'tree':[{'path':'QUEUE.md','type':cfg.get('queue_type','blob'),'mode':cfg.get('queue_mode','100644'),'sha':s['original_blob']}]}
 if cfg.get('duplicate_tree'):o['tree']*=2
elif e.startswith('git/blobs/'):
 sha=e.rsplit('/',1)[1];content=s['blobs'][sha]
 if sha!=s['original_blob'] and cfg.get('wrong_blob'):content=base64.b64encode(b'wrong blob').decode()
 o={'sha':sha,'encoding':'base64','content':content}
elif e.startswith('contents/'):
 o={'type':'file','path':e[9:].split('?ref=')[0],'encoding':'base64','content':s['synthesis']};o.update(cfg.get('published_changes',{}))
elif e=='git/blobs' and method=='POST':
 b=base64.b64decode(data['content'],validate=True);sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();s['blobs'][sha]=data['content'];s['new_blob']=sha;o={'sha':sha}
elif e=='git/trees' and method=='POST':s['new_tree']=data;o={'sha':'d'*40}
elif e=='git/commits' and method=='POST':s['new_commit']=data;o={'sha':NEW}
elif e=='compare/'+HEAD+'...'+NEW:o={'files':[{'filename':x} for x in cfg.get('compare_paths',[QUEUE])]}
elif e.startswith('git/refs/heads/') and method=='PATCH':
 if data!={'sha':NEW,'force':False}:raise RuntimeError('Wrong PATCH')
 if cfg.get('patch_move',True):s['ref']=NEW
 o={'object':{'sha':s['ref']}}
 if cfg.get('patch_fail'):rc=1
 raw=cfg.get('patch_raw')
else:raise RuntimeError('Unmocked endpoint '+e)
if cfg.get('fail_endpoint')==e:rc=1
if cfg.get('raw_endpoint')==e:raw=cfg['raw_response']
p.write_text(json.dumps(s,indent=2)+'\n')
if rc:print('Mock uncertain/error response',file=sys.stderr);sys.exit(1)
print(json.dumps(o) if raw is None else raw)
