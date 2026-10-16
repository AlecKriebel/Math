import os,json,hashlib,subprocess,shutil,time,runpy,copy
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;V1=B.parent;ORIG=B.parents[2]/'original/unsolved_math_prioritization/attempts/6000001';T=B/'private/tmp/nonblocking';T.mkdir(parents=True,exist_ok=True)
R='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python';L=B/'launch_portable_gate.py';G=B/'portable_gate.py';W=B/'portable_worker.py';C=B/'compare_results.py';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();pins={p.name:sha(p) for p in [L,G,W,C]};records=[]
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def base(packet=ORIG,gate=G,worker=W,comparator=C,launcher=True):
 return [R,'-I','-S','-B',str(L if launcher else G),str(packet)]+(['--gate',str(gate)] if launcher else [])+['--gate-sha256',pins[G.name],'--worker',str(worker),'--worker-sha256',pins[W.name],'--comparator',str(comparator),'--comparator-sha256',pins[C.name],'--scratch',str(T)]
def reject(label,cmd,stage=None,marker=None):
 started=datetime.now(timezone.utc).isoformat();t=time.monotonic()
 try:p=subprocess.run(cmd,cwd=T,capture_output=True,text=True,timeout=5)
 except subprocess.TimeoutExpired as exc:raise RuntimeError('BLOCKING REGRESSION '+label) from exc
 elapsed=time.monotonic()-t;require(p.returncode!=0 and 'REJECTED' in p.stderr,'bad input accepted')
 if stage:require(stage in p.stderr,'wrong failure stage '+p.stderr)
 require(marker is None or not marker.exists(),'marker executed')
 records.append(dict(label=label,utc=started,command=cmd,timeout_seconds=5,timed_out=False,elapsed_seconds=elapsed,returncode=p.returncode,stderr=p.stderr,marker_absent=marker is None or not marker.exists()))
 print(label,'rejected',round(elapsed,3),flush=True)
for tool in ['gate','worker','comparator']:
 fifo=T/(tool+'.fifo');os.mkfifo(fifo);marker=T/(tool+'.executed')
 kwargs={tool:fifo};reject('actual_fifo_'+tool,base(**kwargs),stage='nonblocking executable authentication',marker=marker)
 if tool!='gate':reject('direct_gate_actual_fifo_'+tool,base(launcher=False,**kwargs),stage='external executable anchors',marker=marker)
packet=T/'fifo_packet';shutil.copytree(ORIG,packet);p=packet/'public/verify_math.py';p.unlink();os.mkfifo(p);reject('packet_actual_fifo',base(packet=packet),stage='source authentication')
# Deterministically replace a file with FIFO after directory entry stat and before open.
packet=T/'race_packet';shutil.copytree(ORIG,packet)
inject='''import sys,os,runpy
original_open=os.open
replaced=False
def raced_open(path,flags,*args,**kwargs):
 global replaced
 if not replaced and path=='verify_math.py' and 'dir_fd' in kwargs and not (flags & os.O_DIRECTORY):
  replaced=True;os.unlink(path,dir_fd=kwargs['dir_fd']);os.mkfifo(path,dir_fd=kwargs['dir_fd'])
 return original_open(path,flags,*args,**kwargs)
os.open=raced_open
p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')
'''
cmd=base(packet=packet,launcher=False);cmd=cmd[:4]+['-c',inject]+cmd[4:]
reject('regular_stat_to_fifo_open_race',cmd,stage='Opened object is not a regular file')
for tool in ['gate','worker','comparator']:
 oversized=T/(tool+'_oversized.py');oversized.write_bytes(b'X'*262145)
 reject('tool_cap_'+tool,base(**{tool:oversized}),stage='262144-byte cap')
 marker=T/(tool+'_tamper.executed');p=T/(tool+'_marker.py');source={'gate':G,'worker':W,'comparator':C}[tool]
 p.write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n'+source.read_text())
 reject('tool_marker_'+tool,base(**{tool:p}),stage='External executable anchor mismatch',marker=marker)
