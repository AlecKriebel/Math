from pathlib import Path,PurePosixPath
import datetime,hashlib,json,re,subprocess,zipfile,stat
R=Path(__file__).resolve().parent; P=R.parent.parent/'publication'
sha=lambda b:hashlib.sha256(b).hexdigest()
pins=json.loads((R/'PINNED.json').read_text()); original=json.loads((P/'evidence/SUBMITTED_PINS.json').read_text());manifest=json.loads((P/'PACKAGE_MANIFEST.json').read_text())
checks={}; details={}
entries=manifest['files']; checks['manifest_unique']=len(entries)==len({s['path'] for s in entries})
checks['manifest_hashes']=all((P/s['path']).stat().st_size==s['bytes'] and sha((P/s['path']).read_bytes())==s['sha256'] for s in entries)
checks['metadata_exact_wrapper']=json.loads((P/'zenodo-deposit.json').read_text())['metadata']==json.loads((P/'metadata.json').read_text())
files={s['path'] for s in entries}|{'PACKAGE_MANIFEST.json'}
with zipfile.ZipFile(P/'grassmann_calibrations_source_verification_v1.zip') as z:
 infos=z.infolist(); names=[i.filename for i in infos]; checks['zip_count135']=len(infos)==135; checks['zip_unique']=len(set(names))==len(names); checks['crc']=z.testzip() is None
 checks['safe_relative_paths']=all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and n.startswith('grassmann_calibrations_v1/') for n in names)
 checks['no_symlinks']=all(not stat.S_ISLNK(i.external_attr>>16) for i in infos)
 checks['zip_exact_inventory']=set(names)=={'grassmann_calibrations_v1/'+f for f in files}
 checks['zip_exact_file_bytes']=all(z.read('grassmann_calibrations_v1/'+f)==(P/f).read_bytes() for f in files)
 checks['zip_deterministic_attributes']=all(i.date_time==(2026,10,12,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==zipfile.ZIP_DEFLATED for i in infos)
 checks['no_raw_caches_duplicate_archives']=not any('/raw/' in n or '__pycache__' in n or n.endswith(('.zip','.pyc')) for n in names)
 if all(checks[k] for k in ['safe_relative_paths','zip_unique','no_symlinks','crc']): z.extractall(R/'extracted')
 with zipfile.ZipFile(R/'rebuilt.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
  for i in sorted(infos,key=lambda x:x.filename):
   zi=zipfile.ZipInfo(i.filename,date_time=(2026,10,12,0,0,0)); zi.create_system=3; zi.external_attr=0o100644<<16;zi.compress_type=zipfile.ZIP_DEFLATED;out.writestr(zi,z.read(i))
checks['deterministic_rebuild_exact']=sha((R/'rebuilt.zip').read_bytes())==pins['files']['grassmann_calibrations_source_verification_v1.zip']['sha256']
head=original['head_commit']; prefix='unsolved_math_prioritization/attempts/30002816/'
q=subprocess.run(['git','ls-tree','-r','--name-only',head,'--',prefix],cwd='/Users/alec/Documents/Math',capture_output=True,text=True,check=True)
checks['original_full_tree29']=set(q.stdout.splitlines())=={s['repository_path'] for s in original['files']} and len(original['files'])==29
rows=[]
for s in original['files']:
 data=subprocess.run(['git','show',head+':'+s['repository_path']],cwd='/Users/alec/Documents/Math',capture_output=True,check=True).stdout
 rows.append({'path':s['repository_path'],'relative':s['relative'],'git_bytes':len(data),'sha256':sha(data),'git_match':len(data)==s['bytes'] and sha(data)==s['sha256'],'public_match':(P/'evidence/submitted'/s['relative']).read_bytes()==data})
checks['all29_gitshow_bytes']=all(v['git_match'] and v['public_match'] for v in rows);details['original_files']=rows
copy=json.loads((P/'evidence/PACKAGE_REVIEW_01_COPY.json').read_text()); copyrows=[]
for s in copy['files']:
 file=P/s['path']; local=R.parent/'package_01'/file.relative_to(P/'evidence/package_review_01')
 copyrows.append({'path':s['path'],'pinned_match':len(file.read_bytes())==s['bytes'] and sha(file.read_bytes())==s['sha256'],'actual_review01_match':local.exists() and local.read_bytes()==file.read_bytes()})
checks['all29_copied_authored_records']=len(copyrows)==29 and all(v['pinned_match'] and v['actual_review01_match'] for v in copyrows);details['copied_records']=copyrows
links=[]
for f in ['README.md','SUPPLEMENT.md','evidence/INDEX.md']:
 file=P/f
 for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',file.read_text()):
  if not target.startswith(('http:','https:','#')): links.append({'from':f,'label':label,'target':target,'exists':(file.parent/target.split('#')[0]).exists()})
checks['current_navigation_links']=all(x['exists'] for x in links); details['links']=links
checks['publication_gate_pending']=json.loads((P/'evidence/CURRENT_REVIEW_STATE.json').read_text())['preprint_ready_for_immutable_publication'] is False
jsonrows=[]
for f in sorted(files):
 if f.endswith('.json'):
  try:json.loads((P/f).read_text());jsonrows.append({'path':f,'valid':True})
  except Exception as e:jsonrows.append({'path':f,'valid':False,'error':str(e)})
checks['json_parse']=all(x['valid'] for x in jsonrows);details['json']=jsonrows
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'details':details,'zip_sha256':sha((R/'rebuilt.zip').read_bytes())}
(R/'receipts/INVENTORY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(checks,indent=2))
