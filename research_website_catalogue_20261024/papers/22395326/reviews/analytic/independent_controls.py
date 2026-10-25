"""Own exact algebra/graph diagnostics, written before any companion/code reading.
Universal mathematical proof obligations are recorded separately; this is not
an all-network classification by finite enumeration.
"""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
from fractions import Fraction
import sympy as s,json,time
start=time.monotonic();R=Path.cwd()
chars=(0,1,2,3);triples=[(x,y,x^y)for x,y in product(chars,repeat=2)];outputs=[g for g in triples if any(g)]
L=s.Symbol('lam');edge={k:[s.Integer(1)]+list(s.symbols(k+'1:4'))for k in 'abcdef'}
params=[p for k in 'abcdef'for p in edge[k][1:]]+[L]
a,b,c,d,e,f=[edge[k]for k in 'abcdef']
q={g:s.expand(a[g[0]]*b[g[1]]*c[g[2]]*(L*f[g[1]]*d[g[2]]+(1-L)*f[g[0]]*e[g[2]]))for g in triples}
point={p:s.Rational(1,3)if k=='f'else s.Rational(1,2)for k in 'abcdef'for p in edge[k][1:]};point[L]=s.Rational(1,2)
q0=s.Matrix([q[g].subs(point)for g in outputs]);J=s.Matrix([q[g]for g in outputs]).jacobian(params);Jp=J.subs(point)
Jlog=s.diag(*[1/x for x in q0])*Jp*s.diag(*[point[p]if p!=L else 1 for p in params])
def sign(p):return(-1)**sum(p[i]>p[j]for i in range(3)for j in range(i+1,3))
def perm_mat(objects,action):
 idx={v:i for i,v in enumerate(objects)};M=s.zeros(len(objects))
 for j,v in enumerate(objects):M[idx[action(v)],j]=1
 return M
pobjects=[(k,h)for k in 'abcdef'for h in [1,2,3]]+[('lam',0)]
PO=[];PI=[]
for p in permutations([1,2,3]):
 mp={0:0,**dict(zip([1,2,3],p))}
 po=perm_mat(outputs,lambda g:tuple(mp[h]for h in g));pi=perm_mat(pobjects,lambda v:(v[0],mp[v[1]])if v[0]!='lam'else v)
 if po*Jlog!=Jlog*pi:raise ValueError('equivariance')
 PO.append((p,po));PI.append((p,pi))
E0=sum((M for _,M in PO),s.zeros(15))/6;Es=sum((sign(p)*M for p,M in PO),s.zeros(15))/6;Ev=s.eye(15)-E0-Es
iso_ranks=[(E*Jlog).rank()for E in [E0,Ev,Es]]
if iso_ranks!=[4,10,0]:raise ValueError(iso_ranks)
ranks=[]
for r in [1,2,3]:
 blocks=[[1,2,3]]if r==1 else [[1,3],[2]]if r==2 else [[1],[2],[3]]
 emb=s.zeros(19,6*r+1)
 for ki,k in enumerate('abcdef'):
  for j,block in enumerate(blocks):
   for h in block:emb[ki*3+h-1,ki*r+j]=1
 emb[18,6*r]=1;ranks.append((Jlog*emb).rank())
if ranks!=[4,9,14]:raise ValueError(ranks)
idx={g:i for i,g in enumerate(outputs)}
def row(g):return Jlog[idx[g],:]
rows0=s.Matrix.vstack(*(row(g)for g in [(1,1,0),(1,0,1),(0,1,1),(2,1,3)]));J0=s.zeros(4)
for j,k in enumerate('abcf'):
 ki='abcdef'.index(k)
 for h in range(3):J0[:,j]+=rows0[:,ki*3+h]
