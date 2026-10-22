"""Finite exact algebra/metric controls, not universal surface/Anosov proof certification."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import hashlib,json,sys
P=Path(__file__).resolve().parent;checks=[]
def check(n,ok):
 if not ok:raise RuntimeError(n)
 checks.append(n)
def mm(A,B):return [[sum((x*y for x,y in zip(r,c)),Q(0))for c in zip(*B)]for r in A]
def tp(A,B):return [[a*b for a in r for b in s]for r in A for s in B]
def vv(a,b):return[x*y for x in a for y in b]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def pair(a,B,b):return dot(a,[dot(r,b)for r in B])
def det3(A):return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
w=[[Q(0),Q(1)],[Q(-1),Q(0)]];B=tp(w,w)
for a,b in product(range(21),repeat=2):
 a=Q(a,3);b=Q(b,3);logs=sorted([a+b,a-b,-a+b,-a-b],reverse=True)
 check('tensor gap '+str((a,b)),logs[0]-logs[1]==2*min(a,b))
check('directsum equal-factor negative',sorted([2,-2,2,-2],reverse=True)[0]-sorted([2,-2,2,-2],reverse=True)[1]==0)
check('identicalfactor tensor gap remains positive',sorted([4,0,0,-4],reverse=True)[0]-sorted([4,0,0,-4],reverse=True)[1]==4)
# B has two positive and two negative orthogonal directions, all exact.
basis=[[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]]
gram=[[pair(a,B,b)for b in basis]for a in basis]
check('Bsignature22',gram==[[2,0,0,0],[0,-2,0,0],[0,0,-2,0],[0,0,0,2]])
matrices=[[[1,Q(t)],[0,1]]for t in range(-3,4)]+[[[Q(2),0],[0,Q(1,2)]],[[0,-1],[1,0]]]
for i,A in enumerate(matrices):
 for j,C in enumerate(matrices):
  T=tp(A,C);check('Bpreservation '+str((i,j)),mm(mm(list(map(list,zip(*T))),B),T)==B)
for x,y in product(range(-4,5),repeat=2):
 u=vv([1,x],[1,x**3]);v=vv([1,y],[1,y**3])
 check('Segre null '+str((x,y)),pair(u,B,u)==0)
 if x!=y:check('Segre transverse '+str((x,y)),pair(u,B,v)==(y-x)*(y**3-x**3)and pair(u,B,v)!=0)
for x in range(-3,2):
 vals=[x,x+1,x+2];vs=[vv([1,t],[1,t**3])for t in vals];G=[[-pair(a,B,b)for b in vs]for a in vs]
 check('optional triple Qsignature21 '+str(x),sum(G[i][i]for i in range(3))==0 and det3(G)<0)
for n in range(2,21):
 for power in range(1,5):
  pts=[(Q(k,n),Q(k,n)**power)for k in range(n+1)];total=Q(0)
  for k in range(n):
   dx=pts[k+1][0]-pts[k][0];dy=pts[k+1][1]-pts[k][1];total+=dx+dy
   check('monotone length increment '+str((n,power,k)),dx*dx+dy*dy<=(dx+dy)**2)
   check('rotated Lipschitz '+str((n,power,k)),abs(dy-dx)<=dx+dy)
  check('monotone period L1bound '+str((n,power)),total==2)
for t,s in product([Q(-2),Q(-1,2),Q(0),Q(1,3),Q(1)],repeat=2):
 u=[(1-t*t)/(1+t*t),2*t/(1+t*t)];v=[(1-s*s)/(1+s*s),2*s/(1+s*s)]
 du=[-u[1],u[0]];dv=[-v[1],v[0]]
 for a,b in [(Q(1),Q(0)),(Q(0),Q(1)),(Q(1),Q(1)),(Q(-2),Q(3,4))]:
  D=[a*x+b*y for x,y in zip(vv(du,v),vv(u,dv))]
  check('Segre differential isometry '+str((t,s,a,b)),dot(D,D)==a*a+b*b)
for n in range(1,30):
 lam=Q(1,2);x=lam**n;model=x*abs(x)
 check('strictscale secant decay '+str(n),model/x==x and (lam*model*lam)==(lam*x)*abs(lam*x))
for n in range(1,11):
 step=Q(1,n+1)
 def model_h(t):return t*abs(t)
 check('one-fixedpoint C1model secants '+str(n),model_h(step)/step==step and (model_h(1+step)-model_h(1))/step==2+step)
for e in json.loads((P/'PINNED_PR_INPUTS.json').read_text()):
 b=(P/'pinned_pr'/Path(e['path']).name).read_bytes()
 check('PRblob '+Path(e['path']).name,len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'])
for e in json.loads((P/'pinned_pr/MANIFEST.json').read_text())['files']:
 b=(P/'pinned_pr'/e['file']).read_bytes();check('PRmanifest '+e['file'],len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'])
for e in json.loads((P/'pinned_pr/ACCEPTANCE.json').read_text())['bound_files']:
 b=(P/'pinned_pr'/e['file']).read_bytes();check('acceptance '+e['file'],len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'])
for name,expected in [('original_owr2018','0bd596abb171c94b1ff9352fba8f2a2cf91e12dd29180590ce2425054ea17de7'),('psw_published','f51e22b08ecb14183300a9de5e285f68a99746676341d6f9a1ca8da6d925adc2'),('gm_arxiv_v2','a9200c0966535f3700fd6e58407137ffddd679f0da31c73898f1d3d5c9900c37')]:
 b=(P/'sources'/(name+'.pdf')).read_bytes();check('freshprimaryPDF '+name,b.startswith(b'%PDF-')and hashlib.sha256(b).hexdigest()==expected)
check('do not mislabel GMjournalHTML',not(P/'sources/gm_advertised_journal_payload.bin').read_bytes().startswith(b'%PDF-'))
m=json.loads((P/'sources/crossref_psw.json').read_text())['message'];check('PSWversionrecord',m['DOI']=='10.2140/gt.2023.27.3303'and m['title']==['Anosov representations with Lipschitz limit set']and[x['family']for x in m['author']]==['Pozzetti','Sambarino','Wienhard']and m['issued']['date-parts']==[[2023,11,9]])
a=json.loads((P/'sources/psw_arxiv_metadata.json').read_text())['data']['attributes'];check('PSWalternateDOIfamily',a['doi']=='10.48550/arxiv.1910.06627'and any(e.get('relatedIdentifier')=='10.2140/gt.2023.27.3303'for e in a['relatedIdentifiers']))
print(json.dumps({'pass':True,'optimized':sys.flags.optimize,'count':len(checks),'checks':checks,'limitations':'Finite exact algebra/metric controls. Written proof establishes arbitrary-group uniform gap, rectifiability and intrinsic non-C1 via minimality. Historical source check counts not rerun; no proof-assistant certification.','service_writes':0},indent=2))
