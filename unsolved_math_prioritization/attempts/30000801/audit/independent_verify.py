#!/usr/bin/env python3
"""Independent finite controls and external author-freeze verification, not a PDE proof."""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile
import sympy as S

AUTHOR_BYTES = 22361
AUTHOR_SHA = '45ab3bf6abaa90e865cba7899a509de3a8343ab44b32bb09dbbad7ccd9f46434'
MANIFEST_SHA = '8588374c263f35b384d5cb2e74187c0d09198c8cdc63ebb1b60ac240a8f13626'
AUTHOR_FILES = {'APPROACHES.md','AUTHOR_TEST_RESULTS.json','MANIFEST.json','PROOF.md','PUBLIC_METADATA.json','README.md','SOURCE_AUDIT.md','claims.json','requirements.txt','test_fail_closed.py','verify.py'}
PINS = {
 'catalog': (21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566',15458),
 'problems': (68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',15458),
 'reports': (80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b',6701)}
REVIEW_SHA='6c5a284146c34349fd290aa03fea676c2fcd00352dec31988d7a5376d638fe3e'
STATEMENT_SHA='e240b1b64786f66238f5efc7e10d42b166b7de5c2962733213161c6ba79c7c36'

def require(ok,msg):
 if not ok: raise ValueError(msg)

def sha(raw): return hashlib.sha256(raw).hexdigest()

def parse(raw):
 def pairs(xs):
  d={}
  for k,v in xs:
   require(k not in d,'duplicate JSON key')
   d[k]=v
  return d
 return json.loads(raw,object_pairs_hook=pairs)

def frozen(raw):
 require(len(raw)==AUTHOR_BYTES and sha(raw)==AUTHOR_SHA,'external author ZIP identity mismatch')
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  names=z.namelist()
  expected={'navier_30000801/'+name for name in AUTHOR_FILES}
  require(len(names)==len(set(names))==11 and set(names)==expected,'ZIP membership mismatch')
  for i in z.infolist():
   p=PurePosixPath(i.filename)
   require(not p.is_absolute() and '..' not in p.parts and not i.is_dir(),'unsafe member')
   require(not stat.S_ISLNK(i.external_attr>>16),'symlink member')
   require(p.suffix in {'.py','.json','.md','.txt'},'unexpected file type')
  manifest_raw=z.read('navier_30000801/MANIFEST.json')
  require(sha(manifest_raw)==MANIFEST_SHA,'author manifest pin')
  manifest=parse(manifest_raw)
  require(set(manifest)=={'schema','files'} and manifest['schema']=='sha256-byte-inventory-v1','author inventory schema')
  require(set(manifest['files'])==AUTHOR_FILES-{'MANIFEST.json'},'author inventory membership')
  for name,entry in manifest['files'].items():
   b=z.read('navier_30000801/'+name)
   require(entry=={'bytes':len(b),'sha256':sha(b)},'author member digest: '+name)
  md=parse(z.read('navier_30000801/PUBLIC_METADATA.json'))
  cl=parse(z.read('navier_30000801/claims.json'))
  require(cl['full_resolution'] is False and cl['extra_hypotheses_proved_from_target'] is False,'scope mismatch')
  require(cl['nonlinearity']=='lambda*u*exp(2*u^2)' and cl['boundary']==['u=0','Delta_u=0'],'target mismatch')
  require(md['catalog_rank']==816 and md['problem_id']==30000801,'rank/id mismatch')
 return md

def corpus_replay(paths,md):
 if paths is None:return {'status':'NOT_REQUESTED'}
 objects={}
 out={}
 for key,path in zip(PINS,paths):
  b=Path(path).read_bytes(); size,h,n=PINS[key]
  require(len(b)==size and sha(b)==h,'corpus identity: '+key)
  d=parse(b);require(len(d)==n,'corpus cardinality: '+key)
  objects[key]=d
  out[key]={'bytes':size,'sha256':h,'record_count':n,'status':'PASS'}
 ps=[r for r in objects['problems'] if str(r.get('id'))=='30000801']
 cs=[r for r in objects['catalog'] if str(r.get('id'))=='30000801']
 require(len(ps)==len(cs)==1,'unique complete record')
 p,c=ps[0],cs[0]
 require(p['problem_number']=='OWR-1591-003' and p['problem_number'] not in objects['reports'],'report must be absent')
 b=json.dumps([p,objects['reports'].get(p['problem_number'],{})],sort_keys=True).encode('utf-8')
 require(len(b)==4537 and sha(b)==REVIEW_SHA==c['review_hash'],'full default-sorted review replay')
 require(sha(p['statement'].encode('utf-8'))==STATEMENT_SHA==c['statement_hash'],'statement replay')
 require(p['statement']==p['clean_statement'],'corrected record mismatch')
 require(c['rank']==md['catalog_rank']==816,'rank replay')
 return {'status':'PASS','identities':out,'full_review_bytes':len(b),'full_review_sha256':sha(b),'missing_report':'{}','statement_sha256':STATEMENT_SHA}

def pdf_replay(paths,md):
 if paths is None:return {'status':'NOT_REQUESTED'}
 out=[]
 for p,entry in zip(paths,md['inspected_pdfs']):
  b=Path(p).read_bytes()
  require(len(b)==entry['bytes'] and sha(b)==entry['sha256'],'PDF bytes/hash: '+entry['title'])
  out.append({'title':entry['title'],'url':entry['url'],'bytes':len(b),'sha256':sha(b),'status':'PASS'})
 require(len(out)==4,'four inspected PDF identities required')
 return {'status':'PASS','pdfs':out,'limit':'Hashes identify supplied PDFs; scholarly claims require human inspection.'}

def independent_controls():
 require(S.__version__=='1.14.0','SymPy 1.14.0 required')
 names=[]
 def zero(e,name):
  require(S.simplify(S.expand(e))==0,'identity failed: '+name);names.append(name)
 def yes(b,name):require(bool(b),'control failed: '+name);names.append(name)
 r=S.symbols('r',positive=True);A,B,C=S.symbols('A B C',real=True)
 D=lambda f:S.diff(r**3*S.diff(f,r),r)/r**3
 eta=-S.log(1+r*r)
 zero(D(eta)+4*(r*r+2)/(1+r*r)**2,'radial bubble Laplacian via divergence form')
 zero(D(D(eta))-96*S.exp(4*eta),'radial bubble equation')
 zero(S.integrate(192*r**3/(1+r*r)**4,(r,0,S.oo))-16,'direct radial mass integral in units pi squared')
 zero(2*r**3*S.diff(D(-S.log(r)),r)-8,'positive fundamental source flux in units pi squared')
 def flux(v):
  l=D(v);return 2*r**3*(r*S.diff(v,r)*S.diff(l,r)-l*S.diff(r*S.diff(v,r),r)+r*l*l/2)
 zero(flux(A*S.log(1/r))+4*A*A,'negative pure log Pohozaev flux')
 zero(S.limit(flux(A*S.log(1/r)+B+C*r*r),r,0)+4*A*A,'smooth radial perturbation disappears')
 # General-dimension identity, independently differentiated before specializing to d=4.
 for d in (2,3,4,5):
  xs=S.symbols('x:'+str(d));u=S.Function('u')(*xs)
  lap=lambda v:sum(S.diff(v,x,2) for x in xs)
  w=lap(u);xu=sum(x*S.diff(u,x) for x in xs)
  div=sum(S.diff(xu*S.diff(w,x)-w*S.diff(xu,x)+x*w*w/2,x) for x in xs)
  zero(div-xu*lap(w)-S.Rational(d-4,2)*w*w,'general Pohozaev divergence d='+str(d))
 xs=S.symbols('y:4');u=S.Function('v')(*xs);lap=lambda v:sum(S.diff(v,x,2) for x in xs);w=lap(u)
 zero(lap(lap(u*u/2))-u*lap(w)-w*w-4*sum(S.diff(u,x)*S.diff(w,x) for x in xs)-2*sum(S.diff(u,x,y)**2 for x in xs for y in xs),'square-chain identity including all derivative terms')
 # An exact Navier function on the unit ball, not a solution of the nonlinear PDE.
 u=2-3*r*r+r**4
 zero(u.subs(r,1),'Navier test function zero boundary')
 zero(D(u).subs(r,1),'Navier test function zero Laplacian boundary')
 zero(D(u*u/2).subs(r,1)-4,'squared function loses Navier boundary condition')
 z,l=S.symbols('z lambda',real=True);F=l*(S.exp(2*z*z)-1)/4
 zero(S.diff(F,z)-l*z*S.exp(2*z*z),'primitive derivative coefficient')
 c,M,h=S.symbols('c M h',positive=True)
 zero(2*(M+h/M)**2-2*M*M-4*h-2*h*h/M**2,'exact rescaled exponent')
 E=l*z*z*S.exp(2*z*z)
 zero(c*l*z*S.exp(2*z*z)-(c/z)*E,'source density energy weighting')
 zero(4*c*c*F-(c/z)**2*(1-S.exp(-2*z*z))*E,'primitive density energy weighting')
 a,b,d1,d2=S.symbols('a b d1 d2');s1=a+b;s2=a*a+b*b
 zero((s1+d1)**2-(s2+d2)-(2*a*b+2*s1*d1+d1*d1-d2),'weighted-defect sign')
 yes((1+S.Rational(1,2))**2==1+S.Rational(1,4)+1,'positive two-component defect model')
 yes((1+0)**2==1**2+0**2,'zero normalized weight is invisible')
 yes((1+1-S.Rational(1,2))**2==1+1+S.Rational(1,4),'signed-weight cancellation model')
 n=S.symbols('n',positive=True)
 zero(S.limit((1-S.exp(-2*n*n))*n*n/n**2,n,S.oo)-1,'exact primitive neck defect with u=n and c=n squared')
 zero(S.limit(n/n**2,n,S.oo),'source neck vanishes in same measure model')
 # x_k and y_k coalesce despite separation in both bubble scales.
 zero(S.limit(1/n,n,S.oo),'two selected-center limits may coincide')
 yes(S.limit((2/n)/(n**-3),n,S.oo)==S.oo,'relative-scale separation can coexist with coincident limits')
 return names

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--author-zip',required=True)
 p.add_argument('--inputs',nargs=3,metavar=('CATALOG','PROBLEMS','REPORTS'))
 p.add_argument('--pdf-inputs',nargs=4,metavar=('OWR','STRUWE','ROBERT','MARTINAZZI'))
 a=p.parse_args();md=frozen(Path(a.author_zip).read_bytes())
 controls=independent_controls()
 print(json.dumps({'status':'PASS','verdict':'ACCEPT_CONDITIONAL_RESULT_ONLY_FULL_TARGET_UNRESOLVED','full_resolution':False,'author_zip_bytes':AUTHOR_BYTES,'author_zip_sha256':AUTHOR_SHA,'author_manifest_sha256':MANIFEST_SHA,'independent_control_count':len(controls),'controls':controls,'corpus_replay':corpus_replay(a.inputs,md),'pdf_byte_replay':pdf_replay(a.pdf_inputs,md),'limits':'Finite identities, inventory and replay checks are not an analytic proof or a PDE counterexample.'},indent=2,sort_keys=True))

if __name__=='__main__':
 try:main()
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)}),file=sys.stderr);sys.exit(1)
