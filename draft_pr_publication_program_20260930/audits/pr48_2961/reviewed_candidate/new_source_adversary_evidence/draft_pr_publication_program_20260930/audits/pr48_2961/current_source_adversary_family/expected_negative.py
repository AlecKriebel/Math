"""Intentional private control: treating genuine Git null-source as a helper must fail."""
import json
from pathlib import Path
F=Path(__file__).absolute().parent
r=json.loads((F.parent/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json').read_bytes())
c=r['complete_actual_Git_captures'][0]
assert c['schema']=='pr48-root-readonly-git-actual-capture/v1' and c['source'] is None and c['source_unchanged'] is None
print('INTENTIONAL NEGATIVE: genuine Git source=None is not a typed historical helper source; private substituted helper interpretation must exit1.',flush=True)
if type(c['source']) is not dict:raise ValueError('Expected rejection: substituted helper needs typed source and source_unchanged=True')
raise RuntimeError('Negative control unexpectedly accepted')
