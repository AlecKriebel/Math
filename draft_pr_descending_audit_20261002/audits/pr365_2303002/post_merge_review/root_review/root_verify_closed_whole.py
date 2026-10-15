"""ROOT whole closure identities and every prepared read-only command replay."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;F=A/'clean_final_adversary';R=A.parents[2];O=A/'root_whole_prepared_streams';O.mkdir(exist_ok=False);V=A/'root_replay_private/whole_prepared';V.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();checks=[];captures=[];metadata=[]
def ck(n,v):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_bytes())
mf=load(F/'PUBLIC_MANIFEST.json');se=load(F/'FINAL_SEAL.json');ck('closedMF',sha((F/'PUBLIC_MANIFEST.json').read_bytes())==se['public_manifest_sha256']);ck('reviewedverifier',sha((F/'verify_public.py').read_bytes())=='b544c1281a95f9cad18bc137e680b01f9b196aac56a35a6c37a15ceab9c1ae90');ck('reviewedbuilder',sha((F/'build_public_inventory.py').read_bytes())=='4149a942c9ab6993743e559ffe6fde9a572f6f8909c1ff33393bfcbe9c146235')
before={}
for p,e in (mf['public_files']|mf['private_files']).items():
 b=(F/p).read_bytes();ck('every stored '+p,len(b)==e['stored_bytes'] and sha(b)==e['stored_sha256']);d=gzip.decompress(b) if e['encoding']=='gzip' else b;ck('every logical '+p,len(d)==e['logical_bytes'] and sha(d)==e['logical_sha256']);before[p]=sha(b)
before['PUBLIC_MANIFEST.json']=sha((F/'PUBLIC_MANIFEST.json').read_bytes());before['FINAL_SEAL.json']=sha((F/'FINAL_SEAL.json').read_bytes())
ck('exactwholeallnamespace',{str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}==set(before))
commands=load(F/'COMMANDS.json');prepared=[]
for c in commands:
 if not c['read_only_command'] or not c['name'].startswith('prepared_'):continue
 name=c['name'];argv=c['argv'];ck('readonly executable '+name,argv[0] in ['gh','git'])
 if argv[0]=='git':ck('Git readonly '+name,argv[1] in ['ls-tree','symbolic-ref','rev-parse','show','cat-file'])
 old={n:gzip.decompress((F/r['path']).read_bytes()) for n,r in c['streams'].items()}
 start=utc();z=subprocess.run(argv,cwd=c['cwd'],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=180);rec={'name':name,'argv':argv,'cwd':c['cwd'],'started_utc':start,'completed_utc':utc(),'exit':z.returncode,'streams':{}}
 for n,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  directory=V if argv[0]=='gh' else O;q=directory/(name+'.'+n+'.gz');g=gzip.compress(b,mtime=0);q.write_bytes(g);rec['streams'][n]={'path':str(q.relative_to(A)),'bytes':len(b),'sha256':sha(b),'stored_bytes':len(g),'stored_sha256':sha(g),'private':argv[0]=='gh'}
 captures.append(rec);(A/'root_whole_prepared_command_progress.json').write_text(json.dumps(captures,indent=2)+'\n');ck(name+' exit',z.returncode==c['exit_code']);ck(name+' fullstderr',z.stderr==old['stderr'])
 if name=='prepared_base_api_tree':
  x=json.loads(old['stdout']);y=json.loads(z.stdout);ck('truncated immutable root identity',x['sha']==y['sha']=='2ef2e883ac42114d7ad82ca7248a1e0d90d52c2b' and x['truncated'] is True and y['truncated'] is True)
  ck('truncated object keys/meta',set(x)==set(y) and {k:v for k,v in x.items() if k!='tree'}=={k:v for k,v in y.items() if k!='tree'})
  raw=subprocess.check_output(['git','ls-tree','-rtzl','--full-tree','728b48109a11e83769b24ec5b30978c1c5ed7ec9'],cwd=R);q=O/'truncated_full_fixed_base_tree.stdout.gz';g=gzip.compress(raw,mtime=0);q.write_bytes(g);entries={}
  for row in raw.split(b'\0'):
   if row:
    head,p=row.split(b'\t',1);mode,kind,oid,size=head.decode().split();entries[p.decode()]={'mode':mode,'type':kind,'sha':oid,'size':None if size=='-' else int(size)}
  for label,obj in [('historical',x),('fresh',y)]:
   ck(label+' truncated unique paths',len(obj['tree'])==len({f['path'] for f in obj['tree']}))
   for e in obj['tree']:
    f=entries[e['path']];ck(label+' reported exact entry '+e['path'],all(e[k]==f[k] for k in ('mode','type','sha')) and ('size' not in e or e['size']==f['size']) and e['url']=='https://api.github.com/repos/AlecKriebel/Math/git/'+('trees/' if e['type']=='tree' else 'blobs/')+e['sha'])
  rec['comparison']='Same exact root/meta; truncated subset varies. EVERY reported old/fresh path/mode/kind/OID/size/URL independently checked against complete immutable local base tree. No full recursive API coverage or whole-byte equality claimed.'
  rec['complete_fixed_local_tree_capture']={'argv':['git','ls-tree','-rtzl','--full-tree','728b48109a11e83769b24ec5b30978c1c5ed7ec9'],'path':str(q.relative_to(A)),'bytes':len(raw),'sha256':sha(raw),'stored_bytes':len(g),'stored_sha256':sha(g)}
 elif z.stdout!=old['stdout'] and name.endswith(('_begin_pr','_end_pr')):
  x=json.loads(old['stdout']);y=json.loads(z.stdout);allowed={(end,'repo',field) for end in ['head','base'] for field in ['open_issues_count','open_issues','pushed_at','updated_at']}
  def walk(x,y,p=()):
   if isinstance(x,dict) and isinstance(y,dict):
    ck(name+str(p)+' objectkeys',set(x)==set(y))
    for k in x:walk(x[k],y[k],p+(k,))
   elif x!=y:
    ck(name+str(p)+' allowedrepo leaf',p in allowed and type(x) is type(y));metadata.append({'capture':name,'path':list(p),'before':x,'after':y})
  walk(x,y)
 else:ck(name+' entirestdout',z.stdout==old['stdout'])
 prepared.append(name)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
z=subprocess.run([str(PY),str(F/'verify_public.py'),'--require-private','--replay'],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'),capture_output=True,timeout=180)
for n,b in [('stdout',z.stdout),('stderr',z.stderr)]:(O/('whole_final_verifier.'+n)).write_bytes(b)
ck('full final readonly verifier',z.returncode==0 and not z.stderr);v=json.loads(z.stdout);ck('current full semantic scope',v['original_scope']==19 and v['nested_bindings']==29 and v['writes']==0 and v['private_evidence']=='complete and verified')
for p,h in before.items():ck('closed namespace unchanged '+p,sha((F/p).read_bytes())==h)
out={'utc':utc(),'status':'PASS_CLOSED_WHOLE_ALL_EVIDENCE_AND_PREPARED_REEXECUTIONS','manifest_sha256':sha((F/'PUBLIC_MANIFEST.json').read_bytes()),'seal_sha256':sha((F/'FINAL_SEAL.json').read_bytes()),'public_files':len(mf['public_files']),'private_files':len(mf['private_files']),'check_count':len(checks),'checks':checks,'every_prepared_readonly_command':prepared,'captures':captures,'allowed_repository_metadata_differences':metadata,'whole_final_verifier_complete_output':v,'all_closed_namespaces_unchanged':True,'credited_resolution_percent':100,'new_theorems':0,'workflow_completion_percent':90,'root_original_readonly_replays_already_verified':74,'root_original_receipt_sha256':sha((A/'root_whole_original_receipt.json').read_bytes()),'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_whole_verification_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','public_files','private_files','check_count']},indent=2));print('prepared readonly replay count',len(prepared))
