#!/usr/bin/env python3
"""Exact twisted-cohomology certificate over Q[xi], with no floating-point spectrum step."""
import sympy as S,json,hashlib,argparse
from pathlib import Path
from collections import Counter
counts=Counter()
def check(name, value):
 assert value,name
 counts[name]+=1
from sympy.polys.matrices import DomainMatrix
x=S.symbols('x');p=x**4-3*x**3+2*x*x+2*x-1
K=S.QQ.algebraic_field(S.CRootOf(p,0));X=K.unit;Y=X/(X-1);Z=X
zero=K.zero;one=K.one

def mat(rows):return [[K.convert(t) for t in row] for row in rows]
def eye(n):return [[one if i==j else zero for j in range(n)] for i in range(n)]
def zeros(n,m):return [[zero for j in range(m)] for i in range(n)]
def mm(a,b):return [[sum((u*v for u,v in zip(row,col)),zero) for col in zip(*b)] for row in a]
def add(a,b):return [[u+v for u,v in zip(ra,rb)] for ra,rb in zip(a,b)]
def neg(a):return [[-u for u in row] for row in a]
def invmat(a):return DomainMatrix(a,(len(a),len(a)),K).inv().to_list()
def block(a,idx,M):
 for i in range(3):
  for j in range(3):a[i][3*idx+j]+=M[i][j]
def cp(a):return DomainMatrix(a,(len(a),len(a)),K).charpoly()
def polystr(a):return str(S.Poly.from_list([K.to_sympy(t) for t in a],S.symbols('t')).as_expr())
U=1-X*X/4;V=1-Y*Y/4;W=X*Y/4-Z/2
RA=mat([[1,2*W,X*W],[0,X*X/2-1,-X*U],[0,X,X*X/2-1]])
RB=mat([[Y*Y/2-1,0,Y*V],[2*W,1,-Y*W],[-Y,0,Y*Y/2-1]])

def cross(a,b):
 c12=a[0]*b[1]-a[1]*b[0];c13=a[0]*b[2]-a[2]*b[0];c23=a[1]*b[2]-a[2]*b[1]
 return [c13*W+c23*V,-c13*U-c23*W,c12]
OA=[Y/2,X/2,one];OB=[one,X,zero];OC=cross(OA,OB);O=list(map(list,zip(OA,OB,OC)));Oi=invmat(O);Oi3=mm(mm(Oi,Oi),Oi)
check('fixed_representation_adjoint_a',mm(mm(O,RA),Oi)==mm(RA,RB))
check('fixed_representation_adjoint_b',mm(mm(O,RB),Oi)==mm(mm(RB,RA),RB))
I=eye(3)
G=mat([[U,W,0],[W,V,0],[0,0,U*V-W*W]])
check('intertwiner_orthogonality',mm(mm(list(map(list,zip(*O))),G),O)==G)
check('intertwiner_orientation',cp(O)[-1]==-one)
for R in [RA,RB]:
 check('adjoint_metric',mm(mm(list(map(list,zip(*R))),G),R)==G)
 check('adjoint_orientation',cp(R)[-1]==-one)

def red(w):
 r=[]
 for t in w:
  if r and r[-1]==-t:r.pop()
  else:r.append(t)
 return tuple(r)
def inverse(w):return tuple(-i for i in w[::-1])
def subst(w,images):return red(sum((images[t-1] if t>0 else inverse(images[-t-1]) for t in w),()))
phi=((1,2),(2,1,2));phi3=tuple((i,) for i in [1,2])
for _ in range(3):phi3=tuple(subst(w,phi) for w in phi3)
hs=((1,1,1),(2,),(1,2,-1,-1),(1,1,2,-1))

def rewrite(word):
 out=[];v=0
 for t in word:
  if t==1:
   if v==2:out.append(1)
   v=(v+1)%3
  elif t==-1:
   if v==0:out.append(-1)
   v=(v-1)%3
  elif t==2:
   out.append([2,3,4][v]);v=-v%3
  elif t==-2:
   v=-v%3;out.append(-[2,3,4][v])
 check('schreier_closed_word',v==0)
 return red(out)
c=(1,2,-1,-2);rel=rewrite(c*3);imgs=[rewrite(subst(w,phi3)) for w in hs]
check('filled_relator_word',rel==(3,-4,1,2,-1,-3,4,-2))
check('surface_relation_preserved',subst(rel,imgs)==rel)
for w in hs:check('schreier_generator_roundtrip',subst(rewrite(w),hs)==w)
for w,im in zip(hs,imgs):check('schreier_image_roundtrip',subst(im,hs)==subst(w,phi3))
Rbase=[RA,RB];Rbaseinv=[invmat(a) for a in Rbase]
def evalword(w,R,Ri=None):
 if Ri is None:Ri=[invmat(a) for a in R]
 out=I
 for t in w:out=mm(out,R[t-1] if t>0 else Ri[-t-1])
 return out
RH=[evalword(w,Rbase,Rbaseinv) for w in hs];RHi=[invmat(a) for a in RH]
check('closed_adjoint_relation',evalword(rel,RH,RHi)==I)
for i,im in enumerate(imgs):check('normalized_closed_fixed_representation',mm(mm(Oi3,evalword(im,RH,RHi)),invmat(Oi3))==RH[i])

def diffword(w):
 prefix=I;out=zeros(3,12)
 for t in w:
  if t>0:
   block(out,t-1,prefix);prefix=mm(prefix,RH[t-1])
  else:
   prefix=mm(prefix,RHi[-t-1]);block(out,-t-1,neg(prefix))
 return out
