#!/usr/bin/env python3
"""Independent finite checks; asymptotic proofs are in INDEPENDENT_DERIVATION.md."""
from fractions import Fraction as F
from math import comb, factorial, gamma, log, pi, sqrt, exp
from pathlib import Path
import hashlib, json, datetime

ROOT=Path(__file__).resolve().parent

# Bernoulli recursion, independent of any submitted checker. All pi factors
# cancel in conditioned composition probabilities, leaving exact rational b_j.
def bernoulli(n):
    out=[F(1)]
    for m in range(1,n+1):
        out.append(-sum((F(comb(m+1,k))*out[k] for k in range(m)), F(0))/F(m+1))
    return out

MAX_EXACT=10
B=bernoulli(2*MAX_EXACT)
b=[F(0)]+[(-1)**(j+1)*F(2**(2*j-1))*B[2*j]/F(2*j*factorial(2*j)) for j in range(1,MAX_EXACT+1)]
h=[F(1)]
for n in range(1,MAX_EXACT+1):
    h.append(sum((F(j)*b[j]*h[n-j] for j in range(1,n+1)), F(0))/F(n))

def compositions(n):
    if n==0:
        yield ()
    else:
        for j in range(1,n+1):
            for tail in compositions(n-j):
                yield (j,)+tail

def countvec(parts):
    c=[0]*MAX_EXACT
    for j in parts: c[j-1]+=1
    return tuple(c)

def falling(c,r):
    if r>c:return 0
    return factorial(c)//factorial(c-r)

exact=[]
alltests=0
repeat_tests=0
for n in range(1,MAX_EXACT+1):
    # Enumerate the ordered composition law literally, including 1/k!.
    weights={}
    ordered=0
    for parts in compositions(n):
        w=F(1,factorial(len(parts)))
        for j in parts:w*=b[j]
        c=countvec(parts)
        weights[c]=weights.get(c,F(0))+w
        ordered+=1
    total=sum(weights.values(),F(0))
    assert total==h[n]
    selectors={countvec(())}
    for selected_size in range(1,n+1):
        selectors.update(countvec(p) for p in compositions(selected_size))
    local=0
    for r in selectors:
        direct=F(0)
        for c,w in weights.items():
            mult=1
            for cj,rj in zip(c,r): mult*=falling(cj,rj)
            direct+=w*mult
        size=sum((j+1)*rj for j,rj in enumerate(r))
        predicted=h[n-size]
        for j,rj in enumerate(r):predicted*=b[j+1]**rj
        assert direct==predicted,(n,r,direct,predicted)
        local+=1
        if max(r)>=2: repeat_tests+=1
    alltests+=local
    exact.append({'n':n,'ordered_compositions':ordered,'count_vectors':len(weights),'factorial_selectors_checked':local,'normalization_exact':True})

# Direct factorial cancellation, independently computing the D prefactor.
def D(g,k):
    return F(factorial(6*g-5-2*k)*2**(2*k),8*factorial(g-k)*factorial(3*g-3-k)*3**(g-k))
prefactor_tests=0
for g in range(2,51):
    for k in range(1,g):
        expected=F(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
        assert D(g,k+1)/D(g,k)==expected
        prefactor_tests+=1

# Plain-double diagnostic. Coefficients computed from H'=A'H, using
# zeta(2)=pi^2/6 and absolutely summable positive series for higher zeta.
N=4096
avec=[0.0]*(N+1)
avec[1]=pi*pi/12
for j in range(2,N+1):
    z=1.0
    for m in range(2,10001):
        term=m**(-2*j)
        z+=term
        # Integral remainder <= m^(1-2j)/(2j-1).
        if m**(1-2*j)/(2*j-1)<1e-16:break
    avec[j]=z/2
coeff=[1.0]+[0.0]*N
coeff_t=[1.0]+[0.0]*N
t=1.1
for n in range(1,N+1):
    coeff[n]=sum(avec[j]*coeff[n-j] for j in range(1,n+1))/n
    coeff_t[n]=t*sum(avec[j]*coeff_t[n-j] for j in range(1,n+1))/n
num=[]
for n in (16,64,256,1024,4096):
    h_asym=sqrt(2/pi)/sqrt(n)
    ht_asym=2**(t/2)*n**(t/2-1)/gamma(t/2)
    rs=sorted(set([0,int(log(log(n+3))),int(sqrt(n)),n//2,n]))
    num.append({'n':n,'h_over_asymptotic':coeff[n]/h_asym,'h_t_over_asymptotic':coeff_t[n]/ht_asym,'E_tK_over_n_beta':coeff_t[n]/coeff[n]/n**.05,'ratios':[{'r':r,'h_residual_over_h_n':coeff[n-r]/coeff[n],'sqrt_envelope':sqrt((n+1)/(n-r+1))} for r in rs]})

prefactor_asym=[]
for g in (100,1000,10000,100000,1000000):
    n=3*g-3
    cutoff=int(.6*log(2*n))
    acc=0.0
    maxerr=0.0
    for k in range(1,cutoff):
        ratio=12*(g-k)*(3*g-3-k)/((6*g-5-2*k)*(6*g-6-2*k))
        acc+=log(ratio)
        maxerr=max(maxerr,abs(exp(acc)-1))
    prefactor_asym.append({'g':g,'cutoff':cutoff,'max_relative_D_error':maxerr})

out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'fresh exact finite algebra and nonvalidated double diagnostics; neither proves asymptotics','exact_rational_assembly':exact,'total_factorial_selector_tests':alltests,'repeated_size_selector_tests':repeat_tests,'exact_prefactor_tests':prefactor_tests,'all_exact_checks_passed':True,'numerical_coefficients':num,'prefactor_diagnostics':prefactor_asym,'eta':.6*log(1.1)-.05,'eta_claimed_lower_bound':1/220,'low_k_bad_exponent':1-.6*log(2),'large_j_gamma_exponent':2*log(1.5)-.5,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(ROOT/'FRESH_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_exact_checks_passed':True,'selector_tests':alltests,'repeated_size_selectors':repeat_tests,'prefactor_tests':prefactor_tests,'eta':out['eta'],'coefficient_diagnostics':[{k:v for k,v in row.items() if k!='ratios'} for row in num]},indent=2))
