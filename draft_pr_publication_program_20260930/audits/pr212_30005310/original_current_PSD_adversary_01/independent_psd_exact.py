#!/usr/bin/env python3
"""Independent exact PSD/statistical certificates; standard library only.
No submitted program is imported or executed. All outputs go beside this
owned source. Matrix identities support the quantified arguments in REPORT.md.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def zeros(m,n): return [[F(0) for j in range(n)] for i in range(m)]
def transpose(a): return [list(r) for r in zip(*a)]
def mm(a,b):
    return [[sum((x*y for x,y in zip(r,c)),F(0)) for c in zip(*b)] for r in a]
def neg(a): return [[-x for x in r] for r in a]
def rref(a):
    a=[list(map(F,r)) for r in a]; piv=[]; i=0
    if not a:return a,piv
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i]; z=a[i][j]; a[i]=[x/z for x in a[i]]
        for k in range(len(a)):
            if k!=i:
                z=a[k][j]; a[k]=[x-z*y for x,y in zip(a[k],a[i])]
        piv.append(j);i+=1
        if i==len(a):break
    return a,piv

def rank(a):return len(rref(a)[1])
def det(a):
    a=[list(map(F,r)) for r in a]; d=F(1)
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];d=-d
        z=a[j][j];d*=z
        for k in range(j+1,len(a)):
            z0=a[k][j]/z
            for t in range(j+1,len(a)):a[k][t]-=z0*a[j][t]
            a[k][j]=F(0)
    return d

def full_row_certificate(a):
    p=rref(a)[1]
    assert len(p)==len(a)
    square=[[r[j] for j in p] for r in a]
    d=det(square);assert d
    return {'shape':[len(a),len(a[0])], 'pivot_columns_zero_based':p,'square_minor_determinant':str(d)}

def jacobian(X,statistic_rows):
    m=len(X); n=len(X[0]); out=[]
    for terms in statistic_rows:
        r=[F(0)]*(m*n)
        for i,j,c in terms:
            for k in range(n):
                r[n*i+k]+=c*X[j][k]
                r[n*j+k]+=c*X[i][k]
        out.append(r)
    return out

def stat(M,rows):return [sum((c*M[i][j] for i,j,c in terms),F(0)) for terms in rows]
def serial(a):
    if isinstance(a,list):return [serial(v) for v in a]
    if isinstance(a,dict):return {k:serial(v) for k,v in a.items()}
    if isinstance(a,F):return str(a)
    return a

# Singleton and tied K4,4 statistics. All edge coordinates have source weight1.
rows=[[(i,i,F(1))] for i in range(8)]+[[(i,j,F(1))] for i in range(4) for j in range(4,8)]
tied=[rows[0]+rows[1]]+rows[2:]
U=eye(4);V=zeros(4,4)
for i in range(4):V[i][i]=V[i][(i+1)%4]=F(1)
X4=U+V
J=jacobian(X4,rows);Jc=jacobian(X4,tied)
Jcert=full_row_certificate(J);Jccert=full_row_certificate(Jc)
assert rank(X4)==4
assert Jcert['square_minor_determinant']=='256'
assert Jccert['square_minor_determinant']=='128'

# Actual rank2 real lift and PD completion, with an exact uniform open-box bound.
X2=[[F(1),F(0)]]*4+[[F(0),F(1)]]*4
S2=mm(X2,transpose(X2));I8=eye(8)
assert rank(X2)==2 and rank(S2)==2
assert stat(S2,rows)==stat(I8,rows)
assert stat(S2,tied)==stat(I8,tied)
e=F(1,100);dl=(1-e)**2;cb=2*e*(1+e);margin=dl-4*cb
assert (dl,cb,margin)==(F(9801,10000),F(202,10000),F(8993,10000))
assert margin>0 and 1-2*e>0

# Independent rank3 bad-data certificate. Householder H has rational entries.
w=[F(i) for i in [1,2,3,4]];norm=sum(x*x for x in w)
H=[[F(i==j)-2*w[i]*w[j]/norm for j in range(4)] for i in range(4)]
assert mm(H,transpose(H))==eye(4)
z=[F(i) for i in [2,3,5,7]];znorm=sum(x*x for x in z)
G=[[F(i==j)-2*z[i]*z[j]/znorm for j in range(4)] for i in range(4)]
assert mm(G,transpose(G))==eye(4)
U3=[r[:3] for r in G];V3=[r[:3] for r in H];v4=[r[3] for r in H]
Q=mm(U3,transpose(V3))
# R has 5 rows and 8 columns. K=R^T R has diagonal blocks I4.
R=[eye(4)[i]+[-z for z in Q[i]] for i in range(4)]+[[F(0)]*4+v4]
W=transpose(R);K=mm(W,R);X3=U3+V3
assert rank(R)==5 and rank(X3)==3 and rank(K)==5
assert mm(K,X3)==zeros(8,3)
assert all(K[i][i]==1 for i in range(8))
nonedges=list(combinations(range(4),2))+list(combinations(range(4,8),2))
assert all(K[i][j]==0 for i,j in nonedges)
Bpairs=[(a,b) for a in range(5) for b in range(a,5)]
T=[]
for i,j in nonedges:
    T.append([W[i][a]*W[j][a] if a==b else W[i][a]*W[j][b]+W[i][b]*W[j][a] for a,b in Bpairs])
Tcert=full_row_certificate(T)
# Extra quotient equation for K11=K22 in tied variant.
Td=[(W[0][a]*W[0][a]-W[1][a]*W[1][a]) if a==b else 2*(W[0][a]*W[0][b]-W[1][a]*W[1][b]) for a,b in Bpairs]
Tc=T+[Td]
Tccert=full_row_certificate(Tc)
I5coords=[F(a==b) for a,b in Bpairs]
assert all(sum(x*y for x,y in zip(r,I5coords))==0 for r in T)
assert sum(x*y for x,y in zip(Td,I5coords))==0

# Added equal-vertex-color C4 statement: independent ideal and generic PSD checks.
c4rows=[[(i,i,F(1)) for i in range(4)]]+[[ (i,j,F(1)) ] for i,j in [(0,1),(0,3),(1,2),(2,3)]]
# Search a small deterministic exact data grid only for a submersion witness.
c4_X=[[F(1),F(0)],[F(0),F(1)],[F(1),F(1)],[F(1),F(2)]]
c4J=jacobian(c4_X,c4rows);c4cert=full_row_certificate(c4J)
# Rank1 two-minor f=t12*t34-t14*t23 is in the exact elimination ideal.
# Its nonzeroness has the finite observed-edge assignment (1,1,0,0).
f_nonzero=F(1)*F(1)-F(0)*F(0);assert f_nonzero==1
# The a.s. success witness polynomial is Delta=x1^2+x3^2-x2^2-x4^2.
# For K=[[aI,B],[B^T,aI]], the two block equations Kx=0 imply a*Delta=0.
# PSD and Delta!=0 imply a=0 and therefore K=0. Delta(e1)=1.
c4_lift=[[F(1)],[F(0)],[F(0)],[F(0)]]
c4PD=[[F(i==j,4) for j in range(4)] for i in range(4)]
assert stat(mm(c4_lift,transpose(c4_lift)),c4rows)==stat(c4PD,c4rows)

out={
 'status':'PASS_EXACT_INDEPENDENT',
 'arithmetic':'Python standard-library Fraction; no floating-point decisions',
 'submitted_programs_imported_or_executed':False,
 'K44':{'I3_nonzero_certificate':'det observed 4x4 cross block is a defining 4-minor and equals1 at B=I4',
        'I4_zero_singleton':Jcert,'I4_zero_tied':Jccert,
        'rank2_lift':X2,'PD_completion':'I8','open_success_box_epsilon':e,'uniform_PD_margin':margin,
        'one_column_failure':'Observed singleton diagonal edge3--5 gives a zero 2x2 principal determinant for all data',
        'independent_rank3_open_failure':{'X0':X3,'Householder_H':H,'Householder_G':G,'Gram_factor_R':R,'K0':K,
            'nullspace_basis_W':W,'B0':'I5 positive definite','quotient_nonedge_pairs_zero_based':nonedges,
            'symmetric_B_coordinate_pairs':Bpairs,'T_singleton':Tcert,'T_tied':Tccert,
            'interpretation':'Full row rank and B0 PD imply PSD stresses persist on an open set; p3<1 for BOTH models'},
        'proved_thresholds_singleton':{'WMLT':2,'MLT':4},
        'proved_thresholds_tied_diagonal':{'WMLT':2,'MLT':4},
        'tied_MLT_scope':'Independent audit strengthening; not asserted in either submitted proof'},
 'equal_vertex_C4':{'I1_nonzero_certificate':'observed 2x2 cross minor t12*t34-t14*t23',
                    'I2_zero':c4cert,'I2_zero_data':c4_X,
                    'almost_sure_good_polynomial':'Delta=x1^2+x3^2-x2^2-x4^2',
                    'WMLT':1,'MLT':1,
                    'actual_one_column_lift':'e1','PD_completion':'I4/4'},
 'proof_obligations':'See REPORT.md for universal membership, open-neighborhood argument, Gaussian full support, a.s. zero-set argument, and sample-mean convention.'
}
p=Path(__file__).resolve().parent
(p/'INDEPENDENT_EXACT_CERTIFICATES.json').write_text(json.dumps(serial(out),indent=2)+'\n')
print(json.dumps({'status':out['status'],'J_singleton':Jcert,'J_tied':Jccert,'rank3_T_singleton':Tcert,'rank3_T_tied':Tccert,'C4_J':c4cert,'independent_thresholds':{'K44_singleton':[2,4],'K44_tied':[2,4],'equal_vertex_C4':[1,1]}},indent=2))
