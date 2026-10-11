#!/usr/bin/env python3
"""Independent exact reconstruction; does not import either supplied checker.
Uses series division and the implicit slit-map equation, not inverse Catalan
composition; evaluates boundary polynomials by ascending powers.
"""
from fractions import Fraction as Q
from math import isqrt
from collections import deque
import hashlib,json,pathlib,sys

D=10
class G:
    __slots__=('x','y')
    def __init__(self,x=0,y=0):self.x=Q(x);self.y=Q(y)
    def __add__(a,b):
        if not isinstance(b,G):b=G(b)
        return G(a.x+b.x,a.y+b.y)
    __radd__=__add__
    def __neg__(a):return G(-a.x,-a.y)
    def __sub__(a,b):return a+-b
    def __mul__(a,b):
        if not isinstance(b,G):b=G(b)
        return G(a.x*b.x-a.y*b.y,a.x*b.y+a.y*b.x)
    __rmul__=__mul__
    def __truediv__(a,b):
        if not isinstance(b,G):b=G(b)
        n=b.x*b.x+b.y*b.y
        return G((a.x*b.x+a.y*b.y)/n,(a.y*b.x-a.x*b.y)/n)
    def __eq__(a,b):return isinstance(b,G) and a.x==b.x and a.y==b.y
    def sq(a):return a.x*a.x+a.y*a.y
    def coords(a):return [str(a.x),str(a.y)]
Z=G();I=G(1)
def demand(ok,why):
    if not ok:raise RuntimeError(why)
def product(a,b):
    return [sum((a[j]*b[n-j] for j in range(n+1)),Z) for n in range(D+1)]
def divide(a,b):
    out=[]
    for n in range(D+1):out.append((a[n]-sum((b[j]*out[n-j] for j in range(1,n+1)),Z))/b[0])
    return out
def K(a,u):
    den=[I]+[u*a[n] for n in range(1,D+1)]
    return divide(a,product(den,den))
def Phi(a,q,u):
    y=[q*v for v in K(a,u)];b=[Z]*(D+1)
    for n in range(1,D+1):
        b[n]=y[n]+2*u*sum((y[i]*b[n-i] for i in range(1,n)),Z)+u*u*sum((y[i]*b[j]*b[n-i-j] for i in range(1,n) for j in range(1,n-i)),Z)
    demand(K(b,u)==y,'implicit slit inverse identity')
    return b
def upper_abs(a,s):
    x=a.sq();num=x.numerator*s*s;den=x.denominator
    k=isqrt(num*den)//den
    if k*k*den<num:k+=1
    demand(k*k*den>=num and (k==0 or (k-1)*(k-1)*den<num),'least upward sqrt')
    return Q(k,s)
def point(t,sign=1):return G(sign*(1-t*t)/(1+t*t),sign*2*t/(1+t*t))
def poly(a,z):
    total=Z;power=I
    for v in a:total+=v*power;power=power*z
    return total

