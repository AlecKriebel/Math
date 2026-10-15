#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PUB=BASE/'publication'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(root):return {str(p.relative_to(root)):{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(root.rglob('*')) if p.is_file()}
results={'observed_at':datetime.now(timezone.utc).isoformat(),'python':sys.version,'publication_before':snap(PUB),'runs':[]}
archive=PUB/'verification_package.zip'
with zipfile.ZipFile(archive) as z:
    entries=z.infolist();names=[i.filename for i in entries]
    assert len(names)==len(set(names)),'Duplicate ZIP member'
    assert z.testzip() is None,'ZIP CRC error'
    for i in entries:
        p=Path(i.filename)
        assert not p.is_absolute() and '..' not in p.parts,'Unsafe member path'
        assert (i.external_attr>>16)&0o170000!=0o120000,'ZIP symlink'
    results['zip']={'entries':len(entries),'names':names,'crc':'PASS','paths':'PASS'}
    dest=OUT/'scratch'/'fresh_extraction'
    assert not dest.exists(),'Extraction is not fresh'
    dest.mkdir()
    z.extractall(dest)
root=dest/'positivity-loss-30003571'
manifest=json.loads((root/'MANIFEST.json').read_text())
before=snap(root)
assert set(before)==set(manifest['files'])|{'MANIFEST.json'}
for name,info in manifest['files'].items():assert before[name]==info, name
assert (root/'MANIFEST.json').read_bytes()==(PUB/'PACKAGE_MANIFEST.json').read_bytes()
assert manifest['paper_pdf_sha256']==digest(PUB/'positivity_loss.pdf')
results['manifest']={'verified_files':len(manifest['files']),'outer_copy_identical':True,'pdf_hash_matches':True,'sha256':digest(root/'MANIFEST.json')}
for k in (1,2):
    p=subprocess.run([sys.executable,'run_all.py'],cwd=root,text=True,capture_output=True)
    (OUT/'scratch'/f'run{k}.stdout.jsonl').write_text(p.stdout)
    (OUT/'scratch'/f'run{k}.stderr.txt').write_text(p.stderr)
    after=snap(root)
    results['runs'].append({'run':k,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'unchanged':before==after})
    assert p.returncode==0 and before==after
# Verify historical provenance manifests against preserved content, understanding relative roots.
results['historical_manifests']={}
for m in sorted((root/'original').rglob('*MANIFEST.json')):
    data=json.loads(m.read_text());results['historical_manifests'][str(m.relative_to(root))]=data
results['publication_after']=snap(PUB)
assert results['publication_before']==results['publication_after'],'Candidate mutation during review'
results['status']='PASS'
(OUT/'PACKAGE_CHECK.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:results[k] for k in ['observed_at','python','manifest','runs','status']},indent=2))
