"""Own symbolic universal substitution of the primary eight-term quartic.
The polynomial body is transcribed from K3P Theorem5.2 equation6 and checked
against the literal target map. No supplied code is imported or executed.
"""
import sympy as s
from itertools import permutations
import json
G=range(4);triples=[(x,y,x^y) for x in G for y in G];qs={t:s.Symbol('q'+''.join(map(str,t))) for t in triples};q=lambda t:qs[t]
terms=[(1,[(0,0,0),(1,2,3),(2,3,1),(3,1,2)]),(-1,[(0,0,0),(1,3,2),(2,1,3),(3,2,1)]),(-1,[(0,1,1),(1,2,3),(2,0,2),(3,3,0)]),(1,[(0,1,1),(1,3,2),(2,2,0),(3,0,3)]),(1,[(0,2,2),(1,0,1),(2,1,3),(3,3,0)]),(-1,[(0,2,2),(1,1,0),(2,3,1),(3,0,3)]),(-1,[(0,3,3),(1,0,1),(2,2,0),(3,1,2)]),(1,[(0,3,3),(1,1,0),(2,0,2),(3,2,1)])]
F=sum(sign*s.prod(q(t) for t in monomial) for sign,monomial in terms);fn=F.subs(q((0,0,0)),1);lam=s.Symbol('lam');E={k:[s.Integer(1)]+list(s.symbols(k+'1:4')) for k in 'abcdef'}
vals={}
for x,y,z in triples:
 a,b,c,d,e,f=[E[k] for k in 'abcdef'];vals[(x,y,z)]=a[x]*b[y]*c[z]*(lam*f[y]*d[z]+(1-lam)*f[x]*e[z])
identities=[]
for p in permutations(range(3)):
 z=s.expand(F.xreplace({qs[t]:vals[tuple(t[i] for i in p)] for t in triples}));identities.append({'port_permutation':p,'universal_pullback_zero':z==0})
 if z!=0:raise RuntimeError('quartic_identity_failure')
char_signs=[]
for p in permutations([1,2,3]):
 m=[0]+list(p);sign=(-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3));z=s.expand(F.xreplace({qs[t]:qs[tuple(m[h] for h in t)] for t in triples})-sign*F)
 if z!=0:raise RuntimeError('character_sign_identity_failure')
 char_signs.append({'nonzero_character_permutation':p,'sign':sign,'exact_polynomial_identity':True})
point={qs[t]:s.Integer(1) if t==(0,0,0) else s.Rational(1,12) if 0 in t else s.Rational(1,48) for t in triples};gradient={str(qs[t]):str(s.diff(F,qs[t]).subs(point)) for t in triples if t!=(0,0,0) and s.diff(F,qs[t]).subs(point)!=0}
A=s.expand(fn).coeff(q((0,1,1)));B=s.expand(fn-A*q((0,1,1)));spec={v:s.Integer(1) if v in [q((1,3,2)),q((2,1,3)),q((3,2,1))] else s.Integer(0) for v in (A.free_symbols|B.free_symbols)}
if s.expand(A.subs(spec))!=0 or s.expand(B.subs(spec))!=-1:raise RuntimeError('Gauss_irreducibility_specialization')
# A consists of two disjoint squarefree monomials with primitive exponent difference.
mon=s.Poly(A,*sorted(A.free_symbols,key=str)).monoms();disjoint=all(a*b==0 for a,b in zip(*mon))
if len(mon)!=2 or not disjoint or not all(v in [0,1] for m in mon for v in m):raise RuntimeError('primitive_disjoint_support_coefficient')
print(json.dumps({'global_identity':'F composed with literal sunlet map is identically zero over Q, for all six labelled port permutations','universal_identities':identities,'character_sign_identities':char_signs,'normalized_F_nonzero':fn!=0,'gradient_at_common_strict_point':gradient,'irreducibility_control':{'coefficient_A':str(A),'two_disjoint_squarefree_monomials':True,'specialization_A':str(A.subs(spec)),'specialization_remainder_B':str(B.subs(spec)),'argument':'Primitive exponent-difference binomial A is irreducible over C; displayed specialization proves A does not divide B; Gauss lemma for A*q011+B gives irreducibility.'},'combined_with_early_exact_rank':'For each ordinary orientation generic rank14, irreducible closure equal to H14, rank14 smooth relative germ at the shared strict point. Does not prove contextual all-network classification or imported atlases.'},indent=2))
