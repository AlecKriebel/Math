#!/usr/bin/env python3
"""Independent rational reconstruction of Appendix A, without supplied helpers."""
from pathlib import Path
from datetime import datetime,timezone
from math import comb
from fractions import Fraction as F
import sympy as s,json,hashlib,time
R=s.Rational;checks=[];details={};start=time.time()
def ck(x,label):
 if not x:raise AssertionError(label)
 checks.append(label)
def dseq(N):
 c=R(2**N-1,N*2**(N-1));d=[s.S.Zero]*(N+1)
 for k in range(1,N):d[k]=(2*N*(R(1,k)-c)+(k-1)*d[k-1])/(N-k)
 return d
std_expected=[R(24,11),R(261,40),R(343400,28657),R(2268275,128288),R(5758562957,248448224),R(141339691089527,4988552903680),R(15468663676289,466560376100),R(19782952499295763,524622207176704)]
for N in range(2,10):
 states=[('P',k) for k in range(1,N)]+[('R',k) for k in range(1,N)]+[('Q',k) for k in range(1,N+1)];idx={p:i for i,p in enumerate(states)};H=s.zeros(len(states));d=dseq(N);sigma=s.zeros(1,len(states));gamma=s.zeros(len(states),1)
 def put(x,y,z):
  if y in idx:H[idx[x],idx[y]]+=z
 for k in range(1,N):
  for y,z in [(('P',k),R(k,2*N)),(('P',k+1),R(N-k-1,2*N)),(('Q',k+1),R(1,2*N))]:put(('P',k),y,z)
  for y,z in [(('R',k),R(k,2*N)+R((k-1)*(N-k),2*k*N)),(('R',k+1),R(N-k-1,2*N)),(('R',k-1),R((k-1)**2,2*k*N)),(('Q',k),R(1,2*k*N)),(('P',k-1),R(k-1,2*k*N)),(('P',k),R(N-k,2*k*N))]:put(('R',k),y,z)
  gamma[idx['P',k]]=k*d[k];gamma[idx['R',k]]=N*d[k]+R((N+1)*(k-1),k)*d[k-1];sigma[idx['R',k]]=R(comb(N-2,k-1),2**(N-2))
 for k in range(1,N+1):
  for y,z in [(('Q',k),R(k*k-1,2*k*N)),(('Q',k+1),R(N-k,2*N)),(('P',k-1),-R(k-1,2*k*N)),(('P',k),-R(N-k,2*k*N)),(('R',k-1),-R((k-1)**2,2*k*N)),(('R',k),-R((k-1)*(N-k),2*k*N))]:put(('Q',k),y,z)
  gamma[idx['Q',k]]=-(N-k)*d[k]-R((N+1)*(k-1),k)*d[k-1]
 phi=(sigma*(s.eye(len(states))-H).inv(method='DM')*gamma)[0];ck(phi==std_expected[N-2],f'standard exact residual N{N}')
 details['standard_'+str(N)]=str(phi)
# Direct symmetric quotient solve for every finite closure order.
for N in range(3,40):
 aa=[('a',k) for k in range(1,N)];bb=[('b',k) for k in range(2,N)];st=aa+bb;idx={x:i for i,x in enumerate(st)};H=s.zeros(len(st));src=s.zeros(len(st),1);g=s.zeros(len(st),1);d=dseq(N)
 def put(x,y,z):
  if y in idx:H[idx[x],idx[y]]+=z
 for k in range(1,N):
  put(('a',k),('a',k),R(k,2*N));put(('a',k),('a',k-1),R(N-k,2*N));src[idx['a',k]]=d[k]/2;g[idx['a',k]]=R(comb(N-2,k-1),2**(N-1)*(N+1))
 for k in range(2,N):
  put(('b',k),('b',k),R(N*(k-2)+k,2*k*N));put(('b',k),('b',k-1),R(N-k-1,2*N));put(('b',k),('b',k+1),R(k*(k-1),2*(k+1)*N));put(('b',k),('a',k-1),-R(1,N));put(('a',k-1),('b',k),R(k-1,2*k*N));put(('a',k),('b',k),R(N-k,2*k*N));src[idx['b',k]]=d[k-1]/(2*k);g[idx['b',k]]=-R(comb(N-3,k-2),2**(N-2)*(N+1))
 val=(src.T*(s.eye(len(st))-H).inv(method='DM')*g)[0];ck(val>0,f'symmetric exact solve N{N}')
 if N in (3,4):ck(val=={3:R(3,208),4:R(359,26660)}[N],f'symmetric table N{N}')
 details['symmetric_'+str(N)]=str(val)
