import pathlib,stat,json,hashlib,zipfile,subprocess,os,datetime,re
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_02';X=O/'cold_extract';T=O/'tmp';T.mkdir(exist_ok=True)
PYTHON=P/'audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
M='a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23';V='252b38c10858eab3fd2ea2e7314e1d2aeee7a257bb5fb6360bac3e9526949046'
def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
freeze=json.loads((D/'FREEZE.json').read_text());expected={k.removeprefix('package/'):v for k,v in freeze['files'].items() if k.startswith('package/')};need(len(expected)==258,'package closure')
zip_path=D/'anti-invariant-four-manifold-verification-v1.0.zip';need(sha(zip_path.read_bytes())=='ae7d51ded2f03cd307ec394728a94f3e2e6e568903905713da8bfdf0007a24d6','ZIP pin')
records={};total=0
with zipfile.ZipFile(zip_path) as z:
 infos=z.infolist();need(len(infos)==258 and len({i.filename for i in infos})==258,'members');need(set(i.filename for i in infos)==set(expected),'exact file set')
 dirs=set()
 for i in infos:
  n=i.filename;p=pathlib.PurePosixPath(n);need(i.orig_filename==n and re.fullmatch(r'[A-Za-z0-9_./-]+',n) is not None and not p.is_absolute() and str(p)==n and len(p.parts)<=12 and all(c not in ('.','..') and len(c)<=255 for c in p.parts),'path')
  need(not i.is_dir() and i.create_system==3 and i.external_attr>>16 in (0o644,0o100644),'mode');need(i.compress_type in (0,8) and not i.flag_bits&1,'compression');need(0<=i.file_size<=8*1024**2 and 0<=i.compress_size<=8*1024**2 and i.file_size<=200*max(1,i.compress_size),'bounds');total+=i.file_size;need(total<=32*1024**2,'total');need(i.file_size==expected[n]['bytes'],'declared size')
  dirs.update(str(k) for k in p.parents if str(k)!='.');records[n]={'bytes':i.file_size,'compressed_bytes':i.compress_size,'zip_mode_octal':oct(i.external_attr>>16),'sha256':expected[n]['sha256']}
 need(not set(records)&dirs and len({s.casefold() for s in set(records)|dirs})==len(set(records)|dirs),'namespace')
 # All member metadata and bounds authenticated before first decompression.
 X.mkdir(exist_ok=True)
 for i in infos:
  with z.open(i) as stream:b=stream.read(i.file_size+1);need(len(b)==i.file_size and not stream.read(1),'expanded size')
  need(sha(b)==expected[i.filename]['sha256'],'member hash');p=X/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644);need(stat.S_IMODE(p.stat().st_mode)==0o644,'extracted mode')
need(sha((X/'profile/verify_package.py').read_bytes())==V and sha((X/'PACKAGE_MANIFEST.json').read_bytes())==M,'entry pins')
rows=[]
for label,flags,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2),('env2',[],0)]:
 env=os.environ.copy();env['TMPDIR']=str(T);env['TMP']=str(T);env['TEMP']=str(T)
 if label=='env2':env['PYTHONOPTIMIZE']='2'
 else:env.pop('PYTHONOPTIMIZE',None)
 args=[str(PYTHON),'-I','-S','-B',*flags,str(X/'profile/verify_package.py'),'--root',str(X),'--manifest-sha256',M,'--run-checkers']
 p=subprocess.run(args,capture_output=True,env=env,timeout=240);need(p.returncode==0 and not p.stderr,label+' process '+p.stderr.decode(errors='replace'))
 receipt=json.loads(p.stdout);canonical=json.loads((D/f'PACKAGE_REPLAY_{label}.json').read_text())['receipt'];need(receipt==canonical,label+' EXACT receipt');need(receipt['outer_runtime']['optimize']==opt,'outer opt')
 rows.append({'mode':label,'observed_outer_optimization':receipt['outer_runtime']['optimize'],'returncode':p.returncode,'receipt':receipt,'exact_all_fields':True,'command':args,'ambient_PYTHONOPTIMIZE':env.get('PYTHONOPTIMIZE'),'stdout_sha256':sha(p.stdout)})
 print(label+' exact canonical PASS',flush=True)
obj={'status':'PASS','utc':now(),'cold_extraction':True,'package_manifest_sha256':M,'externally_pinned_verifier_sha256':V,'normalized_fields_ignored':[],'modes':rows,'zip_sha256':sha(zip_path.read_bytes()),'metadata_before_decompression':True,'members':records,'total_uncompressed_bytes':total,'extraction_modes':'all regular files0644, no symlinks/hardlinks, canonical names and namespace closure checked before decompression'}
(O/'COLD_REPLAY.json').write_text(json.dumps(obj,indent=2)+'\n')
