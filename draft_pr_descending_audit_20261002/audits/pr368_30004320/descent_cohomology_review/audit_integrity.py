from pathlib import Path
import json,hashlib,subprocess,sys,os,datetime,shutil
O=Path(__file__).resolve().parent;A=O.parent;R=A.parents[2];P=A/'snapshot/problems/30004320_laurent_descent';H='74617174ddfb3ea726cea343a4ba915613724bdc';B='efd29c05204703acca9a0860812f54b94fae54b1';PREFIX='problems/30004320_laurent_descent'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
checks=[]
def ck(name,b):
 assert b,name
 checks.append(name)
def bind(f,row,sizekey='bytes'):
 d=f.read_bytes();ck(str(f.relative_to(A))+' length',len(d)==row[sizekey]);ck(str(f.relative_to(A))+' hash',sha(d)==row['sha256']);return d
start=now();m=json.loads((A/'snapshot_manifest.json').read_bytes());ck('original pins',m['head']==H and m['base']==B and m['pr']==368)
ck('exact recursive target scope',len(m['files'])==54 and sum(r['path'].startswith(PREFIX+'/') for r in m['files'])==53)
actualpaths=set(git('diff','--name-only',B,H).decode().splitlines());ck('Git exact full changed scope',actualpaths=={r['path'] for r in m['files']})
for r in m['files']:
 d=bind(A/'snapshot'/r['path'],r);gd=git('show',H+':'+r['path']);ck(r['path']+' exact Git bytes',gd==d);ck(r['path']+' Git blob',hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==r['git_blob_sha']);ck(r['path']+' mode',git('ls-tree',H,'--',r['path']).decode().startswith('100644 blob '))
api=subprocess.check_output(['gh','api','--paginate','repos/AlecKriebel/Math/pulls/368/files'],cwd=R);(O/'private/API_FILES.json').write_bytes(api);rows=json.loads(api);ck('GitHub API exact file scope',len(rows)==54 and {r['filename'] for r in rows}==actualpaths)
for row in rows:
 r=next(x for x in m['files'] if x['path']==row['filename']);ck('API '+r['path'],row['status']==r['status']=='added' if r['path'].startswith(PREFIX+'/') else row['status']==r['status']);ck('API blob '+r['path'],row['sha']==r['git_blob_sha'])
manifestnames=['FINAL_AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json'];bindings=[]
for name in manifestnames:
 j=json.loads((P/name).read_bytes());base=P/'review' if name.startswith('review/') else P
 for r in j['files']:
  bind(base/r['path'],r);bindings.append({'manifest':name,**r})
 if name.startswith('TURN_') and int(name.split('_')[1])>1:
  i=int(name.split('_')[1]);ck(name+' chain',j['previous_manifest_sha256']==sha((P/f'TURN_{i-1}_MANIFEST.json').read_bytes()))
ck('all public manifest instances',len(bindings)==130)
pub=json.loads((P/'PUBLICATION_MANIFEST.json').read_bytes());ck('publication exact self excluded', {r['path'] for r in pub['files']}=={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name!='PUBLICATION_MANIFEST.json'})
anc=['5e2eb63fd571f2f660ff9ebb436440029b5d1268','d7d898ba23e9d024e79b938e3e0e305d91bb125b','c800217d22d329d6ca397f3c18e5115c77688fb9','24ecf1f2f0ab62082f328545180e4b2ba1640ab7','b08662a16499edf37f0c0eae850cfa00b7778ed6'];prov=[]
for i,c in enumerate(anc,1):
 meta=git('show','--no-patch','--format=%H %P %cI %s',c).decode().strip();ck('author parent '+str(i),meta.split()[1]==(B if i==1 else anc[i-2]));mj=json.loads((P/f'TURN_{i}_MANIFEST.json').read_bytes());ck('author manifest '+str(i),git('show',c+':'+PREFIX+f'/TURN_{i}_MANIFEST.json')==(P/f'TURN_{i}_MANIFEST.json').read_bytes())
 for r in mj['files']:ck('author checkpoint '+str(i)+' '+r['path'],git('show',c+':'+PREFIX+'/'+r['path'])==(P/r['path']).read_bytes())
 prov.append({'turn':i,'commit':c,'metadata':meta})
