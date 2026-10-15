"""Independent package-integrity audit. Writes only in this review folder."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile
from datetime import datetime, timezone
R=Path(__file__).absolute().parent.parent
W=Path(__file__).absolute().parent
frozen=json.loads((R/'FROZEN_INPUTS.json').read_text())
rows=[]
for row in frozen['submission_files']:
    b=(R/row['path']).read_bytes()
    got={'path':row['path'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    assert all(got[k]==row[k] for k in got),row['path']
    rows.append(got)
X=W/'private/extracted'
assert not X.exists()
X.mkdir(parents=True)
with zipfile.ZipFile(R/'output/dipole_spectrum_verification.zip') as z:
    names=z.namelist()
    assert len(names)==len(set(names))==frozen['archive_members']==136
    assert z.testzip() is None
    for name in names:
        p=PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts and not name.endswith('/')
        assert not any(s.startswith('private') or s=='__pycache__' for s in p.parts)
        dst=X/name; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes(z.read(name))
manifest=json.loads((X/'PACKAGE_FILES.json').read_text())
verified=[]
for row in manifest['files']:
    b=(X/row['path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    verified.append(row)
assert set(names)=={'PACKAGE_FILES.json'}|{row['path'] for row in verified}
assert (X/'PACKAGE_FILES.json').read_bytes()==(R/'PACKAGE_FILES.json').read_bytes()
local_matches=[]
for row in verified:
    if (R/row['path']).is_file():
        assert (R/row['path']).read_bytes()==(X/row['path']).read_bytes(),row['path']
        local_matches.append(row['path'])
meta=json.loads((R/'metadata.json').read_text())
deposit=json.loads((R/'deposit.json').read_text())
assert meta==deposit['metadata']==json.loads((X/'metadata.json').read_text())
U=X/'pr_update/30005244'
original=json.loads((U/'ORIGINAL_SUBMISSION_MANIFEST.json').read_text())
assert original['original_PR_head']=='36d5ef15098163e74bf14c2e696f560ce592affd'
assert len(original['files'])==31
archival=[]
for row in original['files']:
    b=(U/row['archive_path']).read_bytes()
    sha=hashlib.sha256(b).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert len(b)==row['bytes'] and sha==row['sha256'] and blob==row['native_blob'],row
    archival.append({'native_path':row['native_path'],'archive_path':row['archive_path'],'bytes':len(b),'sha256':sha,'native_blob':blob,'all_match':True})
result={'utc':datetime.now(timezone.utc).isoformat(),'submission_pins':rows,'archive_members':len(names),'package_hashes_verified':len(verified),'no_extra_or_missing_members':True,'zip_crc_test':'pass','local_files_matched':local_matches,'metadata_deposit_archive_objects_identical':True,'archival_originals':archival,'extraction_directory':'private/extracted','all_passed':True}
(W/'PACKAGE_CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['archival_originals','local_files_matched']},indent=2))
