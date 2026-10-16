"""Independent byte, inventory and historical-original audit; read-only inputs."""
from pathlib import Path,PurePosixPath
import hashlib,json,stat,zipfile
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'preprint/history/review01_frozen'
SUB=HERE.parent/'submitted/unsolved_math_prioritization/attempts/5100063'
sha=lambda b:hashlib.sha256(b).hexdigest()
bad={'private','private_reading','private_transport','__pycache__'}
counts={}
def validate_manifest(path,root):
    data=json.loads(path.read_text());seen=set()
    for row in data['files']:
        name=row['path'];rel=PurePosixPath(name)
        assert name not in seen and not rel.is_absolute() and '..' not in rel.parts and not bad.intersection(rel.parts)
        seen.add(name);p=root/name
        assert p.is_file() and not p.is_symlink()
        raw=p.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],p
    counts[str(path.relative_to(BASE))]=len(seen)
    return seen
source=validate_manifest(BASE/'SOURCE_MANIFEST.json',BASE)
verification=validate_manifest(BASE/'verification/MANIFEST.json',BASE/'verification')
actual={p.relative_to(BASE/'verification').as_posix() for p in (BASE/'verification').rglob('*') if p.is_file()}
assert actual==verification|{'MANIFEST.json'}
native=BASE/'pr_update/5100063'
nativefiles=validate_manifest(native/'CURRENT_PACKET_MANIFEST.json',native)
assert nativefiles|{'CURRENT_PACKET_MANIFEST.json'}=={p.relative_to(native).as_posix() for p in native.rglob('*') if p.is_file()}
validate_manifest(native/'MANIFEST.json',native)
validate_manifest(native/'PUBLICATION_MANIFEST.json',native)
package=json.loads((BASE/'PACKAGE_MANIFEST.json').read_text())
for row in package['submission_files']+[package['source_manifest'],package['manuscript_source'],package['metadata']]:
    data=(BASE/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
assert json.loads((BASE/'deposit.json').read_text())['metadata']==json.loads((BASE/'metadata.json').read_text())
prefix='k904a_outer_focal_inverse_product/'
with zipfile.ZipFile(BASE/'k904a-source-verification.zip') as z:
    infos=z.infolist();names=[i.filename for i in infos]
    assert len(names)==len(set(names))==133
    assert set(names)=={prefix+x for x in source|{'SOURCE_MANIFEST.json'}}
    for i in infos:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and not bad.intersection(p.parts)
        assert not stat.S_ISLNK(i.external_attr>>16)
        assert z.read(i)==(BASE/i.filename.removeprefix(prefix)).read_bytes()
    counts['zip_entries']=len(names)
originals={p.relative_to(SUB).as_posix():p.read_bytes() for p in SUB.rglob('*') if p.is_file()}
assert len(originals)==19
for folder in [BASE/'verification/original_submission',native/'history/original_submission_20261015']:
    actual={p.relative_to(folder).as_posix():p.read_bytes() for p in folder.rglob('*') if p.is_file()}
    assert originals==actual
counts['exact_originals_in_each_of_two_copies']=len(originals)
result={'status':'PASS','scope':'All frozen source and portable/native current manifests, exact inventory and all ZIP payload bytes; both original19-file copies against immutable submitted intake. Historical family manifests retain documented source-relative bases.','counts':counts,'frozen_sha256':{n:sha((BASE/n).read_bytes()) for n in ['manuscript.tex','manuscript.pdf','k904a-source-verification.zip','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json']}}
(HERE/'PACKAGE_INTEGRITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
