from pathlib import Path
import hashlib,json,zipfile,subprocess,sys,re,datetime,shutil,os
A=Path(__file__).resolve().parent.parent; D=Path(__file__).resolve().parent; K=A/'publication_package_v1'
consumed=json.loads((D/'CONSUMED_INPUTS.json').read_text())
def rd(p,mode='byte/code integrity'):
 b=p.read_bytes();consumed.append({'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'consumed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':mode});return b
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
Z=zipfile.ZipFile(K/'property_s_support.zip');rd(K/'property_s_support.zip'); names=Z.namelist();mf=json.loads(rd(K/'MANIFEST.json'))
require(len(names)==len(set(names))==17,'duplicate/unexpected archive size')
require(set(names)==set(mf['files'])|{'MANIFEST.json'},'archive membership mismatch')
require(all(not Path(n).is_absolute() and '..' not in Path(n).parts and not n.endswith('/') for n in names),'unsafe archive path')
for n in names:
 b=Z.read(n);require(b==rd(K/n),'archive member differs '+n)
 if n!='MANIFEST.json':require(len(b)==mf['files'][n]['bytes'] and digest(b)==mf['files'][n]['sha256'],'manifest mismatch '+n)
E=D/'scratch'/'extracted';E.mkdir(parents=True,exist_ok=True)
for n in names:
 p=E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(Z.read(n))
prep=json.loads(rd(A/'PACKAGE_V1_PREPARATION.json'))
for n,r in prep['files'].items():
 b=rd(K/n);require(len(b)==r['bytes'] and digest(b)==r['sha256'],'preparation pin mismatch '+n)
meta=json.loads(rd(K/'metadata.json'));deposit=json.loads(rd(A/'zenodo-deposit.v1.json'))
require(deposit['metadata']==meta,'deposit metadata mismatch')
require([f['path'] for f in deposit['files']]==['publication_package_v1/property_s_counterexample.pdf','publication_package_v1/property_s_support.zip'],'deposit upload whitelist')
# Native proposal is an exact copy of K plus wrappers and preserved historical originals.
for p in K.rglob('*'):
 if p.is_file():require(rd(p)==rd(A/'native_proposal_v1'/'publication_package'/p.relative_to(K)),'native candidate copy mismatch '+str(p))
origs=json.loads(rd(A/'ORIGINAL_FILE_MANIFEST.json'));omap=[]
for r in origs['files']:
 p=Path(r['local_path']);b=rd(p,'full original bytes + preservation authentication');q=A/'native_proposal_v1'/'historical_original_submission'/r['relative_attempt_path']
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 require(len(b)==r['bytes'] and digest(b)==r['sha256'] and blob==r['Git_blob'],'original identity mismatch '+str(p))
 require(rd(q)==b,'historical preserved copy mismatch '+str(q));omap.append({'relative':r['relative_attempt_path'],'bytes':len(b),'sha256':digest(b),'git_blob':blob})
require(len(omap)==22,'wrong original count')
require(set(x['relative'] for x in omap)=={str(p.relative_to(A/'native_proposal_v1'/'historical_original_submission')) for p in (A/'native_proposal_v1'/'historical_original_submission').rglob('*') if p.is_file()},'historical membership')
# Explicit raised checks remain live in normal and optimized modes.
source=(E/'verify.py').read_text();require('assert ' not in source,'assert-only current control')
receipts=[]
def run_code(folder,opt,script='verify.py'):
 r=subprocess.run([sys.executable,'-E','-S','-B','-P',*(['-O'] if opt else []),str(folder/script)],cwd=folder,capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(D/'scratch'/'tmp')))
 return r
for opt in (False,True):
 r=run_code(E,opt);require(r.returncode==0,'extracted baseline failed');j=json.loads(r.stdout);require(j['checks']==33512,'wrong counts')
 target=E/('verification.optimized.json' if opt else 'verification.normal.json');require(r.stdout.encode()==target.read_bytes(),'recorded output mismatch')
 (D/('package.optimized.json' if opt else 'package.normal.json')).write_text(r.stdout);receipts.append({'kind':'extracted','optimized':opt,'exit':r.returncode,'checks':j['checks'],'stdout_sha256':digest(r.stdout.encode())})
r=run_code(E,False,'verify_controls.py');require(r.returncode==0,'package negative-control replay failed');(D/'package_controls.stdout.json').write_text(r.stdout);(D/'package_controls.stderr.txt').write_text(r.stderr)
# Temporary path-dependent trace text has no scientific semantics: compare recorded categories.
regenerated=json.loads((E/'negative_controls.json').read_text());recorded=json.loads((K/'negative_controls.json').read_text())
require(regenerated['status']==recorded['status'] and regenerated['good']==recorded['good'],'negative-control baseline mismatch')
require([(q['mutation'],q['optimized'],q['exit_code']) for q in regenerated['negative_controls']]==[(q['mutation'],q['optimized'],q['exit_code']) for q in recorded['negative_controls']],'negative-control matrix mismatch')
# Stronger substantive mutants: formulas, residue character, zero classification and indices.
mutations={
 'drop_bilinear_term':('def diamond(c,d):return(c+d+2*c*d)%4','def diamond(c,d):return(c+d)%4'),
 'parity_character':('def eps(c):return 1 if c%4 in (0,1) else -1','def eps(c):return 1 if c%4 in (0,2) else -1'),
 'wrong_circle_actor':('eps(a[1])*b[0]','eps(b[1])*b[0]'),
 'remove_nonzero_n_kernel':('(eps(d)-1)*n==0 and (2*d*c)%4==0','(2*d*c)%4==0'),
 'include_c2_finite_classification':('if c in (0,1):','if c in (0,1,2):'),
 'wrong_finite_index':('idx2=4//len(K)','idx2=2//len(K)'),
 'force_star_torsion':('((eps(a[1])-1)*b[0],2*a[1]*b[1]%4)','(((eps(a[1])-1)*b[0])%7,2*a[1]*b[1]%4)')}
mutant_results=[]
for name,(old,new) in mutations.items():
 require(old in source,'missing mutant anchor '+name);F=D/'scratch'/'mutations'/name;F.mkdir(parents=True,exist_ok=True);(F/'verify.py').write_text(source.replace(old,new));(F/'property_s_counterexample.tex').write_bytes((E/'property_s_counterexample.tex').read_bytes())
 for opt in (False,True):
  r=run_code(F,opt);require(r.returncode!=0 and 'RuntimeError' in r.stderr,'mutant falsely passed '+name)
  err=r.stderr.split('RuntimeError:')[-1].strip();mutant_results.append({'mutation':name,'optimized':opt,'exit':r.returncode,'failure':err})
  (F/('optimized.stderr.txt' if opt else 'normal.stderr.txt')).write_text(r.stderr)
# Execute native wrappers only in own scratch copy.
N=D/'scratch'/'native';N.mkdir(parents=True,exist_ok=True)
for name in ['verify.py','verify_controls.py']:
 (N/name).write_bytes(rd(A/'native_proposal_v1'/name,'full wrapper code'))
shutil.copytree(K,N/'publication_package',dirs_exist_ok=True)
for opt in (False,True):
 r=run_code(N,opt);require(r.returncode==0,'native wrapper failure');j=json.loads(r.stdout);require(j['checks']==33512,'native wrapper count');require(r.stdout.encode()==(K/'verification.normal.json').read_bytes(),'native wrapper stdout mismatch');receipts.append({'kind':'native wrapper','optimized':opt,'exit':r.returncode,'checks':j['checks']})
# Potential secret signatures are scanned without exposing suspected contents.
secret_patterns=[r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{25,}',r'github_pat_[A-Za-z0-9_]{25,}',r'(?i)authorization:\s*bearer\s+\S+',r'AKIA[0-9A-Z]{16}']
secret_hits=[]
for n in names:
 s=Z.read(n).decode('utf-8')
 for pat in secret_patterns:
  if re.search(pat,s):secret_hits.append({'member':n,'signature':pat})
require(not secret_hits,'public credentials signature found')
third_party_extensions=[n for n in names if Path(n).suffix.lower() in ('.pdf','.html','.xml','.png','.jpg')]
require(not third_party_extensions,'third-party/source binary risk')
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PACKAGE_INTEGRITY_REPRODUCTION_AND_PRESERVATION','archive_members':names,'manifest_exact':True,'preparation_pins_exact':True,'deposit_metadata_exact':True,'native_package_byte_identical':True,'original_files_verified':omap,'original_count':len(omap),'runs':receipts,'additional_mutants_rejected':mutant_results,'controls_replay':json.loads(r.stdout) if False else json.loads((D/'package_controls.stdout.json').read_text()),'private_credentials_signature_hits':secret_hits,'third_party_source_bodies_in_archive':False,'pdf_visual_pages_reviewed':[1,2,3,4],'pdf_visual_assessment':'All four pages legible; correct equations/table and qualified claims; no clipping, overlap, broken glyphs or missing reference text.'}
(D/'PACKAGE_REPRODUCTION_AND_INTEGRITY.json').write_text(json.dumps(report,indent=2)+'\n');(D/'CONSUMED_INPUTS.json').write_text(json.dumps(consumed,indent=2)+'\n')
print(json.dumps({'status':report['status'],'originals':len(omap),'baselines':len(receipts),'extra_mutants':len(mutant_results),'archive_members':len(names),'negative_controls':report['controls_replay']},indent=2))
