#!/usr/bin/env python3
"""Independent exact dual-stress and scope controls; standard library only."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime, timezone
import hashlib, json

checks=[]
def ck(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def zeros(n,m): return [[Q(0) for _ in range(m)] for _ in range(n)]
def transpose(a): return [list(r) for r in zip(*a)]
def mul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def rref_pivots(a):
    a=[[Q(x) for x in row] for row in a];row=0;piv=[]
    for col in range(len(a[0])):
        at=next((i for i in range(row,len(a)) if a[i][col]),None)
        if at is None: continue
        a[row],a[at]=a[at],a[row]
        z=a[row][col];a[row]=[x/z for x in a[row]]
        for i in range(len(a)):
            if i!=row:
                z=a[i][col];a[i]=[x-z*y for x,y in zip(a[i],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return piv

def det(a):
    a=[[Q(x) for x in row] for row in a];ans=Q(1)
    for j in range(len(a)):
        at=next((i for i in range(j,len(a)) if a[i][j]),None)
        if at is None:return Q(0)
        if at!=j:a[j],a[at]=a[at],a[j];ans=-ans
        z=a[j][j];ans*=z
        for i in range(j+1,len(a)):
            q=a[i][j]/z
            for k in range(j+1,len(a)):a[i][k]-=q*a[j][k]
    return ans

def basis(n,edges,tied=False):
    bs=[]
    if tied:
        k=zeros(n,n)
        for i in range(n):k[i][i]=1
        bs.append(k)
    else:
        for i in range(n):
            k=zeros(n,n);k[i][i]=1;bs.append(k)
    for i,j in edges:
        k=zeros(n,n);k[i][j]=k[j][i]=1;bs.append(k)
    return bs

def stress_certificate(bs,x):
    # Columns are vec(K_i X), so trivial kernel is the derivative-dual condition.
    columns=[[z for row in mul(k,x) for z in row] for k in bs]
    matrix=transpose(columns)
    rows=rref_pivots(transpose(matrix))
    square=[matrix[i] for i in rows]
    return {'shape':[len(matrix),len(matrix[0])], 'rank':len(rows),
            'selected_rows_zero_based':rows, 'square_minor_determinant':str(det(square))}

edges=[(i,j) for i in range(4) for j in range(4,8)]
x=zeros(8,4)
for i in range(4):x[i][i]=1;x[4+i][i]=1;x[4+i][(i+1)%4]=1
bs=basis(8,edges)
singleton=stress_certificate(bs,x)
ck('K44_no_nonzero_dual_stress_at_rank4',singleton['rank']==24 and Q(singleton['square_minor_determinant'])!=0)
merged=[add(bs[0],bs[1])]+bs[2:]
colored=stress_certificate(merged,x)
ck('tied_K44_no_nonzero_dual_stress_at_rank4',colored['rank']==23 and Q(colored['square_minor_determinant'])!=0)
ck('rank4_input',len(rref_pivots(x))==4)

# Exact-rank-3 enhancement of the submitted rank-at-most-3 intersection witness.
z=[[1,0,0],[0,0,1],[1,0,0],[1,0,0]]+[[0,1,0]]*4
g=mul(z,transpose(z))
ck('rank_exactly3_identity_stats_witness',len(rref_pivots(z))==3)
ck('all_diagonal_statistics_one',all(g[i][i]==1 for i in range(8)))
ck('all_cross_statistics_zero',all(g[i][j]==0 for i,j in edges))
ck('tied_diagonal_sum_two',g[0][0]+g[1][1]==2)

e=Q(1,100);diag=(1-e)**2;cross=2*e*(1+e)
ck('uniform_open_box_PD_margin',diag-4*cross==Q(8993,10000)>0)
ck('open_box_rank2_minor_margin',(1-e)**2-e**2==Q(49,50)>0)
ck('MLT_theorem_parameter',next(k for k in range(1,9) if k*(k+1)//2>=8)==4)

# C4 independently: dual injectivity at two observation columns.
c4edges=[(0,1),(1,2),(2,3),(0,3)]
c4basis=basis(4,c4edges,True)
c4x=[[1,0],[0,0],[0,1],[0,0]]
c4cert=stress_certificate(c4basis,c4x)
ck('C4_I2_zero_dual_full_rank',c4cert['rank']==5 and Q(c4cert['square_minor_determinant'])!=0)
ck('C4_rank2_input',len(rref_pivots(c4x))==2)
# J anticommutes with every edge basis and commutes with diagonal identity.
signs=[1,-1,1,-1]
j=zeros(4,4)
for i,s in enumerate(signs):j[i][i]=s
for eidx,k in enumerate(c4basis[1:]):
    a=add(mul(j,k),mul(k,j))
    ck('C4_edge_anticommutator_'+str(eidx),all(z==0 for row in a for z in row))
ck('C4_diagonal_basis_is_identity',all(c4basis[0][i][k]==(i==k) for i in range(4) for k in range(4)))
# The alternate squared norm is not identically zero (e1 is outside its zero set).
ck('C4_generic_quadratic_obstruction_nonzero',signs[0]==1)

out={'status':'PASS_EXACT','UTC':datetime.now(timezone.utc).isoformat(),
     'method':'Independent dual stress maps and exact rational controls; no SymPy, no simulation',
     'checks':checks,'assertions':len(checks),
     'K44_singleton_dual_stress_certificate':singleton,
     'K44_tied_dual_stress_certificate':colored,
     'rank3_identity_statistics_Gram_factor':z,
     'C4_rank2_dual_stress_certificate':c4cert,
     'C4_alternating_form':'x1^2-x2^2+x3^2-x4^2',
     'C4_I1_relation_in_source_edge_coordinates':'t12*t34-t23*t41',
     'scope':'Controls support report analytic proofs; not a priority finding or a Boolean conjecture solution'}
p=Path(__file__).resolve().parent/'INDEPENDENT_CHECKS.json'
p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
