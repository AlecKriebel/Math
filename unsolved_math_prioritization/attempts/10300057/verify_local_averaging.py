"""Own symbolic Frobenius control; not an original-problem solution."""
import sympy as s,json
x,y,z,e=s.symbols('x y z e');a1=s.Matrix([-e*z*z,0,1]);a2=s.Matrix([0,e,1])
def frob(a):
 curl=s.Matrix([s.diff(a[2],y)-s.diff(a[1],z),s.diff(a[0],z)-s.diff(a[2],x),s.diff(a[1],x)-s.diff(a[0],y)])
 return s.expand(a.dot(curl))
assert frob(a1)==0 and frob(a2)==0 and frob((a1+a2)/2)==-e*e*z/2
f=z/(1+e*x*z);assert all(s.simplify(s.diff(f,v)-a1[i]/(1+e*x*z)**2)==0 for i,v in enumerate([x,y,z]))
print(json.dumps({'status':'PASS','checks':6,'alpha1_Frobenius':str(frob(a1)),'alpha2_Frobenius':str(frob(a2)),'average_Frobenius':str(frob((a1+a2)/2)),'scope':'Symbolic local averaging countercontrol only; not a check of the ODE theorem or original foliation question.'},indent=2))
