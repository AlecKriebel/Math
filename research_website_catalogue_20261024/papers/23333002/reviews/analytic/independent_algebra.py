"""Own exact rational polynomial/rank checks; no native or third-party imports.

The universal arbitrary-degree/SOS argument is written in the initial proof.
"""
from fractions import Fraction as F
from itertools import product, permutations
from math import prod
from datetime import datetime, timezone
import hashlib
import json


def need(test,message):
    if not test:raise ValueError(message)


def clean(p):return{e:c for e,c in p.items()if c}
def const(c):return{(0,0,0):F(c)}if c else{}
def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,0)+c
    return clean(out)
def scale(p,c):return clean({e:a*c for e,a in p.items()})
def mul(p,q):
    out={}
    for e,c in p.items():
        for f,d in q.items():
            ef=tuple(a+b for a,b in zip(e,f));out[ef]=out.get(ef,0)+c*d
    return clean(out)
def power(p,n):
    out=const(1)
    for _ in range(n):out=mul(out,p)
    return out
def sub(p,q):return add(p,scale(q,-1))
def derivative(p,j):
    out={}
    for e,c in p.items():
        if e[j]:
            f=list(e);f[j]-=1;out[tuple(f)]=c*e[j]
    return clean(out)
def value(p,v):return sum(c*prod(F(a)**b for a,b in zip(v,e))for e,c in p.items())
def line(p,v):
    out={}
    for e,c in p.items():
        a=c
        for x,n in zip(v,e):a*=F(x)**n
        d=sum(e);out[d]=out.get(d,0)+a
    return clean(out)
