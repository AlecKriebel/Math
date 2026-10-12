from pathlib import Path
import datetime, hashlib, json, stat, zipfile
base=Path(__file__).resolve().parent
audit=base.parent
package=audit/'publication_package_v3'
expected=json.loads((audit/'qualified_publication_20261004/QUALIFIED_INPUT_PINS.json').read_text())
pin=lambda b:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
observed={name:pin((package/name).read_bytes()) for name in expected['pins']}
assert observed==expected['pins']
members={}
with zipfile.ZipFile(package/'even-strand-markov-verification-v3.zip') as z:
    assert z.testzip() is None
    assert len(z.namelist())==10 and len(set(z.namelist()))==10
    for info in z.infolist():
        assert '/' not in info.filename and info.filename not in ('.','..')
        assert stat.S_IFMT(info.external_attr >> 16)==stat.S_IFREG
        b=z.read(info.filename)
        assert b==(package/info.filename).read_bytes()
        members[info.filename]=pin(b)
    d=base/'private/extracted'
    d.mkdir(parents=True,exist_ok=False)
    z.extractall(d)
checksums={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (d/'SHA256SUMS').read_text().splitlines()}
assert set(checksums)==set(members)-{'SHA256SUMS'}
assert all(checksums[n]==members[n]['sha256'] for n in checksums)
original=json.loads((audit/'ORIGINAL_MANIFEST.json').read_text())
assert original['head']==expected['original_head']
original_checked=[]
for row in original['files']:
    p=audit/'original'/row['path']; b=p.read_bytes()
    assert pin(b)=={'bytes':row['bytes'],'sha256':row['sha256']}
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
    original_checked.append(row['path'])
record={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'qualified_inputs':observed,
 'archive_members':members, 'original_head':original['head'],'original_15_exact_verified':original_checked,
 'priority_clearance':False,'qualified_publication_is_explicit_human_exception':True,
 'fresh_review_status':'in progress','review_completion_percent':20}
(base/'INPUT_PINS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
