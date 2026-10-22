#!/usr/bin/env python3
"""Independent finite falsification checks; no literature or universal-proof claim."""
import itertools as it,json,sys

def require(v,msg):
 if not v:raise ValueError(msg)
def check(m,q,e,n):
 errors=[]
 for x in range(n):
  if q[e][x]!=x:errors.append('S2')
  if q[x][e]!=e:errors.append('S4')
  if q[x][x]!=e:errors.append('L1')
  for y in range(n):
   if ((q[x][y]==e and q[y][x]==e)!=(x==y)):errors.append('L3')
   for z in range(n):
    if q[x][m[y][z]]!=m[q[x][y]][q[x][z]]:errors.append('S1')
    if q[m[x][y]][z]!=q[q[x][y]][q[x][z]]:errors.append('S3')
    if q[q[x][y]][q[x][z]]!=q[q[y][x]][q[y][z]]:errors.append('L2')
 return set(errors)
def semilattices(n):
 pairs=list(it.combinations(range(n),2))
 for values in it.product(range(n),repeat=len(pairs)):
  m=[[i if i==j else None for j in range(n)] for i in range(n)]
  for (i,j),v in zip(pairs,values):m[i][j]=m[j][i]=v
  if all(m[m[x][y]][z]==m[x][m[y][z]] for x,y,z in it.product(range(n),repeat=3)):yield m

def main():
 if '--inject-failure' in sys.argv:require(False,'explicit independent false-predicate control')
 result={};census=[]
 for n in range(1,5):
  count=topcount=projections=joint=0
  for m in semilattices(n):
   count+=1
   for e in range(n):
    proj=[[y for y in range(n)] for x in range(n)]
    require(not (check(m,proj,e,n)&{'S1','S2','S3','S4'}),'projection failed');projections+=1
    top=all(m[x][e]==x for x in range(n))
    if top:
     topcount+=1;q=[[e if m[x][y]==x else m[x][y] for y in range(n)] for x in range(n)]
     require(not check(m,q,e,n),'conditional meet formula fails')
     require(all((m[x][y]==x)==(q[x][y]==e) for x,y in it.product(range(n),repeat=2)),'order mismatch');joint+=1
    if n<=3:
     fixed={}
     for x in range(n):fixed[e,x]=x;fixed[x,e]=e;fixed[x,x]=e
     free=[p for p in it.product(range(n),repeat=2) if p not in fixed];valid=0;tables=0
     for values in it.product(range(n),repeat=len(free)):
      q=[[None]*n for _ in range(n)]
      for (x,y),v in {**fixed,**dict(zip(free,values))}.items():q[x][y]=v
      tables+=1
      if not check(m,q,e,n):
       valid+=1;require(top,'counterexample to greatest-element necessity')
       require(all((m[x][y]==x)==(q[x][y]==e) for x,y in it.product(range(n),repeat=2)),'counterexample to order coincidence')
     require((valid>0)==top,'small simultaneous existence classification fails')
     census.append({'n':n,'e':e,'tables':tables,'valid_joint':valid,'top':top})
  result[str(n)]={'labelled_meet_semilattices':count,'top_structures':topcount,'all_point_projections':projections,'conditional_joint_structures':joint}
 # M3, N5, B4 explicit orders reconstructed independently.
 extra={}
 for name,n,le in [('M3',5,lambda x,y:x==0 or y==4 or x==y),('N5',5,lambda x,y:x==0 or y==4 or x==y or (x==1 and y==2)),('B4',4,lambda x,y:x&y==x)]:
  m=[]
  for x in range(n):
   row=[]
   for y in range(n):
    lows=[z for z in range(n) if le(z,x) and le(z,y)];greatest=[z for z in lows if all(le(t,z) for t in lows)];require(len(greatest)==1,'missing explicit meet');row.append(greatest[0])
   m.append(row)
  e=n-1;q=[[e if le(x,y) else m[x][y] for y in range(n)] for x in range(n)];require(not check(m,q,e,n),'extra joint example failed');extra[name]={'joint_pass':True,'meet':m,'operation':q}
  if name=='B4':
   wrong=[[e if le(x,y) else y for y in range(n)] for x in range(n)];require('S1' in check(m,wrong,e,n),'wrong historical operation accepted');extra[name]['wrong_y_branch_rejected_at_S1']=True
  if name=='N5':
   cover=lambda a,b:le(b,a) and a!=b and not any(le(b,z) and le(z,a) and z not in (a,b) for z in range(n))
   require(cover(4,3) and m[2][3]==0 and not cover(2,0),'N5 lower semimodularity witness failed');extra[name]['nondiscrete_lower_semimodular_counterexample']=True
 # Larger hIS4 class must not replace the required identities.
 m=[[min(x,y) for y in range(4)] for x in range(4)];q=[[3,3,3,3],[0,3,3,3],[0,0,3,3],[0,1,2,3]]
 errors=check(m,q,3,4)
 require(errors=={'S3','L2'},'hIS4 countermodel differs')
 require(all(min(x,q[x][y])<=y and q[x][min(x,y)]==q[x][y] for x,y in it.product(range(4),repeat=2)),'hemiimplicative/H4 countermodel malformed')
 print(json.dumps({'status':'PASS','finite_only':True,'enumeration':result,'operation_census_n_le_3':census,'extra_models':extra,'hIS4_countermodel_fails':sorted(errors),'empty_boundary':'No element can be distinguished in empty carrier; no empty instance manufactured.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
