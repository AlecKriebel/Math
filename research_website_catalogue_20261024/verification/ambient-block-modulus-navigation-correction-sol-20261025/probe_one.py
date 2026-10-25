"""One target checker execution using an unchanged retained HTML read override.

Writes only this correction namespace; no original/fixture HTML is written.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import builtins,io,json,hashlib,runpy
R=Path(__file__).resolve().parent;P=R.parents[1]
S=P/'verification/local-ambient-block-modulus-stage-sol-20261025'
A=P/'verification/audit-ambient-block-modulus-code-sol-20261025'
rid,case,mode=sys.argv[1:4]
if rid not in ['23333353','23416806','23441617'] or case not in ['pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href'] or mode not in ['normal','optimized']:
 raise ValueError('only exact retained target controls authorized')
c=json.loads((P/'papers'/rid/'publication.json').read_text())
target=S/'public/research'/c['slug']/'index.html';original=target.read_bytes()
if case=='pristine':changed=original;sample=None
else:
 sample=A/'navigation-fault-samples'/f'{rid}-{case}.html';changed=sample.read_bytes()
 retained=json.loads((A/'mutations'/f'{rid}-{case}-{mode}.json').read_text())
 if hashlib.sha256(changed).hexdigest()!=retained['changed_read_SHA256'] or hashlib.sha256(original).hexdigest()!=retained['original_SHA256'] or changed==original:
  raise RuntimeError('retained exact original/fault identity mismatch')
(R/'read-overrides').mkdir(exist_ok=True)
(R/'read-overrides'/f'{rid}-{case}-{mode}.json').write_text(json.dumps({'record_id':rid,'case':case,'mode':mode,
 'actual_HTML_target':str(target),'original_sha256':hashlib.sha256(original).hexdigest(),
 'exact_read_bytes_sha256':hashlib.sha256(changed).hexdigest(),'retained_sample':str(sample) if sample else None,
 'sample_matches_original_audit_changed_read_receipt':case!='pristine','in_memory_only':True},indent=2)+'\n')
rb,rt=Path.read_bytes,Path.read_text
Path.read_bytes=lambda p:changed if p==target else rb(p)
Path.read_text=lambda p,*a,**k:Path.read_bytes(p).decode(k.get('encoding') or 'utf-8')
sys.path[:0]=[str(S),str(P/'scripts')]
sys.argv=[str(S/'stage_reader.py'),str(R/'final-content-check.stage.py'),rid,'--site',str(S/'public'),
 '--output-dir',str(R/'qa'/mode),'--output-stem',rid+'-'+case]
real_open=builtins.open
def guarded(file,mode='r',*a,**k):
 if any(x in mode for x in 'wax+') and isinstance(file,(str,bytes,Path)):
  if not Path(file).resolve().is_relative_to(R):raise RuntimeError('write outside correction namespace:'+str(file))
 return real_open(file,mode,*a,**k)
builtins.open=guarded;io.open=guarded
runpy.run_path(str(S/'stage_reader.py'),run_name='__main__')
