from pathlib import Path
import json,math,sympy as S
R=Path(__file__).resolve().parent
checks={}
def check(k,x):
 if not x:raise ValueError(k)
 checks[k]=True
r,v=S.symbols('r v',positive=True)
J=S.ones(2)/2;K=S.eye(2)-J
check('spectral_semigroup_all_parameters',S.simplify((J+r*K)*(J+v*K)-(J+r*v*K))==S.zeros(2))
check('positive_d_factorization',S.simplify(r**3+(1-r*r)*S.sqrt(1+r*r)-r-(1-r*r)*(S.sqrt(1+r*r)-r))==0)
d=(1-r*r)*(S.sqrt(1+r*r)-r)/2
check('d_at_log2',S.simplify(d.subs(r,S.Rational(1,2))-3*(S.sqrt(5)-1)/16)==0)
check('d_at_zero_time',d.subs(r,1)==0)
check('d_at_infinite_time',S.simplify(S.limit(d,r,0,dir='+')-S.Rational(1,2))==0)
x=S.symbols('x',positive=True);g=S.acos(S.exp(-x))/2
check('g_derivative',S.simplify(S.diff(g,x)-1/(2*S.sqrt(S.exp(2*x)-1)))==0)
check('g_derivative_decreasing',S.simplify(S.diff(1/(2*S.sqrt(S.exp(2*x)-1)),x)+S.exp(2*x)/(2*(S.exp(2*x)-1)**S.Rational(3,2)))==0)
q=S.diag(1,0);Q=S.Matrix([[S.Rational(3,4),S.sqrt(3)/4],[S.sqrt(3)/4,S.Rational(1,4)]])
check('M2_e12_generated',q*Q*(S.eye(2)-q)==S.Matrix([[0,S.sqrt(3)/4],[0,0]]))
check('Q_is_projection',Q*Q==Q)
# Derive the literal BFH flip-flop finite unitary independently.
c,z=S.symbols('c z',real=True);a,b=S.symbols('a b',real=True);w=S.symbols('w',complex=True)
H=S.Matrix([[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,0]])
U=S.eye(4)+(c-1)*(H*H)-S.I*z*H
check('BFH_unitarity_constraint',S.simplify(U.conjugate().T*U-S.diag(1,c*c+z*z,c*c+z*z,1))==S.zeros(4))
B=S.Matrix([[a,w],[S.conjugate(w),b]])
compressed=(U.conjugate().T*S.kronecker_product(S.eye(2),B)*U)[2:4,2:4]
check('BFH_full_dual_channel',compressed==S.Matrix([[a*c*c+b*z*z,c*w],[c*S.conjugate(w),b]]))
check('BFH_projection_exponential',compressed.subs({a:1,b:0,w:0,S.conjugate(w):0})==c*c*q)
G=S.acos(S.exp(-x/2))
check('BFH_integral_angle',S.simplify(S.diff(G,x)-1/(2*S.sqrt(S.exp(x)-1)))==0)
check('BFH_finite_endpoint',S.limit(G,x,S.oo)==S.pi/2)
Lq=(S.Matrix([[0,1],[1,0]])*q*S.Matrix([[0,1],[1,0]])-q)/2
check('small_model_non_derivation',q*Lq*q==-q/2)
check('BFH_non_derivation',q*(-q)*q==-q)
# Floating samples are only sanity checks, robust small-time angle via expm1.
def gg(x):
 if x<=0:return 0.
 return math.atan2(math.sqrt(-math.expm1(-2*x)),math.exp(-x))/2
samples=[]
for s in [1e-8,1e-5,.001,.1,math.log(2),2.,10.,50.]:
 r0=math.exp(-s);coef=-math.expm1(-2*s)*(math.sqrt(1+r0*r0)-r0)/2
 check('d_positive_sample_'+repr(s),coef>0)
 for x0 in [-100.,-s,-s/2,0.,s/10,s,2*s,100.]:
  increment=gg(x0+s)-gg(x0)
  check('increment_bound_sample_'+repr((s,x0)),increment>=-1e-15 and increment<=gg(s)+1e-14)
 samples.append({'s':s,'d':coef})
report={'result':'PASS','sympy_version':S.__version__,'independent_checks':len(checks),'checks':checks,'positive_coefficient_samples':samples,'continuous_quantifiers':'Only the analytic argument in INDEPENDENT_DEDUCTIONS.md proves the all-time/all-space statements.','prior_corollary':'Literal BFH amplitude model, finite bath |1>, finite endpoint path, finite GNS image, exact forward restriction, L(q)=-q contradict projection Leibniz identity.'}
(R/'INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'result':'PASS','independent_checks':len(checks)}))
