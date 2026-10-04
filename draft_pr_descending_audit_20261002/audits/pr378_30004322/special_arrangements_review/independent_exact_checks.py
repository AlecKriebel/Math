#!/usr/bin/env python3
"""Independent exact Q(w) incidence audit; w^2+w+1=0. No third-party code."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json

class Qw:
    __slots__ = ('a','b')
    def __init__(self,a=0,b=0):
        if isinstance(a,Qw): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=Qw(o); return Qw(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Qw(-self.a,-self.b)
    def __sub__(self,o): return self+-Qw(o)
    def __rsub__(self,o): return Qw(o)+-self
    def __mul__(self,o):
        o=Qw(o); return Qw(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a-self.b*o.b)
    __rmul__=__mul__
    def inv(self):
        norm=self.a*self.a-self.a*self.b+self.b*self.b
        assert norm
        return Qw((self.a-self.b)/norm,-self.b/norm)
    def __truediv__(self,o): return self*Qw(o).inv()
    def __pow__(self,n):
        if n<0: return self.inv()**(-n)
        r=Qw(1)
        for _ in range(n): r=r*self
        return r
    def __bool__(self): return bool(self.a or self.b)
    def __eq__(self,o):
        o=Qw(o); return self.a==o.a and self.b==o.b
    def __hash__(self): return hash((self.a,self.b))
    def __repr__(self):
        if not self.b:return str(self.a)
        return f'({self.a}+{self.b}*w)'

O=Qw(0); U=Qw(1); W=Qw(0,1)
assert W**3==1 and W!=1
def norm(v):
    v=tuple(Qw(x) for x in v)
    first=next(x for x in v if x)
    return tuple(x/first for x in v)
def cross(a,b):
    c=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    return norm(c) if any(c) else None
def dot(a,b): return sum((x*y for x,y in zip(a,b)),O)
def coords(v):return '['+':'.join(map(str,v))+']'
def singular(lines):
    points={cross(a,b) for a,b in combinations(lines,2)}
    assert None not in points
    pts=sorted(points,key=coords)
    r=[sum(dot(l,p)==0 for l in lines) for p in pts]
    assert sum(x*(x-1)//2 for x in r)==len(lines)*(len(lines)-1)//2
    return pts,r
def joined(pts):
    lines=sorted({cross(a,b) for a,b in combinations(pts,2)},key=coords)
    return lines,[sum(1<<i for i,p in enumerate(pts) if dot(l,p)==0) for l in lines]
def covering(masks,n,k):
    full=(1<<n)-1
    bypt=[[j for j,m in enumerate(masks) if m&(1<<i)] for i in range(n)]
    seen=set()
    def rec(covered,chosen):
        if covered==full:return chosen
        remaining=k-len(chosen)
        if remaining<=0:return None
        key=(covered,remaining)
        if key in seen:return None
        seen.add(key)
        uncovered=full^covered
        best=max((m&uncovered).bit_count() for m in masks)
        if uncovered.bit_count()>best*remaining:return None
        p=min((i for i in range(n) if uncovered&(1<<i)),key=lambda i:len(bypt[i]))
        candidates=sorted(bypt[p],key=lambda j:-(masks[j]&uncovered).bit_count())
        for j in candidates:
            ans=rec(covered|masks[j],chosen+[j])
            if ans is not None:return ans
        return None
    return rec(0,[])

def audit(name,lines,print_detail=False):
    lines=sorted(set(map(norm,lines)),key=coords)
    pts,r=singular(lines); joins,masks=joined(pts)
    k=max(m.bit_count() for m in masks) if len(pts)>1 else 1
    cmasks=[sum(1<<i for i,p in enumerate(pts) if dot(l,p)==0) for l in lines]
    print('ARRANGEMENT',name,'lines',len(lines),'points',len(pts),'t',dict(sorted(Counter(r).items())))
    print('ALL_PAIR_JOINED_LINES',len(joins),'collinearity_histogram',dict(sorted(Counter(m.bit_count() for m in masks).items())))
    print('mpl_ALL_LINES',k,'mpl_COMPONENTS',max(m.bit_count() for m in cmasks))
    print('ALL_PROJECTIVE_LINES_JUSTIFICATION: a line containing >=2 points is a pair join; all others have <=1.')
    cover=covering(masks,len(pts),k) if len(pts)>1 else []
    comp=covering(cmasks,len(pts),k)
    print('COVER_COST_mpl',None if cover is None else len(cover),'COMPONENT_ONLY_COVER_COST_mpl',None if comp is None else len(comp))
    if print_detail:
        for i,(p,ri) in enumerate(zip(pts,r)):
            print('POINT',i,coords(p),'arrangement_multiplicity',ri)
        for j,(l,m) in enumerate(zip(joins,masks)):
            print('JOIN_LINE',j,coords(l),'component',l in lines,'point_ids',[i for i in range(len(pts)) if m&(1<<i)])
    if cover is not None:
        for j in cover:
            print('COVER_LINE',coords(joins[j]),'component',joins[j] in lines,'point_ids',[i for i in range(len(pts)) if masks[j]&(1<<i)])
    return lines,pts,r,joins,masks,k,cover

def poly_mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(a+b for a,b in zip(e,f));out[g]=out.get(g,O)+c*d
    return {e:c for e,c in out.items() if c}
def line_poly(l):return {tuple(int(i==j) for i in range(3)):c for j,c in enumerate(l) if c}
def poly_mult(poly,p):
    # Dehomogenize at the first nonzero coordinate and shift the other two.
    from math import comb
    chart=next(i for i,v in enumerate(p) if v)
    q=tuple(v/p[chart] for v in p)
    free=[i for i in range(3) if i!=chart]
    shifted={}
    for exps,c in poly.items():
        for a in range(exps[free[0]]+1):
            for b in range(exps[free[1]]+1):
                coeff=c*comb(exps[free[0]],a)*comb(exps[free[1]],b)*q[free[0]]**(exps[free[0]]-a)*q[free[1]]**(exps[free[1]]-b)
                shifted[a,b]=shifted.get((a,b),O)+coeff
    return min(a+b for (a,b),c in shifted.items() if c)

if __name__=='__main__':
    print('EXACT_FIELD Q(w), w^2+w+1=0; fractions only, no floating point arithmetic.')
    H=[(1,0,0),(0,1,0),(0,0,1)]+[(U,W**i,W**j) for i in range(3) for j in range(3)]
    h=audit('Hesse_12',H,True)
    lines,pts,r,joins,masks,k,cover=h
    assert len(pts)==21 and Counter(r)=={2:12,4:9} and k==5
    # Test both component and auxiliary lines as curve exceptions.
    for j in cover or []:
        pp={ (0,0,0):U }
        for t in cover:pp=poly_mul(pp,line_poly(joins[t]))
        mm=[poly_mult(pp,p) for p in pts]
        assert mm==[sum(bool(masks[t]&(1<<i)) for t in cover) for i in range(len(pts))]
        print('COVER_CURVE_DEGREE',len(cover),'CURVE_MULTIPLICITIES',mm,'SUM',sum(mm),'RATIO',F(len(cover),sum(mm)))
        break
    # A degree-five union omitting every shared-component exception is invalid Bézout input for its lines.
    if cover:
        l=joins[cover[0]]; print('SHARED_COMPONENT_FALSE_BEZOUT_SENTINEL cover_degree',len(cover),'curve_degree',1,'point_count_on_curve',masks[cover[0]].bit_count(),'line',coords(l),'intersection_is_NOT_proper')
    F3=[(U,-W**i,O) for i in range(3)]+[(O,U,-W**i) for i in range(3)]+[(-W**i,O,U) for i in range(3)]
    f=audit('Fermat_n3',F3)
    deletion_stats=Counter()
    for nremove in (1,2,3):
        for rem in combinations(range(9),nremove):
            sub=[l for i,l in enumerate(F3) if i not in rem]
            spts,sr=singular(list(map(norm,sub)));sj,sm=joined(spts)
            sk=max(m.bit_count() for m in sm)
            compk=max(sum(dot(norm(l),p)==0 for p in spts) for l in sub)
            cv=covering(sm,len(spts),sk)
            deletion_stats[nremove,len(spts),sk,compk,cv is not None]+=1
            print('FERMAT_DELETION',rem,'points',len(spts),'t',dict(sorted(Counter(sr).items())),'mpl_ALL',sk,'mpl_COMPONENT',compk,'cover_at_mpl',cv is not None)
    print('FERMAT_DELETION_CLASS_HISTOGRAM',dict(sorted(deletion_stats.items())))
    # Pencil with two added lines, in modular and nonmodular coordinates.
    pencil=[(1,-a,0) for a in (-1,0,1,2)]
    audit('rational_pencil4_plus2_modular',pencil+[(0,1,-1),(1,0,-1)])
    audit('rational_pencil4_plus2_nonmodular',pencil+[(0,1,-1),(1,0,-3)])
    # Exact curve-multiplicity check: irreducible nodal cubic at arrangement crossing points.
    nodal={(0,2,1):U,(3,0,0):-U,(2,0,1):-U}
    rat=list(map(norm,[(1,0,0),(0,1,0),(1,1,0),(1,-1,0),(0,0,1),(1,0,-1)]))
    rp,rr=singular(rat)
    rm=[poly_mult(nodal,p) for p in rp]
    print('NODAL_CUBIC f=y^2*z-x^3-x^2*z; irreducible since x+1 is nonsquare in C(x); node [0:0:1].')
    for p,ri,mi in zip(rp,rr,rm): print('CURVE_VS_ARRANGEMENT_MULTIPLICITY',coords(p),'r',ri,'m_C',mi)
    print('NODAL_CUBIC_SUM',sum(rm),'DEGREE',3,'GENUS_SUM',sum(m*(m-1) for m in rm),'GENUS_BOUND',(3-1)*(3-2))
    assert poly_mult(nodal,norm((0,0,1)))==2
    # Concrete genus/Bézout limitation vector, no claim of geometric realization.
    deg=5;v=[1]*26
    print('GENUS_ALONE_LIMITATION degree',deg,'S',sum(v),'genus_cost',sum(m*(m-1) for m in v),'bound',(deg-1)*(deg-2),'k=5 threshold',deg*5,'REALIZATION_NOT_ASSERTED')
    print('DONE all exact assertions passed.')
