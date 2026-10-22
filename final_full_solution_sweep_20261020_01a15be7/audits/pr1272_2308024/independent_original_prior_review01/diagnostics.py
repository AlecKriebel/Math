"""Finite exact diagnostics only; the universal theorem is proved in DERIVATION.md."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial as fac,comb
import hashlib,json,sys
P=Path(__file__).resolve().parent
checks=[]
def check(name,ok):
 if not ok:raise RuntimeError(name)
 checks.append(name)
def sha(b):return hashlib.sha256(b).hexdigest()
def poly_mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for j,x in enumerate(a):
  for k,y in enumerate(b):c[j+k]+=x*y
 return c
def singleton_norm(a):return sum((Q(abs(x),fac(j)) for j,x in enumerate(a)),Q(0))
for entry in json.loads((P/'PINNED_PR_INPUTS.json').read_text()):
 b=(P/'pinned_pr'/Path(entry['path']).name).read_bytes()
 check('pin '+Path(entry['path']).name,len(b)==entry['bytes'] and sha(b)==entry['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==entry['blob'])
m=json.loads((P/'pinned_pr/PUBLIC_MANIFEST.json').read_text())
check('public manifest membership',m['file_count']==8 and len(m['files'])==7 and {x['path'] for x in m['files']}=={x.name for x in (P/'pinned_pr').iterdir()}-{'PUBLIC_MANIFEST.json'})
for e in m['files']:
 b=(P/'pinned_pr'/e['path']).read_bytes();check('public hash '+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'])
a=json.loads((P/'pinned_pr/ACCEPTANCE.json').read_text())
for e in a['bound_public_artifacts']:
 b=(P/'pinned_pr'/e['path']).read_bytes();check('acceptance hash '+e['path'],len(b)==e['bytes'] and sha(b)==e['sha256'])
for j in range(16):
 for k in range(16):check('factorial2 binomial '+str((j,k)),fac(j+k)**2>=comb(j+k,j)*fac(j)**2*fac(k)**2)
# Arbitrary positive nonmonotone finite ratios: AGM requires no monotonicity.
ratios=[Q((1 if j%2 else 7),10*(j+1)**2) for j in range(30)]
check('ratios intentionally nonmonotone',any(ratios[j+1]>ratios[j] for j in range(len(ratios)-1)))
for n in range(1,31):
 for N in range(n):
  part=ratios[N:n];prod=Q(1)
  for r in part:prod*=r
  check('finite tail AGM '+str((N,n)),prod*(n-N)**(n-N)<=sum(part)**(n-N))
for n in range(31):
 coeff=[0]*n+[1];check('singleton monomial exactnorm '+str(n),singleton_norm(coeff)==Q(1,fac(n)))
polys=[[0],[1],[0,1],[-2,3,0,-1],[1,-1,1,-1,1],[Q(1,3),Q(-2,7),Q(4,5)]]
for i,a in enumerate(polys):
 for j,b in enumerate(polys):check('singleton product '+str((i,j)),singleton_norm(poly_mul(a,b))<=singleton_norm(a)*singleton_norm(b))
for X in [[Q(0)],[Q(0),Q(1)],[Q(-2),Q(0),Q(3)]]:
 for lam in [Q(-5),Q(5),Q(1,2),Q(7,2)]:
  if lam in X:continue
  d=min(abs(x-lam) for x in X)
  for N in [0,1,5,12]:
   actual=sum((max(Q(fac(n),1)/abs(x-lam)**(n+1) for x in X)/fac(n)**2 for n in range(N+1)),Q(0))
   bound=sum((Q(1,fac(n))/d**(n+1) for n in range(N+1)),Q(0))
   check('resolvent finite-prefix exact '+str((X,lam,N)),actual==bound)
# Necessary scope stress: zero values do not identify the coordinate with zero.
check('singleton value collision',Q(0)==Q(0) and singleton_norm([0,1])==1 and singleton_norm([0])==0)
check('singleton higher powers strict shrink',singleton_norm([0,0,1])<singleton_norm([0,1]))
# Weaker binomial-only weights n!: the pole at1 has every singleton derivative term1.
check('binomial alone not nonanalytic',all(Q(fac(n),fac(n))==1 for n in range(1,30)))
check('binomial-only resolvent prefix unbounded',sum(Q(fac(n),fac(n)) for n in range(50))==50)
for name in ['original_2018v2.pdf','abtahi_honary_2007.pdf','feinstein_kamowitz_2003v1.pdf']:
 check('real PDF '+name,(P/'sources'/name).read_bytes().startswith(b'%PDF-'))
check('reject2019 HTMLasPDF',not(P/'sources/original_2019_chapter.pdf').read_bytes().startswith(b'%PDF-'))
check('reject1973 coredata as fullproof',b'<coredata>' in (P/'sources/dales_davie_1973_api.xml').read_bytes() and b'<originalText>' not in (P/'sources/dales_davie_1973_api.xml').read_bytes())
d=json.loads((P/'sources/crossref_dales_davie.json').read_text())['message']
check('1973 DOI metadata exact',d['DOI']=='10.1016/0022-1236(73)90065-7' and d['title']==['Quasianalytic Banach function algebras'] and [x['family'] for x in d['author']]==['Dales','Davie'] and d['issued']['date-parts']==[[1973,5]])
h=json.loads((P/'sources/crossref_abtahi_honary.json').read_text())['message']
check('2007 DOI metadata exact',h['DOI'].casefold()=='10.1017/s0017089507003576' and [x['family'].casefold() for x in h['author']]==['abtahi','honary'] and h['issued']['date-parts']==[[2007,5]])
o=json.loads((P/'sources/datacite_arxiv_original.json').read_text())['data']['attributes']
check('original arxiv metadata version2',o['doi']=='10.48550/arxiv.1809.07200' and o['version']=='2' and o['publicationYear']==2018)
f=json.loads((P/'sources/datacite_arxiv_feinstein.json').read_text())['data']['attributes']
check('FKarxiv version1',f['doi']=='10.48550/arxiv.math/0311091' and f['version']=='1' and f['publicationYear']==2003)
ledger=json.loads((P/'LEDGER_DUPLICATE_CHECK.json').read_text())
check('ledger two stable43colviews',ledger['columns']==43 and ledger['metadata_stable'] and ledger['typed_views_identical'] and ledger['service_write_calls']==0)
print(json.dumps({'optimized':sys.flags.optimize,'pass':True,'count':len(checks),'checks':checks,'scope':'Finite exact rational arithmetic, artifacts/source identity and negative category controls. Does not prove arbitrary-weight limit, infinite convergence, automatic continuity, character exhaustiveness or historical full-scope priority; see DERIVATION/REPORT.','real_service_writes':0},indent=2))