print('direct all finite sector solves complete',flush=True)
minimum=None;argmin=None
for N in range(40,288):
 tt={1:F(2*N,2*N-1)}
 for j in range(2,N):tt[j]=(2*N+(j-1)*tt[j-1])/(2*N-j)
 ell=lambda j:F(3*N*j+3*N-8*j-10,3*N*j*(j+1))
 beta=max(F(4*(j+2),3*(j+1)*(N-2))/(F(11,25)*ell(j)*tt[j]) for j in range(1,N-1));c=F(2*N-5,2*N*(N-2));eps=F(25,11)*c/(1-c);gap=1-beta-eps
 ck(gap>0,f'symmetric phase finite margin N{N}')
 if minimum is None or gap<minimum:minimum=gap;argmin=N
ck(argmin==40 and minimum==F(639304267467075678841,115369588296792467144716),'exact stated finite minimum');details['minimum_margin']={'N':argmin,'value':str(minimum)}
# Independent exact discriminants certify the two cubic sign tails.
N,k,M=s.symbols('N k M',integer=True)
P=21*N*N*k+14*N*N-64*N*k*k-57*N*k+50*k**3+36*k*k-14*k
pc=s.Poly(s.expand((-s.discriminant(P,k)/8).subs(N,25+M)),M).all_coeffs();ck(pc==[5733,736211,37934833,982793213,12893444604,70866894144,41021531998],'P discriminant coefficient list');ck(min([P.subs({N:24,k:j}) for j in range(2,24)])==24,'P N24 exact endpoint range')
G=1881*N*N*k+1881*N*N-6250*N*k*k-21278*N*k-10032*N+6000*k**3+12000*k*k+10032*k+12540
gc=s.Poly(s.expand((-s.discriminant(G,k)/500).subs(N,288+M)),M).all_coeffs();ck(gc==[43034652243,71940715263252,50075984929826764,18577025353519361184,3873653773133773223808,430447522448513182675968,19913301794000751100222464],'G discriminant coefficient list')
ck(all(c>0 for c in s.Poly(s.expand(G.subs({k:0,N:M+288})),M).all_coeffs()),'G constant positive all tail orders')
# Reconstruct standard barrier polynomial using only d lower/upper bounds.
a,m=s.symbols('a m',integer=True)
Ak=(k-1)*(3*k*N-2*k*k-k+2)/k**2;Bk=(3*k+1)*(N-k)/(k+1)
bound=Ak*2*(N-2)/(N*(k-1))-Bk*2/k
poly=s.cancel(bound*N*k*k*(k+1)/2);shift=s.expand(poly.subs({N:a+3+m,k:a+3}))
expected=a**4+a**3*m+10*a**3+5*a*a*m+37*a*a+60*a+2*a*m*(m-1)+6*m*m-22*m+32
ck(s.expand(shift-expected)==0,'standard W barrier polynomial reconstructed');ck(s.discriminant(6*m*m-22*m+32,m)==-284,'standard residual quadratic strict')
# rank-Poisson identity and bounds across distinct finite orders (analytic proof separate).
for NN in range(2,81):
 dd=dseq(NN)
 for kk in range(1,NN):
  ck(2/R(kk)-dd[kk]==R(2**max(0,2-NN),2**max(0,NN-2))*sum(comb(NN-1,j) for j in range(kk,NN))/((NN-1)*comb(NN-2,kk-1)),f'Poisson closed form N{NN}k{kk}')
  ck(R(2*(NN-2),NN*kk)<=dd[kk]<=R(2,kk) and dd[kk]>dd[kk+1],f'Poisson order bounds N{NN}k{kk}')
res={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'labels':checks,'details':details,'seconds':time.time()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Fresh AppendixA quotient solves for all finite closure orders, exact248 phase margins, both discriminant tails and standard barrier polynomial; no published helper import. Finite Poisson controls corroborate separate all-order derivation.'}
Path(__file__).with_name('fresh_phase_results.json').write_text(json.dumps(res,indent=2)+'\n');print({'status':'PASS','checks':len(checks),'seconds':time.time()-start})