packet=T/'oversized_original';shutil.copytree(ORIG,packet);p=packet/'public/verify_math.py';p.write_bytes(p.read_bytes()+b'X'*1000000);reject('original_known_size_cap',base(packet=packet),stage='File exceeds bounded byte cap')
# Directly exercise bounded read's cap+1 stopping path when a regular file grows after fstat.
# This authenticates gate code but imports functions without invoking main, under required flags.
inject='''import sys,runpy,os,tempfile,json
m=runpy.run_path(sys.argv[1],run_name='gate_functions');p=sys.argv[2]
open(p,'wb').write(b'A'*4)
fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
real=os.fstat;once=[False]
def fstat_grow(n):
 info=real(n)
 if n==fd and not once[0]:once[0]=True;open(p,'ab').write(b'B'*100000)
 return info
os.fstat=fstat_grow
try:m['bounded_read'](fd,8)
except RuntimeError as exc:raise SystemExit('REJECTED bounded growth: '+str(exc))
finally:os.close(fd)
raise SystemExit('accepted growing file')
'''
reject('post_fstat_growth_bounded', [R,'-I','-S','-B','-c',inject,str(G),str(T/'growth')],stage='File changed or exceeded byte cap')
# Retain identical comparator semantics and rerun all 32 typed negative controls using copied comparator.
comp=runpy.run_path(str(C));actual=json.loads((V1/'evidence/author_math.stdout').read_text());expected=json.loads((ORIG/'public/VERIFICATION.json').read_text());compare=comp['compare'];compare(actual,expected)
comparison=json.loads((V1/'evidence/COMPARISON.json').read_text());negative_names=[r['case'] for r in comparison['negative_controls']]
typed=[]
def negative(name,mutation):
 a=copy.deepcopy(actual);mutation(a)
 try:compare(a,expected)
 except ValueError:typed.append(name);return
 raise RuntimeError('typed control accepted '+name)
negative('exact_integer_changed',lambda a:a.__setitem__('exact_residuals_checked',27));negative('bool_instead_of_integer',lambda a:a.__setitem__('exact_residuals_checked',True));negative('exact_symbolic_determinant',lambda a:a.__setitem__('two_dimensional_derivative_jet_determinant','575'));negative('missing_exact_key',lambda a:a.pop('symbolic_checks'));negative('extra_key_units_claim',lambda a:a.__setitem__('units','arbitrary_rescaled'));negative('sample_point_units_rescaled',lambda a:a['positive_hessian_completion_samples'][1]['point'].__setitem__(0,1000.0))
for field in sorted(comp['NUMERIC_FIELDS']):
 for label,val in [('nan',float('nan')),('infinity',float('inf')),('boolean',True),('string','1.0'),('integer',1)]:negative(field+'_'+label,lambda a,field=field,val=val:a['positive_hessian_completion_samples'][1].__setitem__(field,val))
for name,field,val in [('negative_eigenvalue','minimum_eigenvalue',-1e-13),('zero_eigenvalue','minimum_eigenvalue',0.0),('negative_residual','H_df_minus_dphi_max_abs',-1e-13),('loosened_author_residual','H_df_minus_dphi_max_abs',2e-6),('material_lambda_change','lambda',actual['positive_hessian_completion_samples'][1]['lambda']+1e-6),('material_eigenvalue_change','minimum_eigenvalue',actual['positive_hessian_completion_samples'][1]['minimum_eigenvalue']+1e-6),('material_residual_change','H_df_minus_dphi_max_abs',2e-10)]:negative(name,lambda a,field=field,val=val:a['positive_hessian_completion_samples'][1].__setitem__(field,val))
for i in range(4):negative('sample_'+str(i)+'_wrong_residual_type',lambda a,i=i:a['positive_hessian_completion_samples'][i].__setitem__('H_df_minus_dphi_max_abs',0))
require(typed==negative_names,'Typed controls changed')
# v1 seal and all 61 listed payloads unchanged, including historical FIFO vulnerability.
manifest=V1/'MANIFEST.json';require(sha(manifest)=='e535bb4b46e2ebac2d80713b9500eb6748a294fd8ff4d91f748c40f11946b091','Historical manifest changed')
for row in json.loads(manifest.read_text())['files']:
 p=V1/row['path'];require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Historical sealed payload changed')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',pins=pins,nonblocking_negative_controls=len(records),records=records,typed_controls=typed,typed_negative_controls=len(typed),historical_v1_seal_unchanged=True,comparator_byte_identical_to_v1=C.read_bytes()==(V1/'compare_results.py').read_bytes(),limits='Five-second subprocess timeouts test actual FIFO and forced stat/open replacement. The externally authenticated launcher must itself be a trusted regular script; Python cannot validate an untrusted script path before opening it. No OS sandbox.')
(B/'evidence/NONBLOCKING_TESTS.json').write_text(json.dumps(result,indent=2)+'\n')
