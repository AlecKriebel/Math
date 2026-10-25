"""Read-only reproducibility check for the proposed generated helper."""
from pathlib import Path
import ast,json,pprint,hashlib
O=Path(__file__).resolve().parent;P=O.parents[1]
pins=json.loads((O/'INPUT_PINS.json').read_text())['target_pins']
norm={r:json.loads((P/'papers'/r/'publication.json').read_text())['source_binding']['abstract_normalization']['exact_presentational_replacements'] for r in pins}
math=json.loads((O/'BODY_MATH_MAP.json').read_text())
source=(O/'spanning_sos_gin_source.template.py').read_text()
for old,value in [('__PIN_LITERAL__',pins),('__NORMALIZATION_LITERAL__',norm),('__MATH_LITERAL__',math)]:source=source.replace(old,pprint.pformat(value,width=110,sort_dicts=False))
ast.parse(source)
if source!=(O/'spanning_sos_gin_source.py').read_text():raise RuntimeError('generated_helper_not_identical')
print(json.dumps({'status':'PASS_READ_ONLY_HELPER_REPRODUCTION','SHA256':hashlib.sha256(source.encode()).hexdigest(),'writes':0}))