contrasts=[((2,2,0),(1,1,0)),((2,0,2),(1,0,1)),((0,2,2),(0,1,1)),((1,2,3),(2,1,3)),((1,3,2),(2,1,3))]
CP=s.Matrix.vstack(*(row(g)-row(h)for g,h in contrasts));JP=CP[:,['abcdef'.index(k)*3+1 for k in 'abcdf']]
if J0.det()!=-s.Rational(1,2)or JP.det()!=-s.Rational(1,4):raise ValueError('selected minor')
# Derive eight-term quartic independently from pendant multidegree (one of
# each nonzero character at each leaf). The only monomials are two cyclic
# three-coordinate products and six q_xyz X_z Y_y Z_x products.
Q={g:s.Symbol('q'+''.join(map(str,g)))for g in outputs};Q[(0,0,0)]=s.Integer(1)
positive=[p for p in permutations([1,2,3])if sign(p)==1];negative=[p for p in permutations([1,2,3])if sign(p)==-1]
Pdiff=s.prod(Q[p]for p in positive)-s.prod(Q[p]for p in negative)
Ssum=sum(sign(p)*Q[p]*Q[(p[2],p[2],0)]*Q[(p[1],0,p[1])]*Q[(0,p[0],p[0])]for p in permutations([1,2,3]))
sub={Q[g]:q[g]for g in outputs};Fminus=s.expand(Pdiff-Ssum);Fplus=s.expand(Pdiff+Ssum)
if s.expand(Fminus.subs(sub))==0:F=Fminus;choice=-1
elif s.expand(Fplus.subs(sub))==0:F=Fplus;choice=1
else:raise ValueError('independent quartic ansatz fails')
# Exact primitive-linear irreducibility mechanism: F=A*U+B, A=VW +/-XYZ
# is irreducible by Gauss, and B not divisible by A as this zero test shows.
U=Q[(1,2,3)];A=s.diff(F,U);B=s.expand(F-A*U)
zero_test={Q[g]:0 for g in outputs};zero_test.update({Q[p]:1 for p in negative})
if A.subs(zero_test)!=0 or B.subs(zero_test)==0:raise ValueError('primitive linear proof witness')
qs={Q[g]:q[g].subs(point)for g in outputs};gradient=s.Matrix([[s.diff(F,Q[g]).subs(qs)for g in outputs]])
if gradient==s.zeros(1,15)or gradient*Jp!=s.zeros(1,19):raise ValueError('conormal')
for p,M in PO:
 if gradient*M!=sign(p)*gradient:raise ValueError('gradient not sign')
# Labelled-port transport preserves the same hypersurface (up to sign).
leafsym=[]
for p in permutations(range(3)):
 changed={Q[g]:Q[tuple(g[i]for i in p)]for g in outputs};fp=s.expand(F.subs(changed,simultaneous=True))
 if fp not in [F,-F]:raise ValueError('leaf transport quartic')
 leafsym.append(1 if fp==F else-1)
(R/'independent-quartic.txt').write_text(str(F)+'\nA=dF/dq123='+str(A)+'\nB_zero_test='+str(B.subs(zero_test))+'\n')
# At a generic anisotropic strict-CT rational point the fixed symmetric sign
# projector is not a global linear constraint. Construct by products of rate
# factors in (0,1), guaranteeing strict CT exactly.
generic={L:s.Rational(2,5)}
for ki,k in enumerate('abcdef'):
 aa=s.Rational(ki+2,ki+4);bb=s.Rational(ki+3,ki+5);cc=s.Rational(ki+4,ki+6)
 for v,x in zip(edge[k][1:],[bb*cc,aa*cc,aa*bb]):generic[v]=x
if Es*J.subs(generic)==s.zeros(15,19):raise ValueError('negative linear invariant control failed')
# Six cubic circuit pullbacks, reconstructed directly from literal q.
circuits=[([(0,0,0),(1,2,3),(2,3,1)],[(0,3,3),(1,0,1),(2,2,0)]),([(0,0,0),(1,3,2),(3,2,1)],[(0,2,2),(1,0,1),(3,3,0)]),([(0,0,0),(2,1,3),(3,2,1)],[(0,1,1),(2,2,0),(3,0,3)]),([(0,0,0),(2,3,1),(3,1,2)],[(0,1,1),(2,0,2),(3,3,0)]),([(0,0,0),(1,3,2),(2,1,3)],[(0,3,3),(1,1,0),(2,0,2)]),([(0,0,0),(1,2,3),(3,1,2)],[(0,2,2),(1,1,0),(3,0,3)])]
core=[(f[1]*f[3]-f[2])*(d[1]*e[3]-d[3]*e[1]*f[2]),(f[1]*f[2]-f[3])*(d[1]*e[2]-d[2]*e[1]*f[3]),-(f[1]*f[3]-f[2])*(d[1]*e[3]*f[2]-d[3]*e[1]),-(f[1]*f[2]-f[3])*(d[1]*e[2]*f[3]-d[2]*e[1]),-(f[1]-f[2]*f[3])*(d[2]*e[3]-d[3]*e[2]*f[1]),(f[1]-f[2]*f[3])*(d[2]*e[3]*f[1]-d[3]*e[2])]
pendants={v:1 for k in 'abc'for v in edge[k][1:]};factors=[]
for (left,right),expected in zip(circuits,core):
 pol=s.expand(s.prod(q[g]for g in left)-s.prod(q[g]for g in right));ratio=s.cancel(pol/(L*(1-L)*expected))
 if not ratio.is_Mul and ratio!=1:raise ValueError(('bad pendant monomial',ratio))
 if s.expand(pol.subs(pendants)-L*(1-L)*expected)!=0:raise ValueError('circuit formula')
 tree={g:a[g[0]]*b[g[1]]*c[g[2]]for g in triples}
 if s.expand(s.prod(tree[g]for g in left)-s.prod(tree[g]for g in right))!=0:raise ValueError('tree zero')
 if pol.subs(point)==0:raise ValueError('strict isotropic separator')
 if pol.subs(L,0)!=0 or pol.subs(L,1)!=0:raise ValueError('inheritance boundary control')
 factors.append(str(ratio))
