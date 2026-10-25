from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, zipfile

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'sources'
def h(path,algo='sha256'):
    return hashlib.new(algo,path.read_bytes()).hexdigest()
receipt=json.loads((SOURCE/'receipt.json').read_text())
assert receipt['complete']
for asset in receipt['files']:
    p=SOURCE/asset['name']
    assert p.stat().st_size==asset['bytes'] and h(p)==asset['sha256'] and h(p,'md5')==asset['md5']
assert h(SOURCE/'record.json')==receipt['record_sha256']
checked=[]
with zipfile.ZipFile(SOURCE/'pr1098_support_v1_0.zip') as z:
    for name in z.namelist():
        if name.endswith('/'):continue
        raw=z.read(name);p=SOURCE/'published-source'/name
        expected=hashlib.sha256(raw).hexdigest()
        assert h(p)==expected
        checked.append({'member':name,'bytes':len(raw),'sha256':expected})
assert len(checked)==124
artifacts={p.name:{'bytes':p.stat().st_size,'sha256':h(p)} for p in sorted(ROOT.iterdir())
           if p.is_file() and p.name not in {'evidence-bindings.json','verdict.json','RESEARCH_LOG.md'}}
out={'created_utc':datetime.now(timezone.utc).isoformat(),'record_id':'23431716',
     'source_receipt_sha256':h(SOURCE/'receipt.json'),'record_sha256':h(SOURCE/'record.json'),
     'source_assets':receipt['files'],'manuscript_source_sha256':h(SOURCE/'published-source/paper.tex'),
     'all_published_files_unchanged':True,'archive_member_count':124,'archive_member_bindings':checked,
     'artifacts':artifacts}
(ROOT/'evidence-bindings.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all124sourcefilesunchanged':True,'report_sha256':h(ROOT/'REVIEW.md'),'evidence_sha256':h(ROOT/'evidence-bindings.json')}))
