#!/usr/bin/env python3
"""Independent finite audit controls, not a proof of Problem 6.111."""
from pathlib import Path
import hashlib, json, math, random, platform
from fractions import Fraction
import numpy as np
import mpmath as mp

ROOT=Path(__file__).resolve().parent
SUB=ROOT.parent/'submission'
rng=random.Random(6111590)
mp.mp.dps=60
out={'problem_id':2306111,'purpose':'Independent verification of displayed partial deductions and existing finite search outputs; no new proof search.','versions':{'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__},'checks':{}}
M=json.loads((SUB/'SHA256SUMS.json').read_text())
errs=[]
for name,row in M['files'].items():
 data=(SUB/name).read_bytes()
 if hashlib.sha256(data).hexdigest()!=row['sha256'] or len(data)!=row['bytes']: errs.append(name)
assert not errs
out['checks']['frozen_manifest']={'sha256':hashlib.sha256((SUB/'SHA256SUMS.json').read_bytes()).hexdigest(),'file_count':len(M['files']),'mismatches':errs}

# Construct the real matrix itself rather than using the author's sigma function.
sv_gap=0.;gram_gap=0.;witness_residual=0.
for _ in range(5000):
 d=complex(rng.uniform(-3,3),rng.uniform(-3,3));q=complex(rng.uniform(-3,3),rng.uniform(-3,3))
 col=-2j*q
 matrix=np.array([[d.real,col.real],[d.imag,col.imag]])
 u,sv,vh=np.linalg.svd(matrix)
 gram=matrix.T@matrix
 analytic=np.array([[abs(d)**2,-2*(d*q.conjugate()).imag],[-2*(d*q.conjugate()).imag,4*abs(q)**2]])
 gram_gap=max(gram_gap,float(np.max(abs(gram-analytic))))
 a=abs(d)**2;b=4*abs(q)**2
 displayed=math.sqrt(max(0.,(a+b-math.sqrt((a-b)**2+16*(d*q.conjugate()).imag**2))/2))
 sv_gap=max(sv_gap,abs(displayed-sv[-1]))
 cos,sin=vh[-1]
 z=complex(rng.uniform(.1,.6),rng.uniform(.1,.6))
 L=cos*d-2j*sin*q
 c=-L/(2*z*complex(cos,-sin))
 witness=cos*(d+2*c*z)-2j*sin*(q+c*z)
 witness_residual=max(witness_residual,abs(witness))
 assert abs(witness)<1e-13
 assert abs(2*abs(c)-sv[-1]/abs(z))<1e-12
assert sv_gap<1e-9 and gram_gap<1e-12
out['checks']['5000_direct_matrix_and_witness_checks']={'max_gram_entry_gap':gram_gap,'max_singular_value_gap':sv_gap,'max_witness_residual':witness_residual}

# The equality model f=z distinguishes boundary equality from interior failure.
for r in [Fraction(1,10),Fraction(1,2),Fraction(999,1000)]:
 assert 1>r # sigma_z=1, eta=1; equality is never reached inside D.
 eta=1/r;c=-1/(2*r)
 assert 2*abs(c)==eta and 1+2*c*r==0
out['checks']['closed_ball_boundary_and_quadratic_failure']={'identity_center_radius':1,'boundary_equality_not_interior_failure':True,'interior_exact_witness_at_eta_1_over_r':True}

# Independently check the radial primitive and logarithmic derivative by high-precision differentiation.
pairs=[('-0.999','-1'),('0','-1'),('1','-1'),('0.4','0'),('0.1','-0.00000001'),('0.1','0.00000001'),('1','0.999'),('0.9001','0.9'),('-0.93','-0.94')]
max_p=mp.mpf(0)
for As,Bs in pairs:
 A,B=mp.mpf(As),mp.mpf(Bs)
 def deriv(z): return mp.exp(A*z) if not B else mp.exp((A-B)/B*mp.log(1+B*z))
 delta=mp.exp(-A) if not B else mp.exp((A-B)/B*mp.log(1-B))
 for zs in ['-0.99','-0.3','0.4']:
  z=mp.mpf(zs)
  p=1+z*mp.diff(deriv,z)/deriv(z)
  residual=abs(p-(1+A*z)/(1+B*z));max_p=max(max_p,residual)
  assert residual<mp.mpf('1e-50')
  r=abs(z);mr=deriv(-r)
  assert mr>delta>r*delta
  delta_scaled=mp.exp(-r*A) if not B else mp.exp((A-B)/B*mp.log(1-r*B))
  assert abs(delta_scaled-mr)<mp.mpf('1e-50')
out['checks']['27_high_precision_extremal_and_scaling_checks']={'maximum_p_residual':str(max_p),'includes_B_zero_small_signed_B_A_zero_and_near_parameter_endpoints':True}
eta=Fraction(3,5)
lo,hi=Fraction(4,5),Fraction(9,10)
assert 1/(1+lo)-eta*lo>0 and 1/(1+hi)-eta*hi<0
out['checks']['exact_rational_loss_of_local_univalence']={'A':0,'B':-1,'eta':'3/5','root_bracket':['4/5','9/10']}

# At the EXISTING stored optimizer points, replace Gaussian quadrature with mp.quad.
rows=json.loads((SUB/'FINITE_SEARCH_RESULTS.json').read_text())['rows']
rechecks=[]
for row in rows:
 b,beta=mp.mpf(str(row['b'])),mp.mpf(str(row['beta']))
 x=list(map(lambda v:mp.mpf(str(v)),row['parameters']))
 raw=[x[3],x[4],mp.mpf(1)];w=[v/sum(raw) for v in raw]
 uu=[mp.exp(1j*v) for v in x[:3]]
 def integrand(t): return mp.exp(-beta*sum(ww*mp.log(1-b*u*t) for ww,u in zip(w,uu)))
 d=integrand(1);q=mp.quad(integrand,[0,1]);a=abs(d)**2;c=4*abs(q)**2
 smaller=(a+c-mp.sqrt((a-c)**2+16*mp.im(d*mp.conj(q))**2))/2
 ratio=mp.sqrt(smaller)*(1+b)**beta
 gap=abs(ratio-mp.mpf(str(row['recheck_ratio_256'])))
 assert gap<mp.mpf('1e-12')
 rechecks.append({'b':float(b),'beta':float(beta),'ratio_60_digit':str(ratio),'absolute_gap_from_256':str(gap)})
out['checks']['existing_15_search_points_independently_rechecked']=rechecks
out['result']='PASS'
out['limitations']='Finite controls and non-interval 60-digit evaluation only. No global optimization certificate, complete starlikeness proof, or literature resolution certificate.'
(ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'result':out['result'],'checks':list(out['checks']),'file':'INDEPENDENT_RESULTS.json'},indent=2))