def monomials(d):return[(a,b,d-a-b)for a in range(d,-1,-1)for b in range(d-a,-1,-1)]
def rref(matrix):
    a=[[F(x)for x in row]for row in matrix];r=0;det=F(1);pivots=[]
    cols=len(a[0])if a else 0
    for c in range(cols):
        row=next((i for i in range(r,len(a))if a[i][c]),None)
        if row is None:continue
        if row!=r:a[r],a[row]=a[row],a[r];det=-det
        pivot=a[r][c];det*=pivot;a[r]=[x/pivot for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                factor=a[i][c];a[i]=[x-factor*y for x,y in zip(a[i],a[r])]
        pivots.append(c);r+=1
        if r==len(a):break
    if len(a)!=cols:det=None
    elif r<cols:det=F(0)
    return r,det,a,pivots
def serial(p):return{' '.join(map(str,e)):str(c)for e,c in sorted(p.items())}
def algebraic_line(p,v,squared):
    out={}
    for d,c in line(p,v).items():
        r=d%2;out[r]=out.get(r,0)+c*squared**(d//2)
    return clean(out)


def main():
    X={(1,0,0):F(1)};Y={(0,1,0):F(1)};Z={(0,0,1):F(1)};variables=[X,Y,Z]
    R=add(*(power(v,6)for v in variables),
          *(scale(mul(power(variables[i],4),power(variables[j],2)),-1)for i in range(3)for j in range(3)if i!=j),
          scale(mul(mul(power(X,2),power(Y,2)),power(Z,2)),3))
    a,b,c=[power(v,2)for v in variables]
    identity=add(mul(power(sub(a,b),2),sub(add(a,b),c)),mul(c,mul(sub(a,c),sub(b,c))))
    need(identity==R,'ordered nonnegative identity')
    for perm in permutations(range(3)):
        changed={tuple(e[perm[i]]for i in range(3)):q for e,q in R.items()}
        need(changed==R,'Robinson symmetry')
    grad=[derivative(R,j)for j in range(3)]
    J=[sub(mul(variables[j],grad[i]),mul(variables[i],grad[j]))for i,j in [(0,1),(0,2),(1,2)]]
    K=[mul(variables[j],grad[i])for i,j in [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)]]
    need(add(*(mul(v,g)for v,g in zip(variables,grad)))==scale(R,6),'Euler identity')
    zeros=[(1,s,t)for s,t in product((-1,1),repeat=2)]+[(1,s,0)for s in (-1,1)]+[(1,0,t)for t in (-1,1)]+[(0,1,t)for t in (-1,1)]
    need(len(set(zeros))==10,'ten distinct projective representatives')
    for v in zeros:
        need(line(R,v)=={}and all(line(g,v)=={}for g in grad+J+K),'whole zero-line polynomial identities')
    for i in range(3):
        v=tuple(int(i==j)for j in range(3))
        need(line(R,v)=={6:F(1)}and all(line(g,v)=={}for g in J+K),'axis polynomial identities')
    ranks={};matrix3=None
    for d in range(4):
        ms=monomials(d);matrix=[[value({e:F(1)},v)for e in ms]for v in zeros]
        rank,det,reduced,pivots=rref(matrix);need(rank==len(ms),'low-degree evaluation injection')
        ranks[str(d)]={'columns':ms,'rank':rank,'determinant':str(det)if det is not None else None}
        if d==3:
            matrix3=matrix
            need(reduced==[[F(int(i==j))for j in range(10)]for i in range(10)],'exact cubic RREF')
    positive=(2,2,1)
    need(value(R,positive)==9 and[value(g,positive)for g in grad]==[12,12,6],'positive tangency direction')
    need(all(value(g,positive)==0 for g in J)and value(K[0],positive)==24,'J not K')
    P=add(*(mul(v,sub(power(v,2),add(*(power(w,2)for w in variables if w is not v))))for v in variables),scale(mul(mul(X,Y),Z),-1))
    H=sub(R,power(P,2));omitted=(1,1,1)
    for v in zeros:
        expected={6:F(-16)}if v==omitted else{}
        need(line(H,v)==expected,'nine-line weakened countercertificate')
    need(line(P,(1,0,0))=={3:F(1)}and line(H,(1,0,0))=={},'weakened countercertificate axis')
    missing_matrix=[row for v,row in zip(zeros,matrix3)if v!=omitted]
    need(rref(missing_matrix)[0]==9,'omitting one zero line loses cubic injection')
    coeff=[P.get(e,F(0))for e in monomials(3)]
    need(all(sum(q*c for q,c in zip(row,coeff))==0 for row in missing_matrix),'explicit missing-row nullvector')
    Q=add(power(sub(const(1),mul(X,Y)),2),power(Y,2),const(F(-1,2)))
    qx,qy=derivative(Q,0),derivative(Q,1)
    kq=[mul(Y,qx),mul(X,qy)];jq=sub(kq[0],kq[1])
    need(kq[0]==scale(mul(power(Y,2),sub(mul(X,Y),const(1))),2),'Q product first equation')
    need(sub(kq[1],const(2))==mul(add(scale(power(X,2),2),const(2)),sub(mul(X,Y),const(1))),'Q xy1 branch impossible')
    need(line(kq[1],(1,0,0))=={2:F(-2)},'Q y0 branch')
    need(value(Q,(0,0,0))==F(1,2)and value(Q,(2,F(1,2),0))==F(-1,4),'Q positive K point and negative global point')
    path={}
    for e,q in Q.items():
        d=-e[0]+e[1];path[d]=path.get(d,0)+q
    need(clean(path)=={0:F(-1,2),2:F(1)},'nonattainment path Laurent identity')
    sq=F(5,24);v=(3,1,0)
    need(algebraic_line(jq,v,sq)=={},'negative tangency point satisfies JQ')
    need(algebraic_line(Q,v,sq)=={0:F(-29,192)},'exact negative tangency value')
    need(algebraic_line(add(qx,scale(X,F(1,4))),v,sq)=={}and algebraic_line(add(qy,scale(Y,F(1,4))),v,sq)=={},'Q gradient eigenvalue minusonequarter')
    need(algebraic_line(kq[0],v,sq)=={0:F(-5,32)},'same negative point excluded from KQ')
    grid=0;zero_count=0
    for point in product(range(-3,4),repeat=3):
        rv=value(R,point);aa,bb,cc=sorted((x*x for x in point),reverse=True)
        need(rv>=0 and(rv==0)==(aa==bb and(cc==0 or cc==aa)),'finite zero-classification control')
        grid+=1;zero_count+=rv==0
    return{'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','polynomial_R':serial(R),'gradient_R':[serial(g)for g in grad],
            'whole_line_identities_checked':10,'axis_identities_checked':3,'zero_representatives':zeros,'evaluation_ranks':ranks,
            'cubic_evaluation_matrix':[[int(x)for x in row]for row in matrix3],
            'positive_J_not_K_point':{'point':positive,'R':9,'gradient':[12,12,6],'K_first':24},
            'weakened_nine_line_countercertificate':{'omitted_line':omitted,'cubic':serial(P),'remainder':serial(H),'missing_line_remainder':'-16*u^6','axis_cubic':'u^3','rank_with_one_row_removed':9,'scope':'Certificate on the weakened nine-line-plus-axis spine only; deliberately not on the actual variety.'},
            'Q_controls':{'Q':serial(Q),'V_real_K_case_split':'y=0 gives -2x^2=0; xy=1 makes second generator2.','negative_global_value':'-1/4 at(2,1/2)','nonattainment_path':'Q(1/u,u)=u^2-1/2','negative_J_point':'x=3s,y=s,s^2=5/24','negative_J_value':'-29/192','negative_J_gradient_eigenvalue':'-1/4','K_first_at_negative_J_point':'-5/32'},
            'grid_controls':{'points':grid,'zeros':zero_count},'Euler_gradient_ideal_positive_control':True,
            'negative_controls':['Omitting onezero line yields an explicit cubic countercertificate on weakenedspine.','J and K varieties differ at(2,2,1).','Q product counterexample does not apply to tangency minors.','Positiveepsilon forces constants onzero lines, not zero constants.'],
            'limits':'Exact polynomial identities/ranks and explicit boundary witnesses; universal arbitrarydegree/numberofsquares/epsilon argument is the written proof, not a finite SOS-degree search.'}


if __name__=='__main__':print(json.dumps(main(),indent=2))
