#!/usr/bin/env python3
"""Exact diagnostics for the standard pi-boundary exclusion; not a knot census."""
from pathlib import Path
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
checks={}
def ck(label,predicate):
    if not bool(predicate): raise AssertionError(label)
    checks[label]='PASS'
# Exponent sums of actual Hantzsche-Wendt presentation (Sell Table 1;
# Chelnokov-Mednykh (3.1)): xy^2x^-1y^2, yx^2y^-1x^2, xyz.
relations=s.Matrix([[0,4,0],[4,0,0],[1,1,1]])
snf=smith_normal_form(relations,domain=ZZ)
ck('hw_relation_full_rank',relations.rank()==3)
ck('hw_homology_order_16',abs(relations.det())==16)
ck('hw_smith_z4_z4',sorted(abs(snf[i,i]) for i in range(3))==[1,4,4])
ck('hw_homology_even_order',abs(relations.det())%2==0)
# Other five types have an explicit epimorphism to Z. The generator order
# for each twist is (alpha,t1,t2,t3), and t1=alpha^k in abelianization.
twists={
    2:s.Matrix([[2,-1,0,0],[0,0,2,0],[0,0,0,2]]),
    3:s.Matrix([[3,-1,0,0],[0,0,1,-1],[0,0,1,2]]),
    4:s.Matrix([[4,-1,0,0],[0,0,1,-1],[0,0,1,1]]),
    6:s.Matrix([[6,-1,0,0],[0,0,1,-1],[0,0,1,0]])}
for k,r in twists.items():
    character=s.Matrix([1,k,0,0])
    ck('twist_'+str(k)+'_relations_annihilate_z_character',r*character==s.zeros(3,1))
    ck('twist_'+str(k)+'_positive_first_betti',4-r.rank()==1)
    ck('twist_'+str(k)+'_surjective_z_character',s.gcd_list(list(character))==1)
ck('torus_positive_first_betti',s.zeros(3).rank()==0)
# A symbolic genus-one check of the universal parity proof. The proof for
# all genera is in PROOF.md and uses the integral intersection form.
a,b,d=s.symbols('a b d',integer=True)
V=s.Matrix([[a,b],[b-1,d]])
ck('seifert_antisymmetric_unimodular',(V-V.T).det()==1)
P=V+V.T
ck('seifert_symmetric_determinant_formula',s.expand(P.det()-(4*a*d-(2*b-1)**2))==0)
ck('seifert_symmetric_determinant_odd',all(int(c)%2==0 for c in s.Poly(s.expand(P.det()-1),a,b,d).coeffs()))
ck('seifert_presentation_is_symmetric',P==P.T)
out={'passed':len(checks),'failed':0,'sympy_version':s.__version__,'checks':checks,'scope':'Exact presentation/SNF and parity diagnostics only; the universal knot double-cover and flat-classification deductions are in PROOF.md. No cone existence or general canonical-component claim is inferred.'}
Path(__file__).with_name('boundary_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
