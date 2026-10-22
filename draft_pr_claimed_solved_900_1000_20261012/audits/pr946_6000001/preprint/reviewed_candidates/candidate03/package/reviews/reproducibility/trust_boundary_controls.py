import json,os,shutil,subprocess,sys,time,hashlib
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;ORIG=B.parents[1]/'original/unsolved_math_prioritization/attempts/6000001';TMP=B/'private/tmp/trust';TMP.mkdir(parents=True,exist_ok=True)
R='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python';PIN='29cb50b07af6a65b633516b5d86eed1dae93d57cf2abfb264b18eb9555a29903'
records=[]
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def execute(packet,mode=0,extra=(),label='case',env2=False):
 temp=TMP/('temporary_'+label);temp.mkdir(exist_ok=True)
 cmd=[R,'-I','-S','-B']+(['-'+'O'*mode] if mode else [])+[str(packet/'verify_publication.py'),PIN,str(packet),*extra]
 env=dict(os.environ,TMPDIR=str(temp),PYTHONDONTWRITEBYTECODE='1')
 if env2:env.update(PYTHONOPTIMIZE='2',PYTHONPATH='/does/not/exist')
 t=time.monotonic();p=subprocess.run(cmd,cwd=TMP,env=env,capture_output=True,text=True,timeout=300)
 records.append(dict(label=label,command=cmd,env2=env2,returncode=p.returncode,stderr=p.stderr,stdout=p.stdout,elapsed_seconds=time.monotonic()-t))
 return p
for mode in (0,1,2):
 for case in ['sentinel_script','fifo','root_symlink','empty_directory','extra_file','proof_symlink']:
  packet=TMP/(str(mode)+'_'+case);shutil.copytree(ORIG,packet);marker=TMP/(str(mode)+'_'+case+'.executed')
  if case=='sentinel_script':
   p=packet/'public/verify_math.py';p.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n'+p.read_text())
  elif case=='fifo':os.mkfifo(packet/'unlisted_fifo')
  elif case=='empty_directory':(packet/'unlisted_empty').mkdir()
  elif case=='extra_file':(packet/'unlisted.txt').write_text('extra')
  elif case=='proof_symlink':
   p=packet/'public/PROOF.md';p.unlink();p.symlink_to(ORIG/'public/PROOF.md')
  elif case=='root_symlink':
   linked=TMP/(str(mode)+'_root_link');linked.symlink_to(packet,target_is_directory=True);packet=linked
  p=execute(packet,mode,label=str(mode)+'_'+case)
  require(p.returncode!=0 and 'REJECTED:' in p.stderr,'unsafe accepted');require(not marker.exists(),'payload executed before auth')
  records[-1]['payload_marker_absent']=True
 # Actual optimized-child bootstrap rejections under each outer mode.
 for child in (1,2):
  packet=TMP/(str(mode)+'_optimized_child_'+str(child));shutil.copytree(ORIG,packet)
  p=execute(packet,mode,('--child-optimize',str(child)),label=str(mode)+'_optimized_child_'+str(child))
  require(p.returncode!=0 and 'optimized child would remove frozen assertions' in p.stderr,'wrong child rejection')
  require('"optimize": '+str(child) in p.stderr,'missing actual flags')
# Real inherited optimization, with a bootstrap capturing flags before original execution.
boot='import sys,json,runpy; print(json.dumps(dict(optimize=sys.flags.optimize,debug=__debug__,isolated=sys.flags.isolated)),file=sys.stderr); p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name="__main__")'
for script in ['public/verify_math.py','independent_global_audit/public/independent_controls.py','independent_audit_b/public/independent_checks.py']:
 for label,opts,env2 in [('ordinary',[],False),('O',['-O'],False),('OO',['-OO'],False),('inherited_env2',[],True)]:
  packet=TMP/('flags_'+label+'_'+script.split('/')[0]);
  if not packet.exists():shutil.copytree(ORIG,packet)
  cmd=[R,'-B',*opts,'-c',boot,str(packet/script)];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
  if env2:env['PYTHONOPTIMIZE']='2'
  p=subprocess.run(cmd,cwd=TMP,env=env,capture_output=True,text=True,timeout=300);actual=json.loads(p.stderr.splitlines()[0]);require(actual['optimize']==(2 if env2 or label=='OO' else 1 if label=='O' else 0),'not actual mode')
  records.append(dict(label='actual_flags_'+label+'_'+script,command=cmd,env2=env2,actual_flags=actual,returncode=p.returncode,stderr=p.stderr,stdout_sha256=hashlib.sha256(p.stdout.encode()).hexdigest(),stdout_status=json.loads(p.stdout).get('status',json.loads(p.stdout).get('verdict')) if p.returncode==0 else None))
# Copy-before-execute controlled source mutation, after snapshot replay tree exists.
packet=TMP/'concurrent_source';shutil.copytree(ORIG,packet);temp=TMP/'temporary_concurrent';temp.mkdir();marker=TMP/'concurrent.executed'
cmd=[R,'-I','-S','-B',str(packet/'verify_publication.py'),PIN,str(packet)]
p=subprocess.Popen(cmd,cwd=TMP,env=dict(os.environ,TMPDIR=str(temp),PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
seen=None;deadline=time.monotonic()+30
while time.monotonic()<deadline and p.poll() is None:
 candidates=list(temp.glob('statistical-embedding-replay-*/packet/public/verify_math.py'))
 if candidates:
  seen=candidates[0];break
 time.sleep(.001)
require(seen is not None,'snapshot tree not observed')
source=packet/'public/verify_math.py';source.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n'+source.read_text())
out,err=p.communicate(timeout=300);require(not marker.exists(),'source tampering executed');require(p.returncode!=0,'concurrent mutation not rejected')
records.append(dict(label='copy_before_execute_source_mutation',command=cmd,authenticated_replay_copy_observed=True,payload_marker_absent=True,returncode=p.returncode,stdout=out,stderr=err,limitation='Original exits on numerical comparison before its final reauthentication. This test proves the mutated source payload did not execute after copied snapshot existed; it does not claim that the final source reauthentication ran.'))
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',controls=len(records),records=records,limitation='Static filesystem attacker controls tested. No claim against malicious kernel, runtime, concurrent directory substitution before reads, or hostile temporary-directory permissions.')
(B/'evidence/TRUST_BOUNDARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(records)},indent=2))
