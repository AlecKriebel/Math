from pathlib import Path
import sympy as s,json
count=0
def eq(a,b,label):
 global count
 count+=1
 if s.simplify(a-b)!=0:raise RuntimeError(label)
def foot(F,A,B):
 d=B-A;n=s.Matrix([d[1],-d[0]])
 return s.simplify(F+(n.dot(A)-n.dot(F))/n.dot(n)*n)
def area(V):return s.simplify(sum(s.det(s.Matrix.hstack(V[i],V[(i+1)%len(V)])) for i in range(len(V)))/2)
r=s.sqrt(21);c=s.sqrt(5)
T=[s.Matrix([r,0]),s.Matrix([-3*r/5,s.Rational(16,5)]),s.Matrix([-3*r/5,-s.Rational(16,5)])]
U=[s.Matrix([r,8]),s.Matrix([-5*r/3,0]),s.Matrix([r,-8])]
records=[]
for i,P in enumerate(T):
 eq(P[0]**2/21+P[1]**2/16,1,'boundary')
 incoming=s.simplify((P-T[(i-1)%3])/s.sqrt((P-T[(i-1)%3]).dot(P-T[(i-1)%3])))
 outgoing=s.simplify((T[(i+1)%3]-P)/s.sqrt((T[(i+1)%3]-P).dot(T[(i+1)%3]-P)))
 n=s.Matrix([P[0]/21,P[1]/16]);ref=incoming-2*incoming.dot(n)/n.dot(n)*n
 for j in range(2):eq(ref[j],outgoing[j],'reflection')
 for j in [i,(i+1)%3]:eq(U[i].dot(s.Matrix([T[j][0]/21,T[j][1]/16])),1,'tangent intersection')
 a=T[i];d=T[(i+1)%3]-a;w=s.symbols('w');pol=s.expand((a[0]+w*d[0])**2/s.Rational(189,25)+(a[1]+w*d[1])**2/s.Rational(64,25)-1)
 eq(s.discriminant(pol,w),0,'strict caustic tangency')
 contact=s.simplify(-pol.coeff(w,1)/(2*pol.coeff(w,2)))
 if not 0<contact<1:raise RuntimeError('contact not inside segment')
 count+=1
for e in [1,-1]:
 F=s.Matrix([e*c,0]);A=area([foot(F,T[i],T[(i+1)%3]) for i in range(3)]);B=area([foot(F,U[i],U[(i+1)%3]) for i in range(3)])
 eq(A,84*(7*r+e*c)/625,'exact A');eq(B,7*(7*r+e*c)/10,'exact B');eq(B,s.Rational(125,24)*A,'same multiplier')
 negT=[-x for x in T];negU=[-x for x in U]
 eq(area([foot(F,negT[i],negT[(i+1)%3]) for i in range(3)]),84*(7*r-e*c)/625,'inverted phase')
 eq(area([foot(F,negU[i],negU[(i+1)%3]) for i in range(3)]),7*(7*r-e*c)/10,'inverted outer phase')
 records.append({'focus':e,'A':str(A),'B':str(B),'multiplier':'125/24'})
print(json.dumps({'status':'PASS_EXACT_ROOT_TRIANGLE_CERTIFICATE','exact_guards':count,'records':records,'signed_orientation_positive':area(T)>0,'universal_proof_by_sampling':False},default=str,sort_keys=True))
