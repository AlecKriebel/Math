"""Exact point-jet controls of plausible antecedent implications; no historical replay."""
from fractions import Fraction as Q
from pathlib import Path
import json

def mat(n):return [[Q(0) for j in range(n)] for i in range(n)]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def torsion(a,d):
 n=len(a); t={}
 for i in range(n):
  for j in range(n):
   t[i,j]=[sum(a[l][i]*d[l][k][j]-a[l][j]*d[l][k][i]-a[k][l]*d[i][l][j]+a[k][l]*d[j][l][i] for l in range(n)) for k in range(n)]
 return t

def bil(t,x,y):return [sum(x[i]*y[j]*t[i,j][k] for i in range(len(x)) for j in range(len(y))) for k in range(len(x))]
def haantjes(a,t):
 n=len(a); out={}
 for i in range(n):
  for j in range(n):
   x=[Q(k==i) for k in range(n)];y=[Q(k==j) for k in range(n)];ax=mv(a,x);ay=mv(a,y)
   v1=mv(a,mv(a,bil(t,x,y)));v2=bil(t,ax,ay);v3=mv(a,bil(t,ax,y));v4=mv(a,bil(t,x,ay));out[i,j]=[v1[k]+v2[k]-v3[k]-v4[k] for k in range(n)]
 return out

def jet(n,f=2,fp=3,diagonal=None):
 a=mat(n);b=mat(n)
 if diagonal is None:
  for i in range(n-1):a[i][i+1]=Q(f);b[i][i+1]=Q(fp)
 else:
  for i,x in enumerate(diagonal):a[i][i]=Q(f*x);b[i][i]=Q(fp*x)
 d=[mat(n) for _ in range(n)];d[n-1]=b
 return a,d

def require(ok,msg):
 if not ok:raise ValueError(msg)
def nonzero(t):return {str((i+1,j+1)):[str(x) for x in v] for (i,j),v in t.items() if any(v)}
rows=[]
for n in range(2,9):
 a,d=jet(n); t=torsion(a,d);h=haantjes(a,t)
 require(bool(nonzero(t))==(n>=4),'incorrect size threshold')
 require(not nonzero(h),'Haantjes scalar cutoff should vanish')
 rows.append({'n':n,'scalar_cutoff_nijenhuis':not bool(nonzero(t)),'scalar_cutoff_haantjes':True,'nonzero_torsion':nonzero(t)})
a,d=jet(2,diagonal=[1,2]); t=torsion(a,d);h=haantjes(a,t)
require(bool(nonzero(t)),'distinct-eigenvalue arbitrary cutoff falsely accepted')
require(not nonzero(h),'diagonal field should have zero Haantjes torsion')
rows.append({'n':2,'diagonal':[1,2],'scalar_cutoff_nijenhuis':False,'scalar_cutoff_haantjes':True,'nonzero_torsion':nonzero(t)})
result={'status':'PASS','exact_arithmetic':'fractions.Fraction','controls':rows,'finite_checks_not_a_general_existence_proof':True,'historical_program_replay':False,'optimized_mode_supported':True}
out=Path(__file__).with_name('PRIOR_ROUTE_CONTROLS_RESULT.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(rows),'detected_false_cutoff_claims':sum(not x['scalar_cutoff_nijenhuis'] for x in rows)}))
