"""Independent local authentication and adversarial algebra/geometric diagnostics.

Does not import another reviewer's or candidate's checker; does not write
outside this review directory or contact providers. The all-period proof is
an analytic argument in REPORT.md, not an inference from finite diagnostics.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations
from math import gcd
import hashlib, json, sys, zipfile

HERE = Path(__file__).resolve().parent
B = HERE.parent
# Resolve the explicitly permitted library-only dependency from the campaign.
VENDOR = Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr261_5100021/initial_review_20261012/reproduction_source_adversary/vendor')
sys.path.insert(0,str(VENDOR))
import sympy as sp
import mpmath as mp

checks=[]
inputs={}
def check(ok,label):
 if not bool(ok):
  raise AssertionError(label)
 checks.append(label)
def pin(path):
 path=Path(path)
 data=path.read_bytes()
 item={'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 inputs[str(path)]=item
 return data
def authenticate(path,item):
 data=pin(path)
 check(len(data)==item['bytes'],str(path)+' byte count')
 check(hashlib.sha256(data).hexdigest()==item['sha256'],str(path)+' SHA256')
 return data

intake=json.loads(pin(B/'INTAKE.json'))
for item in intake['files']:
 body=authenticate(item['local_path'],item)
 oid=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
 check(oid==item['git_blob_oid'],item['repository_path']+' native blob')

manifests=[
 ('priority_primary_lineage/ARTIFACT_MANIFEST.json','public_derived_artifacts'),
 ('priority_primary_lineage/COMPARISON_MANIFEST.json','public_derived_artifacts'),
 ('priority_general_theorem/PUBLIC_MANIFEST.json','included'),
 ('priority_general_theorem/POST_FREEZE_PUBLIC_MANIFEST.json','files'),
 ('priority_repository_archive/public/MANIFEST.json','files'),
]
for rel,key in manifests:
 path=B/rel; d=json.loads(pin(path))
 for item in d[key]:
  authenticate(path.parent/(item.get('relative_path') or item['path']),item)
pin(B/'ROOT_PRIORITY_AUDIT_SYNTHESIS.md')
lineage=json.loads(pin(B/'priority_primary_lineage/VERSION_LINEAGE.json'))
for item in lineage:
 name='invariants_v'+str(item['version']).zfill(2)+'.pdf' if 'version' in item and isinstance(item['version'],int) else 'invariants_final.pdf'
 authenticate(B/'priority_primary_lineage/private_sources'/name,item)
for name in ['invariants_v01_target_page.png','invariants_v11_target_page.png','invariants_final_target_page.png']:
 path=B/'priority_primary_lineage/private_sources'/name
 entries=json.loads((B/'priority_primary_lineage/ARTIFACT_MANIFEST.json').read_text())['private_evidence']
 item=next(x for x in entries if x['relative_path']=='private_sources/'+name)
 authenticate(path,item)
for name in ['cyclic2003.txt','local2003.txt']:
 pin(B/'priority_general_theorem/private_sources'/name)
pin(HERE/'private_reading/current_zenodo_main.txt')

P=B/'priority_repository_archive/private_reading'
record=json.loads(pin(P/'zenodo_23071366_retry.json'))
dc=json.loads(pin(P/'datacite_23071366.json'))['data']
check(record['id']==23071366,'Exact record identity')
check(record['doi']=='10.5281/zenodo.23071366','Record DOI identity')
check(record['status']=='published' and record['metadata']['access_right']=='open','Open published record')
check(record['title']==dc['attributes']['titles'][0]['title'],'DataCite matching exact title')
check(dc['id']==record['doi']==dc['attributes']['doi'],'DataCite exact DOI')
check(dc['attributes']['state']=='findable','DataCite state')
check(dc['attributes']['creators'][0]['familyName']=='Ferudun','DataCite author family')
check(dc['attributes']['url']=='https://zenodo.org/doi/'+record['doi'],'DOI record URL association')
mapping={'main.pdf':('zenodo_23071366_main.pdf','eulersolve_0026.pdf'),
         'arxiv_source.zip':('zenodo_23071366_source.zip','eulersolve_0026_source.zip'),
         'verification_report.md':('zenodo_23071366_verification.md','eulersolve_0026_verification.md')}
get4=json.loads(pin(B/'priority_repository_archive/public/GET_PINS_04.json'))
get3=json.loads(pin(B/'priority_repository_archive/public/GET_PINS_03.json'))
association=[]
for item in record['files']:
 archived,website=mapping[item['key']]
 data=pin(P/archived); other=pin(P/website)
 url='https://zenodo.org/api/records/23071366/files/'+item['key']+'/content'
 check(item['links']['self']==url,'Exact record-owned file URL '+item['key'])
 check(len(data)==item['size'],'Actual official attachment size '+item['key'])
 check('md5:'+hashlib.md5(data).hexdigest()==item['checksum'],'Actual official attachment MD5 '+item['key'])
 check(data==other,'Official attachment equals website bytes '+item['key'])
 capture=next(r for r in get4 if r['name']==archived)
 check(capture['method']=='GET' and capture['status']==200,'Actual successful GET '+item['key'])
 check(capture['url']==capture['final_url']==url,'Recorded GET URL binding '+item['key'])
 check(capture['bytes']==len(data) and capture['sha256']==hashlib.sha256(data).hexdigest(),'GET receipt matches actual bytes '+item['key'])
 association.append({'key':item['key'],'record_url':url,'bytes':len(data),'md5':hashlib.md5(data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest(),'source':'Personally rehashed independent archive-family official GET captures; own fresh GET results recorded separately.'})
rc=next(r for r in get3 if r['name']=='zenodo_23071366_retry.json')
check(rc['status']==200 and rc['method']=='GET','Official record GET succeeded in archive family')
check(rc['bytes']==len(pin(P/'zenodo_23071366_retry.json')) and rc['sha256']==inputs[str(P/'zenodo_23071366_retry.json')]['sha256'],'Official record body receipt authenticates')
source=B/'root_priority_capture_01/reading_private/source'
with zipfile.ZipFile(P/'zenodo_23071366_source.zip') as z:
 for name in ['main.tex','reproducibility/complex_trace_lemma.md']:
  data=z.read(name)
  check(data==pin(source/name),'Inspected full source is actual ZIP member '+name)
check(b'\\date{1 October 2026}' in pin(source/'main.tex'),'Printed TeX date differs from publication metadata')
check(record['metadata']['publication_date']=='2026-09-30','Recorded publication date')
check(record['created']=='2026-09-30T22:04:12.260164+00:00','Recorded creation clock')
check(dc['attributes']['registered']=='2026-09-30T22:04:13.000Z','Recorded DOI registration clock')
fresh_receipts=json.loads(pin(HERE/'FRESH_GET_RECEIPTS.json'))['receipts']
for name,previous in [('current_zenodo_record.json','zenodo_23071366_retry.json'),('current_datacite.json','datacite_23071366.json'),('current_zenodo_main.pdf','zenodo_23071366_main.pdf')]:
 item=next(r for r in fresh_receipts if r['name']==name)
 check(item.get('status')==200 and item['method']=='GET','Own current official GET succeeded '+name)
 data=authenticate(HERE/'private_reading'/name,item)
 check(data==pin(P/previous),'Own current official body equals independently archived body '+name)

symbolic=[]
def identity(expr,label):
 check(sp.cancel(expr)==0,label)
 symbolic.append(label)

# Raw antipedal equations, with no substitution of the candidate pair formula.
h,f,g,r,s=sp.symbols('h f g r s')
mat=sp.Matrix([[h-f,r-g],[h-f,s-g]])
rhs=sp.Matrix([h*(h-f)+r*(r-g),h*(h-f)+s*(s-g)])
q=mat.inv()*rhs
expected=sp.Matrix([h-(r-g)*(s-g)/(h-f),r+s-g])
for j in range(2): identity(q[j]-expected[j],'Raw full-line solution '+str(j))
opp=expected.subs({h:-h,r:-r,s:-s},simultaneous=True)
pair=sp.Matrix([(2*h*g*(r+s)-2*f*(r*s+g*g))/(h*h-f*f),-2*g])
for j in range(2): identity(expected[j]+opp[j]-pair[j],'Raw opposite pair '+str(j))
identity(mat.det()-(h-f)*(s-r),'Raw determinant')

# Eliminate chord roots with the focal support relation, allowing beta<0.
b2,lam=sp.symbols('b2 lam')
a2=b2+f*f+g*g
alpha=(b2-lam)/(b2*b2)
gamma=(a2-lam)/(a2*a2)
beta=(gamma-alpha)/(f*f+g*g)
kappa=alpha+lam/(a2*b2)
A=alpha+beta*g*g
root_sum=-2*h*beta*f*g/A
root_product=(h*h*(alpha+beta*f*f)-1)/A
reduced=(2*h*g*root_sum-2*f*(root_product+g*g))/b2
identity(reduced.subs(h*h,b2+f*f)-(-2*f+2*kappa*f/A),'Focal support and conic root reduction')

# Weighted affine normal conversion in a rational unit-normal chart.
p,Lx,Ly,c=sp.symbols('p Lx Ly c')
nx=(1-p*p)/(1+p*p);ny=2*p/(1+p*p)
alpha=1/(Ly*Ly);gamma=1/(Lx*Lx);beta=(gamma-alpha)/(c*c)
den=alpha+beta*c*c*ny*ny
norm2=Lx*Lx*nx*nx+Ly*Ly*ny*ny
identity(c*nx*nx/den-c*Ly*Ly*Lx*Lx*nx*nx/norm2,'Affine weighted normal x')
identity(c*nx*ny/den-c*Ly*Ly*Lx*Lx*nx*ny/norm2,'Affine weighted normal y')

# Global compact curve identities. Proof of regularity is analytic in report.
z,w,d,e=sp.symbols('z w d e')
F=lambda z,w:d*z*z*w*w-z*z-w*w+2*e*z*w+d
Q=d*z**4+(e*e-d*d-1)*z*z+d
identity(((d*z*z-1)*w+e*z)**2-Q-(d*z*z-1)*F(z,w),'Completed-square compact curve')
v=-z-2*e*w/(d*w*w-1)
identity(F(w,v)-F(z,w),'Root exchange preserves compact curve')
x=sp.symbols('x')
G=(d-x*x)*w*w+2*e*x*w+d*x*x-1
identity(x*x*F(1/x,w)-G,'Complete infinity chart')
identity(sp.diff(G,w).subs(x,0)-2*d*w,'Infinity smoothness derivative')
identity(-2*e*z*z/(d*z*z-1)+2*e/(d-z**-2),'Grouped incident pole cancellation')

# Simple quartic branches: resultant detects all exceptional parameter ranges.
resultant=sp.factor(sp.resultant(Q,sp.diff(Q,z),z))
identity(resultant-16*d**3*((d-1)**2-e*e)**2*((d+1)**2-e*e)**2,'Quartic branch resultant')

# Exact simultaneous-pole edge bookkeeping independent of residue formulas.
bookkeeping_cases=0
for N in range(3,17):
 for mask in range(1<<N):
  J=[j for j in range(N) if mask>>j&1]
  if any((j+1)%N in J for j in J):continue
  edges=[(j-1)%N for j in J]+J
  check(len(edges)==len(set(edges)),f'Nonadjacent pole edge groups N{N} mask{mask}')
  bookkeeping_cases+=1

# Fresh actual tangent and antipedal solves (independent of candidate checkers).
mp.mp.dps=85
def intersect(n1,b1,n2,b2):
 det=n1[0]*n2[1]-n1[1]*n2[0]
 return ((b1*n2[1]-n1[1]*b2)/det,(n1[0]*b2-b1*n2[0])/det),det
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
def neg(x):return(-x[0],-x[1])
numeric=[]
max_error=mp.mpf(0)
for kval in ['0.07','0.63','0.97','0.9997']:
 k=mp.mpf(kval);m=k*k;K=mp.ellipk(m)
 for N in [4,6,8,10,14,18]:
  for tau in range(1,N//2):
   if gcd(tau,N)!=1:continue
   v=2*K*tau/N;delta=2*v
   s=mp.ellipfun('sn',v,m);cn=mp.ellipfun('cn',v,m);dn=mp.ellipfun('dn',v,m)
   a=dn/cn;b=mp.sqrt(1-m)/cn
   lam=b*b*s*s
   alpha=(b*b-lam)/(b**4);gamma=(a*a-lam)/(a**4);beta=(gamma-alpha)/(k*k)
   kappa=alpha+lam/(a*a*b*b);Lx=1/mp.sqrt(gamma);Ly=1/mp.sqrt(alpha)
   base=None
   for phase in ['0.0','0.173','0.491']:
    u=mp.mpf(phase)*K
    pts=[(-a*mp.ellipfun('sn',u+i*delta,m),b*mp.ellipfun('cn',u+i*delta,m)) for i in range(N)]
    normals=[(p[0]/(a*a),p[1]/(b*b)) for p in pts]
    Rs=[intersect(normals[i],1,normals[(i+1)%N],1)[0] for i in range(N)]
    foc=(k,mp.mpf(0));ant=[];min_det=mp.inf
    for i in range(N):
     X=Rs[i];Y=Rs[(i+1)%N]
     qx=(X[0]-k,X[1]);qy=(Y[0]-k,Y[1])
     U,det=intersect(qx,dot(qx,X),qy,dot(qy,Y));ant.append(U);min_det=min(min_det,abs(det))
    mean=tuple(mp.fsum(p[j] for p in ant)/N for j in range(2))
    # Directly reconstruct the claimed pair using independently solved lines.
    errs=[abs(mean[1])]
    if base is not None:errs.extend(abs(mean[j]-base[j]) for j in range(2))
    else:base=mean
    for i in range(N):
     opp=(i+N//2)%N
     errs.extend(abs(Rs[i][j]+Rs[opp][j]) for j in range(2))
     n=normals[(i+1)%N];norm=mp.sqrt(dot(n,n));nx=n[0]/norm;ny=n[1]/norm
     denominator=alpha+beta*k*k*ny*ny
     prediction=(-2*k+2*kappa*k*nx*nx/denominator,2*kappa*k*nx*ny/denominator)
     errs.extend(abs(ant[i][j]+ant[opp][j]-prediction[j]) for j in range(2))
    if N==4:errs.append(abs(mean[0]))
    err=max(errs);max_error=max(max_error,err)
    check(err<mp.mpf('1e-72'),f'Fresh actual geometry k{kval} N{N} tau{tau} phase{phase}')
    check(min_det>0,f'Real nonzero actual determinants k{kval} N{N} tau{tau} phase{phase}')
    numeric.append({'k':kval,'N':N,'tau':tau,'phase_multiple_K':phase,'centroid':[mp.nstr(c,25) for c in mean],'max_error':mp.nstr(err,12),'min_actual_abs_determinant':mp.nstr(min_det,12)})

# Exact padded-odd boundary using a different explicit primitive triangle.
# E: x²/4+y²=1; q=(4-sqrt(13))/3 and lambda=1-q².
q0=(4-sp.sqrt(13))/3
pts=[sp.Matrix([0,1]),sp.Matrix([2*sp.sqrt(1-q0*q0),-q0]),sp.Matrix([-2*sp.sqrt(1-q0*q0),-q0])]
check(0<q0<sp.Rational(1,3),'Odd triangle caustic strict and nondegenerate')
check(sp.simplify(3*q0*q0-8*q0+1)==0,'Odd triangle exact defining quadratic')
lambda0=1-q0*q0
for i in range(3):
 X=pts[i];Y=pts[(i+1)%3]
 check(sp.simplify(X[0]**2/4+X[1]**2-1)==0,'Odd triangle original boundary '+str(i))
 L=sp.Matrix([Y[1]-X[1],X[0]-Y[0]]);constant=L.dot(X)
 check(sp.simplify(constant**2-(4-lambda0)*L[0]**2-(1-lambda0)*L[1]**2)==0,'Odd triangle exact confocal tangency '+str(i))
 contact=sp.Matrix([(4-lambda0)*L[0]/constant,(1-lambda0)*L[1]/constant])
 parameter=sp.simplify((contact-X).dot(Y-X)/(Y-X).dot(Y-X))
 check(bool(parameter>0) and bool(parameter<1),'Odd triangle interior caustic contact '+str(i))
# At either side vertex, equality of unit tangential components reduces to
# this polynomial after squaring two positive quantities; the outward-normal
# signs distinguish specular reflection from unchanged straight flight.
qvar=sp.symbols('qvar')
reflection_polynomial=sp.together(4*(1-qvar*qvar)*(1-3*qvar)**2-16*qvar*qvar*(5+2*qvar-3*qvar*qvar))
check(sp.rem(reflection_polynomial,3*qvar*qvar-8*qvar+1,qvar)==0,'Odd triangle exact unit specular tangency component')
check(1-3*q0>0,'Odd triangle reflection square-root sign')
# Top vertex is symmetric; side incoming normal scalar is positive,
# outgoing normal scalar is negative, by q0,t,L>0. This completes unit
# specular reflection without a potentially ambiguous squared angle.
def exact_mean(points):
 ns=[sp.Matrix([P[0]/4,P[1]]) for P in points]
 Rs=[]
 for i in range(len(points)):
  mat=sp.Matrix.vstack(ns[i].T,ns[(i+1)%len(points)].T)
  Rs.append(sp.simplify(mat.inv()*sp.ones(2,1)))
 Us=[]
 M=sp.Matrix([sp.sqrt(3),0])
 for i in range(len(points)):
  X=Rs[i];Y=Rs[(i+1)%len(points)];qx=X-M;qy=Y-M
  mat=sp.Matrix.vstack(qx.T,qy.T)
  check(sp.simplify(mat.det())!=0,'Exact primitive triangle antipedal determinant '+str(i))
  Us.append(sp.simplify(mat.inv()*sp.Matrix([qx.dot(X),qy.dot(Y)])))
 return sp.simplify(sum(Us,sp.zeros(2,1))/len(Us))
c1=exact_mean(pts+pts);c2=exact_mean([-P for P in pts]+[-P for P in pts])
check(sp.simplify(c1-c2)!=sp.zeros(2,1),'Padded odd-six boundary is not constant')
check(sp.simplify(c1[1]**2)==36 and sp.simplify(c1[1]+c2[1])==0,'Exact padded triangle y means are opposite +/-6')

receipt={'decision':'PASS','completed':True,'utc':datetime.now(timezone.utc).isoformat(),
 'checks':len(checks),'symbolic_identities':symbolic,'pole_bookkeeping_cases':bookkeeping_cases,
 'numeric_geometric_configurations':len(numeric),'numeric_dps':85,'numeric_noninterval':True,
 'max_observed_error':mp.nstr(max_error,15),'actual_deposit_association':association,
 'exact_padded_odd_counterexample_means':[[str(x) for x in c1],[str(x) for x in c2]],
 'claim_limit':'Local authentication and exact identities plus finite noninterval diagnostics. All-period proof judgment and chronology limitations appear in REPORT.md. No provider or publication authority.',
 'numeric_cases':numeric}
(HERE/'INPUT_PINS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'files':list(inputs.values()),'full_third_party_bodies':'Referenced as private inputs; not copied into public packet.'},indent=2)+'\n')
(HERE/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k in ['decision','completed','checks','symbolic_identities','pole_bookkeeping_cases','numeric_geometric_configurations','max_observed_error','exact_padded_odd_counterexample_means']},indent=2))
