"""Fresh exact checks for PR1277, distinct from the weighted statistic.

Standard library only. No source-author code or historical checker is used.
Explicit exceptions remain active under normal/-O/-OO Python.
"""
from fractions import Fraction as F
from math import comb
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def choose(n,k):
    return comb(n,k) if 0<=k<=n else 0


def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return c


def value(a,x):
    out=0
    for c in reversed(a):
        out=out*x+c
    return out


def derivative(a):
    return [k*a[k] for k in range(1,len(a))]


def unweighted(a):
    need(len(a)>1 and all(c>0 for c in a),'positive actual-degree polynomial')
    return [a[k]**2-(a[k-1] if k else 0)*(a[k+1] if k+1<len(a) else 0)
            for k in range(len(a))]


def selection(a):
    return [k for k,c in enumerate(unweighted(a)) if c>=0]


def variations(ids):
    need(all(i<j for i,j in zip(ids,ids[1:])),'increasing index sequence')
    return sum(i%2!=j%2 for i,j in zip(ids,ids[1:]))


def quotient(a,k):
    return F(a[k]**2,a[k-1]*a[k+1])


def synthetic(a,r):
    b=[0]*(len(a)-1);b[-1]=a[-1]
    for k in range(len(a)-2,0,-1):
        b[k-1]=a[k]+r*b[k]
    need(a[0]+r*b[0]==0,'nonzero synthetic remainder')
    return b


def witness(D=10**7,shifts=tuple(range(1,14)),quad=(83,-89,38)):
    need(type(D)is int and D>0,'positive integer D')
    need(len(shifts)==13 and len(set(shifts))==13 and all(j>0 for j in shifts),
         'thirteen distinct positive root shifts')
    need(quad[1]**2-4*quad[0]*quad[2]<0,'quadratic must be nonreal')
    a=list(quad)
    for j in shifts:
        a=mul(a,[D+j,D])
    c=unweighted(a)
    need(all(c[k]<0 for k in (8,9,10)),'three strict unweighted exclusions')
    need(variations(selection(a))<=11,'unweighted parity bound')
    return a,c


