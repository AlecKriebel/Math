"""Independent exact controls using integer partitions and the full zeta model.

The coefficient of pi^(2j) in zeta(2j)/(2j) is rational. Thus all
fixed-total-size assembly probabilities can be checked exactly, without a
height truncation. Bernoulli numbers and reciprocal-square-root power series
are computed independently. No downloaded programs are executed.
"""
from fractions import Fraction as F
from math import comb, factorial, prod
from collections import Counter
import json
C=Counter()
def check(ok,name):
    assert ok,name
    C[name]+=1

def bernoulli(n):
    A=[]
    for m in range(n+1):
        A.append(F(1,m+1))
        for j in range(m,0,-1): A[j-1]=j*(A[j-1]-A[j])
    return A[0]

N=14
# Strip the common pi^(2n) factor from every composition of n.
a=[F(0)]+[abs(bernoulli(2*j))*F(2**(2*j-2),j*factorial(2*j)) for j in range(1,N+1)]
check(a[1]==F(1,12),'true_zeta_weights')
check(a[2]==F(1,360),'true_zeta_weights')
check(a[3]==F(1,5670),'true_zeta_weights')
# H(z)^2 * sin(sqrt(z))/sqrt(z) = 1 after stripping pi powers.
sine=[F((-1)**k,factorial(2*k+1)) for k in range(N+1)]
h=[F(1)]
for n in range(1,N+1):
    # Coefficient n with h_n set to zero consists only of known h_0,...,h_(n-1).
    known=sum((h[i]*h[j]*sine[n-i-j] for i in range(n) for j in range(n) if i+j<=n),F(0))
    h.append(-known/2)
    check(n*h[n]==sum((j*a[j]*h[n-j] for j in range(1,n+1)),F(0)),'sine_vs_exponential_coefficients')

def partitions(n,lo=1):
    if n==0: yield ()
    for j in range(lo,n+1):
        for tail in partitions(n-j,j): yield (j,)+tail

def falling(c,k): return prod(range(c-k+1,c+1)) if c>=k else 0

def beta_cdf(A,B,x):
    # Integer-shape Beta CDF as a binomial tail, exact at rational x.
    if B==0: return F(int(x>=1))
    M=A+B-1
    return sum((comb(M,l)*x**l*(1-x)**(M-l) for l in range(A,M+1)),F(0))

for n in range(1,N+1):
    rows=[]
    for part in partitions(n):
        cnt=Counter(part)
        w=prod(a[j]**m/F(factorial(m)) for j,m in cnt.items())/h[n]
        rows.append((part,cnt,w))
        # Dirichlet diagonal and cross second moments add to (sum X_i)^2=1.
        shape=[2*j for j in part];total=2*n
        diagonal=sum(F(v*(v+1),total*(total+1)) for v in shape)
        cross=sum(F(2*shape[i]*shape[k],total*(total+1)) for i in range(len(shape)) for k in range(i+1,len(shape)))
        check(diagonal+cross==1,'Dirichlet_second_moment_normalization')
    check(sum((w for _,_,w in rows),F(0))==1,'partition_normalization')
    # All ordered triples of labels, including coincident lengths.
    for labels in [(j,) for j in range(1,n+1)]+[(j,k) for j in range(1,n+1) for k in range(1,n+1)]+[(j,j,j) for j in range(1,n+1)]:
        needs=Counter(labels);s=sum(labels)
        actual=sum((w*prod(falling(cnt[j],m) for j,m in needs.items()) for _,cnt,w in rows),F(0))
        expect=prod(a[j]**m for j,m in needs.items())*h[n-s]/h[n] if s<=n else F(0)
        check(actual==expect,'true_zeta_joint_factorial_moments')
    for left,right in [(F(1,4),F(1,2)),(F(1,8),F(3,4))]:
        probs={j:beta_cdf(2*j,2*n-2*j,right)-beta_cdf(2*j,2*n-2*j,left) for j in range(1,n+1)}
        enum=sum((w*sum(probs[j] for j in part) for part,_,w in rows),F(0))
        formula=sum((a[j]*h[n-j]/h[n]*probs[j] for j in range(1,n+1)),F(0))
        check(enum==formula,'exact_normalized_area_window_mean')
        check(0<=enum<=n,'window_mean_bounds')

# Exact graph prefactor comparison, including the k=1 power of two.
def A(g,k):
    return F(factorial(6*g-5-2*k),factorial(g-k)*factorial(3*g-3-k)*3**(g-k))*F(2)**(3*k-3)
for g in range(3,36):
    for k in range(1,min(g-1,8)):
        raw=(A(g,k+1)/F(2)**(k+1))/(A(g,k)/F(2)**k)
        ratio=F(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
        check(raw==ratio,'prefactor_from_source_A')
# Rational witnesses for the strict signs in the analytic tail estimates.
check(F(3,5)*F(1,11)-F(1,20)==F(1,220),'positive_exception_exponent')
check(sum((F(7,10)**k/F(factorial(k)) for k in range(5)),F(0))>2,'log2_less_than_7_over_10')
check(2*F(1,3)-F(1,2)==F(1,6),'large_Gamma_tail_exponent')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())), 'scope':'Independent finite exact controls; asymptotic limits and geometric input are audited in the written review. Full infinite-height zeta weights are handled by cancelling their common pi power at each total size.'},indent=2,sort_keys=True))
