"""Exact algebra and finite DDA diagnostics. The analytic proof is in CANDIDATE.md."""
import json
from itertools import product
import sympy as s
import numpy as np
exact=0
z=s.symbols('z');ii=s.I
p=s.exp(ii*z)*(1-ii*z-z*z)
q=s.exp(ii*z)*(z*z+3*ii*z-3)
assert s.series(p,z,0,4).removeO()==1-z*z/2-2*ii*z**3/3;exact+=1
assert s.series(q,z,0,4).removeO()==-3-z*z/2;exact+=1
r,k=s.symbols('r k',nonzero=True)
g=s.exp(ii*k*r)/(4*s.pi*r)
assert s.simplify(-(s.diff(g,r)/r+k*k*g)-s.exp(ii*k*r)*(1-ii*k*r-k*k*r*r)/(4*s.pi*r**3))==0;exact+=1
assert s.simplify(-(s.diff(g,r,2)-s.diff(g,r)/r)-s.exp(ii*k*r)*(k*k*r*r+3*ii*k*r-3)/(4*s.pi*r**3))==0;exact+=1
# Cubic cancellation on each complete squared-radius shell, with the common
# radial scalar factor omitted. Numerator is |j|² I - 3 j j^T.
for R in (1,2,3,4):
 shells={}
 for j in product(range(-R,R+1),repeat=3):
  t=sum(v*v for v in j)
  if not t or t>R*R:continue
  v=s.Matrix(j);shells[t]=shells.get(t,s.zeros(3))+t*s.eye(3)-3*v*v.T
 for a in shells.values():
  assert a==s.zeros(3);exact+=9
# Every cubic orbit, not merely shell averages, cancels.
from itertools import permutations
for j in ((1,0,0),(1,1,0),(1,1,1),(1,2,3),(2,2,3),(0,2,5)):
 orb=set(tuple(sign[i]*p[i] for i in range(3)) for p in permutations(j) for sign in product((-1,1),repeat=3))
 total=s.zeros(3)
 for v in orb:
  w=s.Matrix(v);total+=sum(t*t for t in v)*s.eye(3)-3*w*w.T
 assert total==s.zeros(3);exact+=9

def points(n):
 t=(np.arange(n)+.5)/n-.5
 return np.array(list(product(t,repeat=3)))

def dynamic(d,kappa):
 r=np.linalg.norm(d,axis=-1);mask=r>0
 safe=np.where(mask,r,1.0);u=d/safe[...,None];t=kappa*safe
 # Taylor cancellation is stable for these diagnostic meshes, smallest r=1/16.
 f=(np.exp(1j*t)*(1-1j*t-t*t)-1)/(4*np.pi*safe**3)
 q=(np.exp(1j*t)*(t*t+3j*t-3)+3)/(4*np.pi*safe**3)
 out=f[...,None,None]*np.eye(3)+q[...,None,None]*u[..., :,None]*u[...,None,:]
 return out*mask[...,None,None]

# Embedded Hilbert-Schmidt difference on nested uniform meshes of the unit cube.
# Each fine/fine cell product has volume (1/(2n))^6.
results=[]
for n in (2,4,8):
 fine=points(2*n);coarse_centers=(np.floor((fine+.5)*n)+.5)/n-.5
 accum=0.0;skew=0.0
 for start in range(0,len(fine),32):
  stop=start+32
  cf=dynamic(fine[start:stop,None,:]-fine[None,:,:],1+.3j)
  cc=dynamic(coarse_centers[start:stop,None,:]-coarse_centers[None,:,:],1+.3j)
  accum+=np.sum(np.abs(cf-cc)**2)
  skew=max(skew,float(np.max(np.abs(cf-cf.swapaxes(-1,-2)))))
 err=float(np.sqrt(accum/(2*n)**6))
 assert np.isfinite(err) and err>0 and skew<1e-12
 results.append({'coarse_n':n,'fine_n':2*n,'hilbert_schmidt_difference':err,'block_symmetry_error':skew})
assert all(b['hilbert_schmidt_difference']<a['hilbert_schmidt_difference'] for a,b in zip(results,results[1:]))
# The static lattice matrix is real symmetric and has exact trace zero numerators.
p=points(3);d=p[:,None,:]-p[None,:,:];r=np.linalg.norm(d,axis=-1);safe=np.where(r>0,r,1);u=d/safe[...,None]
blocks=(np.eye(3)-3*u[..., :,None]*u[...,None,:])/(4*np.pi*safe[...,None,None]**3)
blocks*= (r>0)[...,None,None]/27
mat=blocks.transpose(0,2,1,3).reshape(81,81)
assert np.max(np.abs(mat-mat.T))<1e-14
vals=np.linalg.eigvalsh(mat)
print(json.dumps({'status':'PASS','exact_assertions':exact,'dynamic_hs_diagnostics':results,'static_cube_3_extreme_eigenvalues':[float(vals[0]),float(vals[-1])],'static_matrix_symmetry_error':float(np.max(np.abs(mat-mat.T))),'limitations':'Floating-point matrix checks are diagnostics only, not interval certificates, proof of spectral convergence, or certified lattice endpoint estimates.'},indent=2))
