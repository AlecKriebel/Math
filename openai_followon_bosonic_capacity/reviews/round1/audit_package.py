"""Independent clean candidate audit; writes only review-owned outputs."""
from pathlib import Path
import json, hashlib, zipfile, subprocess, datetime, shutil
root=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
extract=review/'extracted_kit'
extract.mkdir(exist_ok=True)
inv=json.loads((root/'publication/PACKAGE_INVENTORY.json').read_text())
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hashes':{},'checks':[]}
for x in inv['uploads']:
    raw=(root/x['path']).read_bytes()
    assert len(raw)==x['bytes']
    assert hashlib.sha256(raw).hexdigest()==x['sha256']
    assert hashlib.md5(raw).hexdigest()==x['md5']
    record['hashes'][x['path']]=x['sha256']
manifest_raw=(root/'zenodo-deposit.json').read_bytes()
assert hashlib.sha256(manifest_raw).hexdigest()==inv['manifest_sha256']
record['hashes']['zenodo-deposit.json']=inv['manifest_sha256']
with zipfile.ZipFile(root/'publication/zenodo-upload-kit.zip') as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))
    assert set(names)=={x['path'] for x in inv['source_files']}|{'SOURCE_INVENTORY.json'}
    assert json.loads(z.read('SOURCE_INVENTORY.json'))==inv['source_files']
    for x in inv['source_files']:
        raw=z.read(x['path'])
        assert len(raw)==x['bytes']
        assert hashlib.sha256(raw).hexdigest()==x['sha256']
        assert raw==(root/x['path']).read_bytes()
        assert not Path(x['path']).is_absolute() and '..' not in Path(x['path']).parts
        record['hashes'][x['path']]=x['sha256']
    z.extractall(extract)
commands=[['python3','code/verify_certificates.py'],['python3','notes/alternate_priority/repair_identity_audit/symbolic_checks.py'],['python3','notes/upstream_proof/check_interpolation.py'],['tectonic','--keep-logs','--outdir','manuscript','manuscript/main.tex'],['python3','code/build_package.py']]
for i,c in enumerate(commands):
    r=subprocess.run(c,cwd=extract,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (review/f'clean-command-{i+1}.txt').write_text(r.stdout)
    record['checks'].append({'argv':c,'returncode':r.returncode,'output':f'clean-command-{i+1}.txt'})
    assert r.returncode==0,(c,r.stdout)
oldtext=subprocess.check_output(['pdftotext','-layout',str(root/'publication/paper.pdf'),'-'])
newtext=subprocess.check_output(['pdftotext','-layout',str(extract/'manuscript/main.pdf'),'-'])
assert oldtext==newtext
assert (extract/'publication/zenodo-upload-kit.zip').read_bytes()==(root/'publication/zenodo-upload-kit.zip').read_bytes()
record.update({'zip_entries':len(names),'source_files':len(inv['source_files']),'pdf_text_identical':True,'reconstructed_zip_identical':True,'passed':True})
(review/'PACKAGE_AUDIT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['zip_entries','source_files','pdf_text_identical','reconstructed_zip_identical','passed']},indent=2))
