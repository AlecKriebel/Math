"""Finite falsifiable algebra/word probes; not geometric/theorem certificates."""
import datetime,hashlib,itertools,json,pathlib,random,zipfile
H=pathlib.Path(__file__).resolve().parent;d=json.loads((H/'INPUT_FREEZE.json').read_text());P=pathlib.Path(d['root']);out={}
def need(c,m):
 if not c:raise ValueError(m)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def inv(a):return (a[3],-a[1],-a[2],a[0])
def power(a,n):
 if n<0:return power(inv(a),-n)
 r=(1,0,0,1)
 while n:
  if n&1:r=mul(r,a)
  a=mul(a,a);n>>=1
 return r
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def trace(a):return a[0]+a[3]
def det(a):return a[0]*a[3]-a[1]*a[2]
def determinant(a):
 a=[list(r) for r in a];n=len(a);sign=1;old=1
 for k in range(n-1):
  if a[k][k]==0:
   q=next((q for q in range(k+1,n) if a[q][k]),None)
   if q is None:return 0
   a[k],a[q]=a[q],a[k];sign=-sign
  pivot=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):a[i][j]=(a[i][j]*pivot-a[i][k]*a[k][j])//old
  for i in range(k+1,n):a[i][k]=0
  old=pivot
 return sign*a[-1][-1]
def endpoints_disjoint(c,d):
 # Resultant of the two fixed-point quadratics, plus infinity handled separately.
 a,b,z=c[2],c[3]-c[0],-c[1];e,f,g=d[2],d[3]-d[0],-d[1]
 if a==0 and e==0:return False
 return determinant([[a,b,z,0],[0,a,b,z],[e,f,g,0],[0,e,f,g]])!=0
rng=random.Random(1241);matrices=[]
for q in range(300):
 c=(1,0,0,1)
 for j in range(8):
  t=rng.randint(-9,9);c=mul(c,(1,t,0,1) if j%2 else (1,0,t,1))
 matrices.append(c)
for mu in [0,1,2,4,8,-4]:
 v=(1,0,-mu,1)
 for c in matrices:
  p,q,w,s=c;got=comm(v,c);expected=(1+mu*q*s,-mu*q*q,mu*(s*s-1)-mu*mu*q*s,1-mu*q*s+mu*mu*q*q)
  need(got==expected and det(got)==1 and trace(got)==2+mu*mu*q*q,'generic commutator formula')
out['generic_commutator_cases']=len(matrices)*6
series=[]
for mu in [4,6,8,10]:
 c=(1,mu,0,1);v=(1,0,-mu,1)
 for r in range(2,10):
  c=comm(v,c);need(c[1]==-mu**(2**r-1) and trace(c)==2+mu**(2**r),'deep formula')
  M=next(M for M in range(1,11) if endpoints_disjoint(c,mul(mul(power(v,M),c),power(v,-M))))
  series.append({'mu':mu,'r':r,'depth':2*r,'hyperbolic':trace(c)>2,'q_nonzero':c[1]!=0,'disjoint_parabolic_conjugate_M':M})
out['deep_and_fixed_endpoint_checks']=series

def inverse(w):return tuple(-a for a in reversed(w))
def cyclic(w):
 i,j=0,len(w)
 while j-i>=2 and w[i]==-w[j-1]:i+=1;j-=1
 return w[i:j]
def canonical(w):
 w=cyclic(w);n=len(w);x=w+w;i,j,k=0,1,0
 while i<n and j<n and k<n:
  if x[i+k]==x[j+k]:k+=1;continue
  if x[i+k]>x[j+k]:i=i+k+1;i += i==j
  else:j=j+k+1;j += i==j
  k=0
 q=min(i,j);return tuple(x[q:q+n])
def primitive(w):
 w=cyclic(w);pi=[0]*len(w)
 for i in range(1,len(w)):
  j=pi[i-1]
  while j and w[i]!=w[j]:j=pi[j-1]
  if w[i]==w[j]:j+=1
  pi[i]=j
 period=len(w)-pi[-1];return len(w)%period!=0 or period==len(w)
def signed(w,e):return w if e==1 else inverse(w)
family=[(1,)];reps=[((2,1,1,1),(1,2,0,1)),((1,1,0,1),(1,0,-4,1)),((3,2,1,1),(1,-3,0,1))];values=[[p for p,q in reps]];matfamilies=[[p] for p,q in reps];checks=[]
for m in range(1,7):
 family=[signed(w,-e)+(2,)*(2*m)+signed(w,e)+(2,)*(2*m-1)+signed(w,-e)+(2,)*(2*m)+signed(w,e) for w in family for e in [1,-1]]
 need(all(all(a!=-b for a,b in zip(w,w[1:])) for w in family),'free reduction')
 forms={canonical(w) for w in family};need(len(forms)==2**m,'nonconjugacy');need(not forms&{canonical(inverse(w)) for w in family},'inverse separation');need(all(primitive(w) for w in family),'power collision')
 trace_sizes=[]
 # exact recursive evaluations avoid ever using the cyclic-class algorithm to establish traces.
 for i,(p,q) in enumerate(reps):
  new=[]
  for u in matfamilies[i]:
   for e in [1,-1]:
    a=mul(mul(power(u,-e),power(q,2*m)),power(u,e));new.append(mul(mul(a,power(q,2*m-1)),a))
  matfamilies[i]=new;traces={trace(x) for x in new};need(len(traces)==1,'equal exact trace');trace_sizes.append(len(str(abs(next(iter(traces))))))
 checks.append({'m':m,'classes':len(forms),'free_reduced_nonidentity':True,'inverse_classes_disjoint':True,'root_free_in_abstract_F2_only':True,'exact_trace_digit_counts_by_representation':trace_sizes})
out['horowitz_checks']=checks
# Identity/commuting and parabolic parameter controls demonstrate why geometry is separate.
need(trace(comm((1,0,0,1),(2,1,1,1)))==2,'q0 boundary')
out['scope']='Finite exact SL2 and abstract-free-word consistency only; tested mu values are algebraic parameters, not all asserted geometrically realized pairs. Root-freeness in F2 does not imply ambient mapping-class primitivity. No Teichmueller theorem or compact-core infinite quantifier is certified by these calculations.'
out['at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['status']='PASS';(H/'INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','generic_commutator_cases','horowitz_checks']},indent=2))
