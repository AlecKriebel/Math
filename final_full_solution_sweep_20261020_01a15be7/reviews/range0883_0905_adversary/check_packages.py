#!/usr/bin/env python3
"""Independent closed-manifest/archive/Git provenance verifier. Does not run archive code."""
import pathlib,json,subprocess,zipfile,hashlib,stat,datetime,io,tarfile
W=pathlib.Path(__file__).resolve().parent;REPO=W.parents[2]
def git(*a):return subprocess.check_output(['git','-C',str(REPO),*a],stderr=subprocess.DEVNULL)
def digest(x):return hashlib.sha256(x).hexdigest()
def safe(p):return bool(p) and not p.startswith(('/','\\')) and '\\' not in p and all(x not in ('','..','.') for x in p.split('/'))
def zip_safety(z,label):
 infos=z.infolist(); names=[i.filename for i in infos];bad=[]
 for i in infos:
  mode=i.external_attr>>16
  if not safe(i.filename) or i.is_dir() or (stat.S_IFMT(mode) not in (0,stat.S_IFREG)):bad.append(i.filename)
 return {'archive':label,'members':len(names),'safe_unique_regular':not bad and len(names)==len(set(names)),'bad_paths':bad,'crc_bad_member':z.testzip()}
def nested_safety(blob,label,depth=0):
 if depth>4:return []
 out=[]
 if zipfile.is_zipfile(io.BytesIO(blob)):
  with zipfile.ZipFile(io.BytesIO(blob)) as z:
   q=zip_safety(z,label);out.append(q)
   for name in z.namelist():
    if name.endswith(('.zip','.tar.gz','.tgz')):out+=nested_safety(z.read(name),label+'!'+name,depth+1)
 elif label.endswith(('.tar.gz','.tgz')):
  with tarfile.open(fileobj=io.BytesIO(blob),mode='r:gz') as t:
   ms=t.getmembers();bad=[m.name for m in ms if not safe(m.name.rstrip('/')) or not (m.isfile() or m.isdir())];out.append({'archive':label,'members':len(ms),'safe_unique_regular_or_directory':not bad and len(ms)==len({m.name for m in ms}),'bad_paths':bad})
 return out
