"""Exact evaluation controls, new for v2 review; no package-code imports.

Homogeneous forms of degree k are evaluated on (1,t), 0<=t<=k, or
(1,s,t), s,t>=0, s+t<=k. These sets are unisolvent in characteristic zero
(triangular falling-factorial basis), so ranks agree with coefficient ranks.
This verifies exact flags; the symbolic open-set argument supplies genericity.
"""
from fractions import Fraction as F
from itertools import combinations
from math import prod
import json

def monomials(n,d):
    if n==1:return [(d,)]
    return [(a,)+e for a in range(d+1) for e in monomials(n-1,d-a)]

def eliminate(m,p=None):
    a=[[F(v) if p is None else v%p for v in row] for row in m]
    original=list(range(len(a)));rows=[];cols=[];r=0
    for c in range(len(a[0])):
        z=next((z for z in range(r,len(a)) if a[z][c]),None)
        if z is None:continue
        a[z],a[r]=a[r],a[z];original[z],original[r]=original[r],original[z]
        rows.append(original[r]);cols.append(c)
        inv=1/a[r][c] if p is None else pow(a[r][c],-1,p)
        a[r]=[v*inv if p is None else v*inv%p for v in a[r]]
        for z in range(r+1,len(a)):
            t=a[z][c]
            a[z]=[v-t*w if p is None else (v-t*w)%p for v,w in zip(a[z],a[r])]
        r+=1
        if r==len(a):break
    return rows,cols

def determinant(m):
    a=[[F(v) for v in row] for row in m];d=F(1)
    for c in range(len(a)):
        z=next((z for z in range(c,len(a)) if a[z][c]),None)
        if z is None:return F(0)
        if z!=c:a[z],a[c]=a[c],a[z];d=-d
        d*=a[c][c]
        for z in range(c+1,len(a)):
            t=a[z][c]/a[c][c]
            a[z]=[v-t*w for v,w in zip(a[z],a[c])]
    return d

def restricted(ns,section):
    return [[sum(v*s for v,s in zip(row,col)) for col in zip(*section)] for row in ns]

def polar_values(ns,section,v):
    ls=[sum(a*b for a,b in zip(row,v)) for row in restricted(ns,section)]
    return [sum(ns[i][j]*prod(ls[:i]+ls[i+1:]) for i in range(len(ns))) for j in range(len(ns[0]))]

def matrix(ns,section,k,chain=False):
    r=len(section[0]);d=len(ns)-1
    pts=[(1,t) for t in range(k+1)] if r==2 else [(1,s,t) for s in range(k+1) for t in range(k-s+1)]
    values=[polar_values(ns,section,v) for v in pts]
    if chain:values=[[sum(section[j][i]*f[j] for j in range(len(f))) for i in range(r)] for f in values]
    out=[]
    for j in range(len(values[0])):
        for e in monomials(r,k-d):
            out.append([f[j]*prod(x**a for x,a in zip(v,e)) for v,f in zip(pts,values)])
    return out,pts

def control(ns,section,k,expected,p=None,chain=False):
    m,pts=matrix(ns,section,k,chain);rows,cols=eliminate(m,p)
    assert len(cols)==expected,(k,len(section[0]),len(cols),expected)
    out={'degree':k,'section_variables':len(section[0]),'evaluation_matrix_shape':[len(m),len(m[0])],'rank':len(cols),'quotient_dimension':len(pts)-len(cols),'minor_rows':rows,'minor_columns':cols}
    if p is None:
        det=determinant([[m[i][j] for j in cols] for i in rows]);assert det
        out['nonzero_evaluation_minor_determinant']=str(det)
    else:out.update({'prime':p,'rank_computed_by_exact_residue_elimination':True})
    return out

MAIN=[[1,0,0,0],[0,1,0,0],[1,-1,0,0],[1,-2,0,0],[0,0,1,0],[0,0,0,1],[1,0,1,1]]
T=[[1,0,0],[0,1,0],[0,0,1],[1,2,3]]
B=[[1,0],[0,1],[2,3],[7,11]]
NN=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[0,1,0,1],[0,0,1,1],[-1,1,0,1],[-1,0,1,1],[-1,1,1,1]]
W=[[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1],[1,1,1,0],[1,1,0,1],[1,0,1,1]]

