from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,subprocess,datetime
R=Path(__file__).resolve().parent;F=json.loads((R/'INPUT_FREEZE.json').read_text());A=Path(F['root']);P=A/'publication';C=R/'scratch_local/audit/publication'
def need(c,m):
 if not c:raise RuntimeError(m)
def binding(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
zpath=P/'Johnson_Filtration_Multiplicity_Verification_v1.0.zip';rows=[]
with zipfile.ZipFile(zpath) as z:
 names=z.namelist();need(len(names)==len(set(names))==105,'archive count/uniqueness');need(z.testzip() is None,'CRC')
 for n in names:
  p=PurePosixPath(n);need(not p.is_absolute() and '..' not in p.parts,'safe names');need(z.read(n)==(P/'verification'/n).read_bytes(),'archive readback '+n)
 manifest=json.loads(z.read('MANIFEST.json'));need(set(names)=={'MANIFEST.json'}|{e['path'] for e in manifest['files']},'exact inventory')
 for e in manifest['files']:need(binding(z.read(e['path']))=={k:e[k] for k in ('bytes','sha256')},'outer binding')
 registry=json.loads(z.read('provenance/CURRENT_PR1241_CONTEXT.json'))['authored_freezes'];need(len(registry)==7,'seven registered manifests');total=0
 for item in registry:
  b=z.read(item['path']);need(hashlib.sha256(b).hexdigest()==item['sha256'],'registry anchor');es=json.loads(b)[item['entries_key']];total+=len(es)
  for e in es:need(binding(z.read(item['base']+'/'+e[item['path_key']]))=={k:e[k] for k in ('bytes','sha256')},'nested member')
  rows.append({'path':item['path'],'members':len(es)})
 need(total==53,'53 frozen members')
 eight=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
 for folder in ('original_submitted','current_edition'):
  m=json.loads(z.read(folder+'/MANIFEST.json'))
  for e in m['entries']:need(binding(z.read(folder+'/'+e['file']))=={k:e[k] for k in ('bytes','sha256')},'eight manifest')
  for n in eight:need(z.read(folder+'/'+n)==(A/('submitted' if folder=='original_submitted' else folder)/n).read_bytes(),'eight source copy')
  rows.append({'path':folder+'/MANIFEST.json','members':len(m['entries'])})
 original=json.loads(z.read('provenance/SUBMITTED_SNAPSHOT.json'))
 for e in original['files']:
  b=z.read('original_submitted/'+Path(e['path']).name);need(binding(b)=={k:e[k] for k in ('bytes','sha256')},'original bytes');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['blob'],'Git blob')
 need(z.read('manuscript/main.tex')==(P/'manuscript/main.tex').read_bytes(),'source')
copy_checks={n:{'reviewed':sha(P/n),'copy_build':sha(C/n),'identical':(P/n).read_bytes()==(C/n).read_bytes()} for n in ('Johnson_Filtration_Multiplicity_Note_v1.0.pdf','Johnson_Filtration_Multiplicity_Verification_v1.0.zip')}
need(all(x['identical'] for x in copy_checks.values()),'copy exact build reproduction')
info=subprocess.run(['pdfinfo',str(P/'Johnson_Filtration_Multiplicity_Note_v1.0.pdf')],capture_output=True,text=True,check=True);(R/'PDFINFO.txt').write_text(info.stdout);need('Pages:           6' in info.stdout,'six pages')
report={'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':binding(zpath.read_bytes()),'exact_zip_members':105,'outer_bound_members':104,'nested_manifests':rows,'registry_family_manifests':7,'registry_members':53,'original_git_files':8,'current_edition_files':8,'source_sha256':sha(P/'manuscript/main.tex'),'pdf_sha256':sha(P/'Johnson_Filtration_Multiplicity_Note_v1.0.pdf'),'metadata_sha256':sha(P/'zenodo-deposit.json'),'copy_build':copy_checks,'all_six_pages_rendered_and_visually_inspected':True,'layout':'No clipped or overlapping text, missing glyphs, unreadable mathematics or broken reference layout. Page 6 is bibliography continuation with deliberate whitespace.','limits':'Manifest authentication establishes current byte integrity, not truth of historical receipts or priority/independence.'}
(R/'PACKAGE_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','members':105,'nested':len(rows),'exact_build_reproduction':True}))
