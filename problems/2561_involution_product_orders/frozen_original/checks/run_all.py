"""Run all exact checks and verify expected outputs, including a negative control."""
import json, subprocess, sys
from pathlib import Path
if not __debug__:
    raise RuntimeError('Assertions are proof checks: do not run Python with -O.')
HERE=Path(__file__).resolve().parent
for script in ['colored_involutions.py','local_reconstruction.py','alternating_reconstruction.py','four_transposition_checks.py','symplectic_checks.py']:
    subprocess.run([sys.executable,str(HERE/script)],cwd=HERE,check=True)
r=json.loads((HERE/'small_group_results.json').read_text())
for name,expect in {'A5_2':(15,8,120),'A6_2':(45,32,1440),'PSL2_7':(21,16,336),'PSL2_11':(55,24,1320),'A7_2':(105,48,5040),'A8_4':(105,384,40320)}.items():
    z=r[name]
    assert (z['vertices'],z['stabilizer_size'],z['group_order'])==expect
    assert z['all_stabilizer_automorphisms_extend'] and not z.get('incomplete',False)
a=json.loads((HERE/'alternating_reconstruction_results.json').read_text())
for n,size,cs,pairs in [(8,210,18,96),(9,378,38,170),(10,630,78,276),(11,990,150,420),(12,1485,269,608)]:
    z=a[str(n)];assert z['class_size']==size and z['commuting_vertices']==cs
    assert z['signature_fiber_sizes']=={'2':pairs} and z['all_noncommuting_fibers_are_conjugate_pairs']
l=json.loads((HERE/'local_reconstruction_results.json').read_text())
assert l['A7_2']['two_point_criterion_pass'] and l['A7_2']['stable_cell_sizes']=={'2':48}
assert not l['A5_2']['two_point_criterion_pass'] and not l['A6_2']['two_point_criterion_pass']
f=json.loads((HERE/'four_transposition_results.json').read_text())
assert f['9']['fiber_sizes']=={'2':68,'4':196} and f['10']['fiber_sizes']=={'2':272,'4':1032}
assert not f['9']['two_point_criterion_pass'] and not f['10']['two_point_criterion_pass']
s=json.loads((HERE/'symplectic_results.json').read_text())
assert all(x['all_pair_order_and_hyperplane_tests_pass'] for x in s)
assert s[-1]['full_colored_graph']['group_order']==1512
from colored_involutions import alternating_class,tables,solve
M,C=tables(alternating_class(5,2));M2=[[1 if i==j else (2 if M[i][j]==2 else 3) for j in range(15)] for i in range(15)]
try:
    solve(M2,C,max_nodes=10000,max_seconds=10)
except AssertionError as e:
    if not(e.args and isinstance(e.args[0],tuple) and e.args[0][0]=='nonextendible'):raise
else:raise AssertionError('A5 commuting-only negative control was not rejected')
summary={'all_positive_checks_pass':True,'commuting_only_negative_control_rejected':True,'new_proof_attempts':5,'full_problem_resolved':False,'formal_proof_assistant_certificate':False}
(HERE/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
