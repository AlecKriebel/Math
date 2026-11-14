from pathlib import Path
import json,hashlib,shutil
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');E=P/'verification/local-banach-mtp2-stage-sol-20261025';PL=P/'verification/banach-mtp2-next-stage-plan-sol-20261025'
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(E/'inputs').mkdir(exist_ok=True)
for src,dst,pin in [(P/'scripts/render_page.py',E/'inputs/render_page.py','be622123717473cf174c10bfe22b254cb5d57abff9d0e192d15e3c87206ec85f'),(P/'verification/final-content-check.py',E/'inputs/final-content-check.py','f743459809e21a8a590a368c52585023c5bf16f77ddac4f21879fa9bbb7daffb')]:
 if H(src)!=pin:raise ValueError('fresh installed pin changed')
 if dst.exists():raise ValueError('no overwrite')
 dst.write_bytes(src.read_bytes())
for name in ['execute.py','stage_reader.py']:
 src=P/'verification/local-odd-ear-blocking-stage-sol-20261025'/name
 (E/name).write_bytes(src.read_bytes())
# Pinned constants are built only from the two separately authenticated, read approvals.
pins={}
for rid in ['23217863','23146753']:
 q=P/'papers'/rid;c=json.loads((q/'publication.json').read_text());b=c['source_binding']
 ed=q/'reviews/editorial';science=P/'verification'/f'root-clearance-{rid}-20261025.json';authority=P/'verification'/f'root-editorial-{rid}-20261025.json'
 pins[rid]={'publication':H(q/'publication.json'),'promotion':H(q/'promotion.json'),'science':H(science),'editorial':H(authority),'editorial_manifest':H(ed/'MANIFEST.json'),'editorial_seal':H(ed/'SEAL.json'),'public_copy':H(ed/'PUBLIC_COPY.md'),'source_pins':{f.name:H(f) for f in sorted((q/'sources').glob('SOURCE_*.json'))},'inventory':H(q/'sources/archive-members.json'),'raw_metadata_keys':list(json.loads((q/b['raw_record_path']).read_text())['metadata'])}
(E/'helper_constants.json').write_text(json.dumps(pins,indent=2)+'\n')
# Freeze current original input bindings from the already sealed planning packet; no mutable legacy snapshots followed.
x=json.loads((PL/'IMMUTABLE_INPUT_BINDINGS.json').read_text());print('binding schema',type(x),list(x) if isinstance(x,dict) else len(x))
(E/'PROTECTED_PLAN_MANIFEST.json').write_text(json.dumps({'plan_seal':{'path':str(PL/'SEAL.json'),'sha256':H(PL/'SEAL.json')},'plan_manifest':{'path':str(PL/'MANIFEST.json'),'sha256':H(PL/'MANIFEST.json')},'original_bindings_file':{'path':str(PL/'IMMUTABLE_INPUT_BINDINGS.json'),'sha256':H(PL/'IMMUTABLE_INPUT_BINDINGS.json')}},indent=2)+'\n')
print('private code inputs and constants prepared')
