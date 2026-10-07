import datetime, hashlib, json, os, pathlib, stat, zipfile
root=pathlib.Path(__file__).resolve().parent.parent
pkg=root/'publication_package_v1'; own=root/'whole_publication_adversary_r1_20261007'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((pkg/'PACKAGE_MANIFEST.json').read_text())
expected={'PACKAGE_MANIFEST.json':'0d4f2a1fe22d06a787712b60821d477b54880c63c3f5716307a7a2eb0cf4b00f','antipedal_centroids.pdf':'9b50e03c513fe933dfabbead5900a942737b410e6dada8c10ac3a872e43f240e','antipedal_centroids_support.zip':'0889e60d0b5c59111d0de84889f37a412ecb9a71d76149a85c55f0f34dddd931'}
for name,digest in expected.items():
 if sha(pkg/name)!=digest: raise RuntimeError('candidate digest mismatch '+name)
allfiles=sorted(p for p in pkg.rglob('*') if p.is_file())
for p in allfiles:
 if p.is_symlink():raise RuntimeError('symlink '+str(p))
records=[]
for row in manifest['members']:
 p=pkg/row['relative']
 if len(p.read_bytes())!=row['bytes'] or sha(p)!=row['sha256']:raise RuntimeError('manifest mismatch '+row['relative'])
 records.append(row['relative'])
if len(records)!=len(set(records)):raise RuntimeError('duplicate manifest entries')
expectedzip=set(records)-{'antipedal_centroids.pdf'}|{'PACKAGE_MANIFEST.json'}
with zipfile.ZipFile(pkg/'antipedal_centroids_support.zip') as z:
 names=z.namelist()
 if len(names)!=len(set(names)) or set(names)!=expectedzip:raise RuntimeError('ZIP census mismatch')
 for info in z.infolist():
  name=info.filename
  if pathlib.PurePosixPath(name).is_absolute() or '..' in pathlib.PurePosixPath(name).parts:raise RuntimeError('ZIP traversal')
  if stat.S_ISLNK(info.external_attr>>16):raise RuntimeError('ZIP symlink')
  if z.read(name)!=(pkg/name).read_bytes():raise RuntimeError('ZIP bytes mismatch '+name)
 if z.testzip() is not None:raise RuntimeError('ZIP CRC failure')
meta=json.loads((pkg/'metadata.json').read_text()); deposit=json.loads((pkg/'zenodo-deposit.json').read_text())
if deposit['metadata']!=meta:raise RuntimeError('deposit metadata differs')
if deposit['files']!=[{'path':'antipedal_centroids.pdf'},{'path':'antipedal_centroids_support.zip'}]:raise RuntimeError('deposit upload census')
vm=json.loads((pkg/'verification/MANIFEST.json').read_text())
for row in vm['members']:
 p=pkg/'verification'/row['relative']
 if len(p.read_bytes())!=row['bytes'] or sha(p)!=row['sha256']:raise RuntimeError('verification manifest mismatch '+row['relative'])
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'candidate_hashes':expected,'whole_directory_files':len(allfiles),'package_manifest_members':len(records),'support_zip_members':len(names),'verification_files':len([p for p in (pkg/'verification').rglob('*') if p.is_file()]),'whole_directory_census':[{'relative':str(p.relative_to(pkg)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in allfiles],'directory_unmanifested_files':sorted(set(str(p.relative_to(pkg)) for p in allfiles)-set(records)-{'PACKAGE_MANIFEST.json'}),'manifest_bytes_and_sha256':'PASS','zip_census_and_exact_readback':'PASS','no_symlink_duplicate_or_path_traversal':'PASS','verification_manifest_readback':'PASS','deposit_metadata_equality_and_upload_census':'PASS'}
(own/'package_inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='whole_directory_census'},indent=2))
log=own/'RESEARCH_LOG.md'
if not log.exists():log.write_text('# Fresh whole-publication-package adversary, round 1\n\n'+result['UTC']+': Checkpoint 1; actual package inspection PID '+str(os.getpid())+'. Review completion estimate 45%. Read the candidate theorem and proof before prior audit reports. Independently reconstructed absolute-coordinate antipedal line systems and verified both intermediate and final pair coordinates through exact Groebner reduction, plus the positive determinant identity and exact four-period diamond. Independently assessed finite circle-action symmetry, arbitrary vertex stationarity, unconstrained eccentric-angle shift, connected Poncelet-family perimeter constancy, parity, star orientation and double-counted averaging. No mathematical flaw identified so far. Full directory census, candidate SHA-256 binding, 26-member ZIP byte readback, 17-member verification census, metadata equality and manifest hashes pass. Still pending: independent boundary and phase/star controls, fresh portable replay, complete rendered PDF and primary-source/provenance review. No candidate edit, Git/provider action or external-individual contact.\n')
