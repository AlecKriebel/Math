from pathlib import Path,PurePosixPath
import hashlib,json,datetime,zipfile,gzip
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint');O=B.parent/'whole_package_adversary_01';D=B.parent/'initial_review_20261016'
def record(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def matches(p,row):return p.is_file() and not p.is_symlink() and all(record(p)[k]==row[k] for k in ('bytes','sha256'))
results={}
for sub,manifest in [('', 'SOURCE_MANIFEST.json'),('verification','MANIFEST.json'),('pr_update/5100015','MANIFEST.json'),('pr_update/5100015','CURRENT_PACKET_MANIFEST.json')]:
 base=B/sub;obj=json.loads((base/manifest).read_text());rows=obj['files'];assert all(matches(base/r['path'],r) for r in rows)
 results[(Path(sub)/manifest).as_posix()]={'entries':len(rows),'all_actual_bytes_match':True}
# Independently compare all 23 native intake files with both preserved copies,
# not merely archived copies with each other or self-declared hashes.
intake=json.loads((D/'INTAKE.json').read_text());orig=[]
for row in intake['original_source_files']:
 p=D/'submitted'/row['native_path'];rel=p.relative_to(D/'submitted/unsolved_math_prioritization/attempts/5100015')
 assert matches(p,row)
 for folder in [B/'verification/original_submission',B/'pr_update/5100015/history/original_submission_20261016']:
  assert (folder/rel).read_bytes()==p.read_bytes()
 orig.append({'path':rel.as_posix(),**record(p)})
assert len(orig)==23
results['originals']={'all_23_match_actual_native_intake_and_both_preservations':True,'files':orig}
for folder in [B/'verification/original_submission',B/'pr_update/5100015/history/original_submission_20261016']:
 actual={p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()};assert actual=={r['path'] for r in orig}
 frozen=json.loads((folder/'FROZEN_MANIFEST.json').read_text())
 assert all(matches(folder/p,r) for p,r in frozen['files'].items())
results['historical_original_freezes']={'both_valid':True,'entries_each':len(frozen['files'])}
# Bind public submission/deposit fields and each uploaded actual payload.
pkg=json.loads((B/'PACKAGE_MANIFEST.json').read_text());dep=json.loads((B/'deposit.json').read_text());meta=json.loads((B/'metadata.json').read_text())
assert dep['metadata']==meta
for row in pkg['submission_files']+[pkg['source_manifest'],pkg['manuscript_source'],pkg['metadata']]:assert matches(B/row['path'],row)
assert {r['path'] for r in dep['files']}=={r['path'] for r in pkg['submission_files']}
results['package_and_deposit']={'all_actual_bytes_and_metadata_match':True}
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
 names=z.namelist();bad=[p for p in names if any(t.startswith('private') or t in ['__pycache__','node_modules','reproduction_environment'] for t in PurePosixPath(p).parts)]
 assert not bad;assert len(names)==len(set(names))==pkg['source_archive_entries']
 results['zip_safety']={'entries':len(names),'uncompressed_bytes':sum(i.file_size for i in z.infolist()),'compressed_bytes':sum(i.compress_size for i in z.infolist()),'forbidden_path_names':bad,'declared_member_count_matches':True}
# Verify the lossless failed-physical payload, retaining it in place.
f=B/'verification/audits/physical_geometry_adversary_01/FAILED_PROBE_01_COMPLETE.json.gz';raw=gzip.decompress(f.read_bytes());j=json.loads(raw)
results['lossless_failed_physical_payload']={'compressed':record(f),'decompressed_bytes':len(raw),'decompressed_sha256':hashlib.sha256(raw).hexdigest(),'valid_json':True,'type':type(j).__name__}
results['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();results['status']='PASS'
(O/'PACKAGE_CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({k:v for k,v in results.items() if k!='originals'},indent=2))
# Correct the manually anticipated timestamps additively; retain original assertions.
times={p:datetime.datetime.fromtimestamp((O/p).stat().st_mtime,datetime.timezone.utc).isoformat() for p in ['INITIAL_SCOPE.md','independent_proof.md']}
(O/'TIMESTAMP_CORRECTION.md').write_text('# Additive timestamp correction\n\nRecorded UTC '+results['utc']+'. Case estimate 50%.\n\nThe prose timestamps in INITIAL_SCOPE.md (05:35Z) and independent_proof.md (05:42Z) were manually anticipated and are not trustworthy execution timestamps. The original files and assertions are retained unchanged. Actual file modification times read now are '+json.dumps(times)+'. FROZEN_BYTES.json supplies the actual 05:34:05.239599 UTC freeze timestamp; ZIP_NORMALIZED.json supplies the actual 05:35:20.993768 UTC adjacent-execution timestamp. The independent proof assessment was written before any earlier scoped verdict was read. All later timestamps are machine generated.\n')
