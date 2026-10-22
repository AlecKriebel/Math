"""Independent audit controls for 3356; imports no author checker.

The million-bound scan uses an odd-index sieve and a separately written binary
modular exponent routine. It reconstructs the full canonical first-turn digest.
Finite field controls and congruence calculations supplement analytic review;
they do not prove the original universal statement or Chebotarev's theorem.
"""
from math import isqrt
from collections import Counter
import hashlib,json
checks=Counter()
def ck(ok,name):
    if not ok:raise AssertionError(name)
    checks[name]+=1

def modexp(a,n,m):
    result=1;a%=m
    while n>0:
        n,r=divmod(n,2)
        if r:result=(result*a)%m
        a=(a*a)%m
    return result

def euclid(a,b):
    while b:a,b=b,a%b
    return abs(a)

def odd_primes(n):
    flags=bytearray([1])*(n//2+1);flags[0]=0
    for p in range(3,isqrt(n)+1,2):
        if flags[p//2]:
            start=p*p//2
            for i in range(start,len(flags),p):flags[i]=0
    return [2]+[2*i+1 for i in range(1,len(flags)) if flags[i] and 2*i+1<=n]

def scan_million():
    rows=[];counts=Counter();positive=[]
    for q in odd_primes(1000000):
        if q<=3:continue
        p=16*q**4+1;N=p-1;f=modexp(3,N,p)
        if f!=1:row=[q,p,'fermat_composite',f]
        else:
            h=modexp(3,N//2,p);v=modexp(3,N//q,p)
            d2=euclid(h-1,p);dq=euclid(v-1,p)
            if d2==dq==1:
                row=[q,p,'lucas_prime_primitive',h,v];positive.append((q,p))
                ck(h==p-1,'quadratic_nonresidue_phase')
                phase=(-4*q*q)%p
                ck(modexp(3,4*q**4,p)==phase,'quartic_phase_on_certified_primes')
                ck(phase*phase%p==p-1,'gaussian_unit_embedding')
                short=modexp(3,4*q**3,p)
                ck((modexp(short,4,p)==1)==(short==modexp(phase,q%4,p)),'quartic_residual_equivalence')
            elif 1<d2<p:row=[q,p,'factor_composite',d2]
            elif 1<dq<p:row=[q,p,'factor_composite',dq]
            else:raise AssertionError(('unresolved',q,p))
        rows.append(row);counts[row[2]]+=1
    digest=hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
    ck(digest=='f3d31714d79c7d11d55522e037e0afb53b216d454bbdc07cb57945a5cf80393e','independent_first_turn_complete_digest')
    ck(len(rows)==78496 and len(positive)==7669,'independent_first_turn_exact_counts')
    for q,p in positive[:100]:
        N=p-1;c=next(v for v in range(1,16*q+1) if q*v%16==1 and v%q)
        h=modexp(3,q*c,p)
        ck(euclid(q*c,N)==q,'character_control_index_q')
        ck(modexp(h,N//q,p)==1,'character_control_is_not_primitive')
        ck(modexp(h,N//(q*q),p)!=1 and modexp(h,N//(2*q),p)!=1,'character_control_exact_order')
        for k in (2,4,8,16):ck(modexp(h,N//k,p)==modexp(3,N//k,p),'identical_all_two_primary_phases')
    return {'bound':1000000,'prime_q':len(rows),'counts':dict(counts),'digest':digest,'first':positive[0],'last':positive[-1]}

def valuations(n,p):
    v=0
    while n%p==0:v+=1;n//=p
    return v

def totient(n):
    answer=n;p=2
    while p*p<=n:
        if n%p==0:
            answer=answer//p*(p-1)
            while n%p==0:n//=p
        p+=1
    if n>1:answer=answer//n*(n-1)
    return answer

def affine_product(x,y,q):return (x[0]*y[0]%q,(x[0]*y[1]+x[1])%q)
def affine_inverse(x,q):
    a=pow(x[0],-1,q);return (a,(-a*x[1])%q)

def kummer_controls():
    for q in odd_primes(101):
        if q<=3:continue
        M=96*q**5;a=16*q**4+1
        ck(euclid(a,M)==1 and a%q==1,'compatible_cyclotomic_automorphism')
        ck(q*totient(M)==32*q**5*(q-1),'chebotarev_degree_denominator')
        for k in (0,1,2,17,101):
            n=a+M*k
            ck(n%12==5 and valuations(n-1,2)==4 and valuations(n-1,q)==4,'progression_exact_valuations')
        sigma=(2,0);tau=(1,1)
        comm=affine_product(affine_product(affine_product(sigma,tau,q),affine_inverse(sigma,q),q),affine_inverse(tau,q),q)
        ck(comm==tau,'affine_commutator_generates_translation')
        # Primary differences divided by 2+2i are Gaussian integers.
        u=v=-q*q
        ck((2*u-2*v,2*u+2*v)==(0,-4*q*q),'primary_associate_pi')
        real,imag=1,(-4*q*q)%3
        ck(((real*real-imag*imag)%3,(2*real*imag)%3)==(0,1),'F9_quartic_symbol_phase')

def field_controls():
    examples=0
    for p in odd_primes(251):
        for q in (3,5,7,11):
            if (p-1)%q:continue
            for a in range(1,p):
                beta=modexp(a,(p-1)//q,p)
                ck(modexp(beta,q,p)==1,'frobenius_coefficient_is_qth_root')
                roots=[x for x in range(p) if modexp(x,q,p)==a]
                ck(len(roots)==(q if beta==1 else 0),'split_root_count_dichotomy')
                eigen=[]
                for j in range(q):
                    exponent,degree=divmod(j*p,q)
                    direct=modexp(a,exponent,p)
                    ck(degree==j and direct==modexp(beta,j,p),'basis_frobenius_diagonalization')
                    eigen.append(direct)
                ck(sum(v==1 for v in eigen)==(q if beta==1 else 1),'fixed_subspace_dimension_dichotomy')
                ck(modexp(beta,q*(q-1)//2,p)==1,'frobenius_determinant_uninformative')
                disc=((-1)**(q*(q-1)//2)*modexp(q,q,p)*modexp(a,q-1,p))%p
                ck(disc!=0 and modexp(disc,(p-1)//2,p)==1,'binomial_discriminant_square')
                examples+=1
    return examples

def neighboring_certificate():
    p=16*5**42+1;N=p-1;D=N//5
    ck(modexp(6,N,p)==1,'neighbor_fermat')
    for r in (2,5):ck(euclid(modexp(6,N//r,p)-1,p)==1,'neighbor_full_lucas')
    ck(modexp(3,D,p)==1,'neighbor_order_divides_D')
    for r in (2,5):ck(modexp(3,D//r,p)!=1,'neighbor_order_is_exact_D')
    return {'q':5,'m':42,'prime_p':p,'order_3':D,'index':5}

if __name__=='__main__':
    scan=scan_million();kummer_controls();fields=field_controls();neighbor=neighboring_certificate()
    print(json.dumps({'status':'PASS_INDEPENDENT_SCOPED_CONTROLS','exact_assertions':sum(checks.values()),'counts':dict(sorted(checks.items())),'independent_scan':scan,'finite_field_cases':fields,'neighbor':neighbor,'scope':'Million-bound scan reconstructed independently; finite-field/phase/degree controls supplement the full analytic review. No finite scan proves the original universal assertion.'},indent=2,sort_keys=True))