# Exhaust ALL admissible rooted orientations of the exact four-leaf witness.
nodes=['p','q','r','x','y','z','R','X','Y','Z'];leaves=set('RXYZ');edges=[('p','q'),('p','r'),('r','q'),('p','x'),('x','y'),('y','z'),('z','q'),('r','R'),('x','X'),('y','Y'),('z','Z')]
def rootings(heads):
 retics={v for u,v in heads};ordinary=[uv for uv in edges if uv not in heads and uv[::-1]not in heads];ans=[]
 for cut in edges:
  # The retained root-arm head at an endpoint must reproduce the old edge.
  valid=True
  for endpoint in cut:
   oldhead=any(v==endpoint and set((u,v))==set(cut)for u,v in heads)
   if (endpoint in retics)!=oldhead:valid=False
  if not valid:continue
  fixed=[uv for uv in heads if set(uv)!=set(cut)]+[('root',v)for v in cut]
  und=[uv for uv in ordinary if set(uv)!=set(cut)]
  for bits in product([0,1],repeat=len(und)):
   arcs=fixed+[uv if b==0 else uv[::-1]for uv,b in zip(und,bits)];allnodes=nodes+['root'];ins={v:[]for v in allnodes};outs={v:[]for v in allnodes}
   for u,v in arcs:ins[v].append(u);outs[u].append(v)
   if any((len(ins[v]),len(outs[v]))!=((0,2)if v=='root'else(1,0)if v in leaves else(2,1)if v in retics else(1,2))for v in allnodes):continue
   order=[];pending=set(allnodes)
   while pending:
    ready=[v for v in pending if all(u in order for u in ins[v])]
    if not ready:break
    order.extend(ready);pending.difference_update(ready)
   if pending:continue
   dom={}
   for v in order:dom[v]={v}|(set.intersection(*(dom[u]for u in ins[v]))if ins[v]else set())
   if set.intersection(*(dom[v]for v in leaves))!={'root'}:continue
   tc=all(any(w not in retics for w in outs[v])for v in allnodes if v not in leaves)
   ans.append({'cut':cut,'tree_child':tc,'arcs':arcs})
 return ans
first=rootings([('x','y'),('z','y'),('p','r'),('q','r')]);second=rootings([('x','y'),('z','y'),('q','p'),('r','p')])
if [len(first),len(second)]!=[9,7]or not all(v['tree_child']for v in first+second):raise ValueError(('root census',len(first),len(second)))
# Exact domain controls and cherry Jacobian.
s0=s.Rational(4,5);g0=s.Rational(31,50);rho=s.Rational(99,100)
if not(g0>2*s0-1 and g0<s0*s0 and g0/rho>2*(s0/rho)-1):raise ValueError('domain control')
if not(s.sqrt(g0)<2*s.sqrt(s0)-1):raise ValueError('square root negative control')
u,v=s.symbols('u v',positive=True);cj=s.Matrix([u/v,u*v]).jacobian([u,v]).det()
if s.simplify(cj-2*u/v)!=0:raise ValueError('cherry')
result={'status':'OWN_EXACT_CONTROLS_COMPLETED','finite_controls_not_universal_topology_proof':True,'literal_triangle_ranks':ranks,'isotypic_ranks_trivial_standard_sign':iso_ranks,'S3_equivariance_all_six_actions':True,'J0':str(J0),'J0_det':str(J0.det()),'Jperp':str(JP),'Jperp_det':str(JP.det()),'independently_derived_quartic_eight_monomials':True,'quartic_choice_Pdiff_plus_choice_Ssum':choice,'quartic_global_pullback_zero':True,'quartic_primitive_linear_irreducibility_zero_witness':str(B.subs(zero_test)),'quartic_conormal_nonzero_and_annihilates_J':True,'fixed_symmetric_sign_not_global_linear_invariant_negative_control':True,'all_leaf_transports_preserve_quartic_up_to_sign':leafsym,'circuit_factors_six_verified':factors,'inheritance_boundary_circuits_zero_negative_control':True,'embedded_witness_admissible_rootings':[len(first),len(second)],'all_witness_rootings_tree_child':True,'nonisomorphism_reason':'The labelled R neighbour is reticulate only in first; any label-preserving isomorphism fixes that neighbour.','marked_equality_reason':'Only pqr heads change; erase those two heads and site roles, preserving identical full graph and offsite y heads.','principal_positive_not_CT_point':[str(s0),str(g0)],'invalid_square_root_physical_split_detected':True,'valid_rho_split':str(rho),'cherry_determinant':str(cj),'elapsed_seconds':time.monotonic()-start}
(R/'independent-controls-results.json').write_text(json.dumps(result,indent=2)+'\n');(R/'embedded-rooting-census.json').write_text(json.dumps({'first':first,'second':second},indent=2)+'\n');print(json.dumps(result,indent=2))
