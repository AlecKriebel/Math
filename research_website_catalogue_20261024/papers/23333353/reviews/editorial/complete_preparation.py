"""Resume only the object-copy/requirements tail after an authoring typo.

Initial preparation created complete configs and public copy before a Path
indexing typo stopped original-object copying. Preserve their existing bytes;
run only the corrected original tail, without reissuing config writes.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23333353';a=p/'reviews/editorial'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
now=lambda:datetime.now(timezone.utc).isoformat()
def dump(base,name,value):(base/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
rootfile=P/'verification/root-clearance-23333353-20261025.json';rootsha='9a277414cd2b4891af98abac570cc21eab2c9e35eb89d876ea7bc2d106bb7f8c'
assert sha(rootfile)==rootsha
root=json.loads(rootfile.read_text());pub=json.loads((p/'publication.json').read_text());prom=json.loads((p/'promotion.json').read_text());sb=pub['source_binding'];raw=json.loads((p/'sources/record.raw.json').read_text());md=raw['metadata']
before={str(f):sha(f) for f in [p/'publication.json',p/'promotion.json',a/'PUBLIC_COPY.md']}
source=(a/'prepare_editorial.py').read_text();tail='copies=[]\n'+source.split('\ncopies=[]\n',1)[1]
exec(compile(tail,str(a/'prepare_editorial.py')+':object-copy-tail','exec'),globals())
assert all(sha(f)==value for f,value in before.items())
dump(a,'PREPARATION_RESUME_RECEIPT.json',{'utc':now(),'initial_failure':'TypeError: PosixPath object is not subscriptable in original-object copy path expression; occurred after complete configs/public copy were written.','bounded_correction':'P[x.verdict] corrected to P/x.verdict; only the remaining object-copy/requirements tail executed.','existing_config_and_public_copy_hashes_unchanged':before,'source_or_earlier_artifact_mutation':False})
with (a/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — A local preparation path-expression typo stopped original-object copying after configs/prose were complete. Corrected once and resumed only the copy/requirements tail; preexisting generated config/prose bytes verified unchanged. No source, scientific or prior packet changed. Completion estimate85%.\n')
