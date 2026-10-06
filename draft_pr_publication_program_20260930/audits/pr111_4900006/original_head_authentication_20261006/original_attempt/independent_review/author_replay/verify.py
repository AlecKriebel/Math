from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
import json,hashlib
n=0
f=lambda s:-(s-1)*(s-4)/(1+s*s)
df=lambda s:(5+6*s-5*s*s)/(1+s*s)**2
for j in range(2001):
 s=Q(j,100)
 assert f(s)==-1+(5*s-3)/(1+s*s);n+=1
 assert f(s)+4==(3*s*s+5*s)/(1+s*s);n+=1
 assert Q(-4)<=f(s)<=Q(3,2);n+=1
 assert 2*s*df(s)<=(10*s+12*s*s)/(1+s*s)**2<=8;n+=1
 assert 2*f(s)+2*s*df(s)<=11;n+=1
assert f(Q(0))==-4 and f(Q(1))==f(Q(4))==0;n+=1
assert f(Q(1))+2*df(Q(1))==3;n+=1
assert f(Q(4))+8*df(Q(4))==Q(-24,17);n+=1
S={'O':(Q(-4),Q(-4)),'U':(Q(3),Q(0)),'S':(Q(0),Q(-24,17))}
def ky(v):
 v=sorted(v,reverse=True);sm=Q(0)
 for j,x in enumerate(v):
  if sm+x<0:return Q(j)+sm/(-x)
  sm+=x
 return Q(len(v))
expected={'OO':Q(0),'OU':Q(11,4),'OS':Q(1),'UU':Q(203,50),'US':Q(4)+Q(27,1700),'SS':Q(2)}
table={};maxs=[None]*5
for a,b in combinations_with_replacement(['O','U','S'],2):
 v=sorted(S[a]+S[b]+(Q(-100),),reverse=True);k=ky(v)
 assert k==expected[a+b];n+=1
 assert v[-1]==-100;n+=1
 sums=[sum(v[:i+1]) for i in range(5)]
 for i,x in enumerate(sums):maxs[i]=x if maxs[i] is None else max(maxs[i],x)
 table[a+b]={'spectrum':[str(x) for x in v],'pointwise_KY':str(k),'fixed_j4':str(4+sums[3]/100)}
assert maxs==list(map(Q,[3,6,6,6,-94]));n+=1
assert Q(203,50)>Q(79,20)>Q(96,25);n+=1
assert Q(203,50)>Q(4)-Q(8,85);n+=1
assert max(expected.values())==Q(203,50);n+=1
r={'assertions':n,'all_pass':True,'spectral_table':table,'max_partial_sums':[str(x) for x in maxs],'artifact_sha256':hashlib.sha256(Path('COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'scope':'Unrestricted global-attractor maximizer assertion only; no Lorenz-specific, chaotic or generic-system claim.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['assertions','all_pass','artifact_sha256']}))
