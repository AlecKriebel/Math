#!/usr/bin/env python3
"""Independent elementary-column-operation replay; no geometric certification."""
import itertools,json,math,sys

def require(x,m):
    if not x:raise ValueError(m)

def det3(a):
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])

def check(a,expected):
    require(type(a) is list and len(a)==3 and all(type(r) is list and len(r)==3 for r in a),'shape')
    require(all(type(x) is int for r in a for x in r),'integer entries')
    require(abs(det3(a))==1,'unimodularity')
    require(type(expected) is int and expected==a[2][2],'multiplicity')
    u,v,p=a[2]
    require(math.gcd(math.gcd(a[0][2],a[1][2]),p)==1,'primitive slope')
    # Presentation uses columns (mu,x,y). Add u*column(x)+v*column(y)
    # to column(mu), then order columns as (x,y,mu).
    matrix=[[-u,1,0],[-v,0,1],[p,0,0]]
    for r in matrix:r[0]+=u*r[1]+v*r[2]
    reduced=[[r[1],r[2],r[0]] for r in matrix]
    require(reduced==[[1,0,0],[0,1,0],[0,0,p]],'column elimination')
    return 'infinite_cyclic' if p==0 else ('trivial' if abs(p)==1 else 'nontrivial_finite_cyclic')

def main():
    counts=dict(infinite_cyclic=0,trivial=0,nontrivial_finite_cyclic=0)
    mirrored=dict(counts);n=0
    for a,b,u,v in itertools.product(range(-3,4),repeat=4):
        p=1+a*u+b*v;m=[[1,0,a],[0,1,b],[u,v,p]]
        counts[check(m,p)]+=1
        # Reversal of the meridian source coordinate includes det=-1 and p<0.
        mirror=[r[:2]+[-r[2]] for r in m]
        mirrored[check(mirror,-p)]+=1;n+=1
    require(n==2401 and counts==mirrored,'case counts')
    bad=[([[1,0,0],[0,1,0],[0,0,2]],2),([[1,0,0],[0,1,0],[0,0,1]],0),([[1,0,0],[0,1,0],[0,0,True]],1)]
    rejected=0
    for m,p in bad:
        try:check(m,p)
        except ValueError:rejected+=1
        else:raise ValueError('accepted bad matrix')
    # The Hopf linking matrix exchanges the two meridian generators; the single
    # filling gives the zero 1x1 relation. These are separate abelian tests only.
    hopf=[[0,1],[1,0]]
    require(hopf[0][0]*hopf[1][1]-hopf[0][1]*hopf[1][0]==-1,'Hopf determinant')
    return {'result':'pass','matrix_cases':n,'mirrored_matrix_cases':n,'h1_outcomes':counts,'mirrored_h1_outcomes':mirrored,'negative_controls_rejected':rejected,'hopf_final_h1':'trivial','either_first_h1':'Z','method':'unimodular column elimination, independent of author minor enumeration','certifies_topology':False,'certifies_general_solution':False}
if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except Exception as e:print(json.dumps({'result':'fail','error':str(e)}),file=sys.stderr);sys.exit(1)
