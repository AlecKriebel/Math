from pathlib import Path
import sympy as s,json
N=s.symbols('N',integer=True,positive=True);tau,j=s.symbols('tau j',integer=True);x=s.symbols('x',real=True)
g=s.cos(s.expand(2*s.pi*N*(x+j*tau/N)));assert s.simplify(g-s.cos(2*s.pi*N*x))==0
mean=s.integrate(s.cos(2*s.pi*N*x),(x,0,1));assert mean==0
phase0=s.simplify(N*s.cos(2*s.pi*N*0));phase1=s.simplify(N*s.cos(2*s.pi*N/(2*N)));assert phase0==N and phase1==-N
r={'sympy':s.__version__,'per_edge':'cos(2*pi*N*x)','finite_coprime_N_rotation_trace':'N*cos(2*pi*N*x)','spatial_uniform_average':str(mean),'two_phase_traces':[str(phase0),str(phase1)],'exact_identity_for_each_integer_j_tau':True,'scope':'Exact obstruction to inferring phase constancy of finite rational-rotation traces merely from irrational spatial averaging; not a counterexample to the billiard target or a defect in the cited averaging paper.'}
Path(__file__).with_name('RESULT_V3.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
