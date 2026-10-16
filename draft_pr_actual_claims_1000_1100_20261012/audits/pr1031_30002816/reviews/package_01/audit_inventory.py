from pathlib import Path, PurePosixPath
import hashlib,json,subprocess,zipfile,datetime,io,re
R=Path(__file__).resolve().parent;P=R.parent.parent/'publication';H='f6570e093267a7f910faf9cdd60dfbc1c12f5681'
sha=lambda b:hashlib.sha256(b).hexdigest();rows=[];checks={}
pins=json.loads((P/'evidence/SUBMITTED_PINS.json').read_text())
for e in pins['files']:
 b=(P/'evidence/submitted'/e['relative']).read_bytes();g=subprocess.run(['git','show',H+':'+e['repository_path']],capture_output=True)
 rows.append({'path':e['repository_path'],'relative':e['relative'],'git_exit':g.returncode,'git_bytes':len(g.stdout),'git_sha256':sha(g.stdout),'package_bytes':len(b),'package_sha256':sha(b),'all_equal':g.returncode==0 and g.stdout==b and len(b)==e['bytes'] and sha(b)==e['sha256']})
checks['original_29_git_bytes']=len(rows)==29 and all(e['all_equal'] for e in rows)
zpath=P/'grassmann_calibrations_source_verification_v1.zip';zbytes=zpath.read_bytes();z=zipfile.ZipFile(io.BytesIO(zbytes));zs=[];names=z.namelist();safe=True
for e in z.infolist():
 n=e.filename;p=PurePosixPath(n);safe=safe and not p.is_absolute() and '..' not in p.parts and '\\' not in n and '\0' not in n and e.external_attr>>16&0o170000!=0o120000
 b=z.read(e);disk=P/PurePosixPath(n).relative_to("grassmann_calibrations_v1");zs.append({'name':n,'bytes':len(b),'sha256':sha(b),'crc':e.CRC,'timestamp':e.date_time,'compress_type':e.compress_type,'external_attr':e.external_attr,'disk_match':disk.is_file() and disk.read_bytes()==b})
checks.update(zip_count_104=len(names)==104,zip_unique=len(set(names))==len(names),zip_paths_safe=safe,zip_crc_failure=z.testzip(),zip_disk_all_equal=all(e['disk_match'] for e in zs),zip_sorted=names==sorted(names))
manifest=json.loads((P/'PACKAGE_MANIFEST.json').read_text());ms=[]
for e in manifest['files']:
 b=(P/e['path']).read_bytes();ms.append({'path':e['path'],'match':len(b)==e['bytes'] and sha(b)==e['sha256']})
checks['manifest_all_pins']=all(e['match'] for e in ms)
checks['manifest_inventory_exact']=set(e['path'] for e in manifest['files'])|{'PACKAGE_MANIFEST.json'}==set(str(PurePosixPath(n).relative_to("grassmann_calibrations_v1")) for n in names)
links=[]
for file in [P/'README.md',P/'SUPPLEMENT.md',P/'evidence/INDEX.md']:
 for t in re.findall(r'\]\(([^)]+)\)',file.read_text()):
  if not t.startswith(('http:','https:')):links.append({'file':str(file.relative_to(P)),'target':t,'exists':(file.parent/t.split('#')[0]).exists()})
checks['navigation_all_existing']=all(e['exists'] for e in links)
checks['metadata_exact_wrapping']=json.loads((P/'metadata.json').read_text())==json.loads((P/'zenodo-deposit.json').read_text())['metadata']
repro=io.BytesIO()
with zipfile.ZipFile(repro,'w') as out:
 for e in z.infolist():out.writestr(e,z.read(e))
checks['zip_byte_rebuild_same']=repro.getvalue()==zbytes
if safe and len(set(names))==len(names) and z.testzip() is None:z.extractall(R/'extracted')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_head':H,'checks':checks,'zip':{'bytes':len(zbytes),'sha256':sha(zbytes),'entries':zs},'original_git_rows':rows,'manifest_rows':ms,'navigation':links}
(R/'receipts/INVENTORY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(checks,indent=2));print('ZIP',len(zbytes),sha(zbytes))
