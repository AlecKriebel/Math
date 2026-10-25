"""Read-only rehash of all fresh source assets and all safely extracted files."""
from pathlib import Path
import json,hashlib,datetime
here=Path(__file__).resolve().parent
paper=here.parents[2]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
bound=json.loads((here/'source-bindings.json').read_text())
rows=[]
for record in bound['sources']:
    receipt=paper/record['receipt_path']
    assert sha(receipt)==record['receipt_sha256'],receipt
    source=receipt.parent
    assert sha(source/'record.json')==record['record_sha256'],source
    for asset in record['assets']:
        p=source/asset['filename']; actual=sha(p)
        assert actual==asset['sha256'] and p.stat().st_size==asset['bytes'],p
        rows.append({'path':str(p.relative_to(paper)),'sha256':actual,'bytes':p.stat().st_size})
extracted=[]
for source in [paper/'sources',paper/'sources/related-record-22064121']:
    receipt=source/'extraction-integrity.json'; manifest=json.loads(receipt.read_text())
    for row in manifest['members']:
        relative=row['path']
        p=source/relative if relative.startswith('published-source/') else source/'published-source'/relative
        actual=sha(p)
        assert actual==row['sha256'] and p.stat().st_size==row['bytes'],p
        extracted.append({'path':str(p.relative_to(paper)),'sha256':actual})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','public_assets':len(rows),'extracted_regular_files':len(extracted),'all_original_bytes_unchanged':True,'assets':rows,'extracted':extracted}
(here/'final-custody.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['assets','extracted']}))
