"""Exact arbitrary-triangle projection check and focal counterexample power map."""
import json
import sympy as s
r,t=s.symbols('r t',nonzero=True,real=True)
z,x,y=s.symbols('z x y',real=True)
V=[s.Matrix([0,0]),s.Matrix([r,0]),s.Matrix([z,t])]
M=s.Matrix([x,y])
def foot(A,B,P):
 d=B-A
 return A+d*((P-A).dot(d))/d.dot(d)
def area(W):
 return sum(W[i].det(W[(i+1)%len(W)]) for i in range(len(W)))/2
O=s.Matrix([r/2,(z*z+t*t-r*z)/(2*t)])
R2=O.dot(O)
projected=area([foot(V[i],V[(i+1)%3],M) for i in range(3)])
formula=area(V)*(R2-(M-O).dot(M-O))/(4*R2)
assert s.cancel(projected-formula)==0
S=s.sqrt(21);c=s.sqrt(5)
T=[s.Matrix([S,0]),s.Matrix([-3*S/5,s.Rational(16,5)]),s.Matrix([-3*S/5,-s.Rational(16,5)])]
OT=s.Matrix([1/S,0]);RT2=s.Rational(400,21)
assert all(s.simplify((p-OT).dot(p-OT)-RT2)==0 for p in T)
assert s.simplify(area(T)-128*S/25)==0
values=[]
for sign in [1,-1]:
 F=s.Matrix([sign*c,0]);power=s.simplify(RT2-(F-OT).dot(F-OT))
 assert s.simplify(power-(14+sign*2*c/S))==0
 B=s.simplify(area(T)*power/(4*RT2));expected=84*(7*S+sign*c)/625
 assert s.simplify(B-expected)==0
 assert s.simplify(area([foot(T[i],T[(i+1)%3],F) for i in range(3)])-B)==0
 values.append({'focus_sign':sign,'positive_power':str(power),'signed_pedal_area':str(expected)})
ratio=(7*S+c)/(7*S-c)
assert s.simplify(ratio-ratio**-1)!=0
print(json.dumps({'status':'PASS_EXACT_CLASSICAL_SIGNED_TRIANGLE_FORMULA_AND_AUTHENTICATED_FOCAL_POWER_MAP','arbitrary_real_triangle_normal_form':'(0,0),(r,0),(z,t), r*t nonzero; arbitrary real pedal point (x,y)','generic_projection_minus_power_formula':str(s.cancel(projected-formula)),'counterexample_circumcenter':[str(v) for v in OT],'counterexample_circumradius_squared':str(RT2),'candidate_focal_areas':values,'reciprocal_difference':str(s.simplify(ratio-ratio**-1)),'logical_scope':'Exact algebraic identity and exact one-family counterexample; not a historical claim that the old sources explicitly stated focal-ratio nonconstancy.'},indent=2))
