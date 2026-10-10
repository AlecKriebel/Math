#!/usr/bin/env python3
"""Fixed-bootstrap delivery, schema, exact-comparator, and hostile tests."""
import copy,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def thaw(root):
 root.chmod(0o755)
 for p in root.iterdir():
  if p.is_dir() and not p.is_symlink():p.chmod(0o755)
  elif p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o644)
def freeze(root):
 for p in root.iterdir():
  if p.is_file() and not p.is_symlink() and p.stat().st_nlink==1:p.chmod(0o444)
  elif p.is_dir() and not p.is_symlink():p.chmod(0o555)
 root.chmod(0o555)
def main():
 need(len(sys.argv)==3,'packet and external bootstrap hash required');root=Path(os.path.abspath(sys.argv[1]));bp=sys.argv[2]
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B')
 bootstrap=(root/'BOOTSTRAP.py').read_bytes();need(sha(bootstrap)==bp,'external bootstrap pin');code=bootstrap.decode()
 mp=re.search("MANIFEST_SHA256 = '([0-9a-f]{64})'",code).group(1);vp=re.search("VERIFIER_SHA256 = '([0-9a-f]{64})'",code).group(1)
 verifier=(root/'verify_publication.py').read_bytes();need(sha(verifier)==vp,'authenticated verifier');need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==mp,'fixed manifest')
 ns={'__name__':'authenticated_test_target'};exec(compile(verifier,'<authenticated-test-target>','exec'),ns)
 initial=ns['integrity'](root,mp,bp);physical=ns['readonly'](root);mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C')
 baseline=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root)],capture_output=True,cwd=root,env=env,timeout=200)
 need(baseline.returncode==0 and baseline.stderr==b'','baseline failed');result=ns['parse'](baseline.stdout);need(result['whole_delivery_unchanged'] is True,'baseline unchanged')
 for row in result['replays']:
  n=row['script'];ns['compare_output'](n,row['exit_code'],row['stdout'].encode(),row['stderr'].encode(),initial[ns['refname'](n,'stdout')],initial[ns['refname'](n,'stderr')])
 negatives=[]
 def fixture(label,change,args_kind='normal',controls=False):
  with tempfile.TemporaryDirectory(prefix='two-loop-integrity-') as td:
   td=Path(td);p=td/'packet';shutil.copytree(root,p);thaw(p);change(p);freeze(p);args=[str(p)]
   if args_kind=='missing':args=[]
   if args_kind=='extra':args.append('unexpected')
   if args_kind=='symlink-root':
    alias=td/'alias';alias.symlink_to(p,target_is_directory=True);args=[str(alias)]
   if args_kind=='symlink-ancestor':
    alias=td/'alias';alias.symlink_to(td,target_is_directory=True);args=[str(alias/'packet')]
   if controls:args.insert(0,'--controls')
   try:
    r=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),*args],cwd=root,env=env,capture_output=True,timeout=20)
    need(r.returncode==1 and r.stdout==b'' and r.stderr in (b'REJECT: bootstrap integrity validation failed\n',b'REJECT: strict publication validation failed\n'),'negative accepted: '+label)
    need(not (td/'HARNESS_EXECUTED').exists(),'unauthenticated harness executed')
    negatives.append(dict(control=label,entry='controls' if controls else 'validation',exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),unauthenticated_harness_executed=False))
   finally:thaw(p)
 for n in sorted(initial):fixture('changed member '+n,lambda p,n=n:(p/n).write_bytes(b'altered\n'))
 fixture('missing member',lambda p:(p/'ACCEPTANCE.md').unlink());fixture('extra member',lambda p:(p/'EXTRA').write_bytes(b'extra\n'));fixture('extra directory',lambda p:(p/'EXTRA').mkdir())
 def symlink(p):(p/'ACCEPTANCE.md').unlink();(p/'ACCEPTANCE.md').symlink_to(root/'ACCEPTANCE.md')
 def hardlink(p):os.link(p/'ACCEPTANCE.md',p.parent/'linked')
 def fifo(p):(p/'ACCEPTANCE.md').unlink();os.mkfifo(p/'ACCEPTANCE.md')
 fixture('symbolic link member',symlink);fixture('hard link',hardlink);fixture('special FIFO member',fifo)
 fixture('symbolic root',lambda p:None,'symlink-root');fixture('symbolic ancestor',lambda p:None,'symlink-ancestor');fixture('missing required packet argument',lambda p:None,'missing');fixture('extra argument',lambda p:None,'extra')
 def reseal(p):
  (p/'ACCEPTANCE.json').write_bytes(b'{}\n');m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes())
  for x in m['files']:
   if x['path']=='ACCEPTANCE.json':x.update(bytes=3,sha256=sha(b'{}\n'))
  (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
 fixture('resealed manifest cannot replace fixed external pin',reseal)
 def untrusted_harness(p):(p/'MUTATION_TESTS.py').write_text("from pathlib import Path\nPath(__file__).parent.parent.joinpath('HARNESS_EXECUTED').write_text('bad')\n")
 fixture('controls tampered harness rejected before execution',untrusted_harness,controls=True)
 fixture('controls missing harness',lambda p:(p/'MUTATION_TESTS.py').unlink(),controls=True)
 fixture('controls resealed manifest',reseal,controls=True)
 fixture('controls missing packet argument',lambda p:None,'missing',controls=True)
 fixture('controls extra argument',lambda p:None,'extra',controls=True)
 fixture('controls symbolic root',lambda p:None,'symlink-root',controls=True)
 semantic=[]
 def reject(label,call):
  try:call()
  except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:semantic.append(dict(control=label,rejected=True,error=str(e)));return
  raise ValueError('semantic accepted: '+label)
 for label,raw in [('duplicate keys',b'{"a":1,"a":2}'),('NaN',b'{"x":NaN}'),('Infinity',b'{"x":Infinity}'),('negative Infinity',b'{"x":-Infinity}'),('overflow',b'{"x":1e9999}'),('trailing content',b'{} true'),('malformed JSON',b'{')]:reject(label,lambda raw=raw:ns['parse'](raw))
 manifest=ns['parse'](initial['PUBLICATION_MANIFEST.json'])
 def bad_manifest(label,change):
  m=copy.deepcopy(manifest);change(m);reject(label,lambda:ns['validate_manifest'](m,initial))
 for label,value in [('schema bool',True),('schema float',1.0),('schema string','1')]:bad_manifest(label,lambda m,value=value:m.update(schema=value))
 bad_manifest('manifest unknown key',lambda m:m.update(extra=0));bad_manifest('manifest missing key',lambda m:m.pop('schema'));bad_manifest('files wrong type',lambda m:m.update(files={}));bad_manifest('missing inventory row',lambda m:m['files'].pop());bad_manifest('duplicate inventory row',lambda m:m['files'].__setitem__(0,copy.deepcopy(m['files'][1])))
 for label,value in [('bool bytes',True),('float bytes',1.0),('negative bytes',-1),('large bytes',10**30),('string bytes','1')]:bad_manifest(label,lambda m,value=value:m['files'][0].update(bytes=value))
 for value in ['../outside','/tmp/outside',1,'BOOTSTRAP.py','PUBLICATION_MANIFEST.json']:bad_manifest('invalid manifest path '+str(value),lambda m,value=value:m['files'][0].update(path=value))
 bad_manifest('bad digest',lambda m:m['files'][0].update(sha256='z'*64));bad_manifest('row unknown key',lambda m:m['files'][0].update(extra=0));bad_manifest('problem bool',lambda m:m.update(problem_id=True));bad_manifest('problem float',lambda m:m.update(problem_id=30006088.0))
 for expected,validator in [('EXPECTED_ACCEPTANCE','validate_acceptance'),('EXPECTED_STATUS','validate_status')]:
  template=ns[expected]
  for key,value in template.items():
   obj=copy.deepcopy(template);obj[key]=not value if type(value) is bool else value+1 if type(value) is int else str(value)+' CORRUPTED'
   reject(expected+' altered '+key,lambda obj=obj,validator=validator:ns[validator](obj))
  obj=copy.deepcopy(template);obj['schema']=True;reject(expected+' bool integer',lambda obj=obj,validator=validator:ns[validator](obj))
  obj=copy.deepcopy(template);obj['problem_id']=30006088.0;reject(expected+' float integer',lambda obj=obj,validator=validator:ns[validator](obj))
  obj=copy.deepcopy(template);obj['extra']=0;reject(expected+' extra field',lambda obj=obj,validator=validator:ns[validator](obj))
  obj=copy.deepcopy(template);obj.pop('schema');reject(expected+' missing field',lambda obj=obj,validator=validator:ns[validator](obj))
 comparator=[]
 def compare_reject(label,call):
  before=len(semantic);reject(label,call);comparator.append(semantic.pop());need(len(semantic)==before,'separate comparator evidence')
 for script in ns['SCRIPTS']:
  out=initial[ns['refname'](script,'stdout')];err=initial[ns['refname'](script,'stderr')]
  def bad_output(label,raw,error=err,code=0):compare_reject(script+' '+label,lambda:ns['compare_output'](script,code,raw,error,out,err))
  parsed=ns['parse'](out);key='status';status_token=json.dumps(parsed[key]).encode();needle=('"'+key+'": ').encode()+status_token
  need(out.count(needle)==1,'unique comparator status target')
  numeric='finite_graph_checks' if script=='check_exact.py' else 'effective_uid' if script=='audit_exact.py' else 'child_physical_denials'
  value=parsed['environment'][numeric] if script=='audit_exact.py' else parsed[numeric];number_token=('"'+numeric+'": '+str(value)).encode()
  need(out.count(number_token)==1,'unique comparator integer target')
  bad_output('PASS only',b'{"status":"PASS"}\n');bad_output('extra stdout',out+b'PASS\n');bad_output('changed formatting',out.replace(needle,('"'+key+'":').encode()+status_token));bad_output('integer bool',out.replace(number_token,('"'+numeric+'": true').encode()));bad_output('integer float',out.replace(number_token,('"'+numeric+'": '+str(value)+'.0').encode()));bad_output('unexpected stderr',out,b'warning\n');bad_output('exit bool',out,err,False);bad_output('exit float',out,err,0.0);bad_output('wrong exit',out,err,1)
  if script=='guard_checks.py':
   other=initial[script[:-3]+'.mode'+str((sys.flags.optimize+1)%3)+'.reference.stdout'];need(other!=out,'mode-specific guard reference differs');bad_output('wrong optimization mode',other)
  bad_output('duplicate key',out.replace(needle,needle+b', '+needle))
  compare_reject(script+' replaced reference',lambda:ns['compare_output'](script,0,b'{}',err,b'{}',err))
 for a,b in [(True,1),(1.0,1),({'x':[True]}, {'x':[1]}),({'x':[1.0]}, {'x':[1]}),({'x':[1,2]}, {'x':[1]}),({'x':[1],'extra':0}, {'x':[1]}),({'x':['1']},{'x':[1]})]:compare_reject('direct recursive typed comparator',lambda a=a,b=b:ns['compare_typed'](a,b))
 with tempfile.TemporaryDirectory(prefix='two-loop-hostile-') as td:
  td=Path(td);sentinel=td/'TRIGGERED';evil='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("bad")\nraise RuntimeError("hostile import")\n'
  for n in ['sitecustomize.py','usercustomize.py','json.py','hashlib.py','check_exact.py','audit_exact.py','guard_checks.py','DEPENDENCY_RUNNER.py','sympy.py','mpmath.py']:(td/n).write_text(evil)
  hostile=dict(env,PYTHONPATH=str(td),PYTHONSTARTUP=str(td/'sitecustomize.py'),PYTHONHOME=str(td),PYTHONINSPECT='1',PYTHONDONTWRITEBYTECODE='0')
  h=subprocess.run([sys.executable,'-I','-S','-B',*mode,str(root/'BOOTSTRAP.py'),str(root)],cwd=td,env=hostile,capture_output=True,timeout=200)
  need(h.returncode==0 and h.stdout==baseline.stdout and h.stderr==baseline.stderr and not sentinel.exists(),'full hostile baseline differs')
  hostile_record=dict(exit_code=h.returncode,stdout=h.stdout.decode(),stderr=h.stderr.decode(),sentinel_created=False,complete_baseline_output_equal=True)
 final=ns['integrity'](root,mp,bp);need(final==initial,'whole delivery changed')
 print(json.dumps(dict(schema=1,problem_id=30006088,status='PASS',uid=os.getuid(),euid=os.geteuid(),optimization=sys.flags.optimize,bootstrap_sha256=bp,manifest_sha256=mp,physical_denials=physical,baseline=dict(exit_code=baseline.returncode,stdout=baseline.stdout.decode(),stderr=baseline.stderr.decode()),integrity_negative_controls=negatives,semantic_negative_controls=semantic,direct_comparator_negative_controls=comparator,hostile_full_baseline=hostile_record,whole_delivery_unchanged=True,before={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(initial.items())},after={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(final.items())},validation_scope='Two-loop SLE scoped partial-results integrity; exact checks and numerical diagnostics distinct; full comparison unresolved'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:print('REJECT: mutation harness failed: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
