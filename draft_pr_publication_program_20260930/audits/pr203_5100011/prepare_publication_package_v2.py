"""Prepare a new draft only after Root accepts the first whole-package review."""
from pathlib import Path
import hashlib,json,sys,zipfile
A=Path(__file__).resolve().parent;OLD=A/'publication_package_v1';NEW=A/'publication_package_v2'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(rel,b):
 q=NEW/rel;q.parent.mkdir(parents=True,exist_ok=True)
 with q.open('xb') as f:f.write(b)
def prepare():
 r=json.loads((A/'ROOT_WHOLE_PACKAGE_REVIEW_ACCEPTANCE_01.json').read_bytes())
 if not r['Root_accepted_entire_package_review'] or r['reviewed_package']!='publication_package_v1':raise RuntimeError('First review not accepted')
 seal=json.loads((OLD/'PACKAGE_SEAL.json').read_bytes())
 if NEW.exists():raise RuntimeError('Never overwrite an existing package version')
 for rel,x in seal['package_files_excluding_this_seal'].items():
  raw=(OLD/rel).read_bytes()
  if pin(raw)!=x:raise RuntimeError('V1 seal changed '+rel)
  if rel not in ['verification-package.zip','materials/MANIFEST.json']:put(rel,raw)
 src=(NEW/'original_pedal_flag.tex').read_text()
 old='Composition is right to left; put \\(T=\\tau\\sigma\\).\n'
 insert=r'''
On a physical orbit this is exactly the flag step. The reflected chord can
have the incoming chord's supporting line only at normal incidence:
a tangent to \(E\) cannot touch the strictly interior \(C\).
At \(P=(a\cos\theta,b\sin\theta)\), the normal line has coefficients
\[
 [u:v:w]=[-\sin\theta/b:\cos\theta/a:
                 c\sin\theta\cos\theta/(ab)],\qquad c=a^2-b^2 .
\]
Substitution in the dual-caustic equation gives
\(\lambda=a^2\sin^2\theta+b^2\cos^2\theta\ge b^2\), excluded.
Thus reflection selects the other caustic tangent.
The real-component description below also shows that vertex and flag
least periods agree.
'''
 if src.count(old)!=1:raise RuntimeError('Physical flag paragraph anchor changed')
 src=src.replace(old,old+insert,1);(NEW/'original_pedal_flag.tex').write_text(src);(NEW/'materials/original_pedal_flag.tex').write_text(src)
 text=(NEW/'materials/README.md').read_text()
 start='python -B verification/run_checks.py\n';end='python -B -O verification/run_checks.py --guard-false\n'
 if text.count(start)!=1 or text.count(end)!=1:raise RuntimeError('README command anchors changed')
 text=text.replace(start,chr(96)*3+'text\n'+start,1).replace(end,end+chr(96)*3+'\n',1)
 (NEW/'materials/README.md').write_text(text)
 print(json.dumps({'version':'v2 prepared, unsealed','repairs':['Explicit physical/flag step and excluded normal-incidence formula','Fenced reproducibility commands'],'compile_PDF_then_finalize_required':True,'fresh_entire_package_review_required':True}))
def finalize():
 if (NEW/'PACKAGE_SEAL.json').exists():raise RuntimeError('V2 already sealed')
 M=NEW/'materials'
 if (NEW/'original_pedal_flag.tex').read_bytes()!=(M/'original_pedal_flag.tex').read_bytes():raise RuntimeError('Source copies differ')
 files={str(q.relative_to(M)):pin(q.read_bytes()) for q in sorted(M.rglob('*')) if q.is_file()}
 if len(files)!=106:raise RuntimeError('Unexpected material file count')
 put('materials/MANIFEST.json',(json.dumps({'self_excluded':True,'scope':'Authored materials only; manuscript source, exact metadata, finite verification and explicit original/audit allowlists.','files':files},indent=2)+'\n').encode())
 with zipfile.ZipFile(NEW/'verification-package.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for q in sorted(M.rglob('*')):
   if q.is_file():z.write(q,str(q.relative_to(M)))
 for name in ['verify_exact_controls.py','physical_audit.py','signed_edge_checks.py','run_checks.py']:
  if (M/'verification'/name).read_bytes()!=(OLD/'materials/verification'/name).read_bytes():raise RuntimeError('Unexpected math code change')
 print(json.dumps({'v2_materials_finalized':True,'files':107,'zip':pin((NEW/'verification-package.zip').read_bytes()),'PDF_QA_kitcheck_and_seal_required':True}))
if __name__=='__main__':{'prepare':prepare,'finalize':finalize}[sys.argv[1]]()

