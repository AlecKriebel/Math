#!/usr/bin/env python3
"""Replay exact original programs and actual geometry mutations in a private directory."""
from pathlib import Path
import subprocess,json,hashlib,shutil,tempfile,datetime
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent; REPO=HERE.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((AUDIT/'snapshot_manifest.json').read_text())
original=AUDIT/'source_snapshot';before={a['path']:sha(original/a['path']) for a in manifest['files']}
for a in manifest['files']:
 p=original/a['path'];assert p.stat().st_size==a['size'] and sha(p)==a['sha256']
 r=subprocess.run(['git','show',manifest['head']+':unsolved_math_prioritization/attempts/2744/'+a['path']],cwd=REPO,capture_output=True)
 assert r.returncode==0 and r.stdout==p.read_bytes(),a['path']
assert len(before)==15
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':manifest['head'],'original_base':manifest['base'],'original_files_verified':15,'original_bindings':before,'original_replays':[],'mutants':[],'false_prose_runs':[]}
with tempfile.TemporaryDirectory(prefix='cone_actual_',dir=HERE/'private_replay') as tmp:
 d=Path(tmp);private=d/'source_snapshot';shutil.copytree(original,private)
 for rel,result in [('check_controls.py','check_results.json'),('independent_review/submitted_check_controls.py','independent_review/check_results.json'),('independent_review/independent_checks.py','independent_review/independent_results.json')]:
  r=subprocess.run(['/usr/bin/python3',str(private/rel)],cwd=private,capture_output=True,text=True)
  assert r.returncode==0 and not r.stderr,(rel,r.stderr)
  expected=original/('check_results.json' if 'submitted_' in rel else result)
  assert (private/result).read_bytes()==expected.read_bytes(),rel
  out['original_replays'].append({'program':rel,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'result_sha256':sha(private/result),'expected_sha256':sha(expected),'byte_exact':True})
 # Actually poison the nearby scientific narrative: old programs still pass.
 poison=private/'OBSTRUCTION.md';poison.write_text('# False mutation\nThe full problem is solved for every hyperbolic knot. A connected path suffices even through singular points. All real traces are unitary.\n')
 for rel in ['check_controls.py','independent_review/independent_checks.py']:
  r=subprocess.run(['/usr/bin/python3',str(private/rel)],cwd=private,capture_output=True,text=True)
  assert r.returncode==0 and not r.stderr
  out['false_prose_runs'].append({'program':rel,'mutated_artifact_sha256':sha(poison),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'interpretation':'Old exact controls do not read/certify the scientific narrative; this is an expected scope failure of false prose detection.'})
 source=(HERE/'geometric_controls.py').read_text()
 changes=[('singular_node_called_regular',"ck('node_is_singular',s.Matrix([s.diff(f,x),s.diff(f,y)]).subs({x:0,y:0})==s.zeros(2,1))","ck('node_is_singular',s.Matrix([s.diff(f,x),s.diff(f,y)]).subs({x:0,y:0})!=s.zeros(2,1))"),('regeneration_angle_wrong_sign','mu=alpha+z*z','mu=alpha-z*z'),('unitary_family_wrong_conjugate','U=s.diag(c+s.I*d,c-s.I*d)','U=s.diag(c+s.I*d,c+s.I*d)'),('finite_quotient_collapsed','q=s.factor(s.trace(U)**2)','q=s.Integer(4)'),('noncompact_pair_incorrect','B=s.Matrix([[0,-4],[s.Rational(1,4),0]])','B=s.Matrix([[0,-1],[1,0]])'),('o2_wrong_embedding','R[2,2]=Q.det()','R[2,2]=1'),('wrong_schlafli_sign','((-L/2)*(-1))','((L/2)*(-1))'),('source_final_volume_sign','expr==2*s.pi*(alpha-s.pi)','expr==2*s.pi*(s.pi-alpha)')]
 for name,a,b in changes:
  assert source.count(a)==1,(name,source.count(a));folder=d/name;folder.mkdir();p=folder/'geometric_controls.py';p.write_text(source.replace(a,b))
  r=subprocess.run(['/usr/bin/python3',str(p)],cwd=folder,capture_output=True,text=True)
  assert r.returncode!=0 and 'AssertionError:' in r.stderr,(name,r.stdout,r.stderr)
  out['mutants'].append({'name':name,'program_sha256':sha(p),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'rejected':True})
 assert before=={a['path']:sha(original/a['path']) for a in manifest['files']}
out['original_unchanged_after']=True
out['original_assertions']=21+21+121
out['new_geometric_assertions']=28
out['rejected_geometric_mutants']=8
out['scope']='Original algebraic controls and 28 exact new diagnostics do not prove any knot cone-manifold existence or the universal question; see the complete universal conditional source/proof audit.'
(HERE/'REPRODUCTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['original_files_verified','original_assertions','new_geometric_assertions','rejected_geometric_mutants','original_unchanged_after']},indent=2))
