#!/usr/bin/env python3
"""New falsification controls; universal derivation is in REPORT.md.

No sibling checker is imported. Exact density integer moments test Wick
constraints, and pointwise densities independently use joint-law Pfaffians.
Decimal comparisons are diagnostics, never all-dimensional certificates.
"""
from fractions import Fraction as Q
from math import factorial, comb, isqrt
from decimal import Decimal as D, localcontext
from pathlib import Path
from collections import Counter
import json

counts = Counter()
def check(category, value):
    assert value, category
    counts[category] += 1

def hg(k):
    return Q(factorial(2*k), 4**k*factorial(k))

def lag(k):
    return [Q((-1)**j*comb(k,j), factorial(j)) for j in range(k+1)]

def poly_integral(r,s,p):
    return sum((a*b*factorial(i+j+p)
                for i,a in enumerate(lag(r)) for j,b in enumerate(lag(s))), Q(0))

def angular_sin(m):
    # integral_0^(pi/4) sin(theta)^(2m) dtheta = a+b*pi.
    a,b=Q(0),Q(1,4)
    for j in range(1,m+1):
        a=Q(2*j-1,2*j)*a-Q(1,2*j*2**j)
        b=Q(2*j-1,2*j)*b
    check('angular_gamma_coefficient',b==hg(m)/(4*factorial(m)))
    return a,b

