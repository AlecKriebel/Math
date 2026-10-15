#!/usr/bin/env python3
"""Actually execute source-mutated independent controls and old-program prose controls."""
from pathlib import Path
import subprocess,json,hashlib,shutil
HERE=Path(__file__).resolve().parent
source=(HERE/'exact_controls.py').read_text()
mutations={
 'wrong_C_y':("C=S.Matrix([-x**3,y**3,1]);R2=", "C=S.Matrix([-x**3,-y**3,1]);R2="),
 'wrong_height_graph_sign':("gamma=S.Matrix([x,y,(x*x-y*y)/4])", "gamma=S.Matrix([x,y,-(x*x-y*y)/4])"),
 'omit_C_norm_constant':("R2=1+x**6+y**6;q=", "R2=x**6+y**6;q="),
 'wrong_torsion_coefficient':("C.dot(gppp)-3*x*y", "C.dot(gppp)-2*x*y"),
 'wrong_shear_linear_sign':("expected=e/r+e*(x**4+y**4)/(2*r)", "expected=e/r-e*(x**4+y**4)/(2*r)"),
 'omit_push_off_normalization':("P=gamma+e*C/r", "P=gamma+e*C"),
 'wrong_torsion_sign_geodesic_curvature':("S.simplify(kg-k/abs(tors))==0", "S.simplify(kg-k/tors)==0"),
}
rows=[]
for name,(old,new) in mutations.items():
 assert source.count(old)==1,(name,source.count(old))
 folder=HERE/'tmp'/'actual_mutations'/name;folder.mkdir(parents=True,exist_ok=True)
 f=folder/'exact_controls.py';f.write_text(source.replace(old,new))
 result=subprocess.run(['/usr/bin/python3',str(f)],capture_output=True,text=True)
 assert result.returncode!=0 and 'AssertionError:' in result.stderr,name
 rows.append({'name':name,'rejected':True,'exit_code':result.returncode,'exact_assertion':result.stderr.split('AssertionError:',1)[1].strip(),'mutated_program_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'stdout_empty':result.stdout==''})
# Old scripts do not inspect adjacent theorem prose; actual controls demonstrate
# that their successful replay alone cannot validate a claimed global result.
snapshot=HERE.parent/'source_snapshot';old=[]
for label,rel in [('author','verify.py'),('old_independent','review/independent_checks.py')]:
 folder=HERE/'tmp'/'old_prose_mutations'/label;folder.mkdir(parents=True,exist_ok=True)
 f=folder/Path(rel).name;shutil.copy2(snapshot/rel,f)
 prose=folder/'OBSTRUCTION.md'
 prose.write_text('FALSE CLAIM: Every smooth injective spherical binormal is regular and linking is nonzero. The exact cos2t countermodel is wrongly excluded solely because its derivative has zeros.\n')
 result=subprocess.run(['/usr/bin/python3',str(f)],capture_output=True,text=True)
 assert result.returncode==0 and result.stderr=='',label
 expected=(HERE/('author_replay.stdout.json' if label=='author' else 'old_independent_replay.stdout.json')).read_text()
 assert result.stdout==expected,label
 old.append({'label':label,'false_global_prose_accepted':True,'program_unchanged':f.read_bytes()==(snapshot/rel).read_bytes(),'result_byte_exact_original':True,'corrupted_prose_sha256':hashlib.sha256(prose.read_bytes()).hexdigest(),'scope':'Expected: original scripts explicitly claim only local algebra; their unchanged success is not a whole-theorem certificate.'})
out={'actual_program_mutations_rejected':rows,'rejected_count':len(rows),'actual_original_program_false_prose_controls':old,'passed':True}
s=json.dumps(out,indent=2,sort_keys=True)+'\n';(HERE/'mutation_results.json').write_text(s);print(s,end='')
