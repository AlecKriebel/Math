from fractions import Fraction as Q
from itertools import permutations
import json, platform

if not __debug__:
    raise RuntimeError("Curvature verifier requires enabled assertions; do not run with -O.")

# Independent exact sparse ring Q[s,t], no CAS and no numerical thresholds.
class P:
    def __init__(self, data=0):
        self.d = {k:Q(v) for k,v in data.items() if v} if isinstance(data,dict) else ({(0,0):Q(data)} if data else {})
    def __add__(self,o):
        o=o if isinstance(o,P) else P(o)
        d=self.d.copy()
        for k,v in o.d.items(): d[k]=d.get(k,0)+v
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+-o if isinstance(o,P) else self+(-P(o))
    def __rsub__(self,o): return P(o)+(-self)
    def __mul__(self,o):
        o=o if isinstance(o,P) else P(o)
        d={}
        for (a,b),u in self.d.items():
            for (c,e),v in o.d.items():
                k=(a+c,b+e);d[k]=d.get(k,0)+u*v
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=P(1)
        for _ in range(n): out=out*self
        return out
    def at(self,s,t): return sum(v*s**i*t**j for (i,j),v in self.d.items())
    def zero(self): return not self.d
    def show(self): return {str(k):str(v) for k,v in sorted(self.d.items())}
def matzero(A): return all(x.zero() for row in A for x in row)
def det(A):
    n=len(A);out=P()
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=P(sign)
        for i in range(n): term=term*A[i][perm[i]]
        out=out+term
    return out
s=P({(1,0):1}); t=P({(0,1):1});r=s+1
# Differentiated p=x*y**2-z**3 first, without using any displayed M entries:
p_i=[P(1),2*r,P(-3)]
p_ij=[[P(0),P(2),P(0)],[P(2),2*r,P(0)],[P(0),P(0),P(-6)]]
h=[t**3,P(1),t]
p_h=sum((p_i[k]*h[k] for k in range(3)),P())
p_ih=[sum((p_ij[i][k]*h[k] for k in range(3)),P()) for i in range(3)]
p_ijh=[[P(0),P(2),P(0)],[P(2),2*t**3,P(0)],[P(0),P(0),-6*t]]
M=[[2*p_i[i]*p_i[j]*p_h-s*(p_ih[i]*p_i[j]+p_i[i]*p_ih[j]+p_ij[i][j]*p_h)+s**2*p_ijh[i][j]+(2*s**3*t if i==j==2 else 0) for j in range(3)] for i in range(3)]
nc11=2*(t-1)**2*(t+2)
nc12=2*(t-1)*(2*t**2+2*t-1-3*r)
nc13=6*(t-1)*(r-t**2-t+1)
nc22=4*r**3+12*r**2-18*r**2*t+6*r*t**3-6*r*t+2*t**3
nc23=12*r**2*t-18*r**2-6*r*t**3+24*r*t-6*r-6*t**3
nc33=6*(r+2)*t**3+2*(r**3-6*r**2-18*r-4)*t+12*r*(r+2)
claimed=[[nc11,nc12,nc13],[nc12,nc22,nc23],[nc13,nc23,nc33]]
residual=[[M[i][j]-claimed[i][j] for j in range(3)] for i in range(3)]
assert matzero(residual)
Ppoly=2*(t+2)*s**2-3*(t-1)*(3*t+5)*s+3*(t-1)**2*(t+2)**2
Rpoly=(t+2)*(2*t*s**2-3*(t-1)*(3*t+1)*s+3*(t-1)**2*(t**2+4*t+1))
minor=M[0][0]*M[1][1]-M[0][1]**2
NC2=minor-4*s*(t-1)**2*Ppoly
NC3=det(M)-8*s**4*(t-1)**2*Rpoly
NC4=8*(t+2)*Ppoly-(4*(t+2)*s-3*(t-1)*(3*t+5))**2-3*(t-1)**2*(8*t**3+21*t**2+6*t-11)
# NC5 is checked after clearing its harmless t+2 denominator:
NC5=8*t*Rpoly-(t+2)*((4*t*s-3*(t-1)*(3*t+1))**2+3*(t-1)**3*(8*t**2+13*t+3))
for item in [NC2,NC3,NC4,NC5]: assert item.zero()
# t=1 identity; evaluate only the t variable, retaining the s polynomial.
def t_at(A,v):
    return [[P({(i,0):sum(w*Q(v)**j for (ii,j),w in x.d.items() if ii==i) for i in set(k[0] for k in x.d)}) for x in row] for row in A]
