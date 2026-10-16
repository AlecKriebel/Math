"""Read-only packet, ZIP, source-custody and native consistency checks."""
from pathlib import Path,PurePosixPath
from zipfile import ZipFile
import ast,datetime,hashlib,json,stat
R=Path(__file__).resolve().parent;A=R.parent;PK=A/'publication_package_v2';S=PK/'supplement';N=A/'integration_preparation/native_template_pending_02'
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def utc():return datetime.datetime.now(datetime.UTC).isoformat()
issues=[]
def check(b,label):
 if not b:issues.append(label)
outer=json.loads((PK/'REVIEW_PACKET_MANIFEST.json').read_text())
check(sha((PK/'REVIEW_PACKET_MANIFEST.json').read_bytes())=='fd444f73098ff57853bd0e080b70b68bc85e008cccae5bad3b742a5db9c378dd','outer manifest changed')
for f in outer['files']:
 p=PK/f['path'];b=binding(p);check(b['bytes']==f['bytes'] and b['sha256']==f['sha256'],'outer pin: '+f['path'])
ziprec=[];json_count=0;python_count=0;text_count=0;history_source_match=0
with ZipFile(PK/'verification-package.zip') as z:
 check(z.testzip() is None,'CRC failure');names=z.namelist();check(len(names)==len(set(names)),'duplicate ZIP paths')
 manifest=json.loads(z.read('SHA256SUMS.json'));entry={f['path']:f for f in manifest['files']}
 check(set(entry)==set(names)-{'SHA256SUMS.json'},'payload allowset mismatch')
 check({str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}==set(names),'disk supplement names differ')
 for info in z.infolist():
  name=info.filename;p=PurePosixPath(name);data=z.read(name)
  safe=not(p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or '\x00' in name or name.startswith('/') or any(c in name for c in ['\n','\r']))
  mode=info.external_attr>>16
  check(safe and not stat.S_ISLNK(mode) and not info.is_dir(),'unsafe member: '+name)
  check(data==(S/name).read_bytes(),'staged ZIP mismatch: '+name)
  if name!='SHA256SUMS.json':check(len(data)==entry[name]['bytes'] and sha(data)==entry[name]['sha256'],'payload pin: '+name)
  check(data[:4]!=b'%PDF' and b'\x00' not in data and Path(name).suffix.lower() not in ['.pdf','.png','.jpg','.jpeg','.webp','.html','.whl','.pyc'], 'private/binary member: '+name)
  text=data.decode('utf-8');text_count+=1
  if name.endswith('.json'):json.loads(text);json_count+=1
  if name.endswith('.py'):ast.parse(text,filename=name);python_count+=1
  if name.startswith('audit_history/'):
   original=A/name.removeprefix('audit_history/')
   check(original.exists() and original.read_bytes()==data,'archived authored source differs: '+name)
   history_source_match+=1
  ziprec.append({'path':name,'bytes':len(data),'sha256':sha(data),'safe_path':safe,'unix_mode':format(mode,'06o')})

pointer=A/'integration_preparation/CURRENT_TEMPLATE.json';immutable=A/'integration_preparation/NATIVE_TEMPLATE_PENDING_02_MANIFEST.json'
check(pointer.read_bytes()==immutable.read_bytes(),'native pointer differs from immutable manifest')
j=json.loads(pointer.read_text());native={str(p.relative_to(N)) for p in N.rglob('*') if p.is_file()}
check(native==set(j['files']),'native extra/missing files')
for f,pin in j['files'].items():
 p=N/f;b=binding(p);check(b['bytes']==pin['bytes'] and b['sha256']==pin['sha256'],'native pin: '+f)
for p in S.rglob('*'):
 if p.is_file():check(p.read_bytes()==(N/'exact_verification'/p.relative_to(S)).read_bytes(),'native supplement differs: '+str(p.relative_to(S)))
