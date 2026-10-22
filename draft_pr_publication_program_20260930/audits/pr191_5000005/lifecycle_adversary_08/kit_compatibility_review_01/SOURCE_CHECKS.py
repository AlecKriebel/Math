"""Reproduce source-only checks: python3 -B SOURCE_CHECKS.py. No imports/execution of inputs."""
from pathlib import Path
import ast,hashlib,json
p=Path(__file__).resolve().parent
pins=json.loads((p/'INPUT_PINS.json').read_text())['inputs']
texts={}
for x in pins:
 f=Path(x['path']);b=f.read_bytes()
 assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
 assert format(f.stat().st_mode&0o777,'04o')==x['mode']
 texts[f.name]=b.decode();ast.parse(b.decode(),filename=str(f))
h=texts['publish_existing_draft_compatibility_01.py'];k=texts['zenodo.py'];c=texts['lifecycle_common.py']
assert "if command == \"inspect\":\n            sub.add_argument(\"--check-doi\"" in k
assert 'if command == "publish":\n            sub.add_argument("--confirm-id", type=int, required=True)' in k
assert k.index('args = parser.parse_args()')<k.index('print(json.dumps(run(args), indent=2))')
run=next(n for n in ast.parse(k).body if isinstance(n,ast.FunctionDef) and n.name=='run')
returns=[n.value for n in ast.walk(run) if isinstance(n,ast.Return) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='published_summary']
assert len(returns)==3 and sum(isinstance(v.args[-1],ast.Constant) and v.args[-1].value is True for v in returns)==2
calls=[n for n in ast.walk(ast.parse(h)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='kit_call']
assert len(calls)==2
assert any(n.args[1].value=='publish' and any(kw.arg=='check_doi' and isinstance(kw.value,ast.Constant) and kw.value.value is False for kw in n.keywords) for n in calls)
assert any(n.args[1].value=='inspect' and any(kw.arg=='check_doi' and isinstance(kw.value,ast.Constant) and kw.value.value is True for kw in n.keywords) for n in calls)
assert "with marker.open('x')" in h and "m.save_published(g,raw,'publish')" in h
assert "action=='inspect-published' or cmd=='publish'" in c and "if check_doi:args+=['--check-doi']" in c
original=p.parent;manifest=json.loads((original/'MANIFEST.json').read_text())
for n,x in manifest['files'].items():
 b=(original/n).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'] and (original/n).stat().st_mode&0o777==0o444
print('PASS: pinned source/AST checks; CLI compatibility and original frozen artifacts verified; input code execution=0.')
