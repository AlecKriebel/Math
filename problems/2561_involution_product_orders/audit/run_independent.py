"""Portable replay of the independent reviewer controls and exact expected outcomes."""
from pathlib import Path
import json,subprocess,sys
if not __debug__:raise RuntimeError('Do not run the audit with Python -O.')
A=Path(__file__).resolve().parent
for name in ['independent_checks','adversarial_solver_checks','psl2_even_independent','a6_outer_witness']:
    r=subprocess.run([sys.executable,str(A/(name+'.py'))],cwd=A,capture_output=True,text=True)
    (A/(name+'.portable.log')).write_text(r.stdout+r.stderr)
    if r.returncode:raise RuntimeError((name,r.returncode,r.stderr))
r=json.loads((A/'adversarial_solver_results.json').read_text())
assert r['bruteforce_graphs']==1106 and r['all_counts_match'] and r['explicit_negative_control']
assert r['node_limit_fails_closed'] and r['optimized_runner_refused']
a=json.loads((A/'a6_outer_witness.json').read_text());assert a['exceptional_outer_stabilizer_elements']==16
p=json.loads((A/'psl2_even_independent_results.json').read_text());assert p['whole_group_order']==504 and p['all_involutions']==63
z=json.loads((A/'independent_results.json').read_text());assert all(t['pairs'] for t in z if t['k']==2 and t['degree']>=8)
summary={'portable_independent_replay':'PASS','bruteforce_graphs':1106,'original_problem_status':'unsolved','proof_attempts':5,'added_proof_attempts':0}
(A/'portable_replay_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
