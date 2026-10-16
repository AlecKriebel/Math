"""New whole-package review controls; standard library, no package imports."""
from fractions import Fraction
from itertools import combinations
from math import comb
import json

NORMALS=((1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,1))

def rank(rows,mod=None):
    if mod is None:a=[[Fraction(v) for v in row] for row in rows]
    else:a=[[int(v)%mod for v in row] for row in rows]
    k=0
    for j in range(len(a[0])):
        i=next((i for i in range(k,len(a)) if a[i][j]),None)
        if i is None:continue
        a[i],a[k]=a[k],a[i]
        inv=1/a[k][j] if mod is None else pow(a[k][j],-1,mod)
        a[k]=[v*inv if mod is None else v*inv%mod for v in a[k]]
        for i in range(k+1,len(a)):
            t=a[i][j]
            a[i]=[v-t*w if mod is None else (v-t*w)%mod for v,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def mons(r,d):
    if r==1:return [(d,)]
    return [(i,)+t for i in range(d+1) for t in mons(r-1,d-i)]

def multiply(a,b):
    c={}
    for e,v in a.items():
        for f,w in b.items():
            g=tuple(x+y for x,y in zip(e,f));c[g]=c.get(g,0)+v*w
    return {e:v for e,v in c.items() if v}

def linear(v):return {tuple(int(i==j) for i in range(len(v))):x for j,x in enumerate(v) if x}

def polar_product_rule(section):
    r=len(section[0]);factors=[tuple(sum(a[j]*section[j][i] for j in range(4)) for i in range(r)) for a in NORMALS]
    out=[{} for j in range(4)]
    for h,a in enumerate(NORMALS):
        term={(0,)*r:1}
        for i,v in enumerate(factors):
            if i!=h:term=multiply(term,linear(v))
        for j,v in enumerate(a):
            for e,c in term.items():out[j][e]=out[j].get(e,0)+v*c
    return factors,[{e:c for e,c in p.items() if c} for p in out]

def macrank(polars,r,k,mod=None):
    d=max(map(sum,polars[0]));basis=mons(r,k);rows=[]
    for f in polars:
        for m in mons(r,k-d):
            p={tuple(a+b for a,b in zip(m,e)):c for e,c in f.items()}
            rows.append([p.get(e,0) for e in basis])
    return {'degree':k,'rank':rank(rows,mod),'rows':len(rows),'columns':len(basis),'quotient':len(basis)-rank(rows,mod)}

def scalar_rank(section):
    r=len(section[0]);eq=[]
    for i,a in enumerate(NORMALS):
        for k in range(r):
            row=[0]*(4*r+7)
            for j in range(4):row[j*r+k]=a[j]
            row[4*r+i]=-sum(a[j]*section[j][k] for j in range(4));eq.append(row)
    eq.append([0]*(4*r)+[1]*7)
    return {'unknowns':4*r+7,'rank':rank(eq),'nullity':4*r+7-rank(eq)}

def main():
    b=((1,0),(0,1),(2,3),(7,11));t=((1,0,0),(0,1,0),(0,0,1),(1,2,3))
    fb,pb=polar_product_rule(b);ft,pt=polar_product_rule(t)
    dets=[{'pair':[i,j],'determinant':fb[i][0]*fb[j][1]-fb[i][1]*fb[j][0]} for i,j in combinations(range(7),2)]
    assert all(v['determinant'] for v in dets)
    binary=[macrank(pb,2,k) for k in (6,7,8,9)]
    ternary=[macrank(pt,3,k) for k in (6,7)]
    assert [v['rank'] for v in binary]==[4,7,9,10]
    assert [v['rank'] for v in ternary]==[4,12]
    # The chain-rule ternary Jacobian has only three combinations of ambient polars.
    restricted=[]
    for j in range(3):
        f={}
        for k,p in enumerate(pt):
            for e,v in p.items():f[e]=f.get(e,0)+t[k][j]*v
        restricted.append({e:v for e,v in f.items() if v})
    restricted_ranks=[macrank(restricted,3,k) for k in (6,7)]
    assert [v['rank'] for v in restricted_ranks]==[3,9]
    degenerate=((1,0,0),(0,1,0),(0,0,1),(2,0,3));fd,pd=polar_product_rule(degenerate)
    assert macrank(pd,3,7)['rank']==11
    assert macrank(pt,3,7,7)['rank']==11
    # Rank-two flats are obtained by closing every independent pair of normals.
    flats=set()
    for i,j in combinations(range(7),2):
        flats.add(tuple(h for h,a in enumerate(NORMALS) if rank([NORMALS[i],NORMALS[j],a])==2))
    multiple=[list(f) for f in sorted(flats) if len(f)>2]
    assert multiple==[[0,1,2,3]]
    # One multiplicity-four flat, s=3,d=7 in MN Cor.8.12.
    mn={'d':7,'multiplicities':[4],'s':3,'generator_shifts':[6]*5,'syzygy_shifts':[7]*3+[9]}
    options=[(a,b,c) for a in range(1,7) for b in range(a,7) for c in range(b,7) if a+b+c==6 and sum(e==1 for e in (a,b,c))==1]
    assert options==[(1,2,3)]
    out={'claim_scope':'Exact corroboration only; open-set proof supplies genericity.', 'binary_pair_determinants':dets,'binary':binary,'ternary':ternary,'binary_scalar_system':scalar_rank(b),'ternary_scalar_system':scalar_rank(t),'restricted_three_derivative_control':restricted_ranks,'excluded_degenerate_ternary_degree7_rank':11,'excluded_characteristic7_ternary_degree7_rank':11,'codimension_two_flats_multiplicity_ge3':multiple,'MN_resolution_substitution':mn,'Hilbert_Burch_degree_options':options,'threshold':8,'third_variable_first_generator_degree':7}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
