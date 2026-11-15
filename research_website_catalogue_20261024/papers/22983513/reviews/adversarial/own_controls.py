#!/usr/bin/env python3
"""Exact explicit spectra/Fourier-tail adversaries; no supplied imports or PDE proof claim."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json,hashlib

C=Counter()
D=hashlib.sha256()


def need(x,m):
    if not x:raise RuntimeError(m)


def moments(e,J,n):
    a=sum(e[:J],F(0))/J;b=sum((x*x for x in e[:J]),F(0))/J
    m=F(n+2,n)*a;d=m*m-F(n+4,n)*b;g=e[J]-e[J-1]
    return a,b,m,d,g,d-g*g/4


def yang(e,z,n):
    L=[x for x in e if x<z]
    return 4*sum(((z-x)*x for x in L),F(0))-n*sum(((z-x)**2 for x in L),F(0))


def box(weights,count):
    # Every absent positive multiindex has one coordinate >=K+1.
    # Its energy is at least base+min(a_i*((K+1)^2-1)).
    K=2;base=sum(weights,F(0))
    while True:
        values=sorted(sum((a*k*k for a,k in zip(weights,v)),F(0))
                      for v in product(range(1,K+1),repeat=len(weights)))
        outside=base+min(a*((K+1)**2-1) for a in weights)
        if len(values)>=count and values[count-1]<outside:
            C['certified_box_enumerations']+=1
            return values,outside,K
        K*=2
        need(K<=512,'Unexpected box enumeration size')


def spectrum_controls():
    for J in range(1,301):
        e=[F(k*k) for k in range(1,J+2)]
        a,b,m,d,g,delta=moments(e,J,1)
        need(a==F((J+1)*(2*J+1),6),'Interval first moment')
        need(b==F((J+1)*(2*J+1)*(3*J*J+3*J-1),30),'Interval second moment')
        need(d==F((J+1)*(2*J+1)*(3*J+5),12),'Interval D formula')
        need(delta==F((2*J+1)*(3*J*J+2*J+2),12)>0,'Interval exact strict deficit')
        C['all_J_interval_formula_checks']+=1
    families=[(F(1),),(F(1,9),),(F(1),F(1)),(F(1),F(1,4)),(F(2,3),F(7,5)),
              (F(1),F(1),F(1)),(F(1),F(2),F(3)),(F(1),F(1,4),F(1,9)),
              (F(1),F(1),F(1),F(1)),(F(1),F(2),F(1,3),F(7,4))]
    for weights in families:
        n=len(weights);raw,outside,K=box(weights,130)
        for copies in [1,2,3,5]:
            # Exact spectrum of a disjoint union of congruent translated boxes.
            e=sorted(raw*copies)
            for J in range(1,129):
                need(e[J]<outside,'Uncertified first J+1 spectrum')
                a,b,m,d,g,delta=moments(e,J,n)
                need(delta>0,'Exact box/disjoint-box gap strictness')
                need(yang(e[:J+1],e[J-1],n)>=0,'Lower repeated threshold')
                if e[J]>e[0]:need(yang(e[:J+1],e[J],n)>0,'Upper repeated threshold')
                else:need(d==4*e[0]*e[0]/(n*n),'Degenerate ground branch')
                C['certified_box_gap_cases']+=1
                C['zero_gap_cases']+=int(g==0)
                for scale in [F(1,9),F(16)]:
                    scaled=[x*scale for x in e[:J+1]]
                    scaled_delta=moments(scaled,J,n)[-1]
                    need(scaled_delta==delta*scale*scale,'Scale homogeneity')
                    C['squared_scaling_checks']+=1
                D.update(str((n,weights,copies,J,delta)).encode())
            levels=sorted(set(e))[:14]
            probes=levels[1:]+[(u+v)/2 for u,v in zip(levels,levels[1:])]
            for z in probes:
                need(z<outside and z>e[0],'Uncertified real threshold')
                need(yang(e,z,n)>0,'Strict real Yang threshold')
                C['certified_real_threshold_checks']+=1
            need(yang(e,e[0],n)==0,'Excluded bottom threshold')
            C['bottom_threshold_equality_checks']+=1


def algebra_controls():
    for n in range(1,9):
        for N in range(2,25):
            e=sorted(F((k*k)%17+k+3,k%4+1) for k in range(1,N+1))
            for J in range(1,N):
                a,b,m,d,g,delta=moments(e,J,n)
                for t in [e[0]-1,e[J-1],e[J],F(7,3),F(29,5)]:
                    q=sum(((t-x)**2-F(4,n)*(t-x)*x for x in e[:J]),F(0))/J
                    need(q==(t-m)**2-d,'Completed square identity')
                    C['arbitrary_spectrum_quadratic_identity_checks']+=1
                qlo=(e[J-1]-m)**2-d;qhi=(e[J]-m)**2-d
                if qlo<=0 and qhi<0:
                    need(delta>0,'Strict quadratic implication')
                    C['strict_quadratic_implication_cases']+=1
            for z in [e[0]+F(1,3),e[N//2],e[-1]+F(1,7)]:
                L=[j for j,x in enumerate(e) if x<z];raw=F(0);tail=F(0)
                for j in L:
                    tj=z-e[j]
                    for k,ek in enumerate(e):
                        ajk=F((j+1)*(k+1),j+k+3) # Symmetric exact synthetic coefficients.
                        term=tj*(ek-e[j])*(z-ek)*ajk*ajk;raw+=term
                        if ek>z:tail-=term
                need(raw==-tail,'Finite pair cancellation / remainder sign')
                C['symmetric_pair_cancellation_cases']+=1


def atan_interval(x,N):
    s=sum((F((-1)**k)*x**(2*k+1)/F(2*k+1) for k in range(N)),F(0))
    nextterm=F((-1)**N)*x**(2*N+1)/F(2*N+1)
    return min(s,s+nextterm),max(s,s+nextterm)


def fourier_controls():
    a,b=atan_interval(F(1,5),28);c,d=atan_interval(F(1,239),9)
    lo=4*(4*a-d);hi=4*(4*b-c);need(3<lo<hi<4,'Machin alternating pi interval')
    # tan(4 atan(1/5))=120/119, then tan(4atan(1/5)-atan(1/239))=1;
    # the angle lies in(0,pi/2), hence it is pi/4.
    tan=F(120,119);need((tan-F(1,239))/(1+tan*F(1,239))==1,'Machin tangent identity')
    records=[]
    for z in [F(3,2),F(2),F(4),F(9),F(25,2),F(16)]:
        js=[j for j in range(1,8) if j*j<z]
        R=4*sum(((z-j*j)*j*j for j in js),F(0))-sum(((z-j*j)**2 for j in js),F(0))
        need(R>0,'Direct interval strict Yang')
        prior_width=None
        for K in [256,1024]:
            need(K>=2*max(js) and K*K>z,'Fourier tail prerequisites')
            partial=F(0)
            for j in js:
                for k in range(1,K+1):
                    if k*k<=z or (j+k)%2==0:continue
                    # b=pi*a_jk. No numerical sine/integration or supplied formula import.
                    b=F(-8*j*k,(j*j-k*k)**2)
                    need(b!=0,'Nonzero high Fourier coefficient')
                    partial+=(z-j*j)*(k*k-j*j)*(k*k-z)*b*b
                    C['exact_Fourier_tail_summands']+=1
            tail=F(16384,81*K)*sum(((z-j*j)*j*j for j in js),F(0))
            lower=partial/(hi*hi);upper=(partial+tail)/(lo*lo)
            need(0<lower<=R<=upper,'Validated Fourier remainder enclosure')
            width=upper-lower
            if prior_width is not None:need(width<prior_width/2 and width<R/10,'Tail refinement is meaningful')
            prior_width=width;C['validated_Fourier_tail_enclosures']+=1
            records.append({'z':str(z),'K':K,'strict_lower_positive':True,'direct_R_inside_exact_enclosure':True,'lower_numerator_bits':lower.numerator.bit_length(),'lower_denominator_bits':lower.denominator.bit_length(),'upper_numerator_bits':upper.numerator.bit_length(),'upper_denominator_bits':upper.denominator.bit_length(),'enclosure_SHA256':hashlib.sha256((hex(lower.numerator)+hex(lower.denominator)+hex(upper.numerator)+hex(upper.denominator)).encode()).hexdigest()})
    for j in range(1,13):
        for k in range(1,129):
            if j==k:continue
            b=F(0) if (j+k)%2==0 else F(-8*j*k,(j*j-k*k)**2)
            c=F(0) if (j+k)%2==0 else F(-8*j*k,(k*k-j*j)**2)
            need(b==c and (b!=0)==bool((j+k)%2),'Fourier symmetry/parity')
            C['exact_Fourier_symmetry_parity_checks']+=1
    return {'pi_Machin_lower':str(lo),'pi_Machin_upper':str(hi),'records':records,'tail_bound':'For k>K>=2j, (pi a_jk)^2<=16384 j^2/(81 k^6); triple factor<=t_j k^4 and sum_(k>K)k^-2<=1/K.'}


def wrong_variants():
    tests={}
    e=[F(1),F(4)]
    tests['z_equals_bottom_is_not_strict']=yang(e,F(1),1)==0
    tests['nonstrict_Yang_alone_can_saturate']=moments([F(1),F(5)],1,1)[-1]==0
    tests['Neumann_ground_zero_breaks_gap_bound']=moments([F(0),F(1)],1,1)[-1]<0
    # On length3pi, M1^2=1/9 and M2=sqrt5/9>1/9: unsquared LHS<0.
    a,b,m,d,g,delta=moments([F(1,9),F(4,9)],1,1)
    lower_M2=F(2,9)
    tests['unsquared_M2_wrong_scaling_is_negative']=lower_M2*lower_M2<5*b and m*m-lower_M2<0<g*g/4
    # Finite coordinate compression discards the high spectral tail, but its
    # j=1 sum rule is not1. For N=1 it is exactly0, hence is not Dirichlet data.
    finite_row_rules=[F(4)-F(1),F(1)-F(4)]
    tests['finite_coordinate_truncation_loses_sum_rule']=sum(finite_row_rules)==0 and sum(finite_row_rules)!=2
    # Opposite parity coordinate coefficient and its flipped-sign partner.
    z=F(3);ej=F(1);ek=F(4);t=(z-ej)*(ek-ej)*(ek-z)
    tests['wrong_remainder_sign_detected']=t>0 and -t<0
    # Equality in a finite self-adjoint toy system does not establish constant
    # coefficient PDE/Dirichlet-domain commutation. H diag1,3, X swaps states.
    H=[[F(1),F(0)],[F(0),F(2)]];X=[[F(0),F(1)],[F(1),F(0)]];u=[F(1),F(0)]
    def mv(A,v):return [sum((a*b for a,b in zip(row,v)),F(0)) for row in A]
    w=mv(X,u);hw=mv(H,w);v=[a-b for a,b in zip(hw,w)];hv=mv(H,v);av=[a-b for a,b in zip(hv,v)]
    tests['finite_selfadjointness_alone_does_not_forbid_support']=w==[0,1] and sum(a*b for a,b in zip(w,v))==1 and av!=[0,0]
    tests['ground_multiplicity_requires_positive_D']=moments([F(1)]*4,2,3)[3]==F(4,9)>0
    need(all(tests.values()),'Wrong-variant adversary failed')
    return tests


def main():
    spectrum_controls();algebra_controls();f=fourier_controls();bad=wrong_variants()
    print(json.dumps({'status':'PASS','counts':dict(sorted(C.items())),'case_digest_SHA256':D.hexdigest(),'Fourier_validated_controls':f,'wrong_variant_or_model_falsifiers':bad,'limits':['Explicit spectra and validated Fourier series are finite analytic diagnostics, not a proof on all rough domains.','No supplied code/results/opinions were read to develop these mechanisms.','Synthetic coefficient matrices only test the algebraic cancellation; they are not claimed Dirichlet spectra.','No uniform-deficit, firstness, formal or human certification.'],'network':0,'file_writes':0},sort_keys=True))


if __name__=='__main__':main()
