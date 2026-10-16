import pathlib,hashlib,json,zipfile,os,stat,re,subprocess,datetime
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_06';X=O/'cold_extract';T=O/'tmp'
PY=P/'audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
M='a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23';V='252b38c10858eab3fd2ea2e7314e1d2aeee7a257bb5fb6360bac3e9526949046'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,v):
 p=O/n;t=p.with_suffix(p.suffix+'.tmp');f=t.open('x');f.write(json.dumps(v,indent=2)+'\n');f.flush();os.fsync(f.fileno());f.close();os.replace(t,p);assert json.loads(p.read_bytes())==v
started=now();F=json.loads((D/'FREEZE.json').read_bytes());E={n[8:]:v for n,v in F['files'].items() if n.startswith('package/')};assert len(E)==258
Z=D/'anti-invariant-four-manifold-verification-v1.0.zip';assert len(Z.read_bytes())==630346 and sha(Z.read_bytes())=='ae7d51ded2f03cd307ec394728a94f3e2e6e568903905713da8bfdf0007a24d6'
records={};total=0
with zipfile.ZipFile(Z) as z:
 infos=z.infolist();assert len(infos)==258 and set(i.filename for i in infos)==set(E) and len({i.filename for i in infos})==258
 namespace={};dirs=set()
 for i in infos:
  n=i.filename;p=pathlib.PurePosixPath(n);assert i.orig_filename==n and len(n)<=512 and re.fullmatch('[A-Za-z0-9_./-]+',n) and str(p)==n and not p.is_absolute() and len(p.parts)<=12 and all(c not in ('.','..') and len(c)<=255 and not c.endswith('.') and c.split('.')[0].upper() not in {'CON','PRN','AUX','NUL'}|{s+str(k) for s in ('COM','LPT') for k in range(1,10)} for c in p.parts)
  assert not i.is_dir() and i.create_system==3 and i.external_attr>>16 in (0o644,0o100644) and not i.flag_bits&1 and i.compress_type in (0,8)
  assert i.file_size==E[n]['bytes'] and 0<=i.file_size<=8*1024**2 and 0<=i.compress_size<=8*1024**2 and i.file_size<=200*max(1,i.compress_size);total+=i.file_size;assert total<=32*1024**2
  dirs.update(str(q) for q in p.parents if str(q)!='.');records[n]={'bytes':i.file_size,'compressed_bytes':i.compress_size,'mode':oct(i.external_attr>>16),'sha256':E[n]['sha256']}
 assert not set(records)&dirs
 for n in set(records)|dirs:assert n.casefold() not in namespace;namespace[n.casefold()]=n
 save('ZIP_METADATA_BEFORE_DECOMPRESSION.json',{'started_utc':started,'completed_utc':now(),'status':'PASS','count':258,'flat_closure':True,'combined_namespace':True,'total_uncompressed_bytes':total,'members':records})
 X.mkdir(exist_ok=False);T.mkdir(exist_ok=True)
 for i in infos:
  with z.open(i) as s:b=s.read(i.file_size+1);assert len(b)==i.file_size and not s.read(1)
  assert sha(b)==E[i.filename]['sha256'] and b==(D/'package'/i.filename).read_bytes();p=X/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644)
  st=p.lstat();assert stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode)==0o644 and st.st_nlink==1
assert {str(p.relative_to(X)) for p in X.rglob('*') if p.is_file()}==set(E)
assert sha((X/'profile/verify_package.py').read_bytes())==V and sha((X/'PACKAGE_MANIFEST.json').read_bytes())==M
rows=[]
for label,flags,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2),('env2',[],0)]:
 env=os.environ.copy();env.update(TMPDIR=str(T),TMP=str(T),TEMP=str(T));env.pop('PYTHONOPTIMIZE',None)
 if label=='env2':env['PYTHONOPTIMIZE']='2'
 args=[str(PY),'-I','-S','-B',*flags,str(X/'profile/verify_package.py'),'--root',str(X),'--manifest-sha256',M,'--run-checkers'];ts=now();r=subprocess.run(args,capture_output=True,env=env,timeout=240)
 assert r.returncode==0 and not r.stderr,(label,r.returncode,r.stderr);receipt=json.loads(r.stdout);want=json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_bytes())['receipt'];assert json.dumps(receipt,sort_keys=True,allow_nan=False)==json.dumps(want,sort_keys=True,allow_nan=False)
 assert receipt['outer_runtime']['optimize']==opt and len(receipt['checker_replays'])==3 and all(c['runtime']['optimize']==0 for c in receipt['checker_replays']) and receipt['assertion_guard']['result']=='rejected_false_assertion'
 rows.append({'mode':label,'started_utc':ts,'completed_utc':now(),'observed_outer_optimization':opt,'returncode':r.returncode,'receipt':receipt,'stdout_sha256':sha(r.stdout),'command':args,'ambient_PYTHONOPTIMIZE':env.get('PYTHONOPTIMIZE'),'all_canonical_fields_exact':True});save('COLD_MODE_'+label+'.json',rows[-1]);print(label+' PASS exact every field',flush=True)
save('COLD_REPLAY.json',{'status':'PASS','utc':now(),'started_utc':started,'cold_extraction':True,'package_manifest_sha256':M,'externally_pinned_verifier_sha256':V,'normalized_fields_ignored':[],'modes':rows,'members':records,'metadata_before_decompression':True,'package_file_count_including_manifest':258,'all_files_equal_original_package':True})
