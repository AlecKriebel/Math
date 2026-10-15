#!/usr/bin/env python3
"""Independent KS controls: only stdlib; no author imports; Fourier stress.
Finite controls supplement INDEPENDENT_DERIVATION.md, not a proof substitute.
"""
import argparse,hashlib,json,math
from datetime import datetime,timezone
from fractions import Fraction
from pathlib import Path
P=math.pi

def mv(a,x,y):return a[0][0]*x+a[0][1]*y,a[1][0]*x+a[1][1]*y

def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def inv(a):
 d=det(a)
 return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]

def mm(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def tr(a):return [[a[j][i] for j in range(2)] for i in range(2)]

def err(a,b):return max(abs(a[i][j]-b[i][j]) for i in range(2) for j in range(2))

def pair(a,b):return sum(a[i][j]*b[i][j] for i in range(2) for j in range(2))

def op(a):return math.hypot(a[0][0],a[0][1])

class Integrator:
 def __init__(self,n):
  self.n=n;self.points=[]
  for i in range(n):
   t=2*P*(i+.5)/n
   self.points.append((math.cos(t),math.sin(t),math.cos(2*t),math.sin(2*t)))
 def direct(self,s,a):return 2*math.fsum(s(*mv(a,x,y))**2 for x,y,_,_ in self.points)/self.n/det(a)
 def inverse(self,s,a,power=4,det_power=2):
  ai=inv(a)
  return 2*math.fsum(s(x,y)**2/math.hypot(*mv(ai,x,y))**power for x,y,_,_ in self.points)/self.n/det(a)**det_power
 def stress(self,s):
  vals=[s(x,y)**2 for x,y,_,_ in self.points]
  a=4*math.fsum(v*p[2] for v,p in zip(vals,self.points))/self.n
  b=4*math.fsum(v*p[3] for v,p in zip(vals,self.points))/self.n
  return [[a,b],[b,-a]]
 def extrema(self,s):
  v=[s(x,y) for x,y,_,_ in self.points]
  return min(v),max(v)

def integrate(p):
 def mon(i):return Fraction(0) if i%2 else Fraction(2,i+1)
 return sum(v*mon(i)*mon(j) for (i,j),v in p.items())

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--samples',type=int,default=131072);ap.add_argument('--output',default='CHECK_RESULTS.json');a=ap.parse_args()
 it=Integrator(a.samples)
 norms={'zero':lambda x,y:0.,'euclidean':lambda x,y:math.hypot(x,y),
 'quadratic_offdiag':lambda x,y:math.sqrt(3*x*x+1.4*x*y+.8*y*y),
 'weighted_l1':lambda x,y:abs(x)+.18*abs(y),
 'weighted_linf':lambda x,y:max(abs(x),.07*abs(y)),
 'rank_one_rotated':lambda x,y:abs(.3*x+1.7*y),
 'polygon_max_linear':lambda x,y:max(abs(x+.4*y),abs(-.6*x+.9*y),abs(.8*x-.2*y)),
 'l1_fourfold':lambda x,y:abs(x)+abs(y),'linf_fourfold':lambda x,y:max(abs(x),abs(y))}
 mats=[[[1.2,.3],[-.2,.9]],[[.63,-.12],[.28,1.57]],[[1.05,.42],[0.,1.11]]]
 B=[[.4,-.3],[.7,-.2]];ang=.431;R=[[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]];lam=1.37;h=.001
 reports=[];fail=[]
 for name,s in norms.items():
  t=it.stress(s);fe=max(abs(it.direct(s,m)-it.inverse(s,m)) for m in mats)
  plus=[[float(i==j)+h*B[i][j] for j in range(2)] for i in range(2)]
  minus=[[float(i==j)-h*B[i][j] for j in range(2)] for i in range(2)]
  derivative=(it.direct(s,plus)-it.direct(s,minus))/(2*h);prediction=pair(t,B)
  rt=it.stress(lambda x,y:s(*mv(R,x,y)));rp=mm(mm(tr(R),t),R)
  st=it.stress(lambda x,y:lam*s(x,y));sp=[[lam**2*t[i][j] for j in range(2)] for i in range(2)]
  mn,mx=it.extrema(s)
  row={'norm':name,'angular_identity_error':fe,'direct_centered_derivative':derivative,'fourier_stress_derivative':prediction,'derivative_error':abs(derivative-prediction),'rotation_covariance_error':err(rt,rp),'scaling_error':err(st,sp),'stress':t,'sampled_min':mn,'sampled_max':mx}
  reports.append(row)
  if fe>2e-7:fail.append(name+': angular identity')
  if abs(derivative-prediction)>2e-5:fail.append(name+': first variation')
  if err(rt,rp)>2e-7:fail.append(name+': rotation')
 rerr=err(it.stress(lambda x,y:1.9*abs(x)),[[1.9**2,0.],[0.,-1.9**2]])
 qerr=err(it.stress(norms['quadratic_offdiag']),[[3-.8,1.4],[1.4,.8-3]])
 balanced={n:op(it.stress(norms[n])) for n in ('l1_fourfold','linf_fourfold')}
 if rerr>1e-10:fail.append('rank-one exact stress')
 if qerr>1e-10:fail.append('quadratic exact stress')
 if max(balanced.values())>1e-10:fail.append('fourfold stress')
 # Exact variable-field check: u=(x²,y²), V=(x(1-x²)(1-y²),0), square [-1,1]².
 # Differentiate direct energy, including G(phi_t), versus fixed-field stress.
 direct=integrate({(2,0):16,(2,2):-16,(4,0):-32,(4,2):32})
 fixed=integrate({(2,0):4,(2,2):8,(4,0):-12,(4,2):12,(0,2):-4,(0,4):4,(2,4):-12})
 if direct!=Fraction(-128,45) or direct!=fixed:fail.append('variable-field exact rational variation')
 s=norms['quadratic_offdiag'];m=mats[0];e=it.direct(s,m)
 bad_power=abs(e-it.inverse(s,m,power=2));bad_det=abs(e-it.inverse(s,m,det_power=1))
 if bad_power<.01 or bad_det<.01:fail.append('negative controls did not detect mutation')
 lo=math.sqrt(17)-4;Q=4+math.sqrt(17);ce=abs(lo*Q-1)
 if ce>1e-14:fail.append('constant reciprocal')
 result={'utc':datetime.now(timezone.utc).isoformat(),'standard_library_only':True,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'samples':a.samples,'candidate_code_imported':False,'interpretation':'Numerical controls supplement, not replace, analytic proof. No Sobolev/PDE fact is certified by quadrature.','norm_controls':reports,'rank_one_exact_error':rerr,'quadratic_exact_error':qerr,'balanced_fourfold_stress_operator_norms':balanced,'variable_field_control':{'domain':'[-1,1]^2','u':'(x^2,y^2)','V':'(x(1-x^2)(1-y^2),0)','direct_exact':str(direct),'fixed_field_exact':str(fixed),'purpose':'Detect omitted composition/variable-field terms'},'negative_controls':{'wrong_inverse_length_exponent_error':bad_power,'wrong_determinant_exponent_error':bad_det},'constant':{'Q':Q,'minimum_ratio_lower_bound':lo,'reciprocal_error':ce},'failures':fail,'passed':not fail}
 Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'passed':not fail,'failures':fail,'max_angular_error':max(r['angular_identity_error'] for r in reports),'max_derivative_error':max(r['derivative_error'] for r in reports),'max_rotation_error':max(r['rotation_covariance_error'] for r in reports),'variable_field_control':result['variable_field_control'],'negative_controls':result['negative_controls']},indent=2))
 raise SystemExit(bool(fail))
if __name__=='__main__':main()