for native_path,package_path in [('taut_godbillon_vey.tex','taut_godbillon_vey.tex'),('verify.py','supplement/controls/verify_forms.py'),('review/author_replay/verify.py','supplement/controls/verify_forms.py'),('review/independent_checks.py','supplement/controls/independent_symbolic_checks.py')]:check((N/native_path).read_bytes()==(PK/package_path).read_bytes(),'native current copy: '+native_path)
orig=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
for e in orig['files']:
 rel=e['path'].split('10300044/',1)[1];b=binding(N/'historical_original'/rel)
 check(b['bytes']==e['bytes'] and b['sha256']==e['sha256'],'historical original changed: '+rel)
check((N/'CANDIDATE.md').read_bytes()==(N/'historical_original/CANDIDATE.md').read_bytes(),'original proof changed')

# Actual authored policies, rather than filename pattern guessing.
policies={
 'global_taut_geometry_adversary':('PUBLIC_OWN_ALLOWLIST.json','exact_public_own_files'),
 'literal_source_adversary':('PUBLIC_SAFE_ALLOWLIST.json','case_relative_files'),
 'gv_algebra_reproduction_adversary':('SAFE_OWN_ALLOWLIST.json','files'),
 'priority_suspension_literature':('AUTHORED_SAFE_ALLOWLIST.json','files'),
 'priority_volume_obstructions':('SAFE_PUBLIC_OWN_ALLOWLIST.json','paths')}
policy_results={}
for family,(filename,key) in policies.items():
 d=json.loads((A/family/filename).read_text())
 if key not in d:
  policy_results[family]={'pending_key_discovery':list(d)};continue
 allowed=d[key]
 if family=='literal_source_adversary':allowed=[p.split(family+'/',1)[1] for p in allowed]
 if family=='priority_suspension_literature':allowed+=['ADDENDUM_90_PERCENT_SCOPE.md','ADDENDUM_HASHSEAL.json']
 actual={str(p.relative_to(S/'audit_history'/family)) for p in (S/'audit_history'/family).rglob('*') if p.is_file()}
 check(actual==set(allowed),'family allowlist mismatch: '+family)
 policy_results[family]={'declared_count':len(allowed),'archived_count':len(actual),'exact_match':actual==set(allowed)}
target_policy=json.loads((A/'priority_target_history/PUBLIC_AUTHORED_ALLOWLIST.json').read_text())
allowed={x['path'] for x in target_policy['exact_public_authored_files']}
actual={str(p.relative_to(S/'audit_history/priority_target_history')) for p in (S/'audit_history/priority_target_history').rglob('*') if p.is_file()}
check(allowed==actual,'target-history exact safe policy mismatch')
policy_results['priority_target_history']={'declared_count':len(allowed),'archived_count':len(actual),'exact_match':actual==allowed,'excluded_custody_controls_absent':not any(n in actual for n in ['PUBLIC_AUTHORED_ALLOWLIST.json','FINAL_SEAL.json','FINAL_SEAL.sha256'])}

report={'created_utc':utc(),'issues':issues,'all_checks_pass':not issues,'outer_manifest':binding(PK/'REVIEW_PACKET_MANIFEST.json'),'outer_files':{f['path']:binding(PK/f['path']) for f in outer['files']},'zip_file_entries':len(ziprec),'payload_entries_excluding_self_manifest':len(ziprec)-1,'all_UTF8_read':text_count,'JSON_parsed':json_count,'Python_parsed':python_count,'archived_source_byte_matches':history_source_match,'zip_members':ziprec,'native_manifest':binding(immutable),'native_files':len(native),'native_pointer_equal_immutable':pointer.read_bytes()==immutable.read_bytes(),'all_17_originals_preserved':len(orig['files'])==17 and not any('historical original' in i for i in issues),'family_allowlist_results':policy_results}
(R/'PACKAGE_INTEGRITY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['zip_members','outer_files']},indent=2))
