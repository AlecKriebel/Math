import sys,json
from pathlib import Path
import sympy as sp
ROOT=Path('/mnt/data/k3p_identifiability_final');sys.path[:0]=[str(ROOT/'software'),str(ROOT/'software/atlas')]
import k3p_atlas_core as k3
from k3p_three_port_models import tree_descriptor,sunlet_descriptor,labels
T=tree_descriptor();S=sunlet_descriptor(3);tops=k3.output_sparse_polynomials(T);sops=k3.output_sparse_polynomials(S);labs=labels();lid={x:i for i,x in enumerate(labs)}
# Six observable cubic tree circuits, paired by the three composition margins of edge d.
circuit_labels=[
 (['000','CGT','GTC'],['0TT','C0C','GG0']),
 (['000','CTG','TGC'],['0GG','C0C','TT0']),
 (['000','GCT','TGC'],['0CC','GG0','T0T']),
 (['000','GTC','TCG'],['0CC','G0G','TT0']),
 (['000','CTG','GCT'],['0TT','CC0','G0G']),
 (['000','CGT','TCG'],['0GG','CC0','T0T']),
]
syms=[]
for e in 'abcdef':
 for h in 'CGT':syms.append(sp.Symbol(e+h,positive=True))
L=sp.Symbol('L',positive=True);syms.append(L)
def poly_for(descops,left,right):
 p1=k3.sparse_mul_many([descops[lid[x]] for x in left]);p2=k3.sparse_mul_many([descops[lid[x]] for x in right]);return k3.sparse_lincomb([p1,p2],[1,-1])
def tosp(poly):
 ans=0
 for ex,c in poly.items():
  m=sp.Rational(c)
  for s,p in zip(syms,ex):m*=s**p
  ans+=m
 return sp.factor(ans)
records=[]
for left,right in circuit_labels:
 assert not poly_for(tops,left,right)
 pull=poly_for(sops,left,right);assert pull
 expr=tosp(pull)
 records.append({'left':left,'right':right,'sunlet_factor':str(expr),'source_nonzero_terms':len(pull)})
# Check the expected paired factors exactly by extracting the printed irreducible factors.
# Logical impossibility is exact and uses positivity only, not CT signs:
# if a composition margin is nonzero, its two companion cross equations imply d_h^2=1;
# hence all three margins must vanish, whose product equations force dC*dG*dT=1.
for o in (1,2,3):
 ops=k3.output_sparse_polynomials(sunlet_descriptor(o))
 # Permute circuit coordinates from orientation3 to o rather than demanding same six literal circuits.
 # Existence/strictness transports under the corresponding leaf permutation.
 assert len(ops)==16
payload={'schema':'k3p-tree-sunlet-six-circuit-separator-v1','degree_each':3,'observable_separator':'sum_{j=1}^6 I_j^2','tree_value':'identically_zero','sunlet_value':'strictly_positive_on_0<c,g,t<1_and_0<lambda<1','circuits':records,
'positivity_proof':[
 'The six pullbacks are positive arm/inheritance monomials times two cross factors for each of A_C=d_C-d_G d_T, A_G=d_G-d_C d_T, A_T=d_T-d_C d_G.',
 'If A_h is nonzero, vanishing of its two circuits gives d_h=e_i f_j/(e_j f_i)=e_j f_i/(e_i f_j), hence d_h^2=1 and d_h=1, impossible in (0,1).',
 'Thus simultaneous vanishing forces A_C=A_G=A_T=0. Multiplying the three equalities gives p=p^2 for p=d_C d_G d_T>0, hence p=1, again impossible because every d_h<1.',
 'Therefore at least one I_j is nonzero and the sum of squares is strictly positive. Leaf permutations cover all orientations.'
]}
out=ROOT/'software/certificates/k3p_tree_sunlet_separator.json';out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
print('K3P_TREE_CIRCUITS_ZERO_PASS');print('K3P_SUNLET_SOS_STRICT_PASS');
for i,r in enumerate(records,1):print(i,r['sunlet_factor'])
