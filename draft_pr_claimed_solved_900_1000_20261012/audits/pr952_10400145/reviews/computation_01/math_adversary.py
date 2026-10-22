#!/usr/bin/env python3
"""Final math/profile cold launches and substantive altered-mechanism controls."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,time
W=Path(__file__).resolve().parent;T=W/'tmp';rows=[]
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(label,script,args=(),mode='',success=True):
    t=time.perf_counter();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run([sys.executable,'-I','-S','-B',*([mode] if mode else []),str(script),*map(str,args)],cwd=T/'work',env=dict(os.environ,TMPDIR=str(T/'temp')),capture_output=True,timeout=90)
    r={'label':label,'mode':mode or 'normal','utc':utc,'script_sha256':sha(script.read_bytes()),'elapsed_seconds':round(time.perf_counter()-t,6),'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stderr':p.stderr.decode(),'expected_success':success}
    if p.stdout:
        try:r['output']=json.loads(p.stdout)
        except ValueError:r['stdout']=p.stdout.decode()
    rows.append(r);(W/'MATH_ADVERSARY_RESULTS.json').write_text(json.dumps({'schema':'pr952-final-math-adversary-v1','rows':rows},indent=2)+'\n')
    need((p.returncode==0 and not p.stderr) if success else p.returncode!=0,'unexpected '+label+' '+mode)
    return p
initial=(W/'independent_math.py').read_text(); good=None
for mode in ['','-O','-OO']:
    p=run('final-independent-math',W/'independent_math.py',mode=mode)
    if good is None:good=p.stdout
    need(p.stdout==good,'final math optimization changed output')
(W/'MATH_RESULTS.json').write_bytes(good)
for label,old,new in [('drop-tail-factor','range(k+2,2*k+2)','range(k+3,2*k+2)'),('wrong-cubic-linear-part','cubic=[0,-1,0,1]','cubic=[0,1,0,1]'),('omit-first-summand','for k in range(7):jet=','for k in [0,2,3,4,5,6]:jet='),('wrong-q-scale','q=[1,1]\n    need','q=[1,2]\n    need'),('wrong-Gaussian-exponent','power([1,1],N-k)','power([1,1],N-k-1)')]:
    need(old in initial,'mutation anchor');p=T/(label+'.py');p.write_text(initial.replace(old,new))
    for mode in ['','-O','-OO']:run(label,p,mode=mode,success=False)
packet=T/'cold_packet'
for mode in ['','-O','-OO']:
    run('portable-profile-baseline',W/'portable_profile.py',['--packet',packet,'--work-dir',T/'work'],mode)
# Profile negates its own stricter stated mode and ancestor namespace boundary.
for label,p in [('mode-only',T/'integrity_mode-only'),('world-writable',T/'integrity_world-writable'),('parent-symlink',T/'alias/integrity_parent-symlink'),('root-symlink',T/'direct-root-link'),('extra-shadow',T/'integrity_extra-shadow'),('extra-dir',T/'integrity_extra-dir'),('symlink-payload',T/'integrity_symlink-payload'),('fifo',T/'integrity_fifo'),('stale-proof',T/'integrity_stale-proof')]:
    for mode in ['','-O','-OO']:run('portable-reject-'+label,W/'portable_profile.py',['--packet',p,'--work-dir',T/'work'],mode,success=False)
for mode in ['','-O','-OO']:run('portable-no-isolation-positive-driver',W/'portable_profile.py',['--packet',packet,'--work-dir',packet],mode,success=False)
# A missing -I/-S/-B launch is an actual negative outside the run helper.
t=time.perf_counter();p=subprocess.run([sys.executable,str(W/'portable_profile.py'),'--packet',str(packet),'--work-dir',str(T/'work')],cwd=T/'work',capture_output=True,timeout=10)
need(p.returncode!=0 and b'launch requires' in p.stderr,'profile isolation flags not enforced');rows.append({'label':'portable-reject-missing-isolation-flags','elapsed_seconds':round(time.perf_counter()-t,6),'exit_code':p.returncode,'stderr':p.stderr.decode(),'expected_success':False})
r={'schema':'pr952-final-math-adversary-v1','status':'PASS_REVIEW_CONTROLS','row_count':len(rows),'elapsed_seconds_sum':round(sum(x['elapsed_seconds'] for x in rows),6),'rows':rows};(W/'MATH_ADVERSARY_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'rows':len(rows),'elapsed_seconds_sum':r['elapsed_seconds_sum']}))