def main():
    root=pathlib.Path(sys.argv[1]);outpath=pathlib.Path(sys.argv[2])
    data=json.loads((root/'COUNTEREXAMPLE.json').read_text());expected=json.loads((root/'CERTIFICATE_RESULT.json').read_text());alt_expected=json.loads((root/'ALTERNATIVE_RESULT.json').read_text())
    c=[Z,Z]+[G(*v) for v in data['coefficients']]
    q1=Q(63,80);q2=Q(2,25);r=Q(999,1000);gamma=Q(1000000,1002001)
    u1=G(-1);u2=G(Q(-39951,40049),Q(-2800,40049));u3=G(Q(-621,629),Q(100,629))
    demand(all(u.sq()==1 for u in (u1,u2,u3)),'unit-circle directions')
    ident=[Z,I]+[Z]*(D-1)
    a=[x/(q1*q2) for x in K(Phi(Phi(ident,q1,u1),q2,u2),u3)]
    demand(a[0]==Z and a[1]==I,'normalization')
    ahash=hashlib.sha256(json.dumps([v.coords() for v in a],separators=(',',':')).encode()).hexdigest()
    demand(ahash==expected['coefficient_sha256'],'coefficient hash agreement')
    L=sum((c[n]*a[n]*r**(n-1) for n in range(2,D+1)),Z)
    demand(L.x>Q(2517,2500),'L real lower bound')
    demand(str(L.x.numerator)==expected['real_convolution_numerator'] and str(L.x.denominator)==expected['real_convolution_denominator'],'L real exact agreement')
    hcoef=[-v/L for v in c];g=hcoef[:];g[1]=I
    convzero=sum((g[n]*a[n]*r**n for n in range(D+1)),Z)
    demand(convzero==Z,'exact Gaussian rational convolution zero')
    result={'status':'IN_PROGRESS','method':'independent Gaussian rational implementation; implicit slit recurrence and series division','coefficients': [v.coords() for v in a],'coefficient_sha256':ahash,'complex_L':L.coords(),'convolution_at_r':convzero.coords(),'gamma':str(gamma)}
    outpath.write_text(json.dumps(result,indent=2)+'\n');print('independent coefficients, L, and convolution zero PASS',flush=True)
    N=8192;maximum=Q(0);count=0;plus=[(n+1)*c[n] for n in range(1,D+1)];minus=[(n-1)*c[n] for n in range(1,D+1)]
    for j in range(-N,N+1):
        for sign in (1,-1):
            z=point(Q(j,N),sign)
            b=(upper_abs(poly(plus,z),10**9)+upper_abs(poly(minus,z),10**9))/2
            maximum=max(maximum,b);count+=1
    lip=sum(Q(n*(n-1))*(abs(c[n].x)+abs(c[n].y)) for n in range(2,D+1));bound=maximum+lip/N
    demand(count==32770,'complete all-circle listed cover')
    for key,value in [('sample_norm_upper',maximum),('angular_lipschitz_upper',lip),('covering_norm_upper',bound)]:demand(str(value)==expected[key],key)
    demand(bound<Q(251,250) and Q(2510,2517)<gamma,'strict symmetric margin')
    result['symmetric']={'grid_points':count,'maximum':str(maximum),'angular_lipschitz':str(lip),'global_bound':str(bound),'strict_gamma_margin_using_chosen_bounds':str(gamma-Q(2510,2517))};outpath.write_text(json.dumps(result,indent=2)+'\n');print('independent symmetric complete circle certificate PASS',flush=True)
    # Breadth-first traversal, independently tracked leaf partition coverage.
    deriv=[n*hcoef[n] for n in range(1,D+1)];quotient=hcoef[1:];ab=[abs(v.x)+abs(v.y) for v in hcoef]
    queue=deque([(Q(0),Q(1),Q(-1),Q(1),s,0,'') for s in (1,-1)])
    visited=0;leaves=[];maximum_depth=0;minmargin=gamma
    while queue:
        lo,hi,left,right,sign,depth,path=queue.popleft();visited+=1
        demand(visited<=300000 and depth<=40,'finite certificate budget')
        rm=(lo+hi)/2;tm=(left+right)/2;v=point(tm,sign);z=rm*v;der=poly(deriv,z);q=poly(quotient,z);qabs=upper_abs(q,10**10)
        first=der-q;second=der+G(v.x,-v.y)*qabs
        center=(upper_abs(first,10**10)+upper_abs(second,10**10)+Q(1,10**10))/2
        br=sum(Q(n*(n-1))*ab[n]*hi**(n-2) for n in range(2,D+1));bt=sum(Q(2*n*n-2*n+1)*ab[n]*hi**(n-1) for n in range(2,D+1))
        er=br*(hi-lo)/2;et=bt*(right-left)/2;b=center+er+et
        if b<gamma:
            leaves.append({'sign':sign,'path':path,'rectangle':list(map(str,(lo,hi,left,right))),'bound':str(b)})
            minmargin=min(minmargin,gamma-b);maximum_depth=max(maximum_depth,depth)
        elif er>=et:
            queue.extend([(lo,rm,left,right,sign,depth+1,path+'0'),(rm,hi,left,right,sign,depth+1,path+'1')])
        else:
            queue.extend([(lo,hi,left,tm,sign,depth+1,path+'0'),(lo,hi,tm,right,sign,depth+1,path+'1')])
    demand(visited==2*len(leaves)-2,'two full binary partition trees')
    for sign in (1,-1):
        paths={leaf['path'] for leaf in leaves if leaf['sign']==sign}
        demand(sum((Q(1,2**len(p)) for p in paths),Q(0))==1,'complete exact prefix partition')
        for p in paths:demand(not any(p[:j] in paths for j in range(len(p))),'overlapping prefix leaf')
        area=sum((Q(leaf['rectangle'][1])-Q(leaf['rectangle'][0]))*(Q(leaf['rectangle'][3])-Q(leaf['rectangle'][2])) for leaf in leaves if leaf['sign']==sign)
        demand(area==2,'full rectangle area for each semicircle')
    demand(visited==alt_expected['visited_rectangles'] and len(leaves)==alt_expected['certified_leaves'] and maximum_depth==alt_expected['maximum_depth'],'alternative tree statistics')
    demand(str(minmargin.numerator)==alt_expected['smallest_margin_numerator'] and str(minmargin.denominator)==alt_expected['smallest_margin_denominator'],'alternative exact margin')
    leafraw=json.dumps(leaves,sort_keys=True,separators=(',',':')).encode();leafpath=outpath.with_name('INDEPENDENT_DISK_LEAVES.json');leafpath.write_bytes(leafraw+b'\n')
    result['alternative']={'visited_rectangles':visited,'certified_leaves':len(leaves),'maximum_depth':maximum_depth,'smallest_margin':str(minmargin),'complete_two_partition_trees':True,'area_per_semicircle_rectangle':'2','leaf_certificate_sha256':hashlib.sha256(leafraw+b'\n').hexdigest()}
    result['status']='PASS';outpath.write_text(json.dumps(result,indent=2)+'\n');print('independent alternative full-disk certificate PASS',flush=True)
if __name__=='__main__':main()
