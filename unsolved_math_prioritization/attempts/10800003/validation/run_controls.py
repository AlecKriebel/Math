from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile
D=Path(__file__).resolve().parents[1];A=D/'author';F=D/'freeze'
PIN='90f41824fce3c028993e1dcd12651dbeb86c8b2728527e61052da9b54c2e33a7'
BOOT='747e0a67d88e4adb8818077394a132f80b0c8f30ed5c5b1877ea536708ab624f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def inventory(p):return {str(x.relative_to(p)):(sha(x),x.stat().st_size,stat.S_IMODE(x.stat().st_mode)) for x in p.rglob('*') if x.is_file()}
require(sha(F/'AUTHOR_MANIFEST.json')==PIN and sha(F/'bootstrap.py')==BOOT,'initial anchors')
original=inventory(A);work=Path(tempfile.mkdtemp(prefix='critical-value-controls-',dir='/tmp'));results=[]
def cp(tag,writable=True):
 d=work/tag;d.mkdir();shutil.copytree(A,d/'author');shutil.copytree(F,d/'freeze')
 if writable:
  for root in [d/'author',d/'freeze']:
   root.chmod(0o755)
   for p in root.iterdir():p.chmod(0o644)
 return d
def run(argv,cwd):return subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
def authenticated(d,flags):
 if sha(d/'freeze'/'bootstrap.py')!=BOOT:return {'external_rejection':True,'returncode':99,'stdout':b'','stderr':b'bootstrap hash mismatch before execution'}
 r=run([sys.executable,'-I','-S','-B',*flags,str(d/'freeze'/'bootstrap.py'),str(d/'author')],work)
 return {'external_rejection':False,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
def record(mode,name,r,expected):
 require((r['returncode']==0)==expected,'unexpected '+mode+' '+name+' '+r['stderr'].decode(errors='replace'))
 results.append({'mode':mode,'case':name,'expected':'accept' if expected else 'reject','result':'PASS','external_bootstrap_rejection':r['external_rejection']})
def jmut(d,n,fn):
 p=d/'author'/n;j=json.loads(p.read_text());fn(j);p.write_text(json.dumps(j))
def sem(d,case):
 if case=='solved':jmut(d,'CLAIMS.json',lambda j:j.update(status='solved'))
 elif case=='turns4':jmut(d,'CLAIMS.json',lambda j:j.update(approaches_used=4))
 elif case=='bool_id':jmut(d,'CLAIMS.json',lambda j:j.update(problem_id=True))
 elif case=='resolution':jmut(d,'CLAIMS.json',lambda j:j.update(complete_original_resolution=True))
 elif case=='novelty':jmut(d,'CLAIMS.json',lambda j:j.update(novelty_claim=True))
 elif case=='ledger_duplicate':jmut(d,'APPROACH_LEDGER.json',lambda j:j['turns'][1].update(turn=1))
 elif case=='ledger_bool':jmut(d,'APPROACH_LEDGER.json',lambda j:j['turns'][0].update(turn=True))
 elif case=='bool_m':jmut(d,'CERTIFICATE.json',lambda j:j['reflection_m'].__setitem__(8,False))
 elif case=='zero_s':jmut(d,'CERTIFICATE.json',lambda j:j['cusp_s'].__setitem__(0,[0,16]))
 elif case=='zero_denominator':jmut(d,'CERTIFICATE.json',lambda j:j['cusp_s'].__setitem__(0,[1,0]))
 elif case=='cusp_missing':jmut(d,'CERTIFICATE.json',lambda j:j['cusp_s'].pop())
 elif case=='grid_repeated':jmut(d,'CERTIFICATE.json',lambda j:j.update(grid_alpha=[-2,-2,3]))
 elif case=='grid_bool':jmut(d,'CERTIFICATE.json',lambda j:j.update(grid_beta=[False,1,4]))
 elif case=='scaling_false':jmut(d,'CERTIFICATE.json',lambda j:j['scaling']['x9'].update(degree=5))
 elif case=='extra_key':jmut(d,'CERTIFICATE.json',lambda j:j.update(extra='bad'))
 elif case=='duplicate_json':
  p=d/'author'/'CERTIFICATE.json';p.write_text(p.read_text().replace('{','{"schema":"false",',1))
 elif case in ['nan','infinity','overflow']:
  p=d/'author'/'CERTIFICATE.json';s=p.read_text();p.write_text(s.replace('"reflection_m": [','"reflection_m": ['+{'nan':'NaN','infinity':'Infinity','overflow':'1e999'}[case]+',',1))
 elif case=='array_root':(d/'author'/'CERTIFICATE.json').write_text('[]')
 elif case=='bad_utf8':(d/'author'/'CERTIFICATE.json').write_bytes(b'\xff')
 elif case=='missing_input':(d/'author'/'CERTIFICATE.json').unlink()
 elif case=='false_source_hash':jmut(d,'SOURCE_METADATA.json',lambda j:j['sources'][0].update(sha256='z'*64))
 else:raise RuntimeError(case)
def integ(d,case):
 p=d/'author';f=d/'freeze';sentinel=d/'HOSTILE_RAN'
 if case=='altered_proof':(p/'PROOF_AND_STATUS.md').write_text('false theorem')
 elif case=='extra_file':(p/'unexpected.pdf').write_bytes(b'not source data')
 elif case=='missing_file':(p/'CLAIMS.json').unlink()
 elif case=='symlink_file':
  (p/'CLAIMS.json').unlink();(p/'CLAIMS.json').symlink_to(A/'CLAIMS.json')
 elif case=='symlink_root':
  shutil.rmtree(p);p.symlink_to(A,target_is_directory=True)
 elif case=='extra_directory':(p/'extra').mkdir()
 elif case=='fifo':
  (p/'CLAIMS.json').unlink();os.mkfifo(p/'CLAIMS.json')
 elif case=='executable':(p/'verify.py').chmod(0o755)
 elif case=='group_writable':(p/'CLAIMS.json').chmod(0o664)
 elif case=='extra_json_module':(p/'json.py').write_text('raise RuntimeError("imported")')
 elif case=='extra_sitecustomize':(p/'sitecustomize.py').write_text('raise RuntimeError("imported")')
 elif case=='duplicate_manifest':
  q=f/'AUTHOR_MANIFEST.json';q.write_text(q.read_text().replace('{','{"schema":"duplicate",',1))
 elif case in ['hostile_verifier','forged_manifest']:
  payload='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("ran")\nprint("PASS")\n';(p/'verify.py').write_text(payload)
  if case=='forged_manifest':
   q=f/'AUTHOR_MANIFEST.json';j=json.loads(q.read_text())
   for e in j['files']:
    if e['path']=='verify.py':e['bytes']=len(payload.encode());e['sha256']=sha(p/'verify.py')
   q.write_text(json.dumps(j))
 elif case=='substituted_bootstrap':(f/'bootstrap.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("ran")\n')
 else:raise RuntimeError(case)
 return sentinel
semcases=['solved','turns4','bool_id','resolution','novelty','ledger_duplicate','ledger_bool','bool_m','zero_s','zero_denominator','cusp_missing','grid_repeated','grid_bool','scaling_false','extra_key','duplicate_json','nan','infinity','overflow','array_root','bad_utf8','missing_input','false_source_hash']
intcases=['altered_proof','extra_file','missing_file','symlink_file','symlink_root','extra_directory','fifo','executable','group_writable','extra_json_module','extra_sitecustomize','duplicate_manifest','hostile_verifier','forged_manifest','substituted_bootstrap']
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 r=authenticated(D,flags);record(mode,'frozen-baseline',r,True)
 d=cp(mode+'-readonly',False)
 before=inventory(d/'author')
 probe='''from pathlib import Path
import json,os,sys
p=Path(sys.argv[1]);out={"uid":os.geteuid()}
for key,target,mode in [("creation",p/"write-probe","wb"),("append",p/"CLAIMS.json","ab")]:
 try:
  with target.open(mode) as f:f.write(b"bad")
  out[key]="UNEXPECTED_WRITE"
 except PermissionError:out[key]="BLOCKED"
print(json.dumps(out,sort_keys=True))
'''
 pr=run([sys.executable,'-I','-S','-B',*flags,'-c',probe,str(d/'author')],work);po=json.loads(pr.stdout)
 require(pr.returncode==0 and po=={'uid':1000,'creation':'BLOCKED','append':'BLOCKED'},'readonly not enforced')
 r=authenticated(d,flags);record(mode,'readonly-uid1000',r,True)
 require(before==inventory(d/'author'),'readonly changed')
 for case in semcases:
  d=cp(mode+'-semantic-'+case);sem(d,case)
  rr=run([sys.executable,'-I','-S','-B',*flags,str(d/'author'/'verify.py')],work)
  r={'returncode':rr.returncode,'stdout':rr.stdout,'stderr':rr.stderr,'external_rejection':False}
  record(mode,'semantic-'+case,r,False)
 for case in intcases:
  d=cp(mode+'-integrity-'+case);sentinel=integ(d,case);r=authenticated(d,flags);record(mode,'integrity-'+case,r,False);require(not sentinel.exists(),'hostile code executed')
require(inventory(A)==original and sha(F/'AUTHOR_MANIFEST.json')==PIN and sha(F/'bootstrap.py')==BOOT,'frozen bytes or modes changed')
receipt={'schema':'critical-value-collisions-controls-v1','status':'PASS','actual_uid':os.geteuid(),'modes':['normal','O','OO'],'cases':results,'total_cases':len(results),'expected_acceptances':sum(x['expected']=='accept' for x in results),'expected_rejections':sum(x['expected']=='reject' for x in results),'author_manifest_sha256':PIN,'bootstrap_sha256':BOOT,'original_payload_unchanged':True,'read_only_creation_and_append_probes':'BLOCKED in every mode as UID 1000','hostile_sentinel_files_created':0,'limitations':['Semantic controls run the pinned author verifier on deliberately mutated disposable inputs.','Integrity controls ordinarily reject changed bytes at the manifest/hash boundary; they are not independent semantic-parser coverage.','Bootstrap substitutions are rejected before execution using an external hardcoded hash.','No arbitrary-hostile-code sandbox or filesystem-race guarantee.']}
if len(sys.argv)==2: Path(sys.argv[1]).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
elif len(sys.argv)!=1: raise RuntimeError('usage: run_controls.py [external-receipt-path]')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['cases']},sort_keys=True))
