"""Change a real private output read in memory and run one target checker."""
from pathlib import Path
import json,runpy,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
rid,case=sys.argv[1:3];c=json.loads((R/'papers'/rid/'publication.json').read_text());article=O/'public/research'/c['slug']
rb,rt=Path.read_bytes,Path.read_text
if case=='missing_result':
    path=article/'index.html';data=rb(path)
    old=(b'every deterministic positive s_g' if rid=='23387774' else b'every subset J')
    if data.count(old)!=1:raise RuntimeError('expected_one_actual_public_token')
    data=data.replace(old,b'OMITTED_CLAIM_CONTROL',1)
elif case=='changed_complete_support':path=article/c['supplement_filename'];data=rb(path)+b'CHANGED_SUPPORT'
else:raise RuntimeError('unsupported_public_fault')
Path.read_bytes=lambda q:data if q==path else rb(q)
Path.read_text=lambda q,*a,**k:Path.read_bytes(q).decode(k.get('encoding') or 'utf-8')
sys.argv=[str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),rid,'--site',str(O/'public'),'--output-dir',str(O),'--output-stem','negative-public-'+rid+'-'+case]
runpy.run_path(str(O/'stage_reader.py'),run_name='__main__')