D=diffword(rel)
B=[row for r in RH for row in add(I,neg(r))]
L=[row for w in imgs for row in mm(Oi3,diffword(w))]
check('cochain_complex',mm(D,B)==zeros(3,3))
check('relation_chain_map',mm(D,L)==mm(Oi3,D))
check('coboundary_chain_map',mm(L,B)==mm(B,Oi3))

check('relation_rank',DomainMatrix(D,(3,12),K).rank()==3)
check('coboundary_rank',DomainMatrix(B,(12,3),K).rank()==3)
cc=cp(L);c0=cp(Oi3)

def divpoly(a,b):
 a=a[:];out=[]
 while len(a)>=len(b):
  q=a[0]/b[0];out.append(q)
  for j,t in enumerate(b):a[j]-=q*t
  check('polynomial_leading_cancellation',a[0]==zero);a.pop(0)
 check('exact_polynomial_division',all(t==zero for t in a))
 return out
h1=divpoly(divpoly(cc,c0),c0)

tau=2*X*Y-1;tau3=tau**3-3*tau
normal=divpoly(h1,[one,-tau3,one])

# Simplify all coefficients to the chosen positive square root of13.
sqrt13=2-tau
check('quadratic_subfield',sqrt13*sqrt13==K.convert(13))
check('base_cubed_trace',tau3==80-22*sqrt13)
a=(53-5*sqrt13)/2;b=(705-163*sqrt13)/2
check('exact_normal_quartic',normal==[one,-a,b,-a,one])
# Field embedding chosen by xi in (-723/1000,-722/1000) makes sqrt13 positive.
from fractions import Fraction as F
lo=F(18,5);hi=F(361,100)
check('sqrt13_isolation',lo*lo<13<hi*hi)
# In t+1/t, the discriminant is (387sqrt13-1237)/2.
check('positive_reduced_discriminant',(387*lo-1237)/2>0)
check('reduced_vertex_right_of_two',(53-5*hi)/2>4)
check('reduced_polynomial_positive_at_two',(603-153*hi)/2>0)
check('reduced_discriminant_identity',a*a-4*(b-2)==(387*sqrt13-1237)/2)
check('reduced_value_at_two',b-2*a+2==(603-153*sqrt13)/2)
check('base_stays_elliptic',-2<80-22*hi<80-22*lo<2)
# Verify the inverse on both free groups, not just a monodromy test.
phii=((1,1,-2),(2,-1));phii3=((1,),(2,))
for _ in range(3):phii3=tuple(subst(w,phii) for w in phii3)
for j in range(2):
 check('base_automorphism_inverse',subst(phi[j],phii)==(j+1,))
 check('base_automorphism_inverse',subst(phii[j],phi)==(j+1,))
invimgs=[rewrite(subst(w,phii3)) for w in hs]
for j in range(4):
 check('cover_automorphism_inverse',subst(imgs[j],invimgs)==(j+1,))
 check('cover_automorphism_inverse',subst(invimgs[j],imgs)==(j+1,))
# Export coefficients as rational lists in basis(1,xi,xi^2,xi^3).
def enc(a):
 v=[str(t) for t in a.to_list()[::-1]]
 return v+['0']*(4-len(v))
def emat(M):return [[enc(t) for t in row] for row in M]
cert={'field':{'minimal_polynomial':[1,-3,2,2,-1],'root_interval':['-723/1000','-722/1000'],'basis':['1','xi','xi^2','xi^3']},'base_automorphism':phi,'base_cube':phi3,'cover_generators_in_base':hs,'filled_relator':rel,'cover_cube_images':imgs,'inverse_cover_cube_images':invimgs,'adjoint_a':emat(RA),'adjoint_b':emat(RB),'intertwiner':emat(O),'gram_matrix':emat(G),'coboundary_d0':emat(B),'relation_d1':emat(D),'normalized_cochain_action':emat(L),'end_cochain_action':emat(Oi3),'raw_C1_characteristic':[enc(t) for t in cc],'end_C0_C2_characteristic':[enc(t) for t in c0],'H1_characteristic':[enc(t) for t in h1],'normal_characteristic':[enc(t) for t in normal],'relative_cubed_trace':enc(tau3)}
raw=(json.dumps(cert,indent=2,sort_keys=True)+'\n').encode()
parser=argparse.ArgumentParser();parser.add_argument('--write-certificate',action='store_true');args=parser.parse_args()
path=Path(__file__).with_name('TURN_5_COCHAIN_CERTIFICATE.json')
if args.write_certificate:path.write_bytes(raw)
else:check('frozen_certificate_reproduction',path.read_bytes()==raw)
print(json.dumps({'problem_id':11000192,'author_turn':5,'status':'PASS','exact_controls':sum(counts.values()),'groups':dict(sorted(counts.items())),'field':'Q[xi]/(xi^4-3xi^3+2xi^2+2xi-1), xi in(-723/1000,-722/1000)','C1_dimension':12,'relation_rank':3,'coboundary_rank':3,'H1_dimension':6,'relative_dimension':2,'normal_dimension':4,'normal_polynomial':'t^4-((53-5sqrt(13))/2)t^3+((705-163sqrt(13))/2)t^2-((53-5sqrt(13))/2)t+1','normal_root_conclusion':'four positive real reciprocal roots, all off the unit circle, by exact rational bounds','relative_cubed_trace':'80-22sqrt(13)','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256(raw).hexdigest(),'scope':'This explicit fixed point is an ambient saddle despite its stable relative elliptic surface. Neither ambient ergodicity nor impossibility of other nonergodicity mechanisms is certified.'},indent=2,sort_keys=True))
