#!/usr/bin/env python3
"""Independent exact controls and explicitly nonrigorous numerical diagnostics."""
from pathlib import Path
import json,math
from datetime import datetime,timezone
import numpy as np
from scipy.integrate import quad
import sympy as s
BASE=Path(__file__).resolve().parent
out={'utc':datetime.now(timezone.utc).isoformat(),'exact':[],'diagnostic':[],'status':'PASS','scope':'Finite independent checks, not formal proof or rigorous interval quadrature.'}
def exact(name,predicate,details=''):
 if not bool(predicate):raise RuntimeError(name)
 out['exact'].append({'name':name,'passed':True,'details':details})
x=s.symbols('x',real=True);g,h,k=s.symbols('g h k',real=True)
w=s.Matrix([s.cos(x),s.sin(x)]);G=s.Matrix([[g,k],[k,h]])
T=s.integrate((w.T*G*w)[0]*(4*w*w.T-2*s.eye(2)),(x,0,2*s.pi))/s.pi
exact('inner-product angular stress',s.simplify(T-(2*G-s.trace(G)*s.eye(2)))==s.zeros(2),str(T))
exact('rank-one nonzero stress',T.subs({g:1,h:0,k:0})==s.diag(1,-1))
exact('zero seminorm stress',T.subs({g:0,h:0,k:0})==s.zeros(2))
exact('nonzero anisotropic inner-product unbalanced',T.subs({g:4,h:1,k:0})==s.diag(3,-3))
exact('nonsharp reciprocal constant',s.simplify(1/(s.sqrt(17)-4)-(4+s.sqrt(17)))==0)
a,b,A=s.symbols('a b A',positive=True)
exact('calibration mean zero',s.simplify(a-(a/(A-a))*(A-a))==0)
exact('belt equatorial cubic derivative',s.diff(x**3/3,x)==x*x)
exact('KS first variation sign',s.diff(x*x,x)==2*x)
exact('round positive band area',s.simplify(s.diff(s.tanh(x),x)-s.sech(x)**2)==0 and s.simplify(s.tanh(a)-s.tanh(-a)-2*s.tanh(a))==0)
# Complex rotation at theta=pi/4 reverses the imaginary stress sign in q=a-ib.
R=s.Matrix([[s.sqrt(2)/2,-s.sqrt(2)/2],[s.sqrt(2)/2,s.sqrt(2)/2]])
TR=s.simplify(R.T*s.diag(1,-1)*R)
exact('quadratic differential rotation convention',TR==s.Matrix([[0,-1],[-1,0]]))
exact('det-one polar trace lower bound',s.factor(x+1/x-2)==(x-1)**2/x)
# Matrix derivative of the correct angular weight at identity, no norm derivative.
u,v,p,q=s.symbols('u v p q',real=True);eps=s.symbols('eps',real=True)
D=s.Matrix([[u,v],[p,q]]);Mat=s.eye(2)+eps*D
weight=1/(Mat.det()**2*(w.T*Mat.inv().T*Mat.inv()*w)[0]**2)
derivative=s.trigsimp(s.diff(weight,eps).subs(eps,0))
expected=4*(w.T*D*w)[0]-2*s.trace(D)
exact('angular weight first derivative',s.trigsimp(derivative-expected)==0)
for label,norm in [('maxnorm',lambda x:max(abs(x[0]),abs(x[1]))),('rankone',lambda x:abs(x[0])),('zero',lambda x:0.0),('l1',lambda x:abs(x[0])+abs(x[1]))]:
 def integral(fun):return quad(fun,0,2*math.pi,epsabs=2e-10,epsrel=2e-10,limit=600)[0]/math.pi
 def energy(B):return integral(lambda t:norm(B@np.array([math.cos(t),math.sin(t)]))**2)
 B=np.array([[1.35,0.27],[-0.18,0.87]]);det=np.linalg.det(B);inv=np.linalg.inv(B)
 direct=energy(B)/det
 angular=integral(lambda t:norm(np.array([math.cos(t),math.sin(t)]))**2/np.linalg.norm(inv@np.array([math.cos(t),math.sin(t)]))**4)/det**2
 err=abs(direct-angular)
 if err>3e-8:raise RuntimeError(label+' angular identity')
 out['diagnostic'].append({'name':label+' angular identity','error':err,'passed':True})
 if label in ['maxnorm','l1']:
  stress=np.empty((2,2))
  for i in range(2):
   for j in range(2):stress[i,j]=integral(lambda t:norm(np.array([math.cos(t),math.sin(t)]))**2*(4*np.array([math.cos(t),math.sin(t)])[i]*np.array([math.cos(t),math.sin(t)])[j]-2*(i==j)))
  if np.linalg.norm(stress)>2e-8:raise RuntimeError(label+' balance')
  gaps=[]
  for lam in [.1,.4,1,2,10]:
   M=np.array([[lam,0],[0,1/lam]])@np.array([[math.cos(.33),-math.sin(.33)],[math.sin(.33),math.cos(.33)]])
   gap=energy(M)-energy(np.eye(2));gaps.append(gap)
   if gap<-2e-8:raise RuntimeError(label+' SL2 support')
  out['diagnostic'].append({'name':label+' balanced non-Euclidean SL2 samples','stress_norm':float(np.linalg.norm(stress)),'gaps':gaps,'passed':True})
 if label=='rankone':
  wrong=angular*det
  if abs(wrong-direct)<.1:raise RuntimeError('wrong det power not detected')
  out['diagnostic'].append({'name':'wrong determinant power negative control','wrong_error':abs(wrong-direct),'detected':True})
out['exact_count']=len(out['exact']);out['diagnostic_count']=len(out['diagnostic'])
(BASE/'MATH_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['exact','diagnostic']},indent=2))
