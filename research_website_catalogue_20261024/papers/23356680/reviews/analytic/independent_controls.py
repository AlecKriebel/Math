"""Fresh controls, not imported from the publication's historical review suites.
Exact polynomial controls use Fraction. Angular quadrature is diagnostic only.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import cos,sin,pi,sqrt
import json
import numpy as np
ROOT=Path(__file__).resolve().parent

def mul(a,b):
 c={}
 for (i,j),x in a.items():
  for (k,l),y in b.items(): c[i+k,j+l]=c.get((i+k,j+l),Q(0))+x*y
 return c

def der(a,k):
 c={}
 for ij,v in a.items():
  if ij[k]:
   j=list(ij);j[k]-=1;c[tuple(j)]=v*ij[k]
 return c

def integ(a,ta=Q(0),tb=Q(1),xa=Q(0),xb=Q(1)):
 return sum(v*(tb**(i+1)-ta**(i+1))/(i+1)*(xb**(j+1)-xa**(j+1))/(j+1) for (i,j),v in a.items())

# Independent exact weak-Dirichlet identity for a zero-trace polynomial.
w={(1,1):Q(1),(2,1):Q(-1),(1,2):Q(-1),(2,2):Q(1)}
dt,dx=der(w,0),der(w,1)
cross=2*integ(dx);gap=integ(mul(dt,dt))+integ(mul(dx,dx))
assert cross==0 and gap==Q(1,45)
# Exact KS first variation and its integration-by-parts counterpart on a flat subrectangle.
lo,hi=Q(1,16),Q(1,8)
p=mul({(1,0):Q(1),(0,0):-lo},{(1,0):Q(1),(0,0):-lo})
p=mul(p,mul({(0,0):hi,(1,0):Q(-1)},{(0,0):hi,(1,0):Q(-1)}))
p=mul(p,{(0,2):Q(1),(0,3):Q(-2),(0,4):Q(1)})
first=2*integ(mul({(2,0):Q(1)},der(p,0)),lo,hi)
parts=-4*integ(mul({(1,0):Q(1)},p),lo,hi)
assert first==parts and first<0
# Exact fourth-circle moment formula for arbitrary symmetric inner product matrices.
# E[w_i^4]=3/8, E[w_i^2 w_j^2]=1/8, all odd moments vanish.
moment_checks=[]
for g11,g12,g22 in [(Q(4),Q(1),Q(2)),(Q(1),Q(0),Q(0)),(Q(3),Q(0),Q(3))]:
 energy=g11+g22
 t11=8*(g11*Q(3,8)+g22*Q(1,8))-2*energy
 t22=8*(g11*Q(1,8)+g22*Q(3,8))-2*energy
 t12=8*(2*g12*Q(1,8))
 assert (t11,t12,t22)==(g11-g22,2*g12,g22-g11)
 moment_checks.append({'G':[str(g11),str(g12),str(g22)],'T':[str(t11),str(t12),str(t22)]})

# Compare direct angular integrals with the changed-variable formula and compare
# finite differences of direct energy against the independently integrated stress.
# Shifted angular grids avoid giving polyhedral corners special grid status.
N=262144
ang=2*pi*(np.arange(N)+0.371)/N
W=np.stack([np.cos(ang),np.sin(ang)],axis=1)
norms={
 'quadratic':lambda x:np.sqrt(4*x[:,0]**2+2*x[:,0]*x[:,1]+2*x[:,1]**2),
 'rank_one':lambda x:np.abs(x[:,0]+0.3*x[:,1]),
 'l1':lambda x:np.abs(x[:,0])+np.abs(x[:,1]),
 'linfty':lambda x:np.max(np.abs(x),axis=1),
 'skew_polyhedral':lambda x:np.maximum.reduce([np.abs(x[:,0]),np.abs(0.2*x[:,0]+0.7*x[:,1]),np.abs(0.6*x[:,0]-0.4*x[:,1])]),
 'zero':lambda x:np.zeros(len(x))}
As=[np.array([[1.4,.2],[-.1,.7]]),np.array([[.4,.8],[-.3,1.7]])]
Ds=[np.array([[.3,.7],[-.2,-.1]]),np.eye(2),np.array([[0.,-1.],[1.,0.]])]
rows=[]
for name,norm in norms.items():
 sw2=norm(W)**2
 T=2*np.mean(sw2[:,None,None]*(4*W[:,:,None]*W[:,None,:]-2*np.eye(2)),axis=0)
 f=lambda A:float(2*np.mean(norm(W@A.T)**2)/np.linalg.det(A))
 change_errors=[];mutation_errors=[]
 for A in As:
  invw=W@np.linalg.inv(A).T
  transformed=float(2*np.mean(sw2/np.sum(invw*invw,axis=1)**2)/np.linalg.det(A)**2)
  change_errors.append(abs(f(A)-transformed))
  wrong=float(2*np.mean(sw2/np.sum(invw*invw,axis=1)**2)/np.linalg.det(A))
  mutation_errors.append(abs(f(A)-wrong))
 fd=[]
 for D in Ds:
  eps=1e-3
  measured=(f(np.eye(2)+eps*D)-f(np.eye(2)-eps*D))/(2*eps)
  expected=float(np.sum(T*D));fd.append(abs(measured-expected))
 assert max(change_errors)<2e-7,(name,change_errors)
 assert max(fd)<3e-5,(name,fd)
 if name!='zero':assert max(mutation_errors)>1e-3
 if name in ('l1','linfty','zero'):assert np.max(np.abs(T))<1e-12
 if name=='rank_one':assert np.linalg.norm(T)>1
 rows.append({'seminorm':name,'angular_formula_absolute_errors':change_errors,'direct_difference_vs_stress_absolute_errors':fd,'wrong_determinant_power_errors':mutation_errors,'stress':T.tolist()})

out={'exact_scalar_control':{'cross_term':str(cross),'positive_energy_gap':str(gap)},'exact_ks_descent':{'first_variation':str(first),'integration_by_parts':str(parts),'rectangle_t':[str(lo),str(hi)],'rectangle_x':['0','1'],'note':'Polynomial has zero trace and is W1,2; smooth compactly supported nonnegative functions give the general analytic argument.'},'exact_stress_moments':moment_checks,'angular_diagnostic':{'samples':N,'rows':rows,'not_rigorous_error_enclosures':True},'constants':{'elementary':4+sqrt(17),'classical':2*sqrt(2)+sqrt(6)},'all_controls_passed':True}
(ROOT/'independent_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_controls_passed':True,'exact_energy_gap':str(gap),'exact_ks_descent':str(first),'max_angular_error':max(max(r['angular_formula_absolute_errors']) for r in rows),'max_stress_difference_error':max(max(r['direct_difference_vs_stress_absolute_errors']) for r in rows),'negative_control':'omitting one determinant power rejected for every nonzero seminorm'},indent=2))
