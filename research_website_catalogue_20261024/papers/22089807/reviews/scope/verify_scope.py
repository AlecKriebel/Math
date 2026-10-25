from pathlib import Path
import json,hashlib,re,unicodedata
b=Path(__file__).resolve().parents[2];s=b/'reviews/scope';src=b/'sources'
receipt=json.load(open(src/'receipt.json'));queue=json.load(open(src/'queue-entry.json'));record=json.load(open(src/'record.json'))
assert record['id']==queue['record_id']==22089807
assert record['metadata']['version']==queue['version']=='2.0.4'
assert record['metadata']['publication_date']==queue['publication_date']=='2026-08-25'
assert record['doi']==queue['doi']=='10.5281/zenodo.22089807'
for f in receipt['files']:
 d=(src/f['name']).read_bytes();assert len(d)==f['bytes'];assert hashlib.sha256(d).hexdigest()==f['sha256'];alg,digest=f['zenodo_checksum'].split(':');assert hashlib.new(alg,d).hexdigest()==digest
assert len(receipt['files'])==2
outer=json.load(open(s/'archive_inventory.json'));support=json.load(open(s/'support_read_ledger.json'));nested=json.load(open(s/'nested_member_inventory.json'));readers=json.load(open(s/'reader_asset_ledger.json'))
assert len(outer)==len(support)==23 and len(nested)==1662 and len(readers)==2
assert {x['name'] for x in outer}=={x['name'] for x in support}
assert all(x['read_extent'] for x in support)
assert not any(x['hidden'] or x['pdf_magic'] or x['container_magic'] for x in nested)
content=json.load(open(s/'content.json'));verdict=json.load(open(s/'verdict.json'));assert content['follow_up'] is None and verdict['follow_up'] is None
assert content['held_candidate'] and verdict['promotion_authorized'] is False
tex=next((src/'published-source').rglob('main.tex')).read_text();abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
repl={'\\Rsim':'R_sim','\\Rhyb':'R_hyb','\\sigma':'σ','\\lambda':'λ','\\in':'∈','\\geq':'≥','\\ldots':'…'}
for a,v in repl.items():abstract=abstract.replace(a,v)
abstract=abstract.replace('\\[','').replace('\\]','')
def normal(x):return ''.join(c for c in unicodedata.normalize('NFKC',x) if c.isalnum()).lower()
assert normal(abstract)==normal(content['abstract']),(normal(abstract),normal(content['abstract']))
assert not re.search(r'\\(?:input|include)\{',tex)
for p in s.glob('*.json'):json.loads(p.read_text())
print('PASS scope acquisition binding, exhaustive ledger coverage, complete abstract fidelity, held gate, JSON consistency')
