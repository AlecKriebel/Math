"""Independent exact rational checks of the explicit degree24 witness.

No source-author program is read/imported/executed. All guards are explicit
exceptions, including the adverse controls, and survive -O/-OO.
"""
from fractions import Fraction as F
from math import comb, factorial
from itertools import product
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
    ans=0
    for c in reversed(a):
        ans=ans*x+c
    return ans


def derivative(a):
    return [k*a[k] for k in range(1,len(a))]


def primitive(a,base=-1):
    b=[F(0)]+[F(c,k+1) for k,c in enumerate(a)]
    b[0]=-value(b,base)
    return b


def weighted(a):
    need(len(a)>=2 and all(c>0 for c in a), 'strictly positive coefficients, actual degree required')
    return [(k+1)*a[k]*a[k]-k*(a[k-1] if k else 0)*(a[k+1] if k+1<len(a) else 0)
            for k in range(len(a))]


def selected(a):
    cs=weighted(a)
    return [k for k,c in enumerate(cs) if c>0]


def changes(indices):
    need(all(a<b for a,b in zip(indices,indices[1:])), 'increasing selected index convention')
    return sum(a%2!=b%2 for a,b in zip(indices,indices[1:]))


def family(n):
    need(type(n) is int and n>=15,'primitive family starts at15')
    # Expand in the t=x+1 basis, not from the asserted x-coefficient formula.
    out=[0]*(n+1)
    for degree,c in [(n,38),(n-1,-11*n),(n-2,n*(n-1))]:
        for k in range(degree+1):
            out[k]+=c*comb(degree,k)
    return out


def quotient(a,k):
    need(0<k<len(a)-1,'interior quotient index')
    return F(a[k]*a[k],a[k-1]*a[k+1])


def closed_quotient(n,offset):
    constants={5:F(9,10),6:F(14,27),7:F(6,7)}
    return constants[offset]*F(n-offset+1,n-offset)


def validate_witness(D=10**6,js=tuple(range(1,23)),quad=(326,-188,38)):
    need(type(D) is int and D>0,'positive integer perturbation denominator')
    need(len(js)==22 and len(set(js))==22 and all(type(j)is int and j>0 for j in js),
         'twenty-two distinct positive root shifts')
    need(len(quad)==3 and quad[2]>0 and quad[1]**2-4*quad[0]*quad[2]<0,
         'quadratic must have two nonreal roots')
    a=list(quad)
    for j in js:
        a=mul(a,[D+j,D])
    cs=weighted(a)
    need(all(cs[k]<0 for k in (17,18,19)), 'three required weighted negative signs')
    need(changes([k for k,c in enumerate(cs) if c>0])<=20,'parity counterexample bound')
    return a,cs


def divide_linear(a,r):
    # Exact synthetic division by (x-r), descending recurrence.
    b=[0]*(len(a)-1)
    b[-1]=a[-1]
    for k in range(len(a)-2,0,-1):
        b[k-1]=a[k]+r*b[k]
    need(a[0]+r*b[0]==0,'synthetic division remainder')
    return b


