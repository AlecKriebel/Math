"""New standard-library exact checks. No author code or symbolic solver used.

Finite scans are supplements to REPORT.md's algebraic-closure proof, never a
substitute for it. Extension-only singularity and off-hypersurface controls are
explicit. All guards survive optimization.
"""
from itertools import product
from math import factorial, prod, isqrt
import json


def need(ok,why):
    if not ok:raise ValueError(why)


def primes(b):
    return [p for p in range(2,b+1) if all(p%k for k in range(2,isqrt(p)+1))]


def counts(total,length):
    if length==1:
        yield (total,);return
    for x in range(total+1):
        for tail in counts(total-x,length-1):yield (x,)+tail


def unit(m,i,power):
    return tuple(power if j==i else 0 for j in range(m))


def add_exp(a,b):return tuple(x+y for x,y in zip(a,b))


def prefix_vector(p,m,d):
    k=max(1,m-d+p)
    need(k<=min(p,m-1),'nonempty proper-prefix interval')
    v=[p-k+1]+[1]*(k-1)+[d-p-(m-k)+1]+[1]*(m-k-1)
    need(len(v)==m and min(v)>0 and sum(v)==d and sum(v[:k])==p,'prefix composition')
    return tuple(v)


def B(v,p):return (1+sum(sum(v[:i+1]) for i in range(len(v)-1)))%p


