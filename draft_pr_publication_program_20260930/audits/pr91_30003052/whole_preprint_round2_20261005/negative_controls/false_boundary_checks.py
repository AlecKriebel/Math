#!/usr/bin/env python3
"""Independent stdlib-only bounded adversarial controls; never a Koopman spectrum approximation."""
import argparse, cmath, collections, fractions, hashlib, itertools, json, math, pathlib
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=pathlib.Path)
parser.add_argument("--details-output", type=pathlib.Path)
args = parser.parse_args()
F=fractions.Fraction
counts=collections.Counter(); events=[]; numerical=[]; cases=[]
def ck(kind,condition,detail=None):
    if not bool(condition):
        raise RuntimeError('%s: %r'%(kind,detail))
    counts[kind]+=1
    events.append({'kind':kind,'result':True,'detail':detail})
ck("round2_deliberately_false", False)
def M(rows): return [[F(x) for x in row] for row in rows]
def eye(n): return M([[int(i==j) for j in range(n)] for i in range(n)])
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def inv(a):
    n=len(a); aug=[row[:]+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[pivot]=aug[pivot],aug[j]
        q=aug[j][j]; aug[j]=[x/q for x in aug[j]]
        for i in range(n):
            if i!=j:
                q=aug[i][j]; aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]
def power(a,n):
    out=eye(len(a))
    for _ in range(n): out=mul(out,a)
    return out
def infnorm(a):return max(sum(abs(x) for x in row) for row in a)
def l1norm(a):return max(sum(abs(a[i][j]) for i in range(len(a))) for j in range(len(a)))
def vecinf(v):return max(map(abs,v))
def dot(a,v):return sum(x*y for x,y in zip(a,v))
def close(kind,lhs,rhs,tol=2e-10):
    error=abs(lhs-rhs)
    numerical.append({'kind':kind,'error':error,'bound':tol*(1+abs(rhs))})
    ck(kind,error<=tol*(1+abs(rhs)), {'error':'%.4e'%error})

# A coupled max norm in eigencoordinates (the ball is not a product in those coordinates).
# A physical oblique similarity makes projection strongly nonorthogonal in Euclidean coordinates.
S=M([[1,3],[2,7]]); Si=inv(S); H=M([[1,1],[1,-1]]); Hi=inv(H)
physical_norm=mul(H,Si); physical_norm_i=inv(physical_norm)
P=mul(mul(S,M([[1,0],[0,0]])),Si)
ck('rational_inverse',mul(S,Si)==eye(2) and mul(physical_norm,physical_norm_i)==eye(2))
ck('oblique_projection',P!=[list(row) for row in zip(*P)] and mul(P,P)==P)
ck('coupled_norm_projection',infnorm(mul(mul(physical_norm,P),physical_norm_i))==1)
grid=[F(-1),F(-3,4),F(-1,2),F(0),F(1,2),F(3,4),F(1)]
for r in [F(0),F(1,1000),F(1,2),F(999,1000),F(1)]:
    D=M([[-1,0],[0,r]]); A=mul(mul(S,D),Si)
    in_norm=mul(mul(physical_norm,A),physical_norm_i)
    ck('coupled_norm_contraction',infnorm(in_norm)==1,str(r))
    ck('coupled_projection_commutation',mul(A,P)==mul(P,A),str(r))
    for y in itertools.product(grid,repeat=2):
        x=mv(physical_norm_i,y); ax=mv(A,x); px=mv(P,x)
        ck('actual_ball_maps',vecinf(mv(physical_norm,ax))<=1 and vecinf(mv(physical_norm,px))<=1,str(r))
        t=abs(dot(Si[1],x)); at=abs(dot(Si[1],ax))
        ck('actual_left_functional',at==r*t,str(r))
        if 0<r<1:
            ck('actual_zero_function',max(F(0),at-r)==0,str(r))
    if 0<r<1:
        witness=mv(physical_norm_i,[F(1),F(-1)])
        ck('zero_function_nonzero_at_ball_boundary',abs(dot(Si[1],witness))==1 and 1-r>0,str(r))
        for n in [2,4,16,64]:
            expected=mul(mul(S,M([[0,0],[0,r**n]])),Si)
            difference=[[x-y for x,y in zip(row,prow)] for row,prow in zip(power(A,n),P)]
            ck('exact_even_recurrence',difference==expected,{'r':str(r),'n':n})
    cases.append({'case':'coupled_ball','stable_radius':str(r),'contractive':True})

# Deliberately outside the assumptions: peripheral Jordan block and a stable radius above one.
J=M([[1,1],[0,1]])
for n in [1,2,5,20,100]:
    ck('negative_peripheral_Jordan_growth',infnorm(power(J,n))==n+1, n)
bad=mul(mul(H,M([[-1,0],[0,F(6,5)]])),Hi)
ck('negative_noncontraction_rejected',infnorm(bad)>1,str(infnorm(bad)))
ck('endpoint_formula_domain',not(0<F(0)<1) and not(0<F(1)<1))

# Direct complex-function values, with nonreal matrix eigenvalues and off-orbit samples.
# Numerical controls are explicitly distinguished from exact rational checks.
for r in [0.001,0.5,0.999]:
    alpha=r*cmath.exp(0.73j)
    for mag,phase in [(0.1,2.2),(0.9,0.7),(0.999,-2.9),(1e-50,1.2)]:
        mu=mag*cmath.exp(phase*1j); z=cmath.log(mu)/math.log(r)
        def f(x):return 0j if x==0 else cmath.exp(z*math.log(abs(x)))
        ck('positive_exponent_real_part',z.real>0)
        close('actual_complex_power_multiplier',cmath.exp(z*math.log(r)),mu)
        close('nonzero_function_normalization',f(1+0j),1+0j)
        for radius in [0.0,1e-100,1e-20,0.03,0.41,1.0]:
            for angle in [-2.8,0.0,0.83,2.5]:
                x=radius*cmath.exp(angle*1j)
                close('direct_eigenfunction_on_complex_ball',f(alpha*x),mu*f(x))
                if x!=0:
                    close('continuity_modulus_identity',abs(f(x)),radius**z.real)
        ck('kernel_value_zero',f(0j)==0j)

