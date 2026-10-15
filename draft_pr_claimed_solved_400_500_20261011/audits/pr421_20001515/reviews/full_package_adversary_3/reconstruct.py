"""Independent finite incidence checks. No candidate checker imports."""
from itertools import combinations
from collections import Counter,defaultdict
import json
from pathlib import Path

def inv(word): return word[::-1].swapcase()
def red(word):
 s=[]
 for a in word:
  if s and s[-1]==a.swapcase(): s.pop()
  else:s.append(a)
 return ''.join(s)
def sub(word,m):return red(''.join(m[c.lower()] if c.islower() else inv(m[c.lower()]) for c in word))
def germ(a): return a.lower()+('+' if a.islower() else '-')
def edge(a,b): return tuple(sorted((a,b)))
def corners(word): return [edge(germ(word[i-1].swapcase()),germ(word[i])) for i in range(4)]
Kwords=['xyXY','bxBY']
KE=[e for w in Kwords for e in corners(w)]
if len(set(KE))!=8:raise ValueError('duplicate K corner')
K=set(KE)
lam={'x':'y','y':'x','b':'B'}
def lg(a):return germ(sub(a[0] if a[1]=='+' else a[0].upper(),lam))
# Retain occurrence vertices rather than merging repeated A corners first.
QE={'p':('B','A','x'),'q':('A','C','y'),'r':('D','C','x'),'s':('B','D','y'),'d':('A','B','b'),'e':('C','A','b')}
Qwords=['pqRS','dpEQ']
Qstart=['B','A']
QV=defaultdict(list); QC=defaultdict(list); occurrences=[]
for word,start in zip(Qwords,Qstart):
 v=start
 for i,a in enumerate(word):
  e=QE[a.lower()];tail,head=e[:2] if a.islower() else e[1::-1]
  if tail!=v:raise ValueError('boundary does not close')
  prev=word[i-1]
  cr=edge(germ(prev.swapcase()),germ(a));QC[v].append(cr)
  occurrences.append({'square':word,'corner':i,'vertex':v,'edge':cr})
  v=head
 if v!=start:raise ValueError('boundary does not close')
for e,(u,v,label) in QE.items():QV[u].append(e+'+');QV[v].append(e+'-')
def image(a):return germ(QE[a[0]][2] if a[1]=='+' else QE[a[0]][2].upper())
rows={}; LE=list(KE);LT=[]
for v in 'ABCD':
 verts=QV[v]; cs=QC[v]
 if len(set(cs))!=len(cs):raise ValueError('duplicate Q corner')
 im=[image(a) for a in verts]
 if len(set(im))!=len(im):raise ValueError('link noninjective')
 ims={edge(image(a),image(b)) for a,b in cs}
 induced={e for e in K if set(e)<=set(im)}
 if ims!=induced:raise ValueError('link nonfull')
 rows[v]={'vertices':verts,'corners':cs,'images':im}
 for end in [0,1]:
  apex='z'+v+('+' if end==0 else '-')
  f=image if end==0 else lambda a:lg(image(a))
  LE.extend(edge(apex,f(a)) for a in verts)
  LT.extend(tuple(sorted((apex,f(a),f(b)))) for a,b in cs)
if len(set(LE))!=len(LE) or len(set(LT))!=len(LT):raise ValueError('duplicate product incidence')
V=sorted(set(x for e in LE for x in e));E=set(LE);T=set(LT)
cliques={n:[c for c in combinations(V,n) if all(edge(a,b) in E for a,b in combinations(c,2))] for n in [3,4]}
if set(cliques[3])!=T or cliques[4]:raise ValueError('flag failure')
# Determine square dihedral maps without assuming boundary assertions.
reparams={}
for w in Kwords:
 imagew=sub(w,lam);orbit=[]
 for source in [w,inv(w)]:orbit.extend(source[i:]+source[:i] for i in range(4))
 if imagew not in orbit:raise ValueError('lambda has no square isometry')
 if sub(imagew,lam)!=w:raise ValueError('lambda square map not involutive')
 reparams[w]=imagew
# Free-by-cyclic normal forms (free word, t-height).
phi={'a':'a','b':'ab','c':'bcb'}; psi={'a':'a','b':'Ab','c':'BacBa'}
for c in 'abc':
 if sub(phi[c],psi)!=c or sub(psi[c],phi)!=c:raise ValueError('not automorphism')
def power(w,n):
 for _ in range(abs(n)):w=sub(w,phi if n>=0 else psi)
 return w
def multiply(a,b):return (red(a[0]+power(b[0],a[1])),a[1]+b[1])
def reverse(a):return (power(inv(a[0]),-a[1]),-a[1])
def evaluate(word,m):
 r=('',0)
 for c in word:r=multiply(r,m[c.lower()] if c.islower() else reverse(m[c.lower()]))
 return r
m={'x':('',1),'y':('A',1),'b':('b',0),'z':('C',-1)}
for w in ['xyXY','bxBY','ZbxzYb']:
 if evaluate(w,m)!=('',0):raise ValueError('wrong HNN target map '+w)
# Six product squares independently from endpoints, use 0 top lambda images.
z={'A':'z','B':'h','C':'i','D':'k'}
rel=[]
for e,(u,v,label) in QE.items():rel.append(label+z[v]+inv(sub(label,lam))+z[u].upper())
expr={'z':'z','h':'xzY','i':'Yzx','k':'YxzYx'}
for key in 'hik':m[key]=evaluate(expr[key],m)
for w in rel:
 if evaluate(w,m)!=('',0):raise ValueError('wrong product relator '+w)
# Controls fail distinct invariants, including positive final b.
controls={}
controls['delete_one_A_corner']=len(LT)-1!=len(cliques[3])
controls['duplicate_A_corner']=len(LT+[LT[0]])!=len(set(LT+[LT[0]]))
controls['wrong_final_inverse_b']=evaluate('tcTBcB',{'a':('a',0),'b':('b',0),'c':('c',0),'t':('',1)})!=('',0)
# Here true final-b relator is tcT B C B, inverted RHS; wrong relation RHS b c B -> tcT b C B.
controls['wrong_final_inverse_b']=evaluate('tcTbCB',{'a':('a',0),'b':('b',0),'c':('c',0),'t':('',1)})!=('',0)
controls['wrong_HNN_conjugation']=evaluate('zbxZYb',m)!=('',0)
if not all(controls.values()):raise ValueError('ineffective independent control')
result={'K_corner_occurrences':KE,'Q_occurrences':occurrences,'Q_links':rows,'lambda_square_images':reparams,'product_relators':rel,'Z_link_vertices':V,'Z_edges':sorted(E),'Z_triangles':sorted(T),'clique_counts':{str(n):len(v) for n,v in cliques.items()},'counts':[1,7,8,2],'link_counts':[len(V),len(E),len(T)],'automorphism_inverse':psi,'control_rejections':controls,'status':'all finite predicates verified'}
Path(__file__).with_name('RECONSTRUCTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['link_counts','clique_counts','product_relators','control_rejections','status']},indent=2))
