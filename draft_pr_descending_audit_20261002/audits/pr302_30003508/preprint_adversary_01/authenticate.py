"""Independently authenticate the literal frozen public candidate and real ZIP."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat,zipfile
R=Path(__file__).resolve().parent; F=R.parent/'preprint_package_v01'
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
manifest=F/'FIRST_CANDIDATE_MANIFEST.json'
assert pin(manifest)['bytes']==8376
assert pin(manifest)['sha256']=='522fc23022c2975a0d43b66796bc2fa58d95eb4a59b892b835ea034ef78f5a73'
declaration=json.loads(manifest.read_bytes()); rows=declaration['files']
assert len(rows)==23 and len({r['path'] for r in rows})==23
actual=[]
for row in rows:
    p=Path(row['path']); assert p.is_file() and not p.is_symlink()
    q=pin(p); assert all(q[k]==row[k] for k in ('bytes','sha256','mode'))
    assert q['mode']==0o444
    actual.append(q)
inner=json.loads((F/'MANIFEST.json').read_bytes())
assert len(inner['payload'])==19
out=R/'unpacked_actual_zip_v02';out.mkdir()
member_rows=[]
with zipfile.ZipFile(F/'spectral_tensor_verification.zip') as z:
    infos=z.infolist(); assert len(infos)==20
    prefix='spectral-tensor-consistency/'
    expected={prefix+r['path'] for r in inner['payload']}|{prefix+'MANIFEST.json'}
    assert len({i.filename for i in infos})==20 and {i.filename for i in infos}==expected
    for i in infos:
        rel=Path(i.filename);assert not rel.is_absolute() and '..' not in rel.parts and not i.is_dir()
        assert stat.S_ISREG(i.external_attr>>16) and i.external_attr>>16==0o100644
        member=i.filename[len(prefix):]
        b=z.read(i.filename);declared=(F/member).read_bytes();assert b==declared
        if member!='MANIFEST.json':
            row=next(r for r in inner['payload'] if r['path']==member)
            assert row['bytes']==len(b) and row['sha256']==hashlib.sha256(b).hexdigest()
            assert row['ZIP_mode']==i.external_attr>>16
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444)
        member_rows.append({'name':i.filename,'uncompressed_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
                            'ZIP_external_attr':i.external_attr,'ZIP_mode':i.external_attr>>16,
                            'ZIP_date_time':i.date_time,'ZIP_CRC32':i.CRC,'ZIP_compress_type':i.compress_type,'extracted':pin(p)})
for p in sorted(out.rglob('*'),reverse=True):
    if p.is_dir():p.chmod(0o555)
out.chmod(0o555)
metadata=json.loads((F/'record_metadata.json').read_bytes()); wrapper=json.loads((F/'zenodo-deposit.json').read_bytes())
assert wrapper['metadata']==metadata
assert wrapper['files']==[{'path':'spectral_tensor_consistency.pdf'},{'path':'spectral_tensor_verification.zip'}]
assert metadata['creators'][0]['orcid']=='0009-0001-9320-500X'
assert metadata['publication_type']=='preprint' and metadata['publication_date']=='2026-10-05'
assert pin(F/'spectral_tensor_consistency.pdf')['sha256']=='c0f8921a5a0f51e8ea71634d4064505252b7b31d4fdca49f6f8427302401c1a5'
assert pin(F/'spectral_tensor_verification.zip')['sha256']=='3416f9a1e0211d2122744f3ba8af8f6ac33bccf0e9957f223d600af548ccb8da'
receipt={'UTC':datetime.now(timezone.utc).isoformat(),'actual_PID':os.getpid(),'status':'PASS_WHOLE_BYTES_LITERAL23_REAL_ZIP20_METADATA',
         'frozen_manifest':pin(manifest),'literal_public_files':actual,'ZIP':pin(F/'spectral_tensor_verification.zip'),
         'ZIP_members':member_rows,'metadata_equivalence':True,'declared_inner_payload_count':19,
         'PDF_pages':8,'limits':'Byte authentication alone is not scientific verification. ZIP source copies extracted unchanged and frozen; no prior verdict read.'}
write(R/'AUTHENTICATION.json',receipt)
print(json.dumps({'status':receipt['status'],'literal_files':len(actual),'ZIP_members':len(member_rows)},indent=2))
