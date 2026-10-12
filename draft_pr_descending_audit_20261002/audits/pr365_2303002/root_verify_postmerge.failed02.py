"""ROOT sealed postmerge reproduction; captures only in a fresh ROOT namespace."""
from pathlib import Path
import ast,base64,datetime,gzip,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent; R=A.parents[2]; F=A/'post_merge_review'
D=A/'root_replay_private/root_postmerge_002';D.mkdir(exist_ok=False)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
ENV={'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'}
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
records=[];checks=[];differences=[]
def ck(label,yes):
 if not yes:raise AssertionError(label)
 checks.append(label)
def run(name,argv,cwd=R,changes=None):
 env=ENV|dict(changes or {});start=utc();p=subprocess.run([str(x) for x in argv],cwd=cwd,env=dict(os.environ,**env),capture_output=True);end=utc()
 c={'name':name,'argv':[str(x) for x in argv],'cwd':str(cwd),'environment_changes':env,'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'streams':{}}
 for st,b in [('stdout',p.stdout),('stderr',p.stderr)]:
  q=D/(name+'.'+st+'.gz');z=gzip.compress(b,mtime=0);q.write_bytes(z);c['streams'][st]={'path':str(q.relative_to(A)),'stored_bytes':len(z),'stored_sha256':sha(z),'logical_bytes':len(b),'logical_sha256':sha(b)}
 records.append(c);(D/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 return p
def git(name,*argv):
 p=run(name,['git',*argv]);ck(name+' exit/stderr',p.returncode==0 and not p.stderr);return p.stdout
def stored(c,st):
 e=c['streams'][st];b=(F/e['path']).read_bytes();v=gzip.decompress(b)
 ck(c['name']+st+' stored/logical',len(b)==e['stored_bytes'] and sha(b)==e['stored_sha256'] and len(v)==e['logical_bytes'] and sha(v)==e['logical_sha256']);return v
def diff(a,b,path=()):
 if a==b:return
 if isinstance(a,dict) and isinstance(b,dict):
  ck('same JSON keys '+str(path),a.keys()==b.keys())
  for k in a:diff(a[k],b[k],path+(k,))
 elif isinstance(a,list) and isinstance(b,list):
  ck('same JSON list '+str(path),len(a)==len(b))
  for k,(x,y) in enumerate(zip(a,b)):diff(x,y,path+(k,))
 else:
  ck('typed repository metadata '+str(path),path in {(e,'repo',f) for e in ['head','base'] for f in ['open_issues_count','open_issues','pushed_at','updated_at']} and type(a) is type(b));differences.append({'path':list(path),'before':a,'after':b})
pins={'PUBLIC_MANIFEST.json':'62881cea7e5550b8dd0d820726a9103e5f14e1e6a7430fe800dcb610b8b6c366','FINAL_SEAL.json':'d253b663076fff85fa1ccb5f2c5f33e9a74fc24a7093dfa406dce4aeac84c149','verify_public.py':'2b916aa7041e9764fadfed75f2a5a09a7079d6e2adf4a4d3f0b784ef18aca3d0'}
for n,h in pins.items():ck('reviewed '+n,sha((F/n).read_bytes())==h)
m=json.loads((F/'PUBLIC_MANIFEST.json').read_bytes());ck('counts',len(m['files'])==172 and len(m['private_files'])==377 and m['command_count']==119 and m['readonly_commands']==113)
before={str(p.relative_to(F)):sha(p.read_bytes()) for p in F.rglob('*') if p.is_file()}
main=git('root_begin_main','rev-parse','HEAD').decode().strip();ck('current main pin',main=='08adf9cb444d365fd148a2bb3e2951a7f49c6808')
ck('branch main',git('root_begin_branch','branch','--show-current')==b'main\n')
indexpath=git('root_index_path','rev-parse','--git-path','index').decode().strip();index=(R/indexpath).read_bytes()
ck('remote main',git('root_begin_remote','ls-remote','--heads','origin','main').split()[0].decode()==main)
cs=json.loads((F/'COMMANDS.json').read_bytes());readonly=[c for c in cs if c['readonly']];ck('literal readonly count',len(readonly)==113)
historical={'inspect_record_shapes','inspect_summary_sizes','final_code_hashes','repair_file_inventory'}
for c in cs:
 old={st:stored(c,st) for st in ['stdout','stderr']}
 if not c['readonly']:continue
 n=c['name'];p=run('literal_'+n,c['argv'],Path(c['cwd']),c['environment_changes']);ck(n+' exit',p.returncode==c['exit_code']);ck(n+' stderr whole',p.stderr==old['stderr'])
 if n in {'v2_begin_pr_api','v2_end_pr_api'}:diff(json.loads(old['stdout']),json.loads(p.stdout));records[-1]['comparison']='Whole JSON exact except precisely eight typed repository-metadata leaves'
 elif n=='repair_file_inventory':
  ck('rg exact unordered path set',sorted(old['stdout'].splitlines())==sorted(p.stdout.splitlines()));records[-1]['comparison']='Every original/fresh path exact; unordered rg inventory order is not meaningful'
 elif n=='inspect_record_shapes':
  x=json.loads(old['stdout']);y=json.loads(p.stdout);byname={e['name']:e for e in y};ck('historical record subset',all(byname.get(e['name'])==e for e in x));records[-1]['comparison']='Earlier exact records remain an unchanged subset; later captures explicitly added'
 elif n=='inspect_summary_sizes':
  x=old['stdout'].decode().splitlines();y=p.stdout.decode().splitlines();oldfiles=ast.literal_eval(x[0]);freshfiles=dict(ast.literal_eval(y[0]));oldcmds=ast.literal_eval(x[1]);freshcmds=dict(ast.literal_eval(y[1]));ck('historical command exits retained',all(freshcmds[n]==e for n,e in oldcmds));ck('integration factual summary unchanged',ast.literal_eval(x[2])==ast.literal_eval(y[2]))
  for name,size in oldfiles:
   if name=='REPAIR_AND_CLOSURES.json':ck('lossless relocated repair original size',len(gzip.decompress((F/(name+'.gz')).read_bytes()))==size)
   elif name=='RESEARCH_LOG.md':ck('historical log later expanded',freshfiles[name]>=size)
   else:ck('old top size preserved '+name,freshfiles[name]==size)
  records[-1]['comparison']='Timestamped open-namespace sizes/record list; original log later expanded and repair JSON losslessly compressed; exact factual summary unchanged'
 elif n=='final_code_hashes':
  reconstructed=(F/'build_inventory.py').read_bytes().replace(b",'preserve_preseal_driver'",b'');q=D/'build_inventory.reconstructed.py';q.write_bytes(reconstructed)
  for line in old['stdout'].decode().splitlines():
   h,path=line.split('  ',1);name=Path(path).name;source=q if name=='build_inventory.py' else F/'forensic'/(name+'.failed01') if (F/'forensic'/(name+'.failed01')).exists() else F/name;ck('old source hash '+name,sha(source.read_bytes())==h)
  records[-1]['comparison']='Original failed verifier/fixture/report exact retained sources; old builder mechanically reconstructed by one writing-label removal, hash matches but no contemporaneous-preservation claim'
 else:ck(n+' stdout whole',p.stdout==old['stdout']);records[-1]['comparison']='Entire stdout/stderr/exit equal'
 print('PASS_LITERAL',n,flush=True)
actual='904d63bba0651c8f7364144c617e2b66f5d14256';accepted='47dbe2c144a77f590faf144b950f1e759db92e75';base='728b48109a11e83769b24ec5b30978c1c5ed7ec9'
ck('actual parents',git('root_actual_parents','show','-s','--format=%P',actual).decode().split()==[base,accepted]);ck('current sole parent',git('root_current_parent','show','-s','--format=%P',main).decode().split()==[actual])
bindings=json.loads((A/'clean_final_adversary/03_reproduction_bindings.json').read_bytes())['original_bindings']
for i,e in enumerate(bindings):
 path=e['path'];b=git('root_current_blob_'+str(i),'show',main+':'+path);ck('current worktree '+path,b==(R/path).read_bytes());ck('accepted blob '+path,b==git('root_accepted_blob_'+str(i),'show',accepted+':'+path))
def parse_replay(p,private):
 ck('closed verifier exit/stderr',p.returncode==0 and p.stderr==b'');text=p.stdout.decode();decoder=json.JSONDecoder();items=[]
 while text.strip():
  obj,end=decoder.raw_decode(text.lstrip());items.append(obj);text=text.lstrip()[end:]
 ck('child count',len(items)==(5 if private else 4))
 for item in items[:-1]:
  ck('whole child metadata',item['exit_code']==0 and base64.b64decode(item['stderr_base64'])==b'' and item['started_utc']<=item['finished_utc']);body=json.loads(base64.b64decode(item['stdout_base64']));ck('child receipt successful',body.get('status')=='PASS' or body.get('assertions')==3675 or body.get('public_integrity')=='verified')
 final=items[-1];ck('whole verifier semantics',final['passed'] is True and final['private_evidence']==('complete' if private else 'collectively absent') and final['omitted_API_primary_source_ROOT_streams_reproduced']==private and final['actual_merge']==actual and final['observed_main']==main and final['new_theorems']==0);return final
p=run('root_closed_private',[PY,F/'verify_public.py','--require-private','--replay']);private_result=parse_replay(p,True)
fixture=A/'root_replay_private/post_merge_public_only_v2/audits/pr365_2303002/post_merge_review';ck('fixture seal absent',not (fixture/'FINAL_SEAL.json').exists());shutil.copyfile(F/'FINAL_SEAL.json',fixture/'FINAL_SEAL.json')
p=run('root_closed_public_only',[PY,fixture/'verify_public.py','--replay']);public_result=parse_replay(p,False)
ck('current main stable',git('root_end_main','rev-parse','HEAD').decode().strip()==main);ck('remote main stable',git('root_end_remote','ls-remote','--heads','origin','main').split()[0].decode()==main);ck('index stable',(R/indexpath).read_bytes()==index)
ck('entire closed post namespace unchanged',{str(p.relative_to(F)):sha(p.read_bytes()) for p in F.rglob('*') if p.is_file()}==before)
out={'utc':utc(),'status':'PASS_ROOT_COMPLETE_SEALED_POSTMERGE','actual_merge':actual,'current_main':main,'manifest_sha256':pins['PUBLIC_MANIFEST.json'],'seal_sha256':pins['FINAL_SEAL.json'],'check_count':len(checks),'checks':checks,'literal_readonly_commands':113,'writing_commands_not_reexecuted':6,'historical_observations_not_byte_equal':sorted(historical),'typed_repository_metadata_differences':differences,'all_captures':records,'sealed_private_verifier':private_result,'sealed_public_only_verifier':public_result,'credited_resolution_percent':100,'new_theorems':0,'workflow_completion_percent':100,'namespace_unchanged':True,'index_unchanged':True,'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_postmerge_verification_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['checks','all_captures','typed_repository_metadata_differences']},indent=2))