ck('publication parents',git('show','--no-patch','--format=%P',H).decode().strip().split()==[B,anc[-1]])
auth=json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes());ck('author exact self excluded',len(auth['files'])==41)
for r in auth['files']:ck('final author provenance '+r['path'],git('show',anc[-1]+':'+PREFIX+'/'+r['path'])==(P/r['path']).read_bytes())
for r in json.loads((P/'review/REMOTE_BINDING.json').read_bytes())['files']:
 d=(P/r['path']).read_bytes();ck('old remote binding '+r['path'],len(d)==r['size'] and hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==r['git_blob_sha']);ck('actual old Git checkpoint '+r['path'],git('show',anc[-1]+':'+PREFIX+'/'+r['path'])==d)
sourcefiles=[];src=O/'private/named_sources';src.mkdir(exist_ok=True)
for name in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:
 for r in json.loads((P/name).read_bytes())['files']:
  s=next(x for x in json.loads((O/'SOURCE_ACQUISITION.json').read_bytes())['sources'] if x['url']==r['url']);f=O/'private/sources'/(s['id']+'.pdf');bind(f,r);named=src/r['name']
  if not named.exists():os.link(f,named)
  sourcefiles.append(r)
# Read-only execution; every full stdout/stderr captured under owned folder.
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');streams=[]
def run(label,args,expected=None):
 t0=now();p=subprocess.run([sys.executable,*map(str,args)],cwd=O/'private',env=env,capture_output=True);t1=now()
 (O/(label+'.stdout')).write_bytes(p.stdout);(O/(label+'.stderr')).write_bytes(p.stderr);ck(label+' exit',p.returncode==0);ck(label+' stderr empty',p.stderr==b'')
 if expected:ck(label+' complete stdout exact',p.stdout==expected.read_bytes())
 streams.append({'label':label,'args':[sys.executable,*map(str,args)],'started_at':t0,'finished_at':t1,'returncode':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)})
 return p.stdout
for i in range(1,6):run('author_turn_'+str(i),[P/f'check_turn_{i}.py'],P/f'TURN_{i}_CHECKS.json')
run('historical_review_controls',[P/'review/independent_checks.py'],P/'review/INDEPENDENT_CHECKS.json')
out=run('packet_with_sources',[P/'verify_packet.py','--source-dir',src]);ck('full packet JSON exact',json.loads(out)==json.loads((P/'review/AUTHOR_REPLAY.json').read_bytes()))
run('publication_with_sources',[P/'verify_publication.py','--source-dir',src]);out=run('packet_without_sources',[P/'verify_packet.py']);j=json.loads(out);expect=json.loads((P/'review/AUTHOR_REPLAY.json').read_bytes());expect['source_pdfs_checked']=0;expect['source_check']='not requested; raw sources are not distributed';ck('portable full no source contract',j==expect)
run('publication_without_sources',[P/'verify_publication.py'])
receipt={'started_at':start,'finished_at':now(),'status':'PASS','original_head':H,'original_base':B,'root_manifest_checked':54,'exact_target_files':53,'nested_public_manifest_instances':130,'source_pdf_instances':11,'old_remote_bindings':42,'actual_author_checkpoints':prov,'checks_count':len(checks),'checks':checks,'streams':streams,'candidate_author_assertions':128694,'historical_independent_assertions':8664,'limitations':'No actual merge or current-main gate is performed. Historical all-ref/PR search completeness is not independently recreated.'};(O/'INTEGRITY_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k not in ['checks','streams','actual_author_checkpoints']},indent=2))
