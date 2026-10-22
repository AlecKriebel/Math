"""Owned read-only file/receipt checks. No imported inherited program."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,gzip,ast,datetime,stat
O=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015')
P=Path(__file__).resolve().parent.parent
B=O/'preprint';N=P/'native_custody_01';R=P/'root_provider_readback_01'
def h(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(p.read_bytes())
def checked(base,row):
 rel=PurePosixPath(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
 p=base/str(rel);assert p.is_file() and not p.is_symlink() and p.resolve()==p
 raw=p.read_bytes();assert len(raw)==row['bytes'] and h(raw)==row['sha256'],str(p)
 return raw
freezes={
 'manuscript.tex':(16085,'01b7feb398c95ce1a521f379e472e6c856a776408da5b1ccb93db9b0f88a8fe7'),
 'manuscript.pdf':(82528,'8e28a1764160a7f7ef6e9bf4d1a1937062a003ab462ec93ce69c4643a5c36a55'),
 'k303b-source-verification.zip':(683157,'0039aeee870804a149a5ae70f6893335387670e122f833e622d70b42584550f4'),
 'metadata.json':(2143,'ea1306176b6d86a921b4783ddb20016eef79815479c35f8b9e6fe1ce0e666f9c'),
 'deposit.json':(2430,'b5bf1aedcdab7ca6851a776c97170e25ceeeccac88e858cc56078a786d0959ba'),
 'PACKAGE_MANIFEST.json':(1089,'4dc82f095c68bd8bc4e7b81718300d40ba1abe79a7290e70e5795df8e0c1d79b'),
 'FINAL_CLEARANCE.json':(10523,'370cd4bbfb463597680b7b52fd59ba731a762c82296c98ad2571d947f902e065')}
for file,(size,sha) in freezes.items():checked(B,dict(path=file,bytes=size,sha256=sha))
manifest_counts={}
for rel in ['SOURCE_MANIFEST.json','verification/MANIFEST.json','pr_update/5100015/CURRENT_PACKET_MANIFEST.json']:
 mf=B/rel;data=load(mf);rows=data['files'];assert len(set(r['path'] for r in rows))==len(rows)
 for row in rows:checked(mf.parent,row)
 manifest_counts[rel]=len(rows)
 if rel!='SOURCE_MANIFEST.json':assert {str(p.relative_to(mf.parent)) for p in mf.parent.rglob('*') if p.is_file() and p!=mf}=={r['path'] for r in rows}
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
 names=z.namelist();assert len(names)==len(set(names))==211 and z.testzip() is None
 wanted={r['path'] for r in load(B/'SOURCE_MANIFEST.json')['files']}|{'SOURCE_MANIFEST.json'}
 assert {str(PurePosixPath(x).relative_to('k303b_outer_center_pedal_product')) for x in names}==wanted
 for name in names:
  rel=PurePosixPath(name).relative_to('k303b_outer_center_pedal_product');assert '..' not in rel.parts
  assert z.read(name)==(B/str(rel)).read_bytes()
  assert not any(s.startswith('private') or s in ('__pycache__','.venv','node_modules') for s in rel.parts)
  assert not str(rel).endswith('.pdf') or str(rel)=='manuscript.pdf'
original=load(N/'ORIGINAL_INVENTORY_VERIFIED.json')['leaves'];revised=load(N/'REVISED_INVENTORY_VERIFIED.json')['leaves']
for row in original+revised:
 raw=(N/row['archival_path']).read_bytes();assert len(raw)==row['bytes'] and h(raw)==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob']
for row in original:
 rel=row['path'].split('attempts/5100015/',1)[1];raw=(N/row['archival_path']).read_bytes()
 for base in [N/'archive/revised/history/original_submission_20261016',B/'pr_update/5100015/history/original_submission_20261016',B/'verification/original_submission']:
  assert (base/rel).read_bytes()==raw,(base,rel)
# Selected V3 public allowlist bytes and old executable source equivalence.
allow=load(N/'PUBLIC_ALLOWLIST_V3.json');rows=allow['files']
for row in rows:checked(N,row)
old=ast.parse((N/'verify_public_custody_offline.py').read_text());new=ast.parse((N/'verify_public_custody_offline_v3.py').read_text())
assert ast.dump(ast.Module(body=old.body[1:],type_ignores=[]))==ast.dump(ast.Module(body=new.body[1:],type_ignores=[]))
# Actual Root replay receipt: inspect all expected/copy scientific pins and status, do not relabel as owned execution.
replay=load(P/'root_reproduction_01/isolated_replay/REPRODUCTION.json');assert replay['status']=='PASS' and replay['scientific_programs']==8 and replay['verified_frozen_files_before_after']==149
for row in replay['results']:
 assert row['status']=='PASS' and row['returncode']==0 and row['all_scientific_fields_identical'] and row['copied_program_byte_identical']
 assert h((B/'verification'/row['source_program']).read_bytes())==row['program_sha256']
# Actual provider receipts: exact local pins, normalized public metadata, public file MD5 and retained SHA-download observations.
for which in ['ZENODO_INSPECT','TRACKER_GET']:
 receipt=load(R/(which+'_RECEIPT.json'));assert receipt['returncode']==0 and receipt['read_only']
 for field in ['stdout','stderr']:
  row=receipt[field];raw=Path(row['path']).read_bytes();assert len(raw)==row['bytes'] and h(raw)==row['sha256']
meta=load(B/'metadata.json');record=load(R/'PUBLIC_RECORD_23413614.json');actual=record['metadata']
for k in ['title','description','publication_date','creators','keywords','version','access_right']:assert meta[k]==actual[k]
assert actual['license']['id']==meta['license'];assert actual['resource_type']['type']==meta['upload_type'] and actual['resource_type']['subtype']==meta['publication_type']
assert record['doi']=='10.5281/zenodo.23413614' and record['status']=='published' and record['submitted']
for file in record['files']:
 name={'k303b-outer-center-pedal-areas.pdf':'manuscript.pdf','k303b-source-verification.zip':'k303b-source-verification.zip'}[file['key']]
 raw=(B/name).read_bytes();assert file['size']==len(raw) and file['checksum']=='md5:'+hashlib.md5(raw).hexdigest()
obs=load(R/'PUBLIC_RECORD_DOWNLOAD_OBSERVATIONS.json');own=[r for r in obs['records'] if r['id']==23413614][0]
assert own['http_status']==200 and own['response_bytes']==len((R/'PUBLIC_RECORD_23413614.json').read_bytes()) and own['response_sha256']==h((R/'PUBLIC_RECORD_23413614.json').read_bytes())
for item in own['public_downloads']:
 name={'k303b-outer-center-pedal-areas.pdf':'manuscript.pdf','k303b-source-verification.zip':'k303b-source-verification.zip'}[item['name']]
 assert item['sha256']==h((B/name).read_bytes()) and item['bytes']==(B/name).stat().st_size and item['public_download_bytes_verified'] is True
tracker=load(R/'TRACKER_GET_STDOUT.json');values=tracker['values'];hits=[i+1 for i,row in enumerate(values) if any('10.5281/zenodo.23413614' in str(x) for x in row)]
assert hits==[121]
row=values[120];assert len(row)==4 and row[0]=='https://arxiv.org/abs/2004.12497v11' and row[1]=='' and row[2]=='https://doi.org/10.5281/zenodo.23413614'
assert 'Ferudun' in row[3] and 'unrefereed' in row[3].lower()
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','owned_script_sha256':h(Path(__file__).read_bytes()),'frozen_files':len(freezes),'manifest_counts':manifest_counts,'zip_members':211,'native_bodies':len(original)+len(revised),'original_history_identities':23,'V3_public_allowlist_files':len(rows),'V3_executable_AST_identical':True,'actual_Root_replay_inspected_not_reexecuted':8,'actual_Root_provider_and_public_download_receipts_inspected':True,'tracker_unique_doi_row':121,'tracker_cells':row,'limits':'Owned byte/receipt checks; no network or inherited program executed by this script. Provider/download execution remains Root evidence.'}
Path('OWNED_PACKAGE_RESULTS_02.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
