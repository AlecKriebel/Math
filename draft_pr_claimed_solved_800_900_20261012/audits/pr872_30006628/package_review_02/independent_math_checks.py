#!/usr/bin/env python3
"""Fresh finite construction, independent of all inherited diagnostics. Stdlib only.
Exact counts are diagnostics; floating Jacobi values are not validated eigenvalue bounds.
"""
import hashlib,itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
OUT=Path(__file__).resolve().parent
# Actual alphabet: two independent involutions in C2 x C2, and C2, C2.
parts=(0,0,1,2);B=tuple(range(4))
def require(v,m):
 if not v:raise ValueError(m)
def inv(w):return w[::-1]
def reduced(t):
 if t==0:yield ();return
 def extend(w):
  if len(w)==t:yield w;return
  for a in B:
   if not w or parts[a]!=parts[w[-1]]:yield from extend(w+(a,))
 yield from extend(())
def eigenvalues(a):
 # Independent cyclic Jacobi diagonalization of a real symmetric small matrix.
 a=[list(r) for r in a];n=len(a)
 for sweep in range(80):
  worst=0.0
  for p in range(n):
   for q in range(p+1,n):
    apq=a[p][q];worst=max(worst,abs(apq))
    if abs(apq)<1e-14:continue
    tau=(a[q][q]-a[p][p])/(2*apq)
    t=math.copysign(1.0,tau)/(abs(tau)+math.sqrt(1+tau*tau))
    c=1/math.sqrt(1+t*t);s=t*c
    app=a[p][p];aqq=a[q][q]
    a[p][p]=app-t*apq;a[q][q]=aqq+t*apq;a[p][q]=a[q][p]=0.0
    for k in range(n):
     if k in (p,q):continue
     apk=a[p][k];aqk=a[q][k]
     a[p][k]=a[k][p]=c*apk-s*aqk
     a[q][k]=a[k][q]=s*apk+c*aqk
  if worst<1e-13:return sorted((a[i][i] for i in range(n)),reverse=True)
 raise ValueError('Jacobi did not converge')
records=[]
for ell in (9,10,11,12):
 L,e=divmod(ell,3);pattern=((L,L,L),(L,L,L+1),(L,L+1,L+1))[e];types=sorted(set(pattern))
 words={t:list(reduced(t)) for t in types};V={t:[w for w in words[t] if w!=inv(w)] for t in types};vertices=[w for t in types for w in V[t]]
 Vset=set(vertices);index={w:i for i,w in enumerate(vertices)};E=Counter();total=kept=0;maxdeg=0;repeated=0
 C=Counter()
 for i in range(3):
  t,u=pattern[i],pattern[(i+1)%3];C[t,u]+=1;C[u,t]+=1
 require([[C[t,u] for u in types] for t in types]==([[6]],[[2,2],[2,0]],[[0,2],[2,2]])[e],'type positions')
 for w in reduced(ell):
  if parts[w[-1]]==parts[w[0]]:continue
  total+=1;s=0;blocks=[]
  for t in pattern:blocks.append(w[s:s+t]);s+=t
  if any(b not in Vset for b in blocks):continue
  kept+=1;degree=Counter()
  if len(set(blocks))<3:repeated+=1
  for i in range(3):
   x=inv(blocks[i]);y=blocks[(i+1)%3]
   require(x!=y,'loop')
   E[x,y]+=1;E[y,x]+=1;degree[x]+=1;degree[y]+=1
  maxdeg=max(maxdeg,max(degree.values()))
  require(max(degree.values())<=3,'degree contribution')
 completion={}
 for h in set(ell-t-u for t in types for u in types if C[t,u]):
  vh=[w for w in reduced(h) if w!=inv(w)]
  for b,f in itertools.product(B,repeat=2):completion[h,b,f]=sum(parts[b]!=parts[w[0]] and parts[f]!=parts[w[-1]] for w in vh)
 for x,y in itertools.product(vertices,repeat=2):
  t,u=len(x),len(y)
  want=C[t,u]*int(parts[x[0]]!=parts[y[0]])*completion.get((ell-t-u,x[-1],y[-1]),0)
  require(E[x,y]==want,'exact oriented fixed-cut kernel mismatch')
 require(sum(E.values())==6*kept,'total edge incidences')
 classes=defaultdict(list)
 for x in vertices:classes[len(x),x[0],x[-1]].append(x)
 labels=sorted(classes);representatives=[classes[c][0] for c in labels]
 degrees={x:sum(E[x,y] for y in vertices) for x in vertices}
 for label,rows in classes.items():
  require(all(degrees[x]==degrees[rows[0]] for x in rows),'degree compression')
  for x in rows:
   for y in vertices:require(E[x,y]==E[rows[0],y],'row compression')
 require(min(degrees.values())>0,'finite graph has isolated vertex')
 sym=[[math.sqrt(len(classes[labels[i]])*len(classes[labels[j]]))*E[x,y]/math.sqrt(degrees[x]*degrees[y]) for j,y in enumerate(representatives)] for i,x in enumerate(representatives)]
 ev=eigenvalues(sym);require(abs(ev[0]-1)<1e-10,'principal eigenvalue')
 records.append({'ell':ell,'cut_pattern':pattern,'cyclic_rooted_words':total,'retained':kept,'rejected':total-kept,'vertices':len(vertices),'endpoint_classes':len(labels),'oriented_type_matrix':[[C[t,u] for u in types] for t in types],'max_degree_contribution':maxdeg,'retained_repeated_block_words':repeated,'integer_kernel_sha256':hashlib.sha256(json.dumps([(index[x],index[y],v) for (x,y),v in sorted(E.items())]).encode()).hexdigest(),'exact_pair_checks':len(vertices)**2,'exact_kernel':'PASS','finite_mean_second_eigenvalue_float':ev[1],'finite_mean_gap_float':1-ev[1]})
