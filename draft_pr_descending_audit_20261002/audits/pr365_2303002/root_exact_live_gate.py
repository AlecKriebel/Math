"""ROOT exact prepared/ready gate: whole Git/API trees, bodies and queue bytes.

No checkout/index/PR mutation. Run after the independent whole closure; accepts
the draft flag only with --draft, otherwise requires ready before integration.
"""
from pathlib import Path
import base64,datetime,gzip,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];Q='unsolved_math_prioritization/QUEUE.md';P='unsolved_math_prioritization/attempts/2303002/'
V=A/('root_live_draft_private' if '--draft' in sys.argv else 'root_live_private');V.mkdir(exist_ok=False)
checks=[];captures=[];sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def ck(v,n):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def run(args,label):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(args,cwd=R,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=120);streams={}
 for n,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  z=gzip.compress(b,mtime=0);p=V/(label+'.'+n+'.gz');p.write_bytes(z);streams[n]={'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b),'stored_bytes':len(z),'stored_sha256':sha(z)}
 captures.append({'label':label,'argv':args,'cwd':str(R),'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'streams':streams});(A/(V.name+'_progress.json')).write_text(json.dumps(captures,indent=2)+'\n')
 ck(r.returncode==0 and not r.stderr,'full exit/stderr '+label);return r.stdout
def git(label,*args):return run(['git',*args],label)
def api(label,path):return json.loads(run(['gh','api','repos/AlecKriebel/Math/'+path],label))
def entries(raw):return {x.split(b'\t',1)[1].decode():x.split(b'\t',1)[0].decode() for x in raw.split(b'\0') if x}
m=json.loads((A/'repaired_snapshot_manifest.json').read_bytes());o=json.loads((A/'snapshot_manifest.json').read_bytes());H=m['head'];B=m['base'];OLD=o['head'];body=(A/'accepted_pr_body.txt').read_bytes();expected={f['path'] for f in m['files']}
ck(OLD=='4245f1af53840a07f43c05c928c4783bc6c3a467' and H=='47dbe2c144a77f590faf144b950f1e759db92e75' and B=='728b48109a11e83769b24ec5b30978c1c5ed7ec9','literal prepared pair')
ck(len(expected)==19 and expected=={f['path'] for f in o['files']},'closed original19paths')
ck(git('branch','branch','--show-current')==b'main\n','main branch');ck(git('local_main','rev-parse','HEAD').decode().strip()==B,'localmainexact')
first=api('pr_first','pulls/365')
def pr(p):
 ck(p['number']==365 and p['state']=='open' and p['draft']==('--draft' in sys.argv),'exact draft/ready state')
 ck(p['head']['sha']==H and p['base']['sha']==B and p['body'].encode()==body,'full literal head/base/body')
 ck(p['mergeable'] is True and p['mergeable_state']=='clean','clean integration')
pr(first);ck(api('main_first','git/ref/heads/main')['object']['sha']==B,'rawremote main exact')
bt=entries(git('base_entries','ls-tree','-rz','--full-tree',B));ht=entries(git('head_entries','ls-tree','-rz','--full-tree',H));ot=entries(git('original_entries','ls-tree','-rz',OLD,'--',P,Q))
ck({p for p in bt.keys()|ht.keys() if bt.get(p)!=ht.get(p)}==expected,'allrepository deltaexact19')
ck({p for p in ht if p.startswith(P)}==expected-{Q},'exact18mathnamespace');files=[]
for i,f in enumerate(m['files']):
 p=f['path'];b=git('blob_'+str(i),'show',H+':'+p);ck(b==(A/'repaired_snapshot'/p).read_bytes() and len(b)==f['bytes'] and sha(b)==f['sha256'],'wholepreparedbyte '+p)
 ck(ht[p].split()==['100644','blob',blob(b)],'fullmodekindblob '+p);j=api('remote_'+str(i),'contents/'+p+'?ref='+H);d=base64.b64decode(j['content']);ck(d==b and j['size']==len(b) and j['sha']==blob(b) and j['path']==p,'completeAPIbody '+p)
 if p!=Q:ck(b==(A/'snapshot'/p).read_bytes() and ht[p]==ot[p],'alloriginalmathunchanged '+p)
 files.append({'path':p,'bytes':len(b),'sha256':sha(b),'entry':ht[p]})
qb=git('base_queue','show',B+':'+Q);qa=(A/'repaired_snapshot'/Q).read_bytes();old=qb.splitlines(keepends=True);new=qa.splitlines(keepends=True);ck(len(old)==len(new)==1966,'entire1966queue');changes=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];ck(changes==[404],'onlyphysical405');x=old[404].split(b'|');y=new[404].split(b'|');ck(len(x)==len(y) and x[2].strip().split(b' / ')[0]==b'2303002','exactownqueueid');ck([i for i,(u,v) in enumerate(zip(x,y)) if u!=v]==[8],'onlystatuscell8');ck([x[i].strip() for i in (8,9)]==[b'queued',b'0/5'] and [y[i].strip() for i in (8,9)]==[b'already_solved',b'0/5'],'creditedzero-turntransition');ck(bt[Q].split()[:2]==ht[Q].split()[:2],'queue mode/typeunchanged')
tree=git('head_tree','show','-s','--format=%T',H).decode().strip();ck(git('virtual_merge','merge-tree','--write-tree',B,H).decode().splitlines()[0]==tree,'exactvirtualintegrationtree');ck(git('parents','show','-s','--format=%P',H).decode().split()==[OLD,B],'refreshparentorder');test=api('test_merge','git/commits/'+first['merge_commit_sha']);ck([p['sha'] for p in test['parents']]==[B,H] and test['tree']['sha']==tree,'GitHubactualtestmergetreepair')
D=A/'repaired_snapshot'/P;bindings=[]
for name in ['FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json']:
 for f in json.loads((D/name).read_bytes())['files']:
  b=(D/f['path']).read_bytes();ck(len(b)==f['bytes'] and sha(b)==f['sha256'],'nested '+name+'/'+f['path']);bindings.append({'manifest':name,**f})
for path,h in json.loads((D/'final_review/REVIEW_MANIFEST.json').read_bytes()).items():
 b=(D/'final_review'/path).read_bytes();ck(sha(b)==h,'nestedreview '+path);bindings.append({'manifest':'final_review/REVIEW_MANIFEST.json','path':path,'bytes':len(b),'sha256':h})
ck(len(bindings)==29,'entire29bindings');pub=json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes());ck(pub['author_manifest_sha256']==sha((D/'FINAL_FROZEN_MANIFEST.json').read_bytes()) and pub['review_manifest_sha256']==sha((D/'final_review/REVIEW_MANIFEST.json').read_bytes()),'crossmanifestanchors')
audit=[]
for family,mfname in [('path_geometry_review','PUBLIC_MANIFEST.json'),('poisson_components_review','PUBLIC_MANIFEST.json'),('poisson_components_corrections','SUPPLEMENT_MANIFEST.json'),('clean_final_adversary','PUBLIC_MANIFEST.json')]:
 F=A/family;j=json.loads((F/mfname).read_bytes());fs=j.get('files',j.get('public_files'));fs={r['path']:r for r in fs} if isinstance(fs,list) else fs
 for p,f in fs.items():
  b=(F/p).read_bytes();size=f.get('bytes',f.get('stored_bytes'));h=f.get('sha256',f.get('stored_sha256'));ck(len(b)==size and sha(b)==h,'complete current audit '+family+'/'+p)
 audit.append({'family':family,'manifest':mfname,'manifest_sha256':sha((F/mfname).read_bytes()),'seal_sha256':sha((F/'FINAL_SEAL.json').read_bytes()),'public_files':len(fs)})
for name,count in [('root_original_reproduction_receipt.json',387),('root_family_verification_receipt.json',1620)]:
 j=json.loads((A/name).read_bytes());ck(len(j['checks'])==count,'wholeROOTcheckcount '+name)
 ck(all(x['passed'] for x in j['checks']) if isinstance(j['checks'][0],dict) else j['status'].startswith('PASS'),'wholeROOTevidence '+name)
for f in json.loads((D/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs']:
 b=(A/'root_primary_private'/f['file']).read_bytes();ck(len(b)==f['bytes'] and sha(b)==f['sha256'],'fullprimaryPDF '+f['file'])
last=api('pr_last','pulls/365');pr(last);ck(last['merge_commit_sha']==first['merge_commit_sha'],'stabletestmerge');ck(api('main_last','git/ref/heads/main')['object']['sha']==B,'rawmainstableend');ck(git('local_main_last','rev-parse','HEAD').decode().strip()==B,'localmainstableend')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ROOT_EXACT_LIVE','reviewed_head':H,'base':B,'tree':tree,'test_merge':first['merge_commit_sha'],'body_sha256':sha(body),'draft':('--draft' in sys.argv),'check_count':len(checks),'checks':checks,'files':files,'nested_bindings':bindings,'audit_manifests':audit,'captures':captures,'queue_line':405,'only_queue_cells':[8],'genuine_discovery_turns':'0/5','all_other_queue_bytes_preserved':True,'all18mathematical_files_unchanged':True,'program_sha256':sha(Path(__file__).read_bytes())}
(A/('root_exact_live_draft_receipt.json' if '--draft' in sys.argv else 'root_exact_live_receipt.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','reviewed_head','base','tree','test_merge','check_count','draft']},indent=2))
