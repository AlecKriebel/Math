#!/usr/bin/env python3
"""Bind the review's supplementary Reid example to fresh complete primary text."""
import ast,hashlib,json,math,pathlib
from datetime import datetime,timezone
HERE=pathlib.Path(__file__).resolve().parent
code=(HERE.parent/'source_snapshot/review/independent_checks.py').read_text()
tree=ast.parse(code)
relators=next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='relators' for t in n.targets))
text=(HERE/'sources/reid_appendix.txt').read_text()
assert all(r in text for r in relators)
matrix=[[r.count(c)-r.count(c.upper()) for r in relators] for c in 'ab']
flat=[v for row in matrix for v in row]
assert matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]==0 and math.gcd(*flat)==4
assert all(row%4==0 for row in matrix[1])
prefix=[];value=0
for c in relators[0]:
 value+= {'a':-1,'A':1,'b':1,'B':-1}[c];prefix.append(value)
assert prefix.count(min(prefix))==prefix.count(max(prefix))==1
assert prefix.index(min(prefix))+1==4 and prefix.index(max(prefix))+1==9
result={'utc':datetime.now(timezone.utc).isoformat(),'source':json.loads((HERE/'REID_RETRIEVAL.json').read_text()),
 'complete_primary_read':'All5pages including full Lemma2.1, Claims1/2 and proof in Section2, compatibility discussion and references.',
 'relators':relators,'exact_relators_match_primary_text':True,'abelianization_matrix_rows_a_b':matrix,'rank':1,'smith_nonzero_invariant':4,'H1':'Z plus Z/4',
 'orientation_Z4_character_relator_check':True,'Brown_prefix_values':prefix,'unique_min_position':4,'unique_max_position':9,
 'old_script_input_boundary':'Original scripts read no external files: author uses symbolic roots and supplied coefficient rings; independent uses explicit cochains/presentations and graded-ring models. Source-to-manifold interpretation remains written mathematics, not certified by a stdout pass count.',
 'Reid_boundary':'Paper uses SnapPy census/presentation, cusp and approximately plus/minus1 matrix determinants for geometric orientation input. This audit does not independently certify hyperbolicity, exact holonomy matrices or the census. Exact relators/Brown word test bind the published-source example; no cup-product table is inferred from H1.',
 'not_a_new_fulltarget_proof_attempt':True}
(HERE/'BOUND_INPUT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_primary_relators':True,'abelianization':'Z plus Z/4','Brown_word_check':True,'geometry_certified_by_this_program':False},indent=2))