# w^3 is a retained cyclic relator with three parallel edges; L_j norm=6 and degree=3.
w=(0,2,0,3);require(w!=inv(w) and parts[w[0]]!=parts[w[-1]],'power witness')
# 2x2 Laplacian [[3,-3],[-3,3]] has eigenvalues 0,6 exactly.
power={'block':w,'relator':w*3,'signed_vertices':[w,inv(w)],'parallel_edges':3,'per_vertex_degree':3,'laplacian_nonzero_eigenvalue':6,'repeated_cells_two_samples_nonzero_eigenvalue':12}
imbalance=[]
for m in (1,2,10,10**3,10**6,10**12):
 s=math.sqrt(1+8*m);rho=(s-1)/(s+1);margin=1/(s+1)
 imbalance.append({'parts':[m,1,1],'rho':rho,'unequal_limit_second_eigenvalue':rho/2,'true_limit_gap_above_half':margin,'paper_gamma_above_half':margin/2})
# Accepted-label independence under literal linear-word thinning: exact joint counts.
# Enumerate two length-3 draws. Accepted cyclic labels are uniform given count=1 or 2.
linear=list(reduced(3));cyclic=[w for w in linear if parts[w[0]]!=parts[w[-1]]];Cset=set(cyclic);labels=Counter();both=Counter();counts=Counter()
for a,b in itertools.product(linear,repeat=2):
 acc=tuple(w for w in (a,b) if w in Cset);counts[len(acc)]+=1
 if len(acc)==1:labels[acc[0]]+=1
 if len(acc)==2:both[acc]+=1
require(len(set(labels.values()))==1 and set(labels)==Cset,'accepted single label not uniform')
require(len(both)==len(cyclic)**2 and set(both.values())=={1},'accepted two labels not IID')
result={'status':'PASS','scope':'Exact finite counts and constructions plus explicitly floating spectral diagnostics; not the asymptotic proof.','alphabet':'C2xC2 subset of two generating involutions; C2; C2','records':records,'sharp_power_relator_witness':power,'extreme_imbalance_boundary':imbalance,'literal_linear_thinning':{'linear_universe':len(linear),'cyclic_universe':len(cyclic),'two_draw_count_distribution':dict(counts),'uniform_labels_given_count_1':'PASS','IID_labels_given_count_2':'PASS'}}
print(json.dumps(result,indent=2))