def main():
    D=10**6
    q=[326,-188,38]
    p=mul(q,[choose(22,k) for k in range(23)])
    need(p==family(24),'factorized polynomial equals primitive family')
    need(p==[choose(24,k)*((k-18)**2+2) for k in range(25)],'compact coefficient identity')
    need(q[1]**2-4*q[0]*q[2]==-14208,'negative quadratic discriminant')
    need(value(q,-1)!=0,'repeated root has exactly multiplicity22')
    base=family(15)
    # Independently transcribed ascending rational seed coefficients from KSV.
    seed=[F(83,720720),F(1,728),F(17,2288),F(19,792),F(9,176),F(3,40),
          F(11,144),F(3,56),F(3,112),F(1,72),F(1,80),F(1,88),F(1,144),
          F(3,1144),F(9,16016),F(19,360360)]
    need(seed==[F(c,720720) for c in base],'printed seed coefficients')
    primitive_checks=0
    current=seed
    for n in range(15,65):
        pn=family(n)
        need(pn==[choose(n,k)*((n-k-6)**2+2) for k in range(n+1)],'general compact family formula')
        need(all(c>0 for c in pn),'primitive family coefficient positivity')
        need(n*(152-31*n)<0,'family quadratic discriminant')
        if n<=24:
            factor=F(factorial(15),720720*factorial(n))
            need(current==[factor*c for c in pn],'based primitive normalization')
            need(value(current,-1)==0,'based primitive value')
            if n<24:
                current=primitive(current)
            primitive_checks+=1
        if n>15:
            need(derivative(pn)==[n*c for c in family(n-1)],'derivative recurrence')
        for off in (5,6,7):
            need(quotient(pn,n-off)==closed_quotient(n,off),'corrected finite quotient formula')
    need([quotient(p,k) for k in (17,18,19)]==[F(108,119),F(133,243),F(18,19)],'degree24 ratios')
    seed_q=[quotient(base,k) for k in (10,9,8)]
    need(seed_q==[F(99,100),F(140,243),F(27,28)],'seed quotient values')
    # At degree22 the printed v1 endpoint would even cross the wrong side of
    # the weighted threshold. This is a source-correction control, not a claim
    # about a minimal counterexample degree.
    need(F(9,10)*F(23,22)<F(17,18)<quotient(family(22),17),
         'misindexed finite formula changes a weighted sign at degree22')
    # Telescoping checked against actual coefficient quotients for50degrees.
    product_checks=0
    for n in range(15,65):
        for start,off,sq in zip((10,9,8),(5,6,7),seed_q):
            result=sq
            for i in range(start,n-off):
                result*=F(i*(i+2),(i+1)**2)
            need(result==closed_quotient(n,off),'finite telescope endpoint')
            product_checks+=1
    # H bounds: verify its exact numerator, and its discriminant analytically
    # supplies positivity at all real k in the accompanying written proof.
    h=mul(q,[choose(21,k) for k in range(22)])
    need(19032**2-4*552*164956==-2005824,'H discriminant')
    for k in range(24):
        need(h[k]==F(choose(23,k)*(552*k*k-19032*k+164956),506)>0,'H compact formula')
    S=F(253,D)
    E=S+F(51)*S*S/(2*(1-S))
    need(E==F(169712147,666498000000)<F(1,2000),'uniform perturbation bound')
    need(1+F(376*144,552*2)<51,'uniform absolute coefficient bound')
    robust=[]
    for k in (17,18,19):
        lhs=F(2001,1999)**2*quotient(p,k)
        need(lhs<F(k,k+1),'robust weighted-sign margin')
        robust.append(str(F(k,k+1)-lhs))
    a,cs=validate_witness()
    need(len(a)==25 and a[-1]==38*D**22,'actual degree and leading coefficient')
    # A second coefficient expansion uses Newton sums, not factor convolution.
    rootsizes=[D+j for j in range(1,23)]
    e=[1]
    powers=[0]+[sum(b**i for b in rootsizes) for i in range(1,23)]
    for m in range(1,23):
        numerator=sum((-1)**(i-1)*e[m-i]*powers[i] for i in range(1,m+1))
        need(numerator % m ==0,'Newton exact divisibility')
        e.append(numerator//m)
    b=[D**k*e[22-k] for k in range(23)]
    alternative=[326*(b[k] if k<=22 else 0)-188*(b[k-1] if 1<=k<=23 else 0)
                 +38*(b[k-2] if 2<=k<=24 else 0) for k in range(25)]
    need(a==alternative,'two independent integer expansions')
    relative=[]
    for k in range(25):
        r=F(a[k],D**22)
        relative.append(abs(r-p[k])/p[k])
        need(relative[-1]<=E<F(1,2000),'actual uniform coefficient perturbation')
        hk=h[k] if k<24 else 0
        hprev=h[k-1] if k else 0
        need(p[k]==hk+hprev and 0<=hk<=p[k],'first-order coefficient bound')
        T=326*choose(22,k)+188*choose(22,k-1)+38*choose(22,k-2)
        need(F(T,p[k])==1+F(376*k*(24-k),552*((k-18)**2+2))<51,'Tk/ak identity')
    need([k for k,c in enumerate(cs) if c<0]==[17,18,19] and all(cs),'strict complete weighted signs')
    need(selected(a)==list(range(17))+list(range(20,25)),'complete selected indices')
    need(changes(selected(a))==changes(selected(p))==20,'exact parity count')
    # Verify subsequence variation inequality for every deletion of a binary
    # word through length8 (written proof gives the universal local argument).
    binary_controls=0
    for n in range(1,9):
        for bits in product((0,1),repeat=n):
            v=sum(x!=y for x,y in zip(bits,bits[1:]))
            for j in range(n):
                sub=bits[:j]+bits[j+1:]
                need(sum(x!=y for x,y in zip(sub,sub[1:]))<=v,'subsequence variation')
                binary_controls+=1
    # Complete factorization, exact real-root evaluations, derivative tests and
    # synthetic division. Q has no real roots by its negative discriminant.
    rational_roots=[-1-F(j,D) for j in range(1,23)]
    rem=a[:]
    for root in rational_roots:
        need(value(a,root)==0 and value(derivative(a),root)!=0,'simple rational root')
        rem=divide_linear(rem,root)
    need(rem==[D**22*c for c in q],'exact residual nonreal quadratic')
    need(cs[0]==a[0]**2 and cs[-1]==25*a[-1]**2,'endpoint extension')
    need(weighted([1,1,2])==[1,0,12] and selected([1,1,2])==[0,2],'zero is excluded')
    need(weighted([1,1,1])==[1,1,3],'weighting convention toy')
    need(weighted([1,2])==[1,8],'noncyclic coefficient endpoints toy')
    need(selected([7*x for x in a])==selected(a),'positive scaling invariance')
    # Each corruption changes a mathematical hypothesis/formula, with genuine
    # counter-controls for the otherwise invisible zero-selection convention.
    bad=[
        ('nonpositive_coefficient',lambda:weighted([1,0,1])),
        ('negative_scaling',lambda:weighted([-x for x in a])),
        ('zero_leading_coefficient',lambda:weighted(a+[0])),
        ('wrong_quadratic_constant',lambda:validate_witness(quad=(1,-188,38))),
        ('wrong_quadratic_middle_sign',lambda:validate_witness(quad=(326,188,38))),
        ('large_uncontrolled_perturbation',lambda:validate_witness(D=1)),
        ('repeated_root_shifts',lambda:validate_witness(js=(1,)*22)),
        ('missing_linear_factor',lambda:validate_witness(js=tuple(range(1,22)))),
        ('nonincreasing_selected_indices',lambda:changes([0,2,1])),
        ('zero_selected_as_positive',lambda:need(selected([1,1,2])==[0,1,2],'strict-selection change')),
        ('unweighted_replacement',lambda:need(weighted([1,1,1])==[1,0,1],'weighted statistic changed')),
        ('cyclic_coefficient_endpoint',lambda:need(weighted([1,2])==[1,7],'endpoint wrap is false')),
        ('wrong_primitive_basepoint',lambda:need(value(primitive(seed,0),-1)==0,'wrong primitive basepoint')),
        ('printed_endpoint_as_exact_formula',lambda:need(quotient(base,10)==F(9,10)*F(16,15),'misindexed finite factor')),
        ('wrong_H_discriminant_sign',lambda:need(19032**2-4*552*164956>0,'H discriminant sign')),
        ('repeated_root_witness_is_distinct',lambda:need(len({F(-1)})==22,'multiplicity is not distinctness')),
        ('tampered_constant_term',lambda:need(value([a[0]+1]+a[1:],rational_roots[0])==0,'factor identity broken')),
        ('too_small_error_budget',lambda:need(E<F(1,4000),'perturbation bound not that strong')),
    ]
    rejected=[]
    for name,fn in bad:
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    print(json.dumps({'status':'PASS','degree':24,'integer_coefficients':len(a),
        'strictly_positive_coefficients':all(c>0 for c in a),'negative_weighted_indices':[17,18,19],
        'zero_weighted_indices':[],'selected_indices':selected(a),'parity_changes':20,
        'distinct_simple_negative_real_roots':len(rational_roots),'real_roots_with_multiplicity':22,
        'quadratic_discriminant':-14208,'uniform_symbolic_error_bound':str(E),
        'maximum_actual_relative_error':str(max(relative)),
        'robust_ratio_margins':robust,'primitive_degrees_exactly_integrated':primitive_checks,
        'family_degrees_checked':[15,64],'corrected_quotient_products_checked':product_checks,
        'subsequence_binary_deletion_controls':binary_controls,'negative_controls_rejected':rejected,
        'optimization_safe_guards':True,'floating_point_used':False,'source_author_programs_executed':False},
        indent=2,sort_keys=True))


if __name__=='__main__':
    main()
