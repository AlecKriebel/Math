"""Finite coefficient controls for universal priority translations in REVIEW.md."""
import itertools,json
count=0
def check(ok,msg):
 global count
 if not ok:raise RuntimeError(msg)
 count+=1
def dia(c,d):return(c+d+2*c*d)%4
characters=[]
for tail in itertools.product((-1,1),repeat=3):
 ch=(1,)+tail
 if all(ch[dia(c,d)]==ch[c]*ch[d] for c,d in itertools.product(range(4),repeat=2)):
  ker=[c for c in range(4) if ch[c]==1]
  characters.append({'character':ch,'kernel':ker,'additive_closed':all((c+d)%4 in ker for c,d in itertools.product(ker,repeat=2))})
check(len(characters)==4,'four V4 characters')
eps=(1,1,-1,-1)
check(any(r['character']==eps and r['kernel']==[0,1] and not r['additive_closed'] for r in characters),'main kernel')
def circle(a,b):return(a[0]+eps[a[1]]*b[0],dia(a[1],b[1]))
def inverse(a):return(-eps[a[1]]*a[0],a[1])
pts=list(itertools.product(range(-3,4),range(4)))
for x,g in itertools.product(pts,repeat=2):
 n,c=x;m,d=g
 check(circle(circle(g,x),inverse(g))==(eps[d]*n+(1-eps[c])*m,c),'main conjugacy')
 check((circle(x,g)[0]-n-m,(circle(x,g)[1]-c-d)%4)==((eps[c]-1)*m,2*c*d%4),'right star')
check(circle((0,1),(0,1))==(0,0),'circle square')
check(eps[(1+1)%4]==-1,'additive double')
for c,d in itertools.product(range(4),repeat=2):check((-dia(c,d))%4==dia((-c)%4,(-d)%4),'C4 negation isomorphism')
C=list(itertools.product(range(3),repeat=3))
def beta(v,w):return(v[0]*w[1]-v[1]*w[0])%3
def cplus(a,b):return((a[0]+b[0])%3,(a[1]+b[1])%3,(a[2]+b[2]+beta(a[:2],b[:2]))%3)
def ccircle(a,b):return tuple((a[i]+b[i])%3 for i in range(3))
def lamc(a,b):return(b[0],b[1],(b[2]-beta(a[:2],b[:2]))%3)
for a,b,c in itertools.product(C,repeat=3):
 check(cplus(cplus(a,b),c)==cplus(a,cplus(b,c)),'MSTY additive associativity')
 check(lamc(a,cplus(b,c))==cplus(lamc(a,b),lamc(a,c)),'MSTY additive lambda automorphism')
 check(lamc(a,lamc(b,c))==lamc(ccircle(a,b),c),'MSTY lambda homomorphism')
for z,t in itertools.product(range(3),repeat=2):check(pow(2,(z+t)%3,7)==pow(2,z,7)*pow(2,t,7)%7,'order3 scalar action')
check(pow(2,1,7)-1!=0 and pow(2,2,7)-1!=0,'nonzero scalar')
def mplus(a,b):return((a[0]+b[0])%7,)+cplus(a[1:],b[1:])
def mcircle(a,b):return((a[0]+pow(2,a[3],7)*b[0])%7,)+ccircle(a[1:],b[1:])
def minverse(a):return((-pow(2,(-a[3])%3,7)*a[0])%7,)+tuple((-q)%3 for q in a[1:])
mpoints=[(u,)+c for u,c in itertools.product(range(7),C)]
for x,g in itertools.product(mpoints,repeat=2):check(mcircle(mcircle(g,x),minverse(g))==((pow(2,g[3],7)*x[0]+(1-pow(2,x[3],7))*g[0])%7,)+x[1:],'MSTY conjugacy all finite coefficients')
x,y=(0,1,0,0),(0,0,1,0)
check(mplus(x,y)==(0,1,1,1),'MSTY nonclosure witness')
check(x[3]==y[3]==0 and mplus(x,y)[3]!=0,'MSTY kernel nonclosure')
print(json.dumps({'status':'PASS','controls':count,'finite_control_limitation':'Infinitude follows from distinct basis vectors in REVIEW.md, not finite controls.','C4_characters':characters,'main_S':'Z x {0,1}','MSTY_infinite_S':'U x F3^2 x {0}','MSTY_witness':{'x':x,'y':y,'sum':mplus(x,y)}},indent=2))
