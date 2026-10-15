from pathlib import Path
import json, math
import sympy as S

R=Path(__file__).resolve().parent
r=S.symbols('r', real=True, positive=True)
q=S.diag(1,0)
one=S.eye(2)
c=S.sqrt((1+r)/2)
d=S.sqrt((1-r)/2)
Q=S.Matrix([[c*c,c*d],[c*d,d*d]])
checks={}
checks['Q_projection']=S.simplify(Q*Q-Q)==S.zeros(2)
checks['Q_trace_one']=S.simplify(S.trace(Q))==1
checks['GNS_offdiagonal_generator']=q*Q*(one-q)==S.Matrix([[0,c*d],[0,0]])
raw=(r**3+(1-r*r)*S.sqrt(1+r*r)-r)/2
factored=(1-r*r)*(S.sqrt(1+r*r)-r)/2
checks['witness_factorization']=S.simplify(raw-factored)==0
checks['exact_half_witness']=S.simplify(factored.subs(r,S.Rational(1,2))-3*(S.sqrt(5)-1)/16)==0
checks['d_zero_time_limit']=S.limit(factored,r,1,dir='-')==0
checks['d_large_time_limit']=S.limit(factored,r,0,dir='+')==S.Rational(1,2)
checks['square_root_sign_gap']=S.simplify((S.sqrt(1+r*r))**2-r*r)==1
J=S.ones(2)/2; K=S.Matrix([[1,-1],[-1,1]])/2
checks['Markov_projections']=J*J==J and K*K==K and J*K==K*J==S.zeros(2) and J+K==one
Lq=S.diag(-S.Rational(1,2),S.Rational(1,2))
checks['finite_GNS_obstruction_in_own_model']=q*Lq*q==-q/2
def g(x):
    return 0.0 if x<=0 else math.acos(math.exp(-x))/2
minimum=1.0
evaluations=0
worst_increment_error=0.0
for s in [1e-8,1e-6,0.001,0.03,0.4,math.log(2),1,5,40,1000]:
    for x in [-1e6,-2*s,-s,-s/2,0,1e-10,1e-6,0.001,0.1,1,10,1e6]:
        inc=g(x+s)-g(x)
        coefficient=math.cos(inc)**2-math.cos(g(s))**2
        minimum=min(minimum,coefficient)
        worst_increment_error=max(worst_increment_error,inc-g(s),-inc)
        evaluations+=1
checks['positivity_sanity_grid']=minimum>=-1e-14 and worst_increment_error<=1e-14
if not all(checks.values()): raise RuntimeError(checks)
out={'checks':checks,'count':len(checks),'positive_witness_grid_evaluations':evaluations,'minimum_sampled_coefficient':minimum,'maximum_increment_bound_violation':worst_increment_error,'arithmetic':'SymPy 1.14 exact identities; deterministic numerical limiting sanity controls','meaning':'The standalone analytic deductions prove the all-real-time and global claims; finite controls alone do not.'}
(R/'INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
