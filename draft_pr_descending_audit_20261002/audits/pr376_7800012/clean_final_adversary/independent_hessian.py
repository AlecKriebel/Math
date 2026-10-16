"""Independent full matrix derivation through a reduced resolvent."""
import json,pathlib,sys
import sympy as s
ROOT=pathlib.Path(__file__).parent
count=0
def check(v,label):
 global count
 if not v:raise AssertionError(label)
 count+=1
def ga(z,w):return(z[0]+w[0],z[1]+w[1])
def gm(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def gc(z):return(z[0],-z[1])
def gs(z,k):return(z[0]*k,z[1]*k)
Z=(0,0)
def mm(a,b):
 n=len(a);out=[[Z]*n for _ in range(n)]
 for i in range(n):
  for k,ak in enumerate(a[i]):
   if ak!=Z:
    for j,bj in enumerate(b[k]):
     if bj!=Z:out[i][j]=ga(out[i][j],gm(ak,bj))
 return out
def fa(z,w):return(ga(z[0],w[0]),ga(z[1],w[1]))
def fm(z,w):return(ga(gm(z[0],w[0]),gs(gm(z[1],w[1]),3)),ga(gm(z[0],w[1]),gm(z[1],w[0])))
def fg(z,g):return(gm(z[0],g),gm(z[1],g))
N=64;T=[[Z]*N for _ in range(N)];edges=[];roots=[(1,0),(0,1),(-1,0),(0,-1)]
for y in range(8):
 for x in range(8):
  a=x+8*y
  for b,t in [(((x+1)%8)+8*y,(-1 if x==7 else 1,0)),(x+8*((y+1)%8),gs(roots[x%4],-1 if y==7 else 1))]:
   T[a][b]=t;T[b][a]=gc(t);edges.append((a,b,t))
I=[[(int(i==j),0) for j in range(N)] for i in range(N)]
T2=mm(T,T);T3=mm(T2,T);T4=mm(T2,T2);pw=[I,T,T2,T3]
for i in range(N):
 for j in range(N):check(ga(ga(T4[i][j],gs(T2[i][j],-8)),gs(I[i][j],4))==Z,'annihilator')
x=s.symbols('x');rad=s.sqrt(3);lam=[-1-rad,1-rad,-1+rad,1+rad]
poly=[s.Poly(s.expand(s.prod((x-lam[j])/(lam[i]-lam[j]) for j in range(4) if j!=i)),x) for i in range(4)]
res=s.Poly(s.expand(sum(poly[j].as_expr()/(lam[0]-lam[j]) for j in range(1,4))),x)
def pair(expr,scale):
 expr=s.expand(s.simplify(expr)*scale);b=s.simplify(expr.coeff(rad));a=s.simplify(expr-b*rad)
 check(a.is_Integer and b.is_Integer,'field coefficient');return(int(a),int(b))
pc=[pair(poly[0].nth(i),48) for i in range(4)];rc=[pair(res.nth(i),96) for i in range(4)]
def polmat(co):
 return [[tuple(tuple(sum(pw[k][i][j][c]*co[k][h] for k in range(4)) for c in range(2)) for h in range(2)) for j in range(N)] for i in range(N)]
P=polmat(pc);R=polmat(rc)
# The true Hessian times 2304, using a SINGLE reduced resolvent.
H=[]
for e,(a,b,t) in enumerate(edges):
 Ke=[(a,b,gm((0,1),t)),(b,a,gc(gm((0,1),t)))];row=[]
 for f,(c,d,u) in enumerate(edges):
  Kf=[(c,d,gm((0,1),u)),(d,c,gc(gm((0,1),u)))];z=(Z,Z)
  for aa,bb,k in Ke:
   for cc,dd,v in Kf:z=fa(z,fg(fm(P[dd][aa],R[bb][cc]),gm(k,v)))
  row.append((z[0][0]+288*int(e==f),z[1][0]+288*int(e==f)))
 H.append(row)
for e in range(128):
 for f in range(128):
  check(H[e][f]==H[f][e],'full real symmetry')
  u,o=divmod(e,2);v,p=divmod(f,2);d=(v%8-u%8)%8+8*((v//8-u//8)%8)
  check(H[e][f]==H[o][2*d+p],'translation across seams')
 for vertex in range(N):
  check(tuple(sum(H[e][f][q]*(int(b==vertex)-int(a==vertex)) for f,(a,b,t) in enumerate(edges)) for q in range(2))==(0,0),'full gauge columns')
trig=[((2,0),(0,0)),((0,1),(0,1)),((0,0),(2,0)),((0,-1),(0,1)),((-2,0),(0,0)),((0,-1),(0,-1)),((0,0),(-2,0)),((0,1),(0,-1))]
D=10**16;bounds=[(14142135623730950,14142135623730951,2),(17320508075688772,17320508075688773,3),(24494897427831780,24494897427831781,6)]
for lo,hi,q in bounds:check(lo*lo<q*D*D<hi*hi,'fresh radical bounds')
def qm(a,b):
 out=[0]*4
 for i in range(4):
  for j in range(4):out[i^j]+=a[i]*b[j]*(2 if (i&j)&1 else 1)*(3 if (i&j)&2 else 1)
 return out
def zm(z,w):return([a-b for a,b in zip(qm(z[0],w[0]),qm(z[1],w[1]))],[a+b for a,b in zip(qm(z[0],w[1]),qm(z[1],w[0]))])
blocks=[]
for ky in range(8):
 for kx in range(8):
  B=[]
  for o in range(2):
   br=[]
   for p in range(2):
    re=[0]*4;im=[0]*4
    for y in range(8):
     for xx in range(8):
      A,C=H[o][2*(xx+8*y)+p];cos,sin=trig[(kx*xx+ky*y)%8]
      for dst,ph in [(re,cos),(im,sin)]:
       dst[0]+=A*ph[0];dst[1]+=A*ph[1];dst[2]+=C*ph[0];dst[3]+=C*ph[1]
    br.append((re,im))
   B.append(br)
  check(B[0][1][0]==B[1][0][0] and B[0][1][1]==[-v for v in B[1][0][1]],'Fourier hermitian')
  check(B[0][0][1]==B[1][1][1]==[0]*4,'Fourier diagonal real')
  a=zm(B[0][0],B[1][1]);b=zm(B[0][1],B[1][0]);det=([u-v for u,v in zip(a[0],b[0])],[u-v for u,v in zip(a[1],b[1])])
  trace=[a+b for a,b in zip(B[0][0][0],B[1][1][0])]
  lower=trace[0]*D+sum(c*(lo if c>=0 else hi) for c,(lo,hi,q) in zip(trace[1:],bounds))
  check(lower>0,'trace positive')
  if kx or ky:check(det==([0]*4,[0]*4),'nonzero block exact rank one')
  else:check(B==[[([-288,0,224,0],[0]*4),([0]*4,[0]*4)],[([0]*4,[0]*4),([-288,0,224,0],[0]*4)]],'two zero mode eigenvalues')
  diff=trace[:];diff[0]+=576;diff[2]-=448
  dl=diff[0]*D+sum(c*(lo if c>=0 else hi) for c,(lo,hi,q) in zip(diff[1:],bounds))
  check(diff==[0]*4 or dl>0,'trace lower bound')
  blocks.append(dict(kx=kx,ky=ky,block=B,trace_numerator=trace,denominator=4608,strict_lower_numerator=lower,strict_lower_denominator=4608*D))
print(json.dumps(dict(stage='independent_full_matrix',assertions=count,projector48=pc,resolvent96=rc)),flush=True)
# Only now cross-bind full independently derived H to candidate executable.
sys.path.insert(0,str(ROOT/'tmp'/'private_candidate'));import hessian_certificate
capture={}
def prof(frame,event,arg):
 if event=='return' and frame.f_code is hessian_certificate.compute.__code__:capture['H']=frame.f_locals['H']
sys.setprofile(prof);author=hessian_certificate.compute(lambda v:check(v,'candidate exact certificate'));sys.setprofile(None)
for e in range(128):
 for f in range(128):check(capture['H'][e][f]==tuple(6*v for v in H[e][f]),'entire matrix cross-bound')
cert=json.loads((ROOT/'tmp'/'private_candidate'/'TURN_4_CERTIFICATE.json').read_text())
for b,c in zip(blocks,cert['fourier_trace_certificates']):check([6*v for v in b['trace_numerator']]==c['numerator'],'stored trace cross-bound')
(ROOT/'FULL_HESSIAN.json').write_text(json.dumps(dict(scale=2304,matrix=H),separators=(',',':'))+'\n')
(ROOT/'FULL_FOURIER_BLOCKS.json').write_text(json.dumps(blocks,indent=2)+'\n')
print(json.dumps(dict(stage='complete',assertions=count,full_entries=16384,physical_dimension=65,gauge_dimension=63,full_fourier_blocks=64,entire_matrix_match=True)),flush=True)