def printed_integer_moment(n,k,wrong_sign=False):
    # Integral of the unnormalized real one-point density; integral mass n.
    eps=n%2
    c=sum((poly_integral(j,j,k) for j in range(n)),Q(0))
    j1=Q(0)
    for m in range((n+eps-2)//2+1):
        weight=2*hg(m)/factorial(m) if eps else 2*factorial(m)/hg(m+1)
        j1+=weight*poly_integral(n-1,2*m+1-eps,k)
    if eps:
        coeff=Q(factorial((n-1)//2),2)/hg((n-1)//2)
        j2=sum((a*2**(j+k+1)*hg(j+k)
                for j,a in enumerate(lag(n-1))),Q(0))
    else:
        coeff=hg(n//2)/(2*factorial(n//2-1))
        j2=sum((a*2**(j+k+3)*factorial(j+k)*angular_sin(j+k)[0]
                for j,a in enumerate(lag(n-1))),Q(0))
    correction=coeff*(j1-j2)
    return c+correction if wrong_sign else c-correction

integer_rows=[]
for n in range(1,17):
    got=[printed_integer_moment(n,k) for k in range(3)]
    expected=[n,n*n,n*n*(2*n+1)]
    check('joint_law_Wick_density_mass_trace_trace_square',got==expected)
    integer_rows.append({'N':n,'moments_orders_0_1_2':[str(x) for x in got]})

def invert(m):
    n=len(m)
    a=[row[:]+[Q(i==j) for j in range(n)] for i,row in enumerate(m)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j])
        a[k],a[j]=a[j],a[k]
        a[j]=[v/a[j][j] for v in a[j]]
        for k in range(n):
            if k!=j:
                scale=a[k][j]
                a[k]=[x-scale*y for x,y in zip(a[k],a[j])]
    inv=[row[n:] for row in a]
    check('Pfaffian_inverse_exact',all(sum((m[i][k]*inv[k][j] for k in range(n)),Q(0))==Q(i==j) for i in range(n) for j in range(n)))
    return inv

def skew_joint(n):
    # B coefficients derived from the independently integrated bivariate
    # arctangent generating function and its PDE; report proves all indices.
    size=n+n%2
    b=[[Q(0) for _ in range(size)] for _ in range(size)]
    for i in range(0,n,2):
        for j in range(i+1,n,2):
            value=-Q(4,i+1)
            for a in range(i//2+1,(j-1)//2+1):
                value*=Q(2*a,2*a+1)
            b[i][j]=value;b[j][i]=-value
    if n%2:
        for j in range(0,n,2):
            # Border rescaled by 1/sqrt(2*pi).
            b[j][n]=hg(j//2)/factorial(j//2)
            b[n][j]=-b[j][n]
    return b,invert(b)

def atan_inv(q,terms=90):
    a=sum((Q((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(terms)),Q(0))
    r=Q((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(a,a+r),max(a,a+r)

def qadd(a,b):return a[0]+b[0],a[1]+b[1]
def qsub(a,b):return a[0]-b[1],a[1]-b[0]
def qmul(a,b):
    values=[x*y for x in a for y in b]
    return min(values),max(values)
def qdiv(a,b):
    assert b[0]>0
    return qmul(a,(1/b[1],1/b[0]))
def qscale(a,b):return qmul(a,(b,b))
def qsqrt(a):
    scale=10**55
    def bound(q):
        k=isqrt(q.numerator*scale**2//q.denominator)
        return Q(k,scale),Q(k+1,scale)
    return bound(a[0])[0],bound(a[1])[1]

pi_interval=qsub(qscale(atan_inv(5),Q(16)),qscale(atan_inv(239),Q(4)))
check('rational_pi_enclosure',pi_interval[0]>Q(157,50) and pi_interval[1]<Q(22,7))
sqrt_pi=qsqrt(pi_interval)
sqrt2=qsqrt((Q(2),Q(2)))
inv_sqrt_pi=qdiv((Q(1),Q(1)),sqrt_pi)

def half_poly_integral(r,s):
    return sum((a*b*hg(i+j+1)
                for i,a in enumerate(lag(r)) for j,b in enumerate(lag(s))), Q(0))

def printed_half_moment(n):
    # Coordinates sqrt(pi), sqrt(2*pi), sqrt(2/pi).
    eps=n%2
    cx=sum((half_poly_integral(j,j) for j in range(n)),Q(0))
    finite=Q(0)
    for m in range((n+eps-2)//2+1):
        weight=2*hg(m)/factorial(m) if eps else 2*factorial(m)/hg(m+1)
        finite+=weight*half_poly_integral(n-1,2*m+1-eps)
    if eps:
        coeff=Q(factorial((n-1)//2),2)/hg((n-1)//2)
        border=sum((a*2**(j+1)*factorial(j) for j,a in enumerate(lag(n-1))),Q(0))
        return (cx-coeff*finite,Q(0),coeff*border)
    coeff=hg(n//2)/(2*factorial(n//2-1))
    a,b=Q(2),Q(-1)
    terms=[]
    for j in range(n):
        if j:a,b=2*j*a,2*j*b-hg(j)
        terms.append((2*a-2**(j+1)*factorial(j),2*b))
    aa=sum((c*terms[j][0] for j,c in enumerate(lag(n-1))),Q(0))
    bb=sum((c*terms[j][1] for j,c in enumerate(lag(n-1))),Q(0))
    return (cx-coeff*finite+2*coeff*bb,coeff*aa,Q(0))

small_exact={1:(Q(0),Q(0),Q(1)),2:(Q(2),Q(-1,2),Q(0)),
             3:(Q(3,2),Q(0),Q(2)),4:(Q(153,32),Q(-3,4),Q(0))}
for n,c in small_exact.items():
    check('exact_finite_density_half_moments_N1_to_N4',printed_half_moment(n)==c)

# N1 and N2 are derived directly from scalar and ordered singular-value
# polar joint laws, respectively; N3,N4 formulas checked against exact
# density integration in the report with independently reproduced intervals.
def raw_y_interval(n):
    a,b,c=printed_half_moment(n)
    return qadd(qadd(qscale(sqrt_pi,a),qscale(qmul(sqrt_pi,sqrt2),b)),
                qscale(qmul(sqrt2,inv_sqrt_pi),c))
def alpha_interval(n):
    return qdiv(raw_y_interval(n),qscale(qsqrt((Q(n),Q(n))),Q(n)))
small_reserves=[]
for n in range(1,4):
    inc=qsub(alpha_interval(n+1),alpha_interval(n))
    check('validated_N1_N2_N3_reserves',inc[0]>Q(1,160*n*n))
    small_reserves.append({'N':n,'increment_lower':str(inc[0]),'increment_upper':str(inc[1]),'reserve':str(Q(1,160*n*n))})

# New square-only universal coefficient comparison's two polynomial
# certificates. These values guard the reported algebra, not its quantifiers.
for t in range(0,100):
    n=t+2
    check('square_only_gamma_ratio_polynomial',
          (n+1)**3*(2*n-1)**2-n**3*(2*n+1)**2
          ==4*t**4+32*t**3+91*t*t+107*t+43)
    n=t+3
    check('first_diagonal_reserve_polynomial',
          4*n**3-4*n*n-13*n+4==4*t**3+32*t*t+71*t+37)
check('N1_all_diagonals_gamma_product_limit',3*Q(22,7)<8*Q(7,5))

# AP q1 repair: exact right/left Taylor coefficients, including all initial
# exceptions. No tested prefix supplies the universal induction in REPORT.
def binom(a,n):
    p=Q(1)
    for j in range(n):p*=a-j
    return p/factorial(n)
for j in range(101):
    lam=Q(128,3)*binom(Q(3,2),2*j+4)
    even=sum((Q(-1,2)**m/Q(2*j+1-m) for m in range(2*j+1)),Q(0))
    odd=sum((Q(-1,2)**m/Q(2*j+2-m) for m in range(2*j+2)),Q(0))
    check('AP_q1_repair_coefficient_comparison',even>=lam and odd>=0)
    check('AP_ratio_positive_polynomial',
          4*(2*j+5)*(2*j+6)*(j+1)-(4*j+5)*(4*j+7)*(j+2)
          ==24*j*j+77*j+50)

point_rows=[]
mutants=[]
with localcontext() as ctx:
    ctx.prec=85
    def dec(q):return D(q.numerator)/D(q.denominator) if isinstance(q,Q) else D(q)
    pi=dec((pi_interval[0]+pi_interval[1])/2)
    sp=pi.sqrt();s2=D(2).sqrt();sv=(2*pi).sqrt()
    def erf(z):
        total=D(0);term=z;k=0
        while True:
            added=term/D(2*k+1);total+=added
            k+=1;term*=-(z*z)/D(k)
            if abs(term/D(2*k+1))<D('1e-78') and k>z*z:break
            assert k<1000
        return 2*total/sp
    def polyval(a,x):
        value=D(0)
        for c in reversed(a):value=value*x+dec(c)
        return value
    def joint_density(n,x,inv,omit_border=False):
        w=(-x/2).exp()/x.sqrt()
        phi=[w*polyval(lag(j),x) for j in range(n+1)]
        psi=[sv*(1-2*erf((x/2).sqrt()))]
        if n:psi.append(-4*x*phi[0])
        for j in range(1,n):psi.append(D(j)*psi[j-1]/D(j+1)-4*x*phi[j]/D(j+1))
        raw=-sum((phi[i]*dec(inv[i][j])*psi[j] for i in range(n) for j in range(n)),D(0))
        if n%2 and not omit_border:
            raw+=sum((dec(inv[n][j])*phi[j]/sv for j in range(n)),D(0))
        return raw/D(n)
    def source_density(n,x,correction_sign=-1,force_even=False):
        eps=0 if force_even else n%2
        # force_even applies only to Phi2, isolating odd-border failure.
        actual_eps=n%2
        finite=D(0)
        for m in range((n+actual_eps-2)//2+1):
            weight=2*dec(hg(m))*sp/dec(factorial(m)) if actual_eps else 2*dec(factorial(m))/(dec(hg(m+1))*sp)
            finite+=weight*polyval(lag(2*m+1-actual_eps),x)
        phi1=(-x).exp()*finite
        phi2=(2/x).sqrt()*(-x/2).exp()*(D(1) if eps else 1-2*erf((x/2).sqrt()))
        if actual_eps:ratio=dec(factorial((n-1)//2))/(dec(hg((n-1)//2))*sp)
        else:ratio=dec(hg(n//2))*sp/dec(factorial(n//2-1))
        cx=(-x).exp()*sum((polyval(lag(j),x)**2 for j in range(n)),D(0))/D(n)
        return cx+D(correction_sign)*ratio*polyval(lag(n-1),x)*(phi1-phi2)/(2*D(n))
    for n in range(1,11):
        b,inv=skew_joint(n)
        for xstr in ['0.0001','0.1','0.5','1','2','4','8','16']:
            x=D(xstr)
            got=joint_density(n,x,inv);want=source_density(n,x)
            residual=abs(got-want)
            check('pointwise_joint_Pfaffian_vs_source_density',residual<D('1e-60')*(1+abs(got)))
            check('pointwise_density_nonnegative',got>0)
            point_rows.append({'N':n,'x':xstr,'density':str(got),'absolute_residual':str(residual)})
        x=D('0.1');expected=joint_density(n,x,inv)
        alternatives={
            'reverse_orthogonal_correction':source_density(n,x,correction_sign=1),
            'omit_normalized_density_divisor':D(n)*source_density(n,x),
            'wrong_real_variance_rescaling':2*source_density(n,2*x),
            'missing_real_rescaling_Jacobian':2*source_density(n,x),
        }
        if n==1:alternatives.pop('omit_normalized_density_divisor')
        if n%2:
            alternatives['omit_odd_augmented_border']=joint_density(n,x,inv,omit_border=True)
            alternatives['use_even_incomplete_gamma_at_odd_size']=source_density(n,x,force_even=True)
        for name,value in alternatives.items():
            rejected=abs(value-expected)>D('1e-12')*(1+abs(expected))
            check('negative_density_mutant_rejected',rejected)
            mutants.append({'N':n,'mutant':name,'absolute_difference':str(abs(value-expected)),'rejected':rejected})

result={
    'status':'passed',
    'scope':'NEW finite density/Wick/Pfaffian falsification controls, exact small-boundary intervals, square-only coefficient controls and AP boundary coefficient controls; universal claims require REPORT derivation',
    'counts':dict(counts),'total_assertions':sum(counts.values()),
    'integer_density_moments':integer_rows,
    'pointwise_density_diagnostics':point_rows,
    'decimal_diagnostic_precision':85,'decimal_scope':'finite high precision diagnostics, not claimed formal interval certificates',
    'negative_mutants':mutants,
    'validated_small_reserves':small_reserves,
    'exact_small_half_moment_coordinates':{str(n):[str(x) for x in printed_half_moment(n)] for n in small_exact},
    'exact_small_half_moment_basis':['sqrt(pi)','sqrt(2*pi)','sqrt(2/pi)'],
    'no_new_discovery':True,'no_new_substantive_proof_search_turn':True,
}
out=Path(__file__).resolve().with_name('CONTROL_RECEIPTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'counts':result['counts'],'total_assertions':result['total_assertions'],'mutants':len(mutants)},indent=2))
