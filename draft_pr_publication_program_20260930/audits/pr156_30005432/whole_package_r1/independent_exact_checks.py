"""Independent affine certificates and falsification controls, no imported candidate code."""
from pathlib import Path
from itertools import product
import json, subprocess, os
P=Path(__file__).resolve().parent
N=3
zero=(0,)*N
basis=[tuple(int(i==j) for i in range(N)) for j in range(N)]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(k,a):return tuple(k*x for x in a)
def require(c,m):
 if not c:raise RuntimeError(m)
e=(1,1,-1,-1)
def s(a,b):return (a+b+2*a*b)%4
def aplus(x,y):return plus(x[0],y[0]),(x[1]+y[1])%4
def aneg(x):return scale(-1,x[0]),(-x[1])%4
def adiff(x,y):return aplus(x,aneg(y))
def cp(x,y):return plus(x[0],scale(e[x[1]],y[0])),s(x[1],y[1])
def ci(x):return scale(-e[x[1]],x[0]),x[1]
def la(x,y):return adiff(cp(x,y),x)
def st(x,y):return adiff(la(x,y),y)
ct=0
for c,d,f in product(range(4),repeat=3):
 x=(basis[0],c);y=(basis[1],d);z=(basis[2],f)
 require(cp(cp(x,y),z)==cp(x,cp(y,z)),'universal associative coefficients')
 require(cp(x,aplus(y,z))==aplus(adiff(cp(x,y),x),cp(x,z)),'universal left brace coefficients')
 require(la(cp(x,y),z)==la(x,la(y,z)),'universal lambda homomorphism')
 ct+=3
for c,d in product(range(4),repeat=2):
 x=(basis[0],c);y=(basis[1],d)
 require(s(c,d)==c^d,'Klein coordinates')
 require(la(x,y)==(scale(e[c],basis[1]),((1+2*c)*d)%4),'universal lambda formula')
 require(st(x,y)==(scale(e[c]-1,basis[1]),2*c*d%4),'universal star formula')
 require(cp(cp(y,x),ci(y))==(plus(scale(1-e[c],basis[1]),scale(e[d],basis[0])),c),'universal conjugation formula')
 require(adiff(cp(y,x),cp(x,y))[0]==plus(scale(1-e[c],basis[1]),scale(e[d]-1,basis[0])),'universal commutation equation')
 ct+=5
for c in range(4):
 x=(basis[0],c)
 require(cp(x,ci(x))==(zero,0)==cp(ci(x),x),'universal inverse')
 ct+=1
# Direct H and K membership at integer representatives, including both infinite-index regimes.
def numeric_cp(x,y):return (x[0]+e[x[1]]*y[0],s(x[1],y[1]))
def numeric_la(x,y):return (e[x[1]]*y[0],(1+2*x[1])*y[1]%4)
def numeric_st(x,y):return ((e[x[1]]-1)*y[0],2*x[1]*y[1]%4)
regimes=[]
for n,c in product((0,1,-1,10**100),range(4)):
 H_d={d for d in range(4) if 2*c*d%4==0}
 K_d={d for d in range(4) if 2*c*d%4==0 and (e[d]-1)*n==0}
 for L in (H_d,K_d):
  require(0 in L and all(s(d,f) in L for d,f in product(L,repeat=2)),'K/H finite factor closure')
 for m,d in product((-10**100,-2,0,3,10**100),range(4)):
  x=(n,c);g=(m,d)
  H=numeric_st(x,g)==(0,0)
  K=numeric_st(g,x)==(0,0) and numeric_cp(g,x)==numeric_cp(x,g)
  require(H==(d in H_d and (c<2 or m==0)),'H classification')
  require(K==(d in K_d and (c<2 or m==0)),'K classification')
  ct+=2
 # Index proof: for c<2 these are full Z preimages; for c>=2 both contain only m=0.
 regimes.append({'n_regime':'zero' if n==0 else 'nonzero','c':c,'H_factor':sorted(H_d),'K_factor':sorted(K_d),'H_integer_factor':'Z' if c<2 else '{0}','K_integer_factor':'Z' if c<2 else '{0}','indices':[4//len(H_d),4//len(K_d)] if c<2 else ['infinite','infinite']})
# B3 source-map obstruction, independent complete enumeration.
pts=list(product(range(3),range(4)))
def bcp(x,y):return ((x[0]+e[x[1]]*y[0])%3,s(x[1],y[1]))
def bst(x,y):return (((e[x[1]]-1)*y[0])%3,2*x[1]*y[1]%4)
ann=[x for x in pts if all(bst(x,y)==(0,0)==bst(y,x) and bcp(x,y)==bcp(y,x) for y in pts)]
require(ann==[(0,0)],'B3 annihilator')
r=(1,0);x=(0,1)
def fmap(b):return tuple(bst(b,z) for z in (r,x))+tuple(bst(z,b) for z in (r,x))+((0,0),(0,0))
require(fmap((1,0))==fmap((0,0)),'B3 displayed map collision')
# Additional independently chosen mutations, in own scratch only.
source=(P.parent/'publication_package_v1/verify.py').read_text()
mutants={'wrong_star_term':('2*a[1]*b[1]%4','2*a[1]*b[1]%4 + 1'),'wrong_inverse':('def inv(a):return(-eps(a[1])*a[0],a[1])','def inv(a):return(-a[0],a[1])'),'wrong_circle_action':('def circ(a,b):return(a[0]+eps(a[1])*b[0],diamond(a[1],b[1]))','def circ(a,b):return(a[0]+b[0],diamond(a[1],b[1]))')}
mutres=[]
for name,(old,new) in mutants.items():
 require(source.count(old)==1,'mutation anchor '+name)
 d=P/'scratch'/'mutants'/name;d.mkdir(parents=True,exist_ok=True)
 (d/'verify.py').write_text(source.replace(old,new))
 (d/'property_s_counterexample.tex').write_bytes((P.parent/'publication_package_v1/property_s_counterexample.tex').read_bytes())
 for opt in (False,True):
  run=subprocess.run(['python3','-E','-S','-B','-P']+(['-O'] if opt else [])+[str(d/'verify.py')],cwd=d,capture_output=True,text=True)
  (d/('optimized.stderr.txt' if opt else 'normal.stderr.txt')).write_text(run.stderr)
  require(run.returncode!=0 and 'RuntimeError' in run.stderr,'mutant falsely passes '+name)
  mutres.append({'name':name,'optimized':opt,'exit_code':run.returncode,'reason':run.stderr.splitlines()[-1]})
result={'status':'PASS_INDEPENDENT_UNIVERSAL_COEFFICIENT_AND_CLASSIFICATION_AUDIT','universal_affine_checks':276,'total_direct_checks':ct,'regimes':regimes,'B3_annihilator':ann,'B3_map_collision':True,'additional_mutations':mutres,'limits':'Affine identities exhaust finite residues and compare exact formal integer-variable coefficients. Classification and infinite cosets also have written proof in REVIEW.md. Numeric huge-integer controls are supporting boundary checks.'}
(P/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'direct_checks':ct,'mutations_rejected':len(mutres)},indent=2))
