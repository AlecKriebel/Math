import pathlib,json,hashlib,subprocess,sys,datetime,os,shutil
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616';D=A/'reviews/closure_package_adversary_01';T=D/'private_tmp/trusted_initial';P=T/'draft_pr_claimed_solved_900_1000_20261012';CA=P/'audits/pr967_2616';CA.mkdir(parents=True)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
b=(D/'private_tmp/old_trusted_launcher.py').read_bytes()
if sha(b)!='7d98d304d1bc54eab695324984c60a9e2aed2bc48ab62edb7fee6b9c5dce2ead':raise RuntimeError('external launcher pin changed before intake')
(D/'TRUSTED_LAUNCHER_REVIEWED.py').write_bytes(b)
source=b.decode();literal='root=Path("/Users/alec/Documents/Math")';replacement='root=Path('+json.dumps(str(T))+')'
if source.count(literal)!=1:raise RuntimeError('expected single allowed scratch root substitution')
code=source.replace(literal,replacement)
paths={}
for name,h in [('close_pr967.py','c6231a47758a6b037ed005883d39e374946e38bd9aec0c74eb33df3afe2d2a45'),('finalize_pr967_and_gate_next.py','47520f8f86889db8c5b85fc7000486773d2ca4e8601ad00531bad2fdce5143cb')]:
 raw=(A/'closure_engineering_01'/('FINAL02_'+name)).read_bytes()
 if sha(raw)!=h:raise RuntimeError('external helper pin changed')
 paths[P/name]=raw
raw=(A/'CLOSURE_OPERATIONS_INVENTORY.json').read_bytes()
if sha(raw)!='ad94d62072583e62092215bf919c974f237d52efb1f048e60bbee5724a370d0d':raise RuntimeError('old inventory no longer live; use old captured inventory')
paths[CA/'CLOSURE_OPERATIONS_INVENTORY.json']=raw
for p,raw in paths.items():p.write_bytes(raw)
runs=[];sentinel=T/'UNAUTHENTICATED_HELPER_EXECUTED'
def run(label,flags,action='close',ok=False):
 cmd=[sys.executable,*flags,'-c',code,action,'--help'];start=now();r=subprocess.run(cmd,cwd=T,capture_output=True,timeout=20)
 if (r.returncode==0)!=ok or sentinel.exists():raise RuntimeError('trusted launcher control failed '+label)
 runs.append({'label':label,'argv':cmd,'started_utc':start,'completed_utc':now(),'returncode':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'expected_success':ok,'untrusted_sentinel_absent':not sentinel.exists()})
for mode,extra in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 flags=['-I','-S','-B',*extra]
 for action in ['close','finalize']:run(mode+'_actual_captured_initial_'+action+'_help',flags,action,True)
 for p,raw in paths.items():
  for mutation in ['same_size','append','symlink','hardlink']:
   p.unlink()
   if mutation=='same_size':
    evil=('from pathlib import Path; Path('+repr(str(sentinel))+').write_text("EXECUTED")\n').encode();bad=evil+b' '*(len(raw)-len(evil));p.write_bytes(bad)
   elif mutation=='append':p.write_bytes(raw+b'X')
   elif mutation=='symlink':
    target=p.with_name(p.name+'.symlink-target');target.write_bytes(raw);p.symlink_to(target)
   else:
    target=p.with_name(p.name+'.hardlink-target');target.write_bytes(raw);os.link(target,p)
   run(mode+'_'+p.name+'_'+mutation+'_reject_before_compile',flags)
   p.unlink();p.write_bytes(raw)
run('missing_isolated_flag',['-S','-B']);run('missing_no_site_flag',['-I','-B']);run('missing_no_bytecode_flag',['-I','-S'])
(D/'TRUSTED_LAUNCHER_REPRODUCTIONS.json').write_text(json.dumps({'utc':now(),'original_launcher_sha256':sha(b),'scratch_adapter_sha256':sha(code.encode()),'only_adaptation':{'from':literal,'to':replacement},'actual_case_count':len(runs),'helper_compile_optimization':0,'no_service_or_Git_operations':True,'runs':runs},indent=2)+'\n');print(json.dumps({'actual_cases':len(runs),'all_pass':True}))
