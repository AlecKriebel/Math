#!/usr/bin/env python3
"""Read-only candidate audit. All products stay in the reviewer folder."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,html,importlib.util,json,os,shutil,stat,subprocess,sys,zipfile,zlib
HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
PACKAGE=BASE/'package'
PRIVATE=HERE/'private_sources'
EXTRACT=PRIVATE/'fresh_archive'
sys.dont_write_bytecode=True

def require(test,message):
 if not test:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(name,obj):
 (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def info(path):
 d=path.read_bytes();return {'bytes':len(d),'sha256':sha(d)}
freeze=json.loads((HERE/'FROZEN_INPUT.json').read_text())
require((BASE/'PACKAGE_REVIEW_INPUT_4.json').read_bytes()==(HERE/'FROZEN_INPUT.json').read_bytes(),'Freeze changed')
initial={n:{**info(PACKAGE/n),'matches_freeze':info(PACKAGE/n)==record} for n,record in freeze['files'].items()}
require(all(v['matches_freeze'] for v in initial.values()),'Frozen payload changed')
EXTRACT.mkdir(parents=True,exist_ok=True)
sums=json.loads((PACKAGE/'SHA256SUMS.json').read_text())['files']
rows=[]
with zipfile.ZipFile(PACKAGE/'missing_faces_verification_v1.zip') as z:
 names=z.namelist(); require(len(names)==len(set(names))==68,'Archive count/uniqueness')
 require(set(names)==set(sums)|{'SHA256SUMS.json'},'Exact archive membership')
 require(z.testzip() is None,'Archive CRC test')
 for member in z.infolist():
  name=member.filename;p=PurePosixPath(name);mode=member.external_attr>>16
  require(not p.is_absolute() and '..' not in p.parts and '\\' not in name and not member.is_dir(),'Unsafe membership')
  require(not stat.S_ISLNK(mode),'ZIP symlink')
  require(not any(t in p.parts for t in ('private_sources','__pycache__')) and not name.endswith(('.pdf','.png','.pyc')),'Private foreign/derived artifact unexpectedly archived')
  data=z.read(name);require((zlib.crc32(data)&0xffffffff)==member.CRC,'CRC mismatch')
  require(data==(PACKAGE/name).read_bytes(),'Archive/local payload mismatch: '+name)
  if name in sums: require({'bytes':len(data),'sha256':sha(data)}==sums[name],'Payload manifest: '+name)
  destination=EXTRACT/name;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
  rows.append({'name':name,'bytes':len(data),'sha256':sha(data),'crc32':f'{member.CRC:08x}','regular_payload':True})
dump('ARCHIVE_CHECKS.json',{'archive':info(PACKAGE/'missing_faces_verification_v1.zip'),'entries':68,'manifest_payloads':len(sums),'crc_pass':True,'exact_membership_pass':True,'archive_equals_local':True,'safe_membership_pass':True,'members':rows})
historical=EXTRACT/'verification/historical'; original=BASE/'source_snapshot/unsolved_math_prioritization/attempts/30000689'
histrows=[]
for f in sorted(historical.rglob('*')):
 if f.is_file():
  rel=f.relative_to(historical);same=f.read_bytes()==(original/rel).read_bytes();require(same,'Historical snapshot mismatch')
  histrows.append({'path':str(rel),**info(f),'original_match':same})
require(len(histrows)==15,'Historical file count')
manifestrows=[]
for m,key,pathkey in [(historical/'PUBLICATION_MANIFEST.json','public_payload_files','path'),(historical/'audit/AUDIT_MANIFEST.json','audit_files','file'),(historical/'release/FROZEN_AUTHOR_MANIFEST.json','files','path')]:
 for row in json.loads(m.read_text())[key]:
  f=m.parent/row[pathkey];actual=info(f);require(actual=={k:row[k] for k in ('bytes','sha256')},'Historical manifest mismatch')
  manifestrows.append({'manifest':str(m.relative_to(historical)),'reference':row[pathkey],**actual,'match':True})
require(len(manifestrows)==24,'Historical reference count')
auditman=json.loads((historical/'audit/AUDIT_MANIFEST.json').read_text())
for ref in auditman['author_manifest_checks']:
 require(info(historical/'release'/ref['file'])['sha256']==ref['sha256'],'Cross-manifest SHA mismatch')
patchrows=[]
for filename,oldrel in [('check_exact.py','release/check_exact.py'),('check_independent.py','audit/check_independent.py')]:
 destination=PRIVATE/('patched_'+filename);shutil.copyfile(historical/oldrel,destination)
 result=subprocess.run(['patch',str(destination),str(EXTRACT/'verification/patches'/filename.replace('.py','.patch'))],capture_output=True)
 require(result.returncode==0,'Patch application failed: '+result.stderr.decode())
 require(destination.read_bytes()==(EXTRACT/'verification/checks'/filename).read_bytes(),'Patch output mismatch')
 patchrows.append({'script':filename,'output':info(destination),'exact_match':True,'patch_stdout':result.stdout.decode()})
dump('HISTORICAL_PATCH_CHECKS.json',{'original_snapshot_files':histrows,'manifest_references':manifestrows,'original_files':15,'references':24,'additional_author_crosschecks':6,'patches':patchrows})
old=BASE/'references/private_sources/round3_accepted'
oldmetadata=json.loads((old/'metadata.json').read_text());current=json.loads((PACKAGE/'metadata.json').read_text());deposit=json.loads((PACKAGE/'deposit.json').read_text())
require(deposit['metadata']==current,'Canonical metadata copies mismatch')
olddeposit=json.loads((old/'deposit.json').read_text())
expectedold=html.unescape(current['description']);require(expectedold==oldmetadata['description'],'Semantic HTML mismatch')
newexpected=dict(oldmetadata);newexpected['description']=oldmetadata['description'].replace('d >= 3','d &gt;= 3');require(current==newexpected,'Other metadata change')
newdeposit=dict(olddeposit);newdeposit['metadata']=current;require(deposit==newdeposit,'Other deposit change')
reconcile=json.loads((BASE/'ZENODO_DRAFT_METADATA_RECONCILIATION.json').read_text())
require(current['description']==reconcile['differences']['description']['remote'],'Current does not equal server encoding receipt')
require(oldmetadata['description']==reconcile['differences']['description']['canonical'],'Old receipt description mismatch')
with zipfile.ZipFile(old/'missing_faces_verification_v1.zip') as z:
 oldmap={n:z.read(n) for n in z.namelist()}
newmap={r['name']:(EXTRACT/r['name']).read_bytes() for r in rows}
require(set(oldmap)==set(newmap),'Changed ZIP membership')
changed=[n for n in sorted(oldmap) if oldmap[n]!=newmap[n]]
require(changed==['SHA256SUMS.json','metadata.json','verification/audit_evidence/current_package_corrections.json'],'Unexpected archived change')
for n in ('manuscript.tex','manuscript.pdf','README.md'):
 require((PACKAGE/n).read_bytes()==(old/n).read_bytes(),'Unexpected main-payload change')
correctionname='verification/audit_evidence/current_package_corrections.json'
oldcor=json.loads(oldmap[correctionname]);newcor=json.loads(newmap[correctionname]);addition=newcor.pop('subsequent_live_metadata_encoding')
require(oldcor==newcor,'Unexpected correction history change')
repair=json.loads((BASE/'ROUND3_LIVE_METADATA_REPAIR_RECEIPT.json').read_text());require(addition==repair,'Repair receipt differs from archived history')
spec=importlib.util.spec_from_file_location('review_pure_zenodo','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py');kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)
meta,files=kit.load_manifest(PACKAGE/'deposit.json');require(meta==current,'Kit metadata mismatch')
prepared=[]
for f in files: prepared.append({k:str(v) if isinstance(v,Path) else v for k,v in f.items()})
dump('METADATA_CHECKS.json',{'canonical_equal':True,'only_field_changed':'description','literal_change':'d >= 3 -> d &gt;= 3','html_unescape_identical':True,'current_description_equals_safe_server_receipt':True,'all_other_fields_unchanged':True,'old_and_new_deposit_file_lists_equal':True,'changed_archive_entries':changed,'unchanged_source_pdf_readme_checkers_expected_historical':True,'archived_repair_matches_receipt':True,'pure_local_load_manifest_pass':True,'api_client_instantiated':False,'credentials_or_state_loaded':False,'prepared_files':prepared,'metadata':current,'same_unpublished_draft_id_from_receipt_only':23310484})
currentroot=EXTRACT/'verification';manifest=json.loads((currentroot/'CONTROL_MANIFEST.json').read_text());positives=[];parsed={}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for c in manifest['cases']:
 script=currentroot/c['script'];expected=currentroot/c['expected'];require(info(script)['sha256']==c['script_sha256'] and info(expected)['sha256']==c['expected_sha256'],'Current control manifest')
 tree=ast.parse(script.read_text());require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'Current assert reliance')
 for optimized in (False,True):
  command=[sys.executable]+(['-O'] if optimized else [])+[str(script)]
  result=subprocess.run(command,cwd=currentroot,env=env,capture_output=True,timeout=300)
  require(result.returncode==0 and not result.stderr and result.stdout==expected.read_bytes(),'Positive mismatch')
  label=Path(c['script']).stem+('_optimized' if optimized else '_normal')
  (HERE/(label+'.json')).write_bytes(result.stdout)
  positives.append({'script':c['script'],'mode':'optimized' if optimized else 'normal','returncode':result.returncode,'stderr':result.stderr.decode(),'bytes':len(result.stdout),'sha256':sha(result.stdout),'expected_byte_match':True})
 parsed[c['script']]=json.loads(expected.read_text())
for optimized in (False,True):
 command=[sys.executable]+(['-O'] if optimized else [])+['reproduce.py']
 result=subprocess.run(command,cwd=currentroot,env=env,capture_output=True,timeout=300)
 require(result.returncode==0 and not result.stderr,'Driver positive failure')
 (HERE/('driver_optimized.json' if optimized else 'driver_normal.json')).write_bytes(result.stdout)
counts={'author':{'stellar_examples':len(parsed['checks/check_exact.py']['stellar_examples']),'quotient_rank_calculations':4*len(parsed['checks/check_exact.py']['quotient_controls']),'flores_cycles':len(parsed['checks/check_exact.py']['flores_cycles']),'flag':parsed['checks/check_exact.py']['flag_control']},'audit':{k:v for k,v in parsed['checks/check_independent.py'].items() if k!='witness_details'},'bitmask':{k:v for k,v in parsed['checks/check_bitmask_controls.py']['bistellar'].items() if k!='witness_details'},'bitmask_quotient_rank_calculations':sum(4*len(r['quotients']) for r in parsed['checks/check_bitmask_controls.py']['stellar_and_flores'])}
dump('POSITIVE_REPRODUCTION.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'independently_extracted_archive':True,'runs':positives,'direct_run_count':6,'driver_run_count':2,'driver_child_runs':12,'counts':counts,'assert_nodes_current':0})
print('Archive 68 entries / 67 payloads; historical 15 files / 24 references; metadata semantic/exact encoding checks and 6 direct + 2 whole-driver passes complete.')
