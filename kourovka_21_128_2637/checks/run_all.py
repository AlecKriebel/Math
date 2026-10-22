"""Reproduce all author checks and assert the scope-critical outputs."""
from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parent
for name in ['arithmetic_checks.py','cover_homology.py','five_sheet_h4.py','small_quotients.py']:
 subprocess.run([sys.executable,"-B",str(ROOT/name)],check=True,cwd=ROOT)
a=json.loads((ROOT/'arithmetic_results.json').read_text())
c=json.loads((ROOT/'cover_homology_results.json').read_text())
v=json.loads((ROOT/'five_sheet_h4_results.json').read_text())
s=json.loads((ROOT/'small_quotients_results.json').read_text())
assert a['torsion_free_G_indices']==[252,150]
assert c['F4']['b1_Q']==3 and c['H4']['b1_Q']==0
assert v['degree']==300 and v['rank_d2_mod_p']==901 and v['b1_Q_exact']==0
assert s['F4']['image_order_counts']=={'1':1,'2':9,'3':8,'6':12}
assert s['H4']['image_order_counts']=={'1':1,'2':3,'3':2}
summary={'all_author_checks_passed':True,'scripts':4,'s3_assignments_total':2592,'rational_cover_betti':[3,0],'degree_300_cover_b1_Q':0,'full_problem_resolved':False,'independent_audit':'pending'}
(ROOT/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
