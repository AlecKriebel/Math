import sympy as s
import json
checks=[]
d=s.sqrt(13); c=s.sqrt(3); A=2*(d-1)/3;B=(4-d)/3
def exact_zero(name,x):
 value=s.simplify(x)
 assert value==0,(name,value)
 checks.append({'name':name,'result':'EXACT_ZERO'})
exact_zero('confocal caustic',A*A-B*B-3)
for name,r,t,H,J in [('major',s.Integer(2),s.Integer(1),A,B),('minor_rotated',s.Integer(1),s.Integer(2),B,A)]:
 V2=t*t*(1-H*H/(r*r)); D=(r+H)**2+V2; G=r*r*(r+H)/(H*t*t)-1
 exact_zero(name+' side tangency',r*r*V2-H*H*V2-J*J*(r+H)**2)
 exact_zero(name+' reflection squared',D-V2*G*G)
 assert bool(H>0) and bool(V2>0) and bool(G>0)
 checks.append({'name':name+' reflection branch signs','result':'STRICTLY_POSITIVE'})
# Independent explicit pedal-area formula from the exact frozen derivation.
y=s.sqrt(1-A*A/4);D=(2+A)**2+y*y
areas=[]
for sign in [1,-1]:
 U=(sign*c*(2+A)**2+2*y*y)/D; Z=y*(2+A)*(2-sign*c)/D
 areas.append(s.simplify(Z*(A+U)))
R=s.simplify(areas[0]/areas[1]);expected=(2-c)/(2+c)*(d+2*c)/(d-2*c)
exact_zero('major phase direct signed-area ratio',R-expected)
assert bool(d/2>c) and bool(s.Integer(2)>d/2)
checks.append({'name':'major ratio strictly above one by exact inequalities','result':'STRICTLY_POSITIVE'})
# Check the independently derived scalar normal-angle derivative, not a sample.
S,C,E,Rr,Tt=s.symbols('S C E Rr Tt', positive=True)
n=s.Matrix([-S/Rr,C/Tt]);nprime=s.Matrix([-C*E/Rr,-S*E/Tt])
exact_zero('normal angular speed identity',s.det(s.Matrix.hstack(n,nprime))-E*(S*S+C*C)/(Rr*Tt))
# Reconstruct source correction triangle directly using its listed lines.
root21=s.sqrt(21);root5=s.sqrt(5)
V=[s.Matrix([root21,0]),s.Matrix([-3*root21/5,s.Rational(16,5)]),s.Matrix([-3*root21/5,-s.Rational(16,5)])]
def area(Q):return s.simplify(sum(s.det(s.Matrix.hstack(Q[i],Q[(i+1)%3])) for i in range(3))/2)
def foot(F,X,Y):
 v=Y-X;return s.simplify(X+(F-X).dot(v)/v.dot(v)*v)
for fs in [1,-1]:
 F=s.Matrix([fs*root5,0]);q=[foot(F,V[i],V[(i+1)%3]) for i in range(3)]
 exact_zero('candidate triangle orbit area focus '+str(fs),area(q)-s.Rational(84,625)*(7*root21+fs*root5))
 qouter=[]
 for P in V:
  normal=s.Matrix([P[0]/21,P[1]/16]);qouter.append(s.simplify(F+(1-F.dot(normal))/normal.dot(normal)*normal))
 exact_zero('candidate triangle tangent-side area focus '+str(fs),area(qouter)-s.Rational(7,10)*(7*root21+fs*root5))
print(json.dumps({'status':'PASS','sympy_version':s.__version__,'exact_control_count':len(checks),'checks':checks,'independent_major_ratio':str(expected),'independent_minor_ratio':'1 by focus-swapping reflection preserving signed area after cyclic reversal','qualification':'Symbolic verification of frozen independent algebra and submitted triangle; universal E proof audited separately in prose.'},indent=2))
