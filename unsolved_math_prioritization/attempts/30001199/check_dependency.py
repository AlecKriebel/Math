import sympy as s
import json
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
A=s.Matrix([[0,1],[0,0]]);Z=s.zeros(1);D=s.diag(Z,A,Z,A)
R=s.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,0,0],[0,1,0],[0,0,1]])
bar=s.Matrix([[1,0],[0,0],[0,1],[1,0],[0,0],[0,-1]])
E=s.Matrix([[0,1,0,0,-1,0]])
ck(R.rank()==3);ck(R[:3,:].rank()==3);ck(R.row_join(D*R).rank()==R.rank());ck(E*R==s.zeros(1,3))
v=s.Matrix([0,0,1,0,0,-1]);w=s.Matrix([0,1,0,0,-1,0])
ck(D*v==w);ck(bar.row_join(v).rank()==bar.rank());ck(E*bar==s.zeros(1,2))
T=R.row_join(bar);ck(T.rank()==4);ck(T.row_join(v).rank()==4);ck(T.row_join(w).rank()==5)
ck(E*v==s.zeros(1,1));ck(E*w==s.Matrix([2]))
t=s.symbols('t',real=True);ck(D**2==s.zeros(6));ck(E*(s.eye(6)+t*D)*v==s.Matrix([2*t]))
print(json.dumps({'status':'PASS narrow dependency diagnostic','exact_assertions':checks,'diagonal_simulation_dimension':R.rank(),'enlarged_relation_dimension':T.rank(),'dimension_after_adding_drift_of_v':T.row_join(w).rank(),'output_discrepancy_at_time_t':'2*t','main_theorem_counterexample':False,'primary_formula_visually_confirmed':False},indent=2))
