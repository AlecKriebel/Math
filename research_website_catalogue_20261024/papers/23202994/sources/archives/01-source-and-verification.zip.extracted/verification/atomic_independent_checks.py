"""Independent finite scalar and numerical identity audit of pinned atomic source.
Rational checks below are proof checks; floating-point identity checks are diagnostic.
"""
from fractions import Fraction as F
from pathlib import Path
import cmath, math, json, platform, sys
h,H,B=F(17,50),F(27,50),F(4,3)
# Endpoint exponents in the manuscript, excluding the common pi multiplier.
claimed=[F(100079,455650),F(8949,455650),F(216419,554650),F(105489,554650)]
actual=[k*B/(k*k+F(25,36))-v for k,v in [(h,h),(h,H),(H,h),(H,H)]]
assert actual==claimed and all(x>0 for x in actual)
# pi > 3 suffices for both continuous-frequency monotonicity arguments.
for k in [h,H]:
    assert (k*k+F(25,36))/B < 3*k
assert 3*(h*h+F(25,36))/(2*B) < 3*h
# Independent Schur/comparison arithmetic.
beta,delta,d=F(3,10**10),F(3,10**8),F(82,10**9)
errors=[]
for N,dp in [(17,F(1,10**26)+6*beta),(5,F(1,10**26)+6*beta+F(12,1000)*F(13,10**8))]:
    contraction=delta+340*beta*N
    assert contraction<1
    tail=(dp+beta*N*d)/(1-contraction)
    finite=N*(d+340*tail)
    errors.append((tail,finite))
assert sum(t for t,f in errors)/2 < F(3,10**9)
assert sum(f for t,f in errors)/2 < F(1,10**5)
for q,barrier in [(F(465,10**5),F(18,1000)),(F(23,10**6),F(324,10**6))]:
    K=F(301,100)*q+800*F(3,10**9)+F(6,1000)*F(2,1000)
    assert K<barrier
# The normalized lattice's represented residues match the advertised superset.
res=sorted({(m*m+m*n+n*n)%36 for m in range(36) for n in range(36)})
assert res==[0,1,3,4,7,9,12,13,16,19,21,25,27,28,31]
# Construct coefficients afresh by double-precision Laurent convolution.
R=res;kap=math.pi/36
poly={0:1+0j}
for a in R:
    fac={-1:-cmath.exp(1j*math.pi*a/18),0:2+0j,1:-cmath.exp(-1j*math.pi*a/18)}
    out={}
    for j,u in poly.items():
        for k,v in fac.items():out[j+k]=out.get(j+k,0j)+u*v
    poly=out
Pj=[poly[j] for j in range(16)]
def prod(s):return math.prod((2*math.sin(kap*(s-a)))**2 for a in R)
def spec_col(n,s,kind):
    ans=0j
    for j in range(16):
        vals=[Pj[l]*cmath.exp(1j*math.pi*(l-j)*n/18) for l in range(j+1,16)]
        if kind=='c':z=-4*kap*kap*sum((idx+1)*v for idx,v in enumerate(vals))
        else:z=1j*kap*(Pj[j]+2*sum(vals))
        ans+=(2 if j else 1)*z*cmath.exp(1j*math.pi*j*s/18)
    return ans.real
errors_num=[]
for n in [0,1,3,7,21,36]:
    for s in [.25,.7,2.25,5.8,11.3,22.5,33.2,40.3]:
        for kind in ['c','d']:
            direct=(kap*kap*prod(s)/math.sin(kap*(s-n))**2 if kind=='c' else kap*prod(s)/math.tan(kap*(s-n)))
            spect=spec_col(n,s,kind)
            err=abs(direct-spect)/(1+abs(direct))
            assert err<2e-7,(n,s,kind,direct,spect,err)
            errors_num.append(err)
result={'scope':'Independent rational scalar proof checks and floating-point spectral identity diagnostics; not a global analytic proof or formal verification.', 'python':sys.version,'platform':platform.platform(),'residues':res,'fourier_endpoint_exponents':[str(x) for x in actual],'schur_errors':[[str(t),str(f)] for t,f in errors],'numeric_identity_tests':len(errors_num),'numeric_max_normalized_absolute_error':max(errors_num)}
print(json.dumps(result,indent=2))