def main():
    Q=[83,-89,38]
    a=mul(Q,[choose(13,k) for k in range(14)])
    need(a==[choose(15,k)*((k-9)**2+2) for k in range(16)],'compact seed formula')
    need(Q[1]**2-4*Q[0]*Q[2]==-4695,'seed discriminant')
    need(value(Q,-1)==210,'exact repeated multiplicity')
    qs=[quotient(a,k) for k in (8,9,10)]
    need(qs==[F(27,28),F(140,243),F(99,100)] and all(0<q<1 for q in qs),'positive seed ratios below one')
    for k in range(1,15):
        t=k-9;N=14*t**4-6*t**3+177*t*t+15*t-206
        den=k*(15-k)*(t**4+2*t*t+9)
        need(quotient(a,k)-1==F(N,den),'table-free quartic identity')
        need((N<0)==(k in (8,9,10)) and N!=0,'quartic strict signs')
        if abs(t)>=2:
            u=abs(t)
            need(t*t*(14*t*t-6*t)>0,'positive leading part')
            need(177*t*t+15*t-206>=F(339,2)*u*u-206>=472,'uniform quartic lower bound')
    need(selection(a)==list(range(8))+list(range(11,16)),'complete seed indices')
    need(variations(selection(a))==11,'seed parity count')
    outputs=[]
    for D in (10**6,10**7):
        r,c=witness(D)
        need(len(r)==16 and r[-1]==38*D**13,'degree15 and leading coefficient')
        need([k for k,x in enumerate(c) if x<0]==[8,9,10] and all(c),'complete strict sign pattern')
        need(variations(selection(r))==11,'exact perturbed parity')
        roots=[-1-F(j,D) for j in range(1,14)]
        rem=r[:]
        for root in roots:
            need(value(r,root)==0 and value(derivative(r),root)!=0,'simple rational root')
            rem=synthetic(rem,root)
        need(rem==[D**13*x for x in Q],'residual nonreal quadratic')
        errors=[abs(F(r[k],D**13)-a[k])/a[k] for k in range(16)]
        outputs.append({'D':D,'degree':15,'strict_positive_coefficients':True,
                        'distinct_simple_negative_roots':13,'real_roots_with_multiplicity':13,
                        'negative_unweighted_indices':[8,9,10],'zero_unweighted_indices':[],
                        'parity_changes':11,'max_actual_relative_error':str(max(errors)),
                        'role':'exact supplemental frozen witness' if D==10**6 else 'symbolically bounded main witness'})
        if D==10**7:
            E=F(D+13,D)**13-1
            bound=F(169,D-169)
            need(E<=bound<F(1,50000),'finite-product perturbation bound')
            need(169*50000<D-169,'integer E comparison')
            need(F(83,2)*E<F(83,100000)<F(1,1000),'coefficient relative bound')
            for k in range(16):
                B=choose(13,k);b=1
                # Independently build the linear product to test its elementary
                # symmetric coefficient estimate, without using the quadratic.
                linears=[1]
                for j in range(1,14):
                    linears=mul(linears,[F(D+j,D),1])
                lk=linears[k] if k<=13 else 0
                need(0<=lk-B<=E*B,'linear-product coefficient error')
                s=83*choose(13,k)+89*choose(13,k-1)+38*choose(13,k-2)
                need(F(s,choose(15,k))==F(32*k*k-1110*k+17430,210)<=83,
                     'absolute convolution bound')
                need(errors[k]<=F(83,2)*E<F(1,1000),'actual coefficient error within proof bound')
            need(F(99,100)*F(1001,999)**2<1,'strict ratio stability')
            need(99*1001**2==99198099<99800100==100*999**2,'integer ratio comparison')
    # A zero term must be retained here, in contrast to weighted Conj9.
    need(unweighted([1,1,1])==[1,0,1] and selection([1,1,1])==[0,1,2],
         'zero differences selected under Conj10')
    need(unweighted([1,2])==[1,4],'zero-extended endpoints')
    bad=[
        ('zero_coefficient',lambda:unweighted([1,0,1])),
        ('zero_leading_term',lambda:unweighted(a+[0])),
        ('negative_scale',lambda:unweighted([-x for x in a])),
        ('strict_only_selection',lambda:need(selection([1,1,1])==[0,2],'zero wrongly excluded')),
        ('weighted_expression',lambda:need(unweighted([1,1,1])==[1,1,3],'weighted substitute')),
        ('cyclic_endpoint',lambda:need(unweighted([1,2])==[1,3],'coefficient wrap')),
        ('wrong_middle_sign',lambda:witness(quad=(83,89,38))),
        ('real_quadratic',lambda:witness(quad=(1,-89,38))),
        ('repeated_shifts',lambda:witness(shifts=(1,)*13)),
        ('missing_factor',lambda:witness(shifts=tuple(range(1,13)))),
        ('large_perturbation',lambda:witness(D=1)),
        ('negative_ratios_claim',lambda:need(all(q<0 for q in qs),'ratios are positive')),
        ('multiplicity_as_distinct',lambda:need(len({F(-1)})==13,'repeated seed is not distinct')),
        ('reordered_indices',lambda:variations([0,2,1])),
        ('tampered_seed_constant',lambda:need(value([a[0]+1]+a[1:],-1)==0,'seed factor identity')),
        ('wrong_quartic_constant',lambda:need(14*(-1)**4-6*(-1)**3+177*(-1)**2+15*(-1)-205==-24,'quartic constant changed')),
    ]
    rejected=[]
    for name,fn in bad:
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    print(json.dumps({'status':'PASS','seed_degree':15,'seed_real_roots_multiplicity':13,
        'seed_distinct_real_roots':1,'seed_parity_count':11,'seed_negative_unweighted_indices':[8,9,10],
        'seed_ratios':[str(q) for q in qs],'quadratic_discriminant':-4695,'perturbations':outputs,
        'nonnegative_selection_includes_zero':True,'negative_controls_rejected':rejected,
        'optimization_safe_guards':True,'source_author_programs_executed':False,'floating_point_used':False},
        indent=2,sort_keys=True))


if __name__=='__main__':
    main()
