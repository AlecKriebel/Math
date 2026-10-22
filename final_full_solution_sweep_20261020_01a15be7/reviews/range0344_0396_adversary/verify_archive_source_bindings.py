from pathlib import Path
import json,zipfile,subprocess,hashlib,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review'
initial=json.loads((O/'independent_classification_initial.json').read_text())['classifications'];output=[];faults=[]
PREFIX={356:'alternating-antimorphic-verification/submitted_problem/',359:'basin-boundaries-verification/candidate/',364:'biconstrained-asymmetry-verification/reference/',367:'verification/reference/'}
for n in [344,356,359,364,367]:
 r=next(r for r in initial if r['pr']==n);z=zipfile.ZipFile(next((P/f'pr{n:04d}_public').glob('*.zip')));names=z.namelist();rootpath=next(x['path'] for x in r['changed_paths'] if x['path'].endswith('/PUBLICATION_MANIFEST.json')).rsplit('/',1)[0]+'/'
 source=[];embedded=[];paper=[]
 for f in r['changed_paths']:
  path=f['path']
  if not path.startswith(rootpath):continue
  rel=path[len(rootpath):]
  b=subprocess.check_output(['git','show',f"{r['head']}:{path}"])
  if n in PREFIX and not rel.startswith('preprint/') and rel!='PREPRINT_RELEASE.md':
   arc=PREFIX[n]+rel;ok=arc in names and z.read(arc)==b
   source.append({'repository_path':path,'archive_path':arc,'byte_identical':ok})
   if not ok:faults.append({'pr':n,'source_binding':path})
  if rel.startswith('preprint/') and (rel.endswith('.zip') or rel.endswith('.pdf')):
   pub=P/f'pr{n:04d}_public'/Path(rel).name
   embedded.append({'repository_path':path,'public_file':pub.name,'byte_identical':pub.exists() and b==pub.read_bytes(),'pinned_sha256':hashlib.sha256(b).hexdigest()})
  if rel.endswith('.tex'):
   tex=next(x for x in names if x.endswith('.tex'));paper.append({'repository_path':path,'archive_path':tex,'byte_identical':z.read(tex)==b})
 output.append({'pr':n,'original_public_reference_files_verified':len(source),'source_reference_bindings':source,'embedded_publication_file_bindings':embedded,'manuscript_bindings':paper,'qualification':'PR344 public derivative is bound by its current full manifest and manuscript; it does not contain all15 historical original problem files, which remain preserved in Git. No claim that the ZIP archives those15 is made.' if n==344 else None})
(O/'archive_source_bindings.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':output,'faults':faults},indent=2)+'\n')
print(json.dumps({'summary':[{'pr':r['pr'],'originals':r['original_public_reference_files_verified'],'embedded':r['embedded_publication_file_bindings'],'manuscripts':r['manuscript_bindings']} for r in output],'faults':faults},indent=2))
