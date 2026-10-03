"""Source-first independent exact controls. No candidate imports, network, or dependencies."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd, isqrt
from functools import reduce
from pathlib import Path
import json

def cross(a,b):
 return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def canonical(a):
 a=tuple(F(x) for x in a)
 if not any(a): raise ValueError('zero projective representative')
 first=next(x for x in a if x)
 return tuple(x/first for x in a)
def on(l,p): return sum(a*b for a,b in zip(l,p))==0
def singulars(lines):
 ls=sorted(set(canonical(l) for l in lines))
 pts=sorted(set(canonical(cross(a,b)) for a,b in combinations(ls,2)))
 return ls,pts

def all_line_k(pts):
 pts=sorted(set(canonical(p) for p in pts))
 if not pts:return 0,[]
 if len(pts)==1:return 1,[]
 ls=sorted(set(canonical(cross(a,b)) for a,b in combinations(pts,2)))
 rec=[{'line':l,'point_indices':[i for i,p in enumerate(pts) if on(l,p)]} for l in ls]
 return max(len(x['point_indices']) for x in rec),rec

def cutoff(r,k):
 if not(0<r<k*k):return None
 a=k*k-r;b=2*k+3*r-r*k;c=1-3*r
 return (-b+isqrt(b*b-4*a*c))//(2*a)

def balanced_Q(M,r):
 q,s=divmod(M,r)
 return r*q*(q-1)+2*q*s

def monomials(d):return [(a,b,d-a-b) for a in range(d+1) for b in range(d+1-a)]
def jet_matrix(pts,d,ms):
 mons=monomials(d);rows=[];labels=[]
 for i,(p,m) in enumerate(zip(pts,ms)):
  chart=next(j for j in [2,1,0] if p[j])
  idx=[j for j in range(3) if j!=chart]
  u,v=p[idx[0]]/p[chart],p[idx[1]]/p[chart]
  for a in range(m):
   for b in range(m-a):
    row=[]
    for exp in mons:
     s,t=exp[idx[0]],exp[idx[1]]
     row.append(F(0) if a>s or b>t else comb(s,a)*comb(t,b)*u**(s-a)*v**(t-b))
    rows.append(row);labels.append([i,chart,a,b])
 return mons,labels,rows

def rref(matrix,ncols):
 a=[list(row) for row in matrix];pivs=[];h=0
 for col in range(ncols):
  ix=next((i for i in range(h,len(a)) if a[i][col]),None)
  if ix is None:continue
  a[h],a[ix]=a[ix],a[h];p=a[h][col];a[h]=[v/p for v in a[h]]
  for i in range(len(a)):
   if i!=h and a[i][col]:
    q=a[i][col];a[i]=[v-q*w for v,w in zip(a[i],a[h])]
  pivs.append(col);h+=1
  if h==len(a):break
 return a,pivs

def jet_record(pts,d,ms):
 mons,labels,mat=jet_matrix(pts,d,ms);a,piv=rref(mat,len(mons));basis=[]
 for free in range(len(mons)):
  if free in piv:continue
  v=[F(0)]*len(mons);v[free]=F(1)
  for row,col in zip(a,piv):v[col]=-row[free]
  assert all(sum(x*y for x,y in zip(row,v))==0 for row in mat)
  basis.append(v)
 return {'d':d,'m':ms,'M':sum(ms),'Q':sum(m*(m-1) for m in ms),'monomials':mons,'labels':labels,'matrix':mat,'rref':a,'pivot_columns':piv,'rank':len(piv),'nullity':len(mons)-len(piv),'nullspace_basis':basis}

def vectors(r,d,total,prefix=()):
 if r==0:
  if total==0:yield prefix
  return
 for m in range(max(0,total-d*(r-1)),min(d,total)+1):yield from vectors(r-1,d,total-m,prefix+(m,))

def finite_control(name,pts):
 pts=sorted(set(canonical(p) for p in pts));r=len(pts);k,ls=all_line_k(pts);D=cutoff(r,k)
 tests=[]
 if D is not None:
  for d in range(2,D+1):
   for m in vectors(r,d,k*d+1):
    # Filtering is justified only as a screen for irreducible candidate vectors.
    if sum(v*(v-1) for v in m)>(d-1)*(d-2):continue
    tests.append(jet_record(pts,d,m))
 return {'name':name,'points':pts,'r':r,'k':k,'all_point_pair_lines':ls,'D':D,'tests':tests,'violating_forms':[i for i,t in enumerate(tests) if t['nullity']]}

def encoder(x):
 if isinstance(x,F):return str(x)
 raise TypeError(type(x))

def main():
 out={'protocol':'SOURCE-FIRST; controls coded and executed before candidate or historical review reads','field':'Q; Fraction exact arithmetic','controls':[]}
 for name,lines in [('single_line',[(1,0,0)]),('pencil',[(1,0,0),(0,1,0),(1,-1,0),(2,3,0)]),('triangle',[(1,0,0),(0,1,0),(0,0,1)]),('five_tangent_lines',[(1,t,t*t) for t in range(5)])]:
  ls,pts=singulars(lines);k,rec=all_line_k(pts)
  out['controls'].append({'name':name,'lines':ls,'points':pts,'r':len(pts),'k_all':k,'k_components':max((sum(on(l,p) for p in pts) for l in ls),default=0),'all_point_pair_lines':rec})
  if name in ['triangle','five_tangent_lines']:out['controls'].append(finite_control(name+'_finite',pts))
  if name=='single_line':assert len(pts)==0
  if name=='pencil':assert len(pts)==k==1
  if name=='triangle':assert len(pts)==3 and k==2
 pts=[(t,t*t,1) for t in range(7)]+[(2,2,1)]
 c=finite_control('nonarrangement_conic_countercontrol',pts)
 assert c['r']==8 and c['k']==3 and c['D']==2 and len(c['violating_forms'])==1
 out['controls'].append(c)
 for name,d,pts,ms in [('irreducible_nodal_cubic_multiplicity',3,[(0,0,1),(-1,0,1),(3,6,1),(8,24,1),(15,60,1)],[2,1,1,1,1]),('reducible_xy_genus_invalid',2,[(0,0,1),(0,1,1),(1,0,1)],[2,1,1])]:
  rec=jet_record([canonical(p) for p in pts],d,ms);assert rec['nullity']>0
  out['controls'].append({'name':name,'points':pts,'jet_test':rec})
 out['cutoff_grid']=[]
 for k in range(2,21):
  for r in range(1,k*k):
   D=cutoff(r,k);a=k*k-r;b=2*k+3*r-r*k;c=1-3*r
   assert a*(D+1)**2+b*(D+1)+c>0
   assert a*D*D+b*D+c<=0
   for d in range(2,min(D+3,150)):
    assert balanced_Q(k*d+1,r)>=F((k*d+1)**2,r)-(k*d+1)
    if d>D:assert balanced_Q(k*d+1,r)>(d-1)*(d-2)
   out['cutoff_grid'].append({'r':r,'k':k,'D':D})
 out['equality_r_k_squared']=[{'k':4,'r':16,'d':4*t,'m':[t+1]+[t]*15,'M':16*t+1,'Q':16*t*t-14*t,'genus_rhs':(4*t-1)*(4*t-2),'status':'necessary genus constraints survive; no curve existence asserted'} for t in [1,2,10,100,1000]]
 for c in out['equality_r_k_squared']:assert c['M']>c['k']*c['d'] and c['Q']<=c['genus_rhs']
 p=Path(__file__).with_name('independent_full_output.json');p.write_text(json.dumps(out,default=encoder,indent=2)+'\n')
 summary={'control_count':len(out['controls']),'cutoff_grid_cases':len(out['cutoff_grid']),'finite_cases':[{k:c[k] for k in ['name','r','k','D']}|{'tests':len(c['tests']),'violating_forms':len(c['violating_forms'])} for c in out['controls'] if 'tests' in c]}
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
