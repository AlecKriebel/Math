"""Independent exact integer and rational-interval diagnostics, not all-n proof.

No supplied programme/result is imported. All asserted certificates use integers
or Fraction intervals; no binary floating point decides a scientific inequality.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt,gcd
from functools import lru_cache
import json,sys
F=[0,1]
for n in range(2,121):F.append(F[-1]+F[-2])
counts={};boundaries={}
def check(name,ok):
    counts[name]=counts.get(name,0)+1
    if not ok:raise ValueError(name)
def atan_bounds(x):
    # Twelve alternating terms end negative; the next positive term bounds tail.
    s=sum(((-1)**k*x**(2*k+1)/Q(2*k+1) for k in range(12)),Q())
    return s,s+x**25/Q(25)
a,b=atan_bounds(Q(1,5));c,d=atan_bounds(Q(1,239));PI_LO=16*a-4*d;PI_HI=16*b-4*c
t=Q(1,5);t2=2*t/(1-t*t);t4=2*t2/(1-t2*t2)
check('Machin_tangent_identity',(t4-Q(1,239))/(1+t4*Q(1,239))==1)
check('rational_pi_interval_nonempty',3<PI_LO<PI_HI<Q(22,7))
def cos_poly(x,N):
    s=term=Q(1)
    for k in range(1,N+1):term=-term*x*x/Q((2*k-1)*(2*k));s+=term
    return s
@lru_cache(None)
def cos_bounds(q,r):
    r=abs(r)
    if 2*r==q:return Q(-1),Q(-1)
    if 4*r==q:return Q(),Q()
    if r==0:return Q(1),Q(1)
    lo=2*PI_LO*r/q;hi=2*PI_HI*r/q
    check('cos_argument_inside_decreasing_halfcircle',0<lo<hi<PI_LO)
    # Cosine decreases on[0,pi]; odd/even alternating sums bound the value.
    return max(Q(-1),cos_poly(hi,13)),min(Q(1),cos_poly(lo,14))
def sqrt_bounds(x):
    B=10**18;k=isqrt(x.numerator*B*B//x.denominator);lo=Q(k,B);hi=lo if lo*lo==x else Q(k+1,B)
    check('rational_sqrt_enclosure',lo*lo<=x<=hi*hi)
    return lo,hi
def squared_chord_interval(q,p,i,j):
    a=Q(i,q);b=Q(j,q);U=2*(a+b-2*a*b);lo,hi=sqrt_bounds(a*(1-a)*b*(1-b));lo*=4;hi*=4
    r=((j-i)*p)%q
    if 2*r>q:r-=q
    cl,ch=cos_bounds(q,r);products=[cl*lo,cl*hi,ch*lo,ch*hi]
    return 2*(U-max(products)),2*(U-min(products))

arith=[];terminal=quarter=tie=0
for n in range(3,19):
    q,p=F[n],F[n-1];minimum=None;minimizers=[]
    check('consecutive_Fibonacci_coprime',gcd(q,p)==1)
    for m in range(1,q):
        j=2
        while F[j+1]<=m:j+=1
        h=n-j;det=F[j]*F[j]-F[j-1]*F[j+1]
        check('unimodular_det',det==(-1)**(j-1))
        check('addition_identity',q==F[j]*F[h+1]+F[j-1]*F[h])
        check('stronger_index_comparison',F[n-2]==F[j-1]*F[h]+F[j-2]*F[h-1] and F[j]*F[h]>=F[n-2])
        r=(m*p)%q
        if 2*r>q:r-=q
        ell=(m*p-r)//q
        product=m*abs(r)
        if minimum is None or product<minimum:minimum=product;minimizers=[m]
        elif product==minimum:minimizers.append(m)
        terminal+=h==1;quarter+=4*abs(r)==q;tie+=2*abs(r)==q
        for shift in [-1000000,-2,0,1,1000000]:
            L=ell+shift;res=m*p-L*q;S=(F[j]*m-F[j+1]*L)//det;T=(F[j]*L-F[j-1]*m)//det
            check('exact_basis_coordinates',m==S*F[j]+T*F[j+1] and L==S*F[j-1]+T*F[j])
            check('complete_basis_sign_cases',S!=0 and ((T==0 and S>0) or S*T<0))
            check('opposed_error_identity',res==(-1)**(j-1)*(S*F[h]-T*F[h-1]))
            check('universal_lemma_instance',abs(res)>=F[h] and m*abs(res)>=F[n-2] and 3*m*abs(res)>=q)
    check('exact_finite_product_index',minimum==F[n-2])
    arith.append({'n':n,'q':q,'minimum_m_abs_residue':minimum,'expected_classical_index':F[n-2],'minimizing_m':minimizers})
check('terminal_h1_covered',terminal>0);check('quarter_residue_covered',quarter>0);check('half_residue_tie_covered',tie>0)

for n in range(3,121):
    q,p=F[n],F[n-1]
    check('parity_inverse_convention',(p*p-(-1)**n)%q==0)
    for j in range(2,n):
        h=n-j
        check('all_index_error_identities',p*F[j]-q*F[j-1]==(-1)**(j-1)*F[h] and p*F[j+1]-q*F[j]==(-1)**j*F[h-1])
for A in range(13):
    for B in range(A+1,13):
        a,b=Q(A,12),Q(B,12);delta=b-a;U=2*(a+b-2*a*b);V2=16*a*(1-a)*b*(1-b)
        check('latitude_Gram_identity',U*U-V2==4*delta*delta and U-2*delta==4*a*(1-b)>=0)
        for c in [Q(-1),Q(-2,3),Q(),Q(1,5),Q(3,5),Q(9,10)]:
            check('squared_geometric_certificate',U*U+c*c*V2-4*delta*delta*(1-c*c)==V2+c*c*U*U)
check('continuous_positive_case_equality',2*(Q(5,4)-Q(3,5)*Q(3,4))==4*Q(1,2)*Q(4,5)==Q(8,5))

chords=[]
for n in range(3,12):
    q,p=F[n],F[n-1];witnesses=[];margin=None;certpairs=0
    for i in range(q):
        for j in range(i+1,q):
            lo,hi=squared_chord_interval(q,p,i,j);target=Q(4,q);certpairs+=1
            if (i,j)==(0,1):
                check('direct_interval_pole_witness',lo==hi==target);witnesses.append([i,j])
            else:
                check('direct_interval_nonwitness_strict',lo>target)
                margin=(lo-target) if margin is None else min(margin,lo-target)
            m=j-i;r=(m*p)%q
            if 2*r>q:r-=q
            if 4*abs(r)>=q:
                rational_lower=Q(4*m,q)+Q(8*i*(q-j),q*q)
                check('nonpositive_branch_exact_certificate',rational_lower>=target and ((i,j)==(0,1) or rational_lower>target))
            else:check('positive_branch_exact_certificate',Q(16*m*abs(r),q*q)>=Q(16,3*q)>target)
    chords.append({'n':n,'q':q,'certified_all_pairs':certpairs,'unique_exact_witnesses':witnesses,'minimum_certified_nonwitness_margin':None if margin is None else str(margin)})

# Exact excluded-convention controls, not counterexamples to the written claim.
lo,hi=squared_chord_interval(16,1,7,8)
check('arbitrary_coprime_step_counterexample',hi<Q(1,4))
check('q16_algebraic_counterexample_certificate',Q(2)>Q(100,81))
check('midpoint_q2_counterexample',2*(Q(5,4)+Q(3,4))==4 and 4!=Q(4,2))
north=squared_chord_interval(5,3,0,1);south=squared_chord_interval(5,3,4,5)
check('both_endpoints_second_pole_witness',north==south==(Q(4,5),Q(4,5)))
check('odd_reversed_order_needs_reflection',(3*3)%5!=1 and (-3*3)%5==1)
check('n2_singleton_is_excluded',F[2]==1)
result={'status':'PASS','arithmetic':'Integer/Fraction arithmetic only for every decision; cosine via Machin pi and alternating rational Taylor bounds, square roots via exact integer-square enclosures.','finite_diagnostics_are_universal_proof':False,'universal_proof_artifact':'EARLY_RECONSTRUCTION.md','checks_total':sum(counts.values()),'checks_by_name':counts,'arithmetic_all_m_n_range':[3,18],'arithmetic_records':arith,'identity_index_n_range':[3,120],'direct_interval_allpairs_n_range':[3,11],'chord_records':chords,'terminal_h1_instances':terminal,'quarter_residue_instances':quarter,'half_residue_ties':tie,'rational_pi_interval':[str(PI_LO),str(PI_HI)],'q16_excluded_counterexample_interval':[str(lo),str(hi)],'source_code_results_imported':False,'floating_point_decisions':False}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','checks_total','arithmetic_all_m_n_range','identity_index_n_range','direct_interval_allpairs_n_range','terminal_h1_instances','quarter_residue_instances','half_residue_ties']},indent=2))
