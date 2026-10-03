"""Exact 8x8 uniform-quarter-flux Hessian in Q(sqrt3), with Fourier certificates."""
from gaussian_matrix import matrix,matmul,add as ga,mul as gm,conj as gc,scale,Z
from fractions import Fraction as F
import json

def qa(x,y):return(x[0]+y[0],x[1]+y[1])
def qm(x,y):return(x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qs(x,k):return(x[0]*k,x[1]*k)
def ca(x,y):return tuple(a+b for a,b in zip(x,y))
def cm(x,y):
 re=qa(qm(x[:2],y[:2]),qs(qm(x[2:],y[2:]),-1));im=qa(qm(x[:2],y[2:]),qm(x[2:],y[:2]));return re+im

def gaussian_times(x,z):return tuple(z[0]*a-z[1]*b for a,b in zip(x[:2],x[2:]))+tuple(z[1]*a+z[0]*b for a,b in zip(x[:2],x[2:]))
COEFFICIENTS=[[(12,-8),(18,-10),(0,2),(-3,1)],[(12,8),(-18,-10),(0,-2),(3,1)],[(12,8),(18,10),(0,-2),(-3,-1)],[(12,-8),(-18,10),(0,2),(3,-1)]]

def compute(check):
 L=8;N=64
 u={(x,y):2*int(x==L-1) for x in range(L) for y in range(L)}
 v={(x,y):(x+2*int(y==L-1))%4 for x in range(L) for y in range(L)}
 T=matrix(L,u,v);T2=matmul(T,T);T3=matmul(T2,T);T4=matmul(T2,T2);I=[[(int(i==j),0) for j in range(N)] for i in range(N)]
 for i in range(N):
  for j in range(N):check(ga(ga(T4[i][j],scale(T2[i][j],-8)),scale(I[i][j],4))==Z)
 powers=[I,T,T2,T3];projections=[]
 # Each stored entry is the numerator of the true spectral projector, divided by48.
 for co in COEFFICIENTS:
  P=[]
  for i in range(N):
   row=[]
   for j in range(N):
    z=(0,0,0,0)
    for (a,b),power in zip(co,powers):
     c,d=power[i][j];z=ca(z,(a*c,b*c,a*d,b*d))
    row.append(z)
   P.append(row)
  projections.append(P)
 # Polynomial orthogonality modulo t^4-8t^2+4, without dense field matrix products.
 for k,A in enumerate(COEFFICIENTS):
  for l,B in enumerate(COEFFICIENTS):
   C=[(0,0)]*7
   for i,a in enumerate(A):
    for j,b in enumerate(B):C[i+j]=qa(C[i+j],qm(a,b))
   for d in range(6,3,-1):C[d-2]=qa(C[d-2],qs(C[d],8));C[d-4]=qa(C[d-4],qs(C[d],-4))
   check(C[:4]==[qs(a,48) for a in A] if k==l else C[:4]==[(0,0)]*4)
 for d in range(4):check(tuple(sum(c[d][j] for c in COEFFICIENTS) for j in range(2))==((48,0) if d==0 else (0,0)))
 for co,eigen in zip(COEFFICIENTS,[(-1,-1),(1,-1),(-1,1),(1,1)]):
  shifted=[(0,0)]+co[:];shifted[0]=qa(shifted[0],qs(shifted[4],-4));shifted[2]=qa(shifted[2],qs(shifted[4],8));check(shifted[:4]==[qm(a,eigen) for a in co])
 for P in projections:check(tuple(sum(P[i][i][j] for i in range(N)) for j in range(4))==(48*16,0,0,0))
 edges=[];Ks=[]
 for y in range(L):
  for x in range(L):
   a=x+L*y
   for b in [((x+1)%L)+L*y,x+L*((y+1)%L)]:
    edges.append((a,b));z=gm((0,1),T[a][b]);Ks.append([(a,b,z),(b,a,gc(z))])
 P0=projections[0];H=[]
 for e,Ke in enumerate(Ks):
  row=[]
  for f,Kf in enumerate(Ks):
   z=(1728,1728) if e==f else (0,0)
   for P,weight in zip(projections[1:],[(6,0),(0,2),(-3,3)]):
    total=(0,0,0,0)
    for a,b,k in Ke:
     for c,d,l in Kf:total=ca(total,gaussian_times(cm(P0[d][a],P[b][c]),gm(k,l)))
    z=qa(z,qs(qm(total[:2],weight),-1))
   row.append(z)
  H.append(row)
 # H is the true Hessian multiplied by13824.
 for e in range(128):
  se,oe=divmod(e,2);xe,ye=se%L,se//L
  for f in range(128):
   sf,of=divmod(f,2);xf,yf=sf%L,sf//L
   check(H[e][f]==H[f][e]);check(H[e][f]==H[oe][2*((xf-xe)%L+L*((yf-ye)%L))+of])
 # All vertex-gauge directions are in the exact kernel.
 for e in range(128):
  for a in range(N):
   z=(0,0)
   for f,(tail,head) in enumerate(edges):
    if head==a:z=qa(z,H[e][f])
    if tail==a:z=qa(z,qs(H[e][f],-1))
   check(z==(0,0))
 cos=[(2,0),(0,1),(0,0),(0,-1),(-2,0),(0,-1),(0,0),(0,1)]
 sin=[(0,0),(0,1),(2,0),(0,1),(0,0),(0,-1),(-2,0),(0,-1)]
 traces=[];D=10**15;roots=[(1414213562373095,1414213562373096,2),(1732050807568877,1732050807568878,3),(2449489742783178,2449489742783179,6)]
 for lo,hi,k in roots:check(lo*lo<k*D*D<hi*hi)
 for ky in range(L):
  for kx in range(L):
   real=[0]*4;imag=[0]*4
   for y in range(L):
    for x in range(L):
     A,B=qa(H[0][2*(x+L*y)],H[1][2*(x+L*y)+1]);index=(kx*x+ky*y)%8
     for dst,ph in [(real,cos[index]),(imag,sin[index])]:
      a,b=ph
      for i,t in enumerate([A*a,A*b,B*a,B*b]):dst[i]+=t
   check(imag==[0]*4)
   lower=real[0]*D
   for coeff,(lo,hi,k) in zip(real[1:],roots):lower+=coeff*(lo if coeff>=0 else hi)
   check(lower>0)
   delta=[real[0]+3456,real[1],real[2]-2688,real[3]];delta_lower=delta[0]*D
   for coeff,(lo,hi,k) in zip(delta[1:],roots):delta_lower+=coeff*(lo if coeff>=0 else hi)
   check(delta==[0]*4 or delta_lower>0)
   traces.append(dict(kx=kx,ky=ky,numerator=real,denominator=27648,strict_lower_numerator=lower,strict_lower_denominator=27648*D))
 zero_block=[[tuple(sum(H[o][2*s+oo][j] for s in range(N)) for j in range(2)) for oo in range(2)] for o in range(2)]
 check(zero_block==[[(-864,672),(0,0)],[(0,0),(-864,672)]])
 # First derivative vanishes: every nearest-neighbor projector entry is-a T/16.
 for a,b in edges:
  expected=gaussian_times((-3,-3,0,0),T[a][b]);check(P0[a][b]==expected)
 return dict(fourier_trace_certificates=traces,zero_mode_hessian_scaled=zero_block,hessian_scale=13824,physical_dimension=65,gauge_kernel_dimension=63)

if __name__=='__main__':
 count=0
 def check(x):
  global count
  assert x;count+=1
 result=compute(check);result['assertions']=count
 print(json.dumps(result,indent=2,sort_keys=True))