out=[]
for n in [883,885,888,894,904,905]:
 d=json.loads((W/'inputs'/f'PR{n:04}_DISPOSITION.json').read_text());c=json.loads((W/'inputs'/f'PR{n:04}_PUBLICATION_COVERAGE_DETAILS.json').read_text());h=d['inventory_head_sha'];p=next((W/'downloads_private'/str(n)).glob('*.zip'));z=zipfile.ZipFile(p);names=z.namelist();mf='package_index.json' if 'package_index.json' in names else 'PACKAGE_MANIFEST.json';m=json.loads(z.read(mf));files=m['files'];files={x['path']:x for x in files} if isinstance(files,list) else files
 payload=[]
 for name,entry in files.items():
  b=z.read(name);payload.append({'path':name,'bytes':len(b),'sha256':digest(b),'matches':len(b)==entry['bytes'] and digest(b)==entry['sha256']})
 prefix=f"unsolved_math_prioritization/attempts/{c['problem_id']}/";sh=c.get('source_head',h);tree=git('ls-tree','-r','--name-only',sh,'--',prefix).decode().splitlines();originals=[]
 for path in tree:
  rel=path[len(prefix):];member=('original_packet/' if n in (904,905) else 'source/')+rel; b=git('show',f'{sh}:{path}');a=z.read(member)
  cp=prefix+'verification/source/'+rel if n==894 else path
  try: current=git('show',f'{h}:{cp}');ce=current==b;cb=digest(current)
  except subprocess.CalledProcessError:ce=False;cb=None
  originals.append({'path':path,'original_git_blob':git('rev-parse',f'{sh}:{path}').decode().strip(),'member':member,'bytes':len(b),'sha256':digest(b),'archive_equal':b==a,'current_path':cp,'current_equal':ce,'current_sha256':cb})
 ns='original_packet/' if n in (904,905) else 'source/'; archived_originals=[x for x in names if x.startswith(ns)]; tree_members=[x['member'] for x in originals]
 pdfp=next((W/'downloads_private'/str(n)).glob('*.pdf'));pdf=pdfp.read_bytes();pdfpins=[]
 if n==883:pdfpins.append({'kind':'embedded','member':'output/pdf/note.pdf','equal':z.read('output/pdf/note.pdf')==pdf})
 elif n in (904,905):
  def scan(j,loc=''):
   if isinstance(j,dict):
    if j.get('sha256')==digest(pdf):pdfpins.append({'kind':'manifest_external','locator':loc,'pin':j,'equal':j.get('bytes')==len(pdf)})
    for k,v in j.items():scan(v,loc+'/'+k)
   elif isinstance(j,list):
    for i,v in enumerate(j):scan(v,loc+'/'+str(i))
  scan(m)
 else:
  path=c['public_pdf_verified_separately_against_head'];pdfpins.append({'kind':'pinned_git','path':path,'equal':git('show',f'{h}:{path}')==pdf})
 copies=c.get('manuscript_matches_all_current_head_copies',c.get('public_pdf_and_manuscript_match_all_current_head_copies',[])); copies+= [x['path'] for x in c.get('current_manuscript_copy_bindings',[])]; copychecks=[]
 for path in copies:
  member='note.tex' if path.endswith('.tex') else 'output/pdf/note.pdf';copychecks.append({'path':path,'member':member,'equal':git('show',f'{h}:{path}')==z.read(member)})
 fixtures=[]
 for f in c.get('explicit_historical_tooling_fixture',[]):fixtures.append({'path':f['path'],'member':f['archive_member'],'equal':git('show',f"{h}:{f['path']}")==z.read(f['archive_member']),'distinct_from_actual_note':z.read(f['archive_member'])!=z.read('note.tex')})
 manuscript=z.read('note.tex');(W/'downloads_private'/str(n)/'note.tex').write_bytes(manuscript)
 for fn in ['README.md','EDITION_HISTORY.md','SOURCE_CORRECTION.md','SOURCE_VERSION_CORRECTION.md','CURRENT_PRIORITY.md','SOURCE_MANIFEST.json','ORIGINAL_SNAPSHOT.json']:
  if fn in names:(W/'downloads_private'/str(n)/fn).write_bytes(z.read(fn))
 out.append({'pr':n,'archive':p.name,'safety':zip_safety(z,p.name),'manifest':mf,'manifest_sha256':digest(z.read(mf)),'manifest_matches_receipt':digest(z.read(mf))==c['manifest_sha256'],'closed_manifest':set(names)==set(files)|{mf},'manifest_payload_count':len(files),'all_payloads_match':all(x['matches'] for x in payload),'payloads':payload,'source_head':sh,'original_tree_count':len(tree),'original_namespace_exact':set(archived_originals)==set(tree_members),'all_originals_match':all(x['archive_equal'] for x in originals),'original_bindings':originals,'current_original_matches':sum(x['current_equal'] for x in originals),'current_differences':[x['path'] for x in originals if not x['current_equal']],'pdf_pins':pdfpins,'all_pdf_pins_verified':bool(pdfpins) and all(x['equal'] for x in pdfpins),'manuscript_copy_checks':copychecks,'historical_fixture_checks':fixtures,'nested_archive_safety':nested_safety(p.read_bytes(),p.name)})
(W/'PACKAGE_CHECKS.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':out},indent=2)+'\n')
for x in out:print(x['pr'],x['safety'],x['manifest_payload_count'],x['closed_manifest'],x['all_payloads_match'],x['original_tree_count'],x['original_namespace_exact'],x['all_originals_match'],x['current_original_matches'],x['all_pdf_pins_verified'],x['current_differences'])
