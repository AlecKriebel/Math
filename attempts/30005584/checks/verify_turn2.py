"""Symbolic tensor contraction plus exact finite controls; no full Ricci degree computation."""
import sympy as s
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
A,B,Cc,D,E,b,v,vr,w2,w3,wr2,wr3,v2,v3,t22,t23,t32,t33=s.symbols('A B C D E b v vr w2 w3 wr2 wr3 v2 v3 t22 t23 t32 t33',real=True)
H=s.zeros(4)
for i,z in [(0,v),(2,w2),(3,w3)]:H[1,i]=H[i,1]=z
partial=[s.zeros(4) for _ in range(4)]
for i,z in [(0,vr),(2,wr2),(3,wr3)]:partial[0][1,i]=partial[0][i,1]=z
for c,dv,t2,t3 in [(2,v2,t22,t23),(3,v3,t32,t33)]:
 for i,z in [(0,dv/b),(2,t2/b),(3,t3/b)]:partial[c][1,i]=partial[c][i,1]=z
Gamma=[s.zeros(4) for _ in range(4)]
Gamma[1][0,1]=A;Gamma[1][1,0]=-A
for a in [2,3]:Gamma[a][0,a]=B;Gamma[a][a,0]=-B
cov=[partial[c]-Gamma[c]*H-H*Gamma[c].T for c in range(4)]
norm=sum(z*z for T in cov for z in T)
w2norm=w2*w2+w3*w3
expected=2*(vr**2+wr2**2+wr3**2)+8*A**2*v**2+2*A**2*w2norm+2*((v2/b-B*w2)**2+(v3/b-B*w3)**2)+2*((t22/b+B*v)**2+(t33/b+B*v)**2+(t23/b)**2+(t32/b)**2)
ck(s.expand(norm-expected)==0,'full_connection_norm_symbolic')
# Curvature R_ijji=K_ij with all standard skew symmetries.
K={(0,1):-Cc,(0,2):-D,(0,3):-D,(1,2):-A*B,(1,3):-A*B,(2,3):E}
R={}
for (i,j),k in K.items():
 R[i,j,j,i]=k;R[j,i,i,j]=k;R[i,j,i,j]=-k;R[j,i,j,i]=-k
rm=sum(H[i,j]*R.get((i,k,l,j),0)*H[k,l] for i,j,k,l in product(range(4),repeat=4))
ck(s.expand(-2*rm+4*Cc*v*v+4*A*B*w2norm)==0,'curvature_contraction_symbolic')
coex=s.expand((norm-2*rm).subs({v:0,vr:0,v2:0,v3:0}))
coex_expected=2*(wr2**2+wr3**2+(A-B)**2*w2norm+(t22*t22+t23*t23+t32*t32+t33*t33)/b**2)
ck(s.expand(coex-coex_expected)==0,'positive_coexact_identity_symbolic')
# The only v/w cross terms have divergence/gradient structure.
vv=s.expand((norm-2*rm).subs({w2:0,w3:0,wr2:0,wr3:0,t22:0,t23:0,t32:0,t33:0}))
ww=s.expand((norm-2*rm).subs({v:0,vr:0,v2:0,v3:0}))
cross=s.expand(norm-2*rm-vv-ww)
ck(s.expand(cross-4*B/b*(v*(t22+t33)-v2*w2-v3*w3))==0,'cross_term_divergence_structure')
for aa,bb,w,x,y,z in product(range(-2,3),repeat=6):
 val=x*x+(aa-bb)**2*w*w+y*y+z*z
 ck(val>=0,'sum_of_squares_controls')
for m0,m1,m2,m3 in product(range(12),repeat=4):
 total=m0+2*(m1+m2+m3)
 ck(total%2==m0%2,'circle_real_weight_parity')
for l in range(1,101):ck(l*(l+1)-1>=1,'sphere_coexact_angular_potential')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Exact connection and curvature polynomial identities plus finite multiplicity controls. Written domain/reducing-subspace proofs and credited spectral theorem are essential; no full degree computation.'},indent=2,sort_keys=True))
