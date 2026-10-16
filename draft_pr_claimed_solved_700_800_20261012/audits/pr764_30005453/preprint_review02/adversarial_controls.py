"""Fresh package mutations and rational controls; one private fixture per mode."""
from pathlib import Path
from fractions import Fraction as F
import datetime,importlib.util,json,os,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'preprint/support'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def child():
 sys.path.insert(0,str(SOURCE))
 import verify_bundle as v,build_package as b
 with tempfile.TemporaryDirectory(dir=ROOT/'tmp',prefix='guard-fixture-') as td:
  fixture=Path(td)/'source'
  with zipfile.ZipFile(ROOT/'frozen/source-and-verification.zip') as z:z.extractall(fixture)
  v.ROOT=fixture;b.ROOT=fixture
  original={p.relative_to(fixture).as_posix():p.read_bytes() for p in fixture.rglob('*') if p.is_file()}
  records=[]
  def rebind(name):
   m=json.loads((fixture/'MANIFEST.json').read_text())
   for row in m['files']:
    if row['path']==name:row.update(b.identity((fixture/name).read_bytes()));break
   (fixture/'MANIFEST.json').write_text(json.dumps(m))
  def reject(label,action,fragment):
   try:
    action();sys.argv=['verify_bundle.py','--integrity-only'];v.main()
   except (ValueError,FileNotFoundError,KeyError) as e:
    need(fragment in str(e),label+' wrong guard: '+str(e))
    records.append({'case':label,'exception':type(e).__name__,'message':str(e)})
   else:raise RuntimeError('Mutation accepted: '+label)
   for p in sorted(fixture.rglob('*'),key=lambda p:len(p.parts),reverse=True):
    n=p.relative_to(fixture).as_posix()
    if p.is_symlink() or (p.is_file() and n not in original):p.unlink()
    elif p.is_dir() and not any(p.iterdir()):p.rmdir()
   for n,raw in original.items():
    p=fixture/n;p.parent.mkdir(parents=True,exist_ok=True)
    if not p.is_file() or p.read_bytes()!=raw:p.write_bytes(raw)
  reject('changed_source',lambda:(fixture/'paper.tex').write_bytes(original['paper.tex']+b'changed'),'Content mismatch')
  reject('missing_source',lambda:(fixture/'README.md').unlink(),'File inventory mismatch')
  reject('unlisted_file',lambda:(fixture/'unexpected.txt').write_text('extra'),'File inventory mismatch')
  reject('unlisted_empty_directory',lambda:(fixture/'unexpected').mkdir(),'Directory inventory mismatch')
  def symlink():
   (fixture/'README.md').unlink();(fixture/'README.md').symlink_to('paper.tex')
  reject('symlink',symlink,'Symlink')
  def duplicate():
   m=json.loads(original['MANIFEST.json']);m['files'].append(m['files'][0]);(fixture/'MANIFEST.json').write_text(json.dumps(m))
  reject('duplicate_manifest_entry',duplicate,'Duplicate/self path')
  def unsafe():
   m=json.loads(original['MANIFEST.json']);m['files'][0]['path']='../escape';(fixture/'MANIFEST.json').write_text(json.dumps(m))
  reject('unsafe_manifest_entry',unsafe,'Unsafe path')
  def change_json(name,edit):
   p=fixture/name;m=json.loads(p.read_text());edit(m);p.write_text(json.dumps(m));rebind(name)
  reject('metadata_rebound',lambda:change_json('zenodo-metadata.json',lambda m:m['metadata'].update(title='Altered')),'Publication metadata mismatch')
  reject('priority_permission_rebound',lambda:change_json('audit/PRIORITY_GATE.json',lambda m:m.update(first_sole_new_theorem_claim_allowed=True)),'Priority scope mismatch')
  reject('candidate_anchor_rebound',lambda:change_json('historical_candidate/PUBLICATION_MANIFEST.json',lambda m:m.update(extra='tampered')),'Historical candidate pin mismatch')
  reject('review_manifest_rebound',lambda:change_json('audit/review_deterministic_family/MANIFEST.json',lambda m:m.update(extra='tampered')),'Review manifest pin mismatch')
  reject('snapshot_wrong_source_rebound',lambda:change_json('audit/SNAPSHOT.json',lambda m:m['files'][0].update(path='wrong-problem/file')),'Wrong source problem')
  for label,out in [('builder_same_directory',fixture),('builder_descendant_directory',fixture/'nested-output')]:
   try:
    sys.argv=['build_package.py','--output-dir',str(out)];b.main()
   except ValueError as e:
    need('outside closed input' in str(e),'Builder wrong guard');records.append({'case':label,'message':str(e)})
   else:raise RuntimeError('Builder accepted closed output')
  need(v.read_closed(fixture)==original,'Fixture restoration failed')
 return {'outer_optimized':not __debug__,'rejected_controls':records,'single_fixture_removed':True}
def finite():
 checks=0
 for a in [1,2,7,10**6]:
  for d in [1,2,7,10**6]:
   for rate in [F(1),F(1,10**70)]:
    q=rate/a+F(3,7)*rate/(a+d);lam=a*q;jump=F(1,a)
    need(lam*jump==q and lam*jump*jump==jump*q and jump*q<=q,'Exact jump/bracket')
    need(lam<=rate+F(3,7)*rate,'Endpoint bound');checks+=1
 strips=0
 for beta in [1,2,3]:
  z=[F(1,2),F(1,10**40),F(2,3)];M=F(1,5);K=F(2);B=max(z);eps=M/8
  while B*2*beta*(2*K)**(beta-1)*eps/(M/2)**beta>=M/4:eps/=2
  T=lambda x:sum((x[0]+x[j])**beta for j in [1,2])
  p=z[0]*T(z)
  for sign in [1,-1]:
   x=[z[0]+sign*(M-eps/2),z[1]+(-min(M,z[1]/2) if sign>0 else M),z[2]+(-min(M,z[2]/2) if sign>0 else M)]
   deriv=p/T(x)-x[0]
   need(deriv<=-M/2 if sign>0 else deriv>=M/2,'Extreme strip direction');strips+=1
 for n in [1,20,100,1000]:
  z=F(1,2**n);p=2*z*z;need((2*z)**2==2*p,'Small-rate one-edge equilibrium')
 for a in [F(1,100),F(1,3),F(19,10)]:
  d=2-a;need(a*(1/(a+d)+1/(a+d))==a,'Critical excluded control')
 return {'exact_jump_bracket_cases':checks,'exact_extreme_strip_cases':strips,'vanishing_rate_degree_one_cases':4,'critical_positive_nonuniqueness_cases':3,'scope':'Finite diagnostics only; analytic verification independently reconstructs the infinite proof.'}
if __name__=='__main__':
 if '--child' in sys.argv:print(json.dumps(child(),sort_keys=True))
 else:
  results=[]
  for flags in [[],['-O']]:
   e=os.environ.copy();e.pop('PYTHONOPTIMIZE',None);e['PYTHONDONTWRITEBYTECODE']='1'
   p=subprocess.run([sys.executable,'-B',*flags,__file__,'--child'],capture_output=True,text=True,env=e,timeout=120)
   need(p.returncode==0,p.stderr);results.append(json.loads(p.stdout))
  receipt={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','guard_modes':results,'finite_controls':finite()}
  (ROOT/'ADVERSARIAL_CONTROLS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
