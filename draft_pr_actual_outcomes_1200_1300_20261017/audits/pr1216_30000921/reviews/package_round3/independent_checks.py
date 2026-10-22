#!/usr/bin/env python3
"""Fresh exact algebra, immutable archive replay, and corruption controls.
No Git/application operations; all changed inputs are disposable review copies.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
import datetime,hashlib,json,math,random,shutil,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
PUB=HERE.parent.parent/'publication'
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
class Q:
 def __init__(self,r=0,i=0):self.r=F(r);self.i=F(i)
 def __add__(a,b):
  if not isinstance(b,Q):b=Q(b)
  return Q(a.r+b.r,a.i+b.i)
 __radd__=__add__
 def __neg__(a):return Q(-a.r,-a.i)
 def __sub__(a,b):return a+-b if isinstance(b,Q) else a+Q(-b)
 def __mul__(a,b):
  if not isinstance(b,Q):b=Q(b)
  return Q(a.r*b.r-a.i*b.i,a.r*b.i+a.i*b.r)
 __rmul__=__mul__
 def __truediv__(a,b):
  if not isinstance(b,Q):b=Q(b)
  return a*Q(b.r/b.sq(),-b.i/b.sq())
 def sq(a):return a.r*a.r+a.i*a.i
 def __eq__(a,b):return (a-b).sq()==0
 def __pow__(a,n):
  out=Q(1)
  for _ in range(n):out=out*a
  return out

def algebra():
 rng=random.Random(20261017);cases=steps=oracle=prior=0
 def randq():return Q(F(rng.randrange(-4,5),rng.randrange(1,5)),F(rng.randrange(-4,5),rng.randrange(1,5)))
 def ordinary_shift(jets,alpha):
  out=[Q() for _ in jets]
  for k,a in enumerate(jets):
   for j in range(k+1):out[j]=out[j]+a*math.comb(k,j)*((-alpha)**(k-j))/math.factorial(k)
  return out
 def conv(a,b):
  out=[Q() for _ in range(len(a)+len(b)-1)]
  for i,x in enumerate(a):
   for j,y in enumerate(b):out[i+j]=out[i+j]+x*y
  return out
 def derivative(poly,n,alpha):return sum((poly[k]*F(math.factorial(k),math.factorial(k-n))*(alpha**(k-n)) for k in range(n,len(poly))),Q())
 def construct(a,q,m,eta,mutant=None):
  c=[];vals=[]
  for k in range(len(a)):
   n=k+m;A=q[m]*F(math.factorial(n),math.factorial(k))
   if mutant=='wrong_factorial':A=q[m]*(k+1)
   S=A*a[k]
   if mutant!='drop_cross':
    for j in range(m+1,min(len(q)-1,n)+1):S=S+q[j]*F(math.factorial(n),math.factorial(n-j))*(a[n-j]+c[n-j])
   ck=Q() if S.sq()>=eta**2 else (Q(eta)-S)/A
   if mutant=='omit_correction':ck=Q()
   c.append(ck);vals.append(S+A*ck)
  return c,vals
 for m in [1,2,3,5]:
  for extra in [0,1,3]:
   for trial in range(4):
    alpha=randq();eta=F(trial+1,5);q=[Q() for _ in range(m)]+[Q(1,1)]+[randq() for _ in range(extra)];a=[Q() if trial==0 else randq() for _ in range(10)]
    c,values=construct(a,q,m,eta);b=[x+y for x,y in zip(a,c)];polyp=ordinary_shift([q[k]*math.factorial(k) for k in range(len(q))],alpha);polyf=ordinary_shift(b,alpha);product=conv(polyp,polyf)
    for n in range(m):need(derivative(product,n,alpha)==Q(),'low order');oracle+=1
    for k,ck in enumerate(c):
     need(values[k].sq()>=eta**2,'barrier');den=q[m].sq()*F(math.factorial(k+m),math.factorial(k))**2
     need(ck.sq()<=4*eta**2/den,'correction bound');need(derivative(product,k+m,alpha)==values[k],'independent global polynomial oracle');oracle+=1
     steps+=1
     for j in range(k):need(b[j]==a[j]+c[j],'old jet changed');prior+=1
    cases+=1
 mutants=[]
 # These really call changed constructive algorithms, then test ordinary products.
 for mutant in ['omit_correction','wrong_factorial','drop_cross']:
  rejected=False
  for m in [1,2,3]:
   for trial in range(4):
    a=[Q() for _ in range(10)];q=[Q()]*m+[Q(1,1),Q(2,-1)];c,predicted=construct(a,q,m,F(1),mutant);p=ordinary_shift([q[k]*math.factorial(k) for k in range(len(q))],Q());f=ordinary_shift([x+y for x,y in zip(a,c)],Q());prod=conv(p,f)
    if any(derivative(prod,k+m,Q()).sq()<1 or derivative(prod,k+m,Q())!=predicted[k] or c[k].sq()>F(4)/(q[m].sq()*F(math.factorial(k+m),math.factorial(k))**2) for k in range(10)):rejected=True
  need(rejected,'mutant not detected '+mutant);mutants.append(mutant)
 # Annular finite block cases: normal, complex, zero, and very large fixed targets.
 blocks=[]
 for N,beta in [(100,[0,1+2j,-3j]),(10**100,[0,200+30j,-90j]),(10**6,[1e-12+0j,0,10j])]:
  ell=(N+1)**-.5;errors=[]
  for k,z in enumerate(beta):
   l=(N+k+1)**-.5;gamma=z if abs(z)>=l else l*(z/abs(z) if z else 1)
   need(l<=abs(gamma)*(1+1e-14) and abs(gamma)<=math.log(N+k+math.e)*(1+1e-14),'annulus');errors.append(abs(gamma-z));need(errors[-1]<=ell*(1+1e-12),'block error')
  for R in [0,1,5]:
   val=sum(errors[k]*R**k/math.factorial(k) for k in range(len(beta)))+sum((N+k+1)**-.5*R**k/math.factorial(k) for k in range(len(beta),100))
   need(val<=ell*math.exp(R)*(1+1e-12),'shifted baseline majorant')
  blocks.append({'N':str(N),'target_jets':[str(z) for z in beta]})
 return {'exact_fixed_p_cases':cases,'recursive_steps':steps,'independent_ordinary_global_coordinate_checks':oracle,'prior_jet_checks':prior,'executed_algorithm_mutants_rejected':mutants,'annular_blocks':blocks,'limits':'Finite checks corroborate only algebra/majorants. Huge arbitrary target admission, infinite tails, Baire density and simultaneous quantifiers are analytically reviewed.'}

def archive():
 target=HERE/'_extract';shutil.rmtree(target,ignore_errors=True);target.mkdir()
 zpath=PUB/'Polynomial_Multipliers_Verification_v1.0.zip'
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();need(len(names)==len(set(names))==104,'inventory count');need(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names),'unsafe zip paths');z.extractall(target)
 root=json.loads((target/'MANIFEST.json').read_text());need(len(root['files'])==103,'root members')
 manifests=[]
 for p in sorted(target.rglob('MANIFEST.json')):
  obj=json.loads(p.read_text());entries=obj.get('entries',obj.get('files'));need(isinstance(entries,list),'schema');seen=set()
  for e in entries:
   rel=e.get('file',e.get('path'));need(rel not in seen,'duplicate');seen.add(rel);b=(p.parent/rel).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'binding '+rel)
  manifests.append({'path':str(p.relative_to(target)),'entries':len(entries)})
 need(len(manifests)==6,'nested count')
 for e in json.loads((target/'provenance/SUBMITTED_SNAPSHOT.json').read_text())['files']:
  b=(target/'original_submitted'/Path(e['path']).name).read_bytes();need(sha(b)==e['sha256'] and len(b)==e['size'],'original sha');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'original blob')
 # Authored files only; no copied source bodies or private runtime files.
 need(not any(PurePosixPath(n).suffix.lower() in {'.pdf','.png','.jpg','.env'} or 'sources' in PurePosixPath(n).parts for n in names),'third party/runtime body leaked')
 runs=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(target/'verify.py')],capture_output=True,text=True);need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout),'stdout_sha256':sha(r.stdout.encode())})
 controls=[]
 def replay_bad(kind,mutate):
  cp=HERE/'_corrupt';shutil.rmtree(cp,ignore_errors=True);shutil.copytree(target,cp);mutate(cp)
  for flags in [[],['-O'],['-OO']]:
   r=subprocess.run([sys.executable,'-B',*flags,str(cp/'verify.py')],capture_output=True,text=True);need(r.returncode!=0,'corruption accepted '+kind);controls.append({'kind':kind,'flags':flags,'rejected':True})
 def rebind_root(cp,rel):
  p=cp/'MANIFEST.json';obj=json.loads(p.read_text());b=(cp/rel).read_bytes()
  for e in obj['files']:
   if e['path']==rel:e.update(bytes=len(b),sha256=sha(b))
  p.write_text(json.dumps(obj))
 for m in manifests[1:]:
  rel=m['path'];obj=json.loads((target/rel).read_text());e=obj.get('entries',obj.get('files'))[0];payload=str(PurePosixPath(rel).parent/e.get('file',e.get('path')))
  def mutate(cp,payload=payload):
   p=cp/payload;p.write_bytes(p.read_bytes()+b'\ncorruption\n');rebind_root(cp,payload)
  replay_bad('coupled_root_with_stale_nested:'+rel,mutate)
 replay_bad('unlisted_member',lambda cp:(cp/'extra.txt').write_text('extra'))
 replay_bad('corrupt_archived_manuscript',lambda cp:(cp/'manuscript/main.tex').write_text('corrupt'))
 replay_bad('missing_file',lambda cp:(cp/'README.md').unlink())
 def dup(cp):
  p=cp/'MANIFEST.json';o=json.loads(p.read_text());o['files'].append(o['files'][0]);p.write_text(json.dumps(o))
 replay_bad('duplicate_root_member',dup)
 return {'archive_sha256':sha(zpath.read_bytes()),'members':len(names),'manifests':manifests,'runs':runs,'controls':controls,'no_source_bodies':True}

def supplied_worker():
 # Importing does not execute main or write its receipt. Worker uses pure fixtures.
 import importlib.util
 spec=importlib.util.spec_from_file_location('supplied_regression',PUB/'workflow_regression.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 result=m.worker();old=json.loads((PUB/'WORKFLOW_REGRESSION_RECEIPT.json').read_text());need(all(r['result']==result for r in old['runs']),'supplied receipt semantically stale')
 need(old['program_sha256']==sha((PUB/'workflow_regression.py').read_bytes()),'regression program stale')
 for n,h in old['repaired_workflow_sha256'].items():need(sha((PUB/n).read_bytes())==h,'workflow stale '+n)
 return result
if __name__=='__main__':
 result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'algebra':algebra(),'archive':archive(),'supplied_worker_replay':supplied_worker(),'scope':'No external mutations; no real Git operations. Fresh extraction and changed controls are under ignored review directories.'}
 (HERE/'INDEPENDENT_CHECK_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'algebra':result['algebra'],'archive_members':result['archive']['members'],'corruption_mode_runs':len(result['archive']['controls']),'supplied_worker':result['supplied_worker_replay']['status']},indent=2))
