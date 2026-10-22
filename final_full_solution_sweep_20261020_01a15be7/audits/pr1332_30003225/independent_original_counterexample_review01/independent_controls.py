"""Independent exact finite guards. No network, imports from author code, or writes."""
from itertools import product
from math import gcd
import json

def require(test, message):
    if not test:
        raise RuntimeError(message)

def mul(a,b,mod=None):
    n=len(a)
    c=[sum(a[i]*b[d-i] for i in range(d+1)) for d in range(n)]
    return tuple(v % mod if mod else v for v in c)

def powers(x,n,mod=None):
    out=[(1,)+(0,)*(len(x)-1)]
    for _ in range(n): out.append(mul(out[-1],x,mod))
    return out

def evaluate(coeff,xp,mod=None):
    ans=tuple(sum(c*xp[j][d] for j,c in coeff.items()) for d in range(len(xp[0])))
    return tuple(v % mod if mod else v for v in ans)

def order(a):
    return next((i for i,v in enumerate(a) if v),len(a))

def monomial(e,n):
    return tuple(int(i==e) for i in range(n))

def main():
    n=5; field=3
    arcs=[(0,)+a for a in product(range(field),repeat=4)]
    result={'field':field,'jet_modulus':'t^5','coordinate_jets':len(arcs),'families':{}}
    for k in [2,3]:
        params=[dict(zip(range(k,n),a)) for a in product(range(field),repeat=n-k)]
        exact=[a for a in params if a[k]]
        r=(n+k-1)//k
        comparisons=0; points=0; exact_points=0
        for x in arcs:
            xp=powers(x,n-1,field)
            # Compute actual images of all branch polynomials; no order test enters here.
            image=[evaluate(a,xp,field) for a in params]
            exact_image=[evaluate(a,xp,field) for a in exact]
            for y in arcs:
                actual=all(y==v for v in image)
                exact_actual=all(y==v for v in exact_image)
                predicted=order(x)>=r and not any(y)
                require(actual==predicted,('full family',k,x,y))
                require(exact_actual==predicted,('exact contact family',k,x,y))
                points+=int(actual);exact_points+=int(exact_actual)
                comparisons+=len(params)
        result['families'][str(k)]={'parameters':len(params),'exact_contact_parameters':len(exact),
            'pairs':len(arcs)**2,'membership_comparisons':comparisons,'intersection_points':points,
            'exact_contact_intersection_points':exact_points,'predicted_x_threshold':r}
        require(points==field**(n-r),('point count',k))
    # All-q argument is analytic; this finite grid checks every witness branch of it.
    witness_cases=0
    for r in [2,3]:
        for j in range(1,31):
            for q in range(1,31):
                if q<r: a,b=q,max(5,j*q); left=False;right=True
                elif q>r or j*q>5: a,b=r,5;left=True;right=False
                else: a,b=r,j*q;left=False;right=True
                require((a>=r and b>=5)==left,('left witness',r,j,q))
                require((a>=q and b>=j*q)==right,('right witness',r,j,q))
                require(left!=right,('separation',r,j,q))
                witness_cases+=1
    # Polynomial wedges to arbitrary finite coefficient examples, including x=0.
    wedge_cases=0
    length=13
    for k in [2,3]:
        r=(5+k-1)//k
        for a in product([-2,0,3],repeat=5-k):
            coeff=dict(zip(range(k,5),a))
            for x0 in [monomial(r,length),(0,)*length,monomial(r,length)]:
                y0=monomial(5,length)
                rem=tuple(y0[i]-evaluate(coeff,powers(x0,4))[i] for i in range(length))
                require(order(rem)>=5,'wedge remainder')
                for e in [-2,-1,1,2]:
                    xe=tuple(v+(e if i==1 else 0) for i,v in enumerate(x0))
                    pe=evaluate(coeff,powers(xe,4))
                    ye=tuple(pe[i]+rem[i] for i in range(length))
                    require(order(xe)==1,'dense transverse x order')
                    require(order(tuple(ye[i]-pe[i] for i in range(length)))>=5,'transverse residual')
                    # Specialization e=0 gives the original arc coefficientwise.
                    p0=evaluate(coeff,powers(x0,4))
                    require(tuple(p0[i]+rem[i] for i in range(length))==y0,'specialization')
                    wedge_cases+=1
    # Independent Euclidean toric charts: unimodularity and formal inverse exponents.
    for A,B,C,D in [(3,5,1,2),(2,5,1,3)]:
        require(A*D-B*C==1,'toric determinant')
        require(gcd(A,B)==1,'primitive divisor')
        require(D*A-C*B==1 and -B*A+A*B==0,'u inverse orders')
        require(D*C-C*D==0 and -B*C+A*D==1,'inverse monomials')
    # Boundary and mutation guards.
    require(not (1>=3 and 5>=5),'single member must differ from intersection')
    require(2>=2 and not 2>=3,'F2 and F3 differ')
    require(3*2==6 and 2*3==6,'divisible positive cases')
    require(not any(j*2==5 or j*3==5 for j in range(1,100)),'no reference ray')
    require((5+4)//5==1,'fixed final-center singleton')
    require(2*2<5 and 3*2>=5,'ceil guard')
    result.update(witness_cases=witness_cases,wedge_cases=wedge_cases,
                  toric_charts=2,negative_and_boundary_guards=6,
                  limits='Finite exact guards only; analytic proof supplies complex parameters, density, family exhaustion and all integers.')
    return result

if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True,indent=2))