def residue_vector(p,m):
    # Independent dynamic program on residues, not the interval inequality.
    need(3<=m<p,'degree-p residue branch')
    L=p-m;target=(-1-m*(m-1)//2)%p;states={0:[]}
    for _ in range(L):
        nxt={}
        for r,ws in states.items():
            for w in range(m):nxt.setdefault((r+w)%p,ws+[w])
        states=nxt
    need(target in states,'weighted residue reachable')
    e=[0]*m
    for w in states[target]:e[m-1-w]+=1
    v=tuple(1+x for x in e)
    need(min(v)>0 and sum(v)==p and B(v,p)==0,'B-zero composition')
    return v


def terms(p,m,d,kind,v=None):
    if v is None:v=(d-m+1,)+(1,)*(m-1)
    H=[]
    if kind in ('diagonal','binary'):
        H=[unit(m,i,d) for i in range(m)]
        if kind=='binary':H.append((d-1,1)+(0,)*(m-2))
    else:
        H=[add_exp(unit(m,i,d-1),unit(m,i+1,1)) for i in range(m-1)]+[unit(m,m-1,d)]
    need(sum(v)==d and min(v)>0 and all(sum(e)==d and 0 in e for e in H),'homogeneous support')
    return tuple(v),H


def moment(p,Q,H):
    # Multinomial expansion with parameters still formal. Each surviving
    # positive coordinate power sum contributes -1; normalization cancels them.
    mon=[Q]+H;out={};f=factorial(p-1)
    for ee in counts(p-1,len(mon)):
        powers=[sum(k*v[i] for k,v in zip(ee,mon)) for i in range(len(Q))]
        if not all(x>0 and x%(p-1)==0 for x in powers):continue
        coeff=f
        for k in ee:coeff//=factorial(k)
        key=ee[1:];out[key]=(out.get(key,0)+coeff)%p
    return {k:v for k,v in out.items() if v}


def parameter_eval(C,A,p):
    return sum(c*prod(pow(a,k,p) for a,k in zip(A,e)) for e,c in C.items())%p


def polynomial(Q,H,A,p):
    F={Q:1}
    for a,e in zip(A,H):F[e]=(F.get(e,0)+a)%p
    return {e:c for e,c in F.items() if c%p}


def deriv(F,i,p):
    out={}
    for e,c in F.items():
        if e[i]%p:
            z=list(e);z[i]-=1;z=tuple(z);out[z]=(out.get(z,0)+c*e[i])%p
    return {e:c for e,c in out.items() if c}


def evaluate(F,x,p):return sum(c*prod(pow(a,k,p) for a,k in zip(x,e)) for e,c in F.items())%p


def projective(q,m):
    for i in range(m):
        for tail in product(range(q),repeat=m-i-1):yield (0,)*i+(1,)+tail


def bad_diagonal(p,m,d,A):
    t=d-m+1
    return pow(d,d,p)*pow(A[0],t,p)*prod(A[1:])%p==((-1)**d*pow(t,t,p))%p


def family(p,m,d):
    need(p in primes(p) and m>=3 and d>=m,'main theorem domain')
    if p==2 and d%2:
        kind='binary';v,H=terms(p,m,d,kind);A=(1,)*len(H)
    elif d%p:
        kind='diagonal';v,H=terms(p,m,d,kind);A=None
    elif d>p:
        kind='prefix_chain';v,H=terms(p,m,d,kind,prefix_vector(p,m,d));A=None
    elif m<p:
        kind='B_chain';v,H=terms(p,m,d,kind,residue_vector(p,m));A=None
    else:
        kind='equal_prime';v,H=terms(p,m,d,kind,(1,)*m);A=(1,)*(m-1)+(2,)
    C=moment(p,v,H);r=len(H)
    need(C.get((0,)*r)==1 and all(max(e)<=p-2 for e in C),'constant1 and individual degrees')
    if kind=='diagonal':need(all(e[-1]<=p-3 for e in C),'sharp last individual degree')
    if A is None:
        A=next((a for a in product(range(1,p),repeat=r) if parameter_eval(C,a,p)),None)
        need(A is not None,'nonzero-grid coefficient selection')
        if kind=='diagonal':
            good=[a for a in range(1,p) if parameter_eval(C,A[:-1]+(a,),p)]
            need(len(good)>=2,'at least two count-good final values')
            A=next((A[:-1]+(a,) for a in good if not bad_diagonal(p,m,d,A[:-1]+(a,))),None)
            need(A is not None,'same equation count good and avoids singular candidate')
    value=parameter_eval(C,A,p);need(value!=0,'count-good final equation')
    F=polynomial(v,H,A,p);D=[deriv(F,i,p) for i in range(m)]
    np=sing=total=0
    for x in projective(p,m):
        total+=1
        if evaluate(F,x,p)==0:
            np+=1;sing+=all(evaluate(g,x,p)==0 for g in D)
    need(np%p==(1+(-1)**m*value)%p and np%p!=1,'independent projective count congruence')
    need(sing==0,'no rational singularity (supplementary only)')
    if kind in ('equal_prime','binary'):need(value==1,'fixed-family moment exactly1')
    return F,{'p':p,'m':m,'d':d,'branch':kind,'v':v,'A':A,'C_value':value,
              'point_count':np,'projective_points_examined':total,
              'equation':[[list(e),c] for e,c in sorted(F.items())],
              'moment_terms':[[list(e),c] for e,c in sorted(C.items())]}


class Extension:
    def __init__(self,p,k=2):
        self.p=p;self.k=k;self.q=p**k
        need(k==2 or (p,k)==(2,3),'supported exact extension')
        if k==2:
            self.alpha=1 if p==2 else next(a for a in range(2,p) if pow(a,(p-1)//2,p)==p-1)
            self.beta=1 if p==2 else 0
    def add(self,a,b):
        if self.k==3:return a^b
        return (a%self.p+b%self.p)%self.p+self.p*((a//self.p+b//self.p)%self.p)
    def mul(self,a,b):
        if self.k==3:
            z=0
            while b:
                if b&1:z^=a
                b>>=1;a<<=1
                if a&8:a^=11  # u^3+u+1, an irreducible cubic over F2.
            return z
        p=self.p;a0,a1=a%p,a//p;b0,b1=b%p,b//p
        return (a0*b0+self.alpha*a1*b1)%p+p*((a0*b1+a1*b0+self.beta*a1*b1)%p)
    def power(self,a,n):
        z=1
        while n:
            if n&1:z=self.mul(z,a)
            a=self.mul(a,a);n//=2
        return z
    def inv(self,a):
        need(a!=0,'nonzero field denominator');return self.power(a,self.q-2)


def ext_eval(F,x,K):
    z=0
    for e,c in F.items():
        t=c%K.p
        for a,k in zip(x,e):t=K.mul(t,K.power(a,k))
        z=K.add(z,t)
    return z


def ext_singular(F,x,K):
    return ext_eval(F,x,K)==0 and all(ext_eval(deriv(F,i,K.p),x,K)==0 for i in range(len(x)))


def main():
    prefix_cases=residue_cases=0
    for p in primes(43):
        for d in range(2*p,121,p):
            for m in range(3,d+1):prefix_vector(p,m,d);prefix_cases+=1
        for m in range(3,p):residue_vector(p,m);residue_cases+=1
    records=[];forms={}
    for p in (2,3,5,7):
        for m in (3,4,5):
            for d in range(m,m+5):
                F,r=family(p,m,d);records.append(r);forms[p,m,d]=F
    F,r=family(7,7,7);records.append(r);forms[7,7,7]=F
    extension_checks=[]
    for p,m,d in [(2,3,3),(2,4,5),(2,3,4),(3,3,3),(3,3,4),(3,3,6),(5,3,5),(5,4,5)]:
        K=Extension(p);F=forms[p,m,d];examined=0
        for x in projective(K.q,m):
            need(not ext_singular(F,x,K),'bounded extension singularity');examined+=1
        extension_checks.append({'p':p,'extension_degree':2,'m':m,'d':d,'points_examined':examined})
    # Field arithmetic sanity, independent from the hypersurface formulas.
    for p in (2,3,5):
        K=Extension(p)
        need(all(K.mul(a,K.inv(a))==1 for a in range(1,K.q)),'extension inverses')
        need(all(K.mul(a,K.add(b,c))==K.add(K.mul(a,b),K.mul(a,c))
                 for a,b,c in product(range(K.q),repeat=3)),'extension distributivity')
    rejected=[]
    def reject(name,fn):
        try:fn()
        except ValueError:rejected.append(name)
        else:raise ValueError('corruption accepted: '+name)
    # A genuine F9 singularity absent over F3: d4, v=(2,1,1), all Ai=1.
    Q,H=terms(3,3,4,'diagonal');bad=polynomial(Q,H,(1,1,1),3);K9=Extension(3)
    need(not any(ext_singular(bad,x,Extension(3)) for x in projective(3,3)),
         'bad diagonal has no F3-rational singularity')
    geometric_point=(1,4,5)  # 1,1+u,(1+u)^(-1), u²=-1.
    need(ext_singular(bad,geometric_point,K9),'explicit extension-only diagonal singularity')
    reject('rational_scan_as_geometric_authority',lambda:need(not ext_singular(bad,geometric_point,K9),'geometric singularity'))
    reject('all_nonzero_diagonal_coefficients_smooth',lambda:need(not bad_diagonal(3,3,4,(1,1,1)),'bad discriminant'))
    # Equal-prime forbidden a1 has a rational singularity in every tested p.
    equal_bad=[]
    for p in (3,5,7):
        Q,H=terms(p,p,p,'equal_prime',(1,)*p);bad=polynomial(Q,H,(1,)*p,p)
        x=(1,)+tuple((-i)%p for i in range(1,p));need(evaluate(bad,x,p)==0 and all(evaluate(deriv(bad,i,p),x,p)==0 for i in range(p)),'forbidden a1 witness')
        equal_bad.append({'p':p,'point':x})
    reject('equal_prime_a1',lambda:need(evaluate(bad,x,p)!=0 or any(evaluate(deriv(bad,i,p),x,p) for i in range(p)),
                                       'verified explicit singular point for a1'))
    # B0 gradient critical point is off the hypersurface. Omitting F is wrong.
    Q,H=terms(5,4,5,'B_chain',(2,1,1,1));off=polynomial(Q,H,(1,1,1,1),5);x=(2,3,2,1)
    need(B(Q,5)==0 and all(evaluate(deriv(off,i,5),x,5)==0 for i in range(4)) and evaluate(off,x,5)==1,'critical point outside F')
    reject('omit_F_in_dividing_characteristic',lambda:need(evaluate(off,x,5)==0,'critical is not singular'))
    # In characteristic2, deleting the repair term makes the cubic singular.
    Q,H=terms(2,3,3,'diagonal');unrepaired=polynomial(Q,H,(1,1,1),2);x=(1,1,1)
    need(evaluate(unrepaired,x,2)==0 and all(evaluate(deriv(unrepaired,i,2),x,2)==0 for i in range(3)),'missing repair singular point')
    reject('omit_binary_repair',lambda:need(not all(evaluate(deriv(unrepaired,i,2),x,2)==0 for i in range(3)),'repair necessary'))
    Q,H=terms(2,3,4,'prefix_chain',prefix_vector(2,3,4));zero_tail=polynomial(Q,H,(1,1,0),2);x=(0,0,1)
    need(evaluate(zero_tail,x,2)==0 and all(evaluate(deriv(zero_tail,i,2),x,2)==0 for i in range(3)),'zero last coefficient creates boundary singularity')
    reject('allow_zero_chain_coefficient',lambda:need(not all(evaluate(deriv(zero_tail,i,2),x,2)==0 for i in range(3)),'nonzero coefficient hypothesis'))
    reject('Fermat_before_coordinate_descent',lambda:need(K9.power(4,2)==1,'K9 torus element need not have (p-1)power1'))
    reject('wrong_exponent_composition',lambda:need(sum((1,1,1))==6,'composition degree'))
    reject('drop_prefix_and_B_conditions',lambda:need(any(sum((1,1,3)[:i])%5==0 for i in (1,2)) or B((1,1,3),5)==0,'neither sufficient chain condition'))
    reject('extend_main_integrality_to_n1',lambda:family(2,2,2))
    reject('allow_composite_p',lambda:family(4,3,4))
    reject('allow_degree_below_m',lambda:family(3,4,3))
    reject('zero_exponent_power_sum',lambda:need(sum(pow(x,0,3) for x in range(3))%3==2,'zero exponent sum is0 not-1'))
    reject('grid_degree_p_minus1',lambda:need(any((1-pow(a,4,5))%5 for a in range(1,5)),'nonzero polynomial vanishes on whole nonzero grid'))
    reject('replace_sharp_bound_by_p_minus2',lambda:need(len([a for a in (1,2) if (a-2)%3])>=2,'one count-good choice can be the forbidden choice'))
    # Classical n1 foil: smooth degree2 norm, but two geometric points.
    K4=Extension(2);binary_norm={(2,0):1,(1,1):1,(0,2):1}
    roots=[x for x in projective(4,2) if ext_eval(binary_norm,x,K4)==0]
    need(len(roots)==2 and not any(ext_singular(binary_norm,x,K4) for x in roots),
         'smooth binary irreducible norm is not geometrically integral')
    need(not any(evaluate(binary_norm,x,2)==0 for x in projective(2,2)),'binary norm point-free over F2')
    # Literal AIM foil: the cubic norm from F8 has no F2-points, but geometric
    # singularities. Build its three conjugate linear factors, not an author list.
    K8=Extension(2,3);norm={(0,0,0):1}
    for j in range(3):
        linear={unit(3,i,1):K8.power(c,2**j) for i,c in enumerate((1,2,4))};out={}
        for e,a in norm.items():
            for f,b in linear.items():z=add_exp(e,f);out[z]=K8.add(out.get(z,0),K8.mul(a,b))
        norm={e:a for e,a in out.items() if a}
    need(all(a in (0,1) for a in norm.values()),'norm descends to F2')
    need(not any(evaluate(norm,x,2)==0 for x in projective(2,3)),'classical cubic norm is point-free')
    norm_singular=next(x for x in projective(8,3) if ext_singular(norm,x,K8))
    reject('norm_form_as_smooth_witness',lambda:need(not ext_singular(norm,norm_singular,K8),'norm is geometrically singular'))
    print(json.dumps({'status':'PASS','prefix_compositions':prefix_cases,'B_residue_compositions':residue_cases,
      'families':records,'family_count':len(records),'projective_points_examined':sum(x['projective_points_examined'] for x in records),
      'extension_checks':extension_checks,'extension_only_singular_witness':{'p':3,'degree':4,'point_F9':geometric_point},
      'forbidden_equal_prime_witnesses':equal_bad,'off_hypersurface_critical_point':{'p':5,'point':(2,3,2,1),'F_value':1},
      'binary_norm_geometric_roots':roots,'cubic_norm':[[list(e),c] for e,c in sorted(norm.items())],
      'cubic_norm_singular_point_F8':norm_singular,'negative_controls_rejected':rejected,
      'source_author_code_executed':False,'floating_point_used':False,
      'bounded_scans_not_geometric_smoothness_authority':True,'optimization_safe_guards':True},indent=2,sort_keys=True))


if __name__=='__main__':main()