def main():
    main=[control(MAIN,T,k,r) for k,r in [(6,4),(7,12)]]+[control(MAIN,B,k,r) for k,r in [(6,4),(7,7),(8,9)]]
    # Evaluate the purported syzygy as an exact polynomial identity at ten
    # unisolvent binary points, without coefficient expansion.
    for t in range(10):
        f=polar_values(MAIN,B,(1,t));assert sum(a*b for a,b in zip([11,11*t,-73*(2+3*t),25*(7+11*t)],f))==0
    # Valid open binary flag whose trace coefficient 4rho_x+rho_z+rho_w is zero.
    zero_trace=[[1,0],[0,1],[2,3],[F(5,6),1]]
    assert all(a[0]*c[1]-a[1]*c[0] for a,c in combinations(restricted(MAIN,zero_trace),2))
    assert 4*1+2-6==0
    zero_trace_controls=[control(MAIN,zero_trace,k,r) for k,r in [(6,4),(7,7),(8,9)]]
    for v in [(1,t) for t in range(8)]:
        f=polar_values(MAIN,zero_trace,v)
        assert sum(a*b for a,b in zip([v[0],v[1],2*(2*v[0]+3*v[1]),-6*(F(5,6)*v[0]+v[1])],f))==0
    chain=[control(MAIN,T,k,r,chain=True) for k,r in [(6,3),(7,9)]]
    degenerate=control(MAIN,[[1,0,0],[0,1,0],[0,0,1],[2,0,3]],7,11)
    # A degree-seven polynomial evaluated on a small grid mod7 is not
    # unisolvent; use prime101 for independent residue arithmetic instead.
    residue=control(MAIN,T,7,12,p=101)
    prior={}
    for name,ns,t,b in [('NN_Simis',NN,T,B),('Walther',W,[[1,0,0],[0,1,0],[0,0,1],[5,11,23]],[[1,0],[0,1],[13,29],[304,678]])]:
        assert len(eliminate(ns)[1])==4
        lr=restricted(ns,b);assert all(a[0]*c[1]-a[1]*c[0] for a,c in combinations(lr,2))
        # Check compatible flag, rather than independently good unrelated maps.
        coeff=b[2]
        assert [[row[0]+row[2]*coeff[0],row[1]+row[2]*coeff[1]] for row in t]==b
        prior[name]=[control(ns,b,k,r) for k,r in [(8,4),(9,8),(10,11)]]+[control(ns,t,k,r) for k,r in [(8,4),(9,12)]]
    flats=set()
    for i,j in combinations(range(7),2):
        flats.add(tuple(h for h,row in enumerate(MAIN) if len(eliminate([MAIN[i],MAIN[j],row])[1])==2))
    multiple=[list(f) for f in sorted(flats) if len(f)>2];assert multiple==[[0,1,2,3]]
    determinants=[a[0]*c[1]-a[1]*c[0] for a,c in combinations(restricted(MAIN,B),2)]
    assert all(determinants)
    assert determinant([[1,0,0,0],[0,1,0,0],[2,3,1,0],[7,11,3,1]])==1
    print(json.dumps({'method':'Exact homogeneous evaluation at provably unisolvent grids, direct ambient product-rule evaluations; no archived implementation imported.','main':main,'displayed_binary_syzygy_exact':True,'zero_trace_coefficient_branch':{'section_rows':[[str(v) for v in row] for row in zero_trace],'rho':[1,2,-6],'scalar_trace_coefficient':0,'pairwise_factors_distinct':True,'controls':zero_trace_controls},'restricted_arrangement_chain_rule_control':chain,'degenerate_ternary':degenerate,'prime101_corroboration':residue,'new_supplement_controls':prior,'binary_pair_determinants':determinants,'only_multiple_rank2_flat':multiple,'compatible_GL4_determinant':1,'claim_scope':'Finite flag corroboration; general characteristic-zero gin conclusion requires symbolic proof.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
