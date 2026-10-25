"""Bind the review to primary source bytes without opening other review opinions."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, zipfile

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parent.parent
SOURCES = PAPER/'sources'
PREFIX = 'AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor/'
WORK = SOURCES/'published-source'/PREFIX
RELEASE = WORK/'releases/v2.0'

def dig(path, algo='sha256'):
    h = hashlib.new(algo)
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

receipt = json.loads((SOURCES/'receipt.json').read_text())
assert receipt['record_id'] == '21753997' and receipt['complete']
asset = receipt['files'][0]
archive = SOURCES/asset['name']
assert archive.stat().st_size == asset['bytes']
assert dig(archive) == asset['sha256']
assert dig(archive, 'md5') == asset['md5']
assert dig(SOURCES/'record.json') == receipt['record_sha256']
checked = []
with zipfile.ZipFile(archive) as z:
    for name in z.namelist():
        if name.startswith(PREFIX) and not name.endswith('/'):
            raw = z.read(name)
            local = SOURCES/'published-source'/name
            expected = hashlib.sha256(raw).hexdigest()
            assert local.exists() and dig(local) == expected
            checked.append({'member': name, 'bytes': len(raw), 'sha256': expected})
assert len(checked) == 126

reader = []
for name in receipt['archives'][0]['reader_pdf_members']:
    p = SOURCES/'published-source'/name
    reader.append({'member': name, 'bytes': p.stat().st_size, 'sha256': dig(p)})
main = RELEASE/'output/pdf/manuscript-v2.0.0.pdf'
assert dig(main) == 'fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b'
initial = json.loads((ROOT/'submitted-replay-inputs.json').read_text())
# The complete selected-member comparison above also confirms every replay
# source remains identical to its published ZIP member after isolated replay.
primaryreceipt = PAPER/'reviews/scope/primary_source_receipts.json'
rawprimary = json.loads(primaryreceipt.read_text())
for filename, expected in [
    ('boros-craciun-yu.pdf','e63bdc76a0d3f712c8e0b54f527a8f8a1e9969930248db7527b8c91abe0fcace'),
    ('feliu-henriksson-pascual-escudero.pdf','fb711f96966a225b12a49ce1f130a89e000c9d2e7d54becf6cf7158865927a54')
]:
    assert dig(PAPER/'reviews/scope/.reference-cache'/filename) == expected
ownfiles = {}
for p in sorted(ROOT.iterdir()):
    if p.is_file() and p.name not in {'evidence-bindings.json','verdict.json','RESEARCH_LOG.md'}:
        ownfiles[p.name] = {'bytes': p.stat().st_size, 'sha256': dig(p)}
out = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'record_id': '21753997', 'record_url': 'https://zenodo.org/records/21753997',
    'source_receipt_sha256': dig(SOURCES/'receipt.json'),
    'record_sha256': dig(SOURCES/'record.json'),
    'public_asset': asset,
    'main_pdf': {'path': str(main), 'sha256': dig(main), 'pages': 14},
    'current_manuscript_source': {'path': str(RELEASE/'source/MANUSCRIPT_V2.md'), 'sha256': dig(RELEASE/'source/MANUSCRIPT_V2.md')},
    'reader_pdf_members': reader,
    'source_integrity': {'selected_file_count':126,'all_selected_members_equal_authenticated_zip':True,'members':checked},
    'primary_receipt': {'path':str(primaryreceipt),'sha256':dig(primaryreceipt),'contents':rawprimary},
    'review_artifacts': ownfiles
}
(ROOT/'evidence-bindings.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({'selected_source_files_unchanged':126,'main_sha256':dig(main),'evidence_sha256':dig(ROOT/'evidence-bindings.json')}))