M1=t_at(M,1)
expected1=[[P(),P(),P()],[P(),2*s**2*(2*r+1),-6*s**2],[P(),-6*s**2,2*s**2*(r+2)]]
assert matzero([[M1[i][j]-expected1[i][j] for j in range(3)] for i in range(3)])
# Leading t^3 coefficient equals direction e_x by linearity.
Ex=[[P({(i,0):v for (i,j),v in x.d.items() if j==3}) for x in row] for row in M]
a=[1,2,-3];b=[0,1,-1]
Excert=[[P(2*a[i]*a[j])+6*s*b[i]*b[j] for j in range(3)] for i in range(3)]
assert matzero([[Ex[i][j]-Excert[i][j] for j in range(3)] for i in range(3)])
assert all(sum((Ex[i][j] for j in range(3)),P()).zero() for i in range(3))
# Independent rational grid exercises coefficient evaluation and exact Sylvester tests.
grid_s=[Q(1,100),Q(1,3),Q(1),Q(3),Q(100)]
grid_t=[Q(0),Q(1,100),Q(1,2),Q(99,100),Q(1),Q(101,100),Q(2),Q(10),Q(100)]
count=0
for ss in grid_s:
    for tt in grid_t:
        mm=[[x.at(ss,tt) for x in row] for row in M]
        if tt==1:
            assert mm[0]==[0,0,0] and mm[1][1]>0 and mm[2][2]>0 and mm[1][1]*mm[2][2]-mm[1][2]**2>0
        else:
            assert mm[0][0]>0 and minor.at(ss,tt)>0 and det(M).at(ss,tt)>0
        count+=1
# Negative control: changing sign of entire curvature matrix is detected at r=2,t=0.
# Negative control: direction h=(-1,1,-1) is outside K; extending t to -1 violates PSD.
bad_sign_leading=-M[0][0].at(Q(1),Q(0))
outside_det=det(M).at(Q(1),Q(-1))
assert bad_sign_leading<0 and outside_det<0
results = {
 "python":platform.python_version(),
 "method":"stdlib fractions; independently differentiated log via p tensor; exact sparse Q[s,t]",
 "NC1_entries_zero":9,
 "NC2_NC3_NC4_NC5_residuals_zero":True,
 "t1_matrix_identity":True,
 "ex_endpoint_gram_identity":True,
 "ex_kernel_ones":True,
 "rational_grid_cases":count,
 "wrong_sign_control_M11":str(bad_sign_leading),
 "outside_cone_control_r2_tminus1_det":str(outside_det),
 "independent_M_at_r2_t0":[[str(x.at(Q(1),Q(0))) for x in row] for row in M],
 "independent_Ex_at_r2":[[str(x.at(Q(1),Q(0))) for x in row] for row in Ex]
}

# A second derivative mechanism: exact bivariate line expansion, with no p tensor.
# [epsilon*eta^2] f(q+epsilon*h+eta*u) = D^3 f[h,u,u]/2.
eps=P({(1,0):1}); eta=P({(0,1):1})
series_cases=0
for ss in grid_s:
    for tt in grid_t:
        rr=ss+1; hh=[tt**3,Q(1),tt]
        for uu in [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[2,-3,5]]:
            xx=P(rr)+eps*hh[0]+eta*uu[0]
            yy=P(1)+eps*hh[1]+eta*uu[1]
            zz=P(1)+eps*hh[2]+eta*uu[2]
            dp=(xx*yy**2-zz**3-ss)*Q(1,ss)
            dz=zz-1
            minus_log_p=-dp+Q(1,2)*dp**2-Q(1,3)*dp**3
            minus_log_z=-dz+Q(1,2)*dz**2-Q(1,3)*dz**3
            D3=2*(minus_log_p+minus_log_z).d.get((1,2),Q(0))
            matrix_quad=sum(uu[i]*M[i][j].at(ss,tt)*uu[j] for i in range(3) for j in range(3))
            assert -ss**3*D3==matrix_quad
            series_cases+=1
results["independent_bivariate_logarithm_series_contractions"] = series_cases

# Concrete outside-cone failure; q=(2,1,1), h=(-1,1,-1), u=(5,1,2).
uu=[5,1,2]
outside_quad=sum(uu[i]*M[i][j].at(Q(1),Q(-1))*uu[j] for i in range(3) for j in range(3))
assert outside_quad==Q(-2)
# The -log(z) term is needed for this negative curvature certificate too.
# Dropping it gives M0=M-2*s^3*t E33 and a negative determinant at r=5,t=2.
M0=[[M[i][j]-(2*s**3*t if i==j==2 else 0) for j in range(3)] for i in range(3)]
M0det=det(M0).at(Q(4),Q(2))
assert M0det==Q(-24576)
results["outside_cone_control_r2_tminus1_u5_1_2_quadratic"] = str(outside_quad)
results["omitted_log_z_control_r5_t2_det"] = str(M0det)
print(json.dumps(results, indent=2, sort_keys=True))