# A genuinely continuous nonpolynomial observable in a nilpotent/peripheral kernel.
S3=M([[1,2,1],[1,3,0],[0,1,1]]); Si3=inv(S3)
D3=M([[-1,0,0],[0,0,1],[0,0,0]])
A3=mul(mul(S3,D3),Si3); P3=mul(mul(S3,M([[1,0,0],[0,0,0],[0,0,0]])),Si3)
ck('nilpotent_l1_contraction',l1norm(D3)==1)
ck('nilpotent_matrix_iterate_identity',power(A3,4)==power(A3,2))
def g(v):return abs(v[1])/(1+abs(v[0]))+max(F(0),abs(v[2])-F(1,4))
def h(v):return abs(v[0])+abs(v[1])/(1+abs(v[2]))+max(F(0),abs(v[2])-F(1,4))
nil_samples=[v for v in itertools.product([F(-1),F(-1,2),F(0),F(1,2),F(1)],repeat=3) if sum(map(abs,v))<=1]
for v in nil_samples:
    x=mv(S3,v); ax=mv(A3,x)
    ck('nonpolynomial_nilpotent_ideal',g(mv(Si3,mv(power(A3,2),x)))==0)
    ck('nonpolynomial_Q_commutes_K',h(mv(Si3,mv(A3,mv(P3,x))))==h(mv(Si3,mv(P3,ax))))
    ck('nilpotent_zero_eigenfunction',dot(Si3[2],ax)==0)
ck('nilpotent_order_sharp_witness',g(mv(D3,[F(0),F(0),F(1)]))>0 and g(mv(power(D3,2),[F(0),F(0),F(1)]))==0)
ck('nilpotent_zero_function_nonzero',dot(Si3[2],mv(S3,[F(0),F(0),F(1)]))==1)

# Exact high-order finite group closure through integer modular residues, independent of SymPy.
for phases in [(F(2,101),),(F(2,101),F(3,103),F(0)),(F(15,35),F(2,7),F(15,35)),(F(0),F(0)),(F(5,12),F(7,12))]:
    q=math.lcm(*(a.denominator for a in phases)); generators=[int(a*q)%q for a in phases]
    found={0}; pending=[0]
    while pending:
        a=pending.pop()
        for gen in generators:
            value=(a+gen)%q
            if value not in found:found.add(value);pending.append(value)
    divisor=math.gcd(q,*generators)
    ck('exact_integer_group_closure',found==set(range(0,q,divisor)),{'generators':list(map(str,phases)),'order':len(found)})
    ck('exact_generated_inverses',all((-g)%q in found for g in generators))
    cases.append({'case':'finite_group','phases':list(map(str,phases)),'order':len(found)})
low_degree={(p-q)%101 for p,q in itertools.product(range(3),repeat=2)}
ck('negative_finite_monomial_coverage',len(low_degree)==5 and len(low_degree)<101)

# Finite samples cannot distinguish an infinite group from a sufficiently close rational rotation.
theta=math.sqrt(2); rational=F(theta).limit_denominator(1000000)
phase_error=max(abs(cmath.exp(2j*math.pi*n*theta)-cmath.exp(2j*math.pi*n*float(rational))) for n in range(501))
ck('negative_finite_rotation_identifiability',phase_error<1e-8,{'rational':str(rational),'max_error':'%.4e'%phase_error})
small_delta=1e-8; m=1000
avg=abs(sum(cmath.exp(small_delta*j*1j) for j in range(m))/m)
ck('negative_uniform_Cesaro_rate',avg>0.999999, {'terms':m,'phase_gap':small_delta,'average_modulus':avg})
cases.append({'case':'finite_rotation_indistinguishability','irrational_model':'sqrt(2) float','rational':str(rational),'first_powers':501,'max_error':phase_error})
cases.append({'case':'Cesaro_nonuniformity','terms':m,'phase_gap':small_delta,'average_modulus':avg})

detail={'events':events,'numerical_error_records':numerical,'cases':cases}
raw=(json.dumps(detail,indent=2,sort_keys=True)+'\n').encode()
if args.details_output is not None:
    args.details_output.parent.mkdir(parents=True, exist_ok=True)
    args.details_output.write_bytes(raw)
receipt={'status':'PASS_BOUNDED_CONTROLS','total_controls':sum(counts.values()),'checks':dict(sorted(counts.items())),
         'exact_rational_or_discrete_controls':sum(counts.values())-len(numerical)-counts['negative_finite_rotation_identifiability']-counts['negative_uniform_Cesaro_rate']-counts['positive_exponent_real_part'],
         'floating_controls':len(numerical)+counts['negative_finite_rotation_identifiability']+counts['negative_uniform_Cesaro_rate']+counts['positive_exponent_real_part'],
         'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
         'details_sha256':hashlib.sha256(raw).hexdigest(),
         'limitations':'Finite algebra and sampled numerical diagnostics only. No infinite-dimensional spectrum, universal arbitrary-norm theorem, density, continuity, recurrence or historical-priority conclusion is derived from finite controls.'}

raw = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
if args.output is not None:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(raw, encoding="utf-8")
print(raw, end="")
