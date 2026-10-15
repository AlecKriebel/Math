"""Review3 one-read frozen inputs; never performs a network operation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, os, zipfile, io, struct

ROOT=Path('/Users/alec/Documents/Math')
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
AUTHOR=AUDIT/'reviews/native_transport_author'
SNAP=HERE/'tmp/inputs'
def pin(data): return {'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
gate_data=(AUDIT/'FINAL_PUBLICATION_GATE.json').read_bytes()
gate=json.loads(gate_data)
paths=[AUDIT/'FINAL_PUBLICATION_GATE.json',ROOT/'zenodo_deposit_tool/zenodo.py']
paths += [p for p in AUTHOR.iterdir() if p.is_file()]
paths += [AUDIT/n for n in gate['reviewed_inputs']]
paths += [AUDIT/n for n in gate['final_repair_pins']]
paths += [AUDIT/n for n in ['NATIVE_PUBLISHED_API_CALIBRATION.json','NATIVE_PUBLISHED_CONTENT_CALIBRATION.json','NATIVE_PUBLISHED_CONTENT_WILDCARD_CALIBRATION.json','NATIVE_PUBLISHED_FILE_COLLECTION_CALIBRATION.json']]
paths += [AUDIT/'reviews/native_transport_review2'/n for n in ['FINDINGS.md','VERDICT.json','INPUT_BINDING.json','FINAL_INPUT_RECHECK.json','reproduce_f5.py','FILE_LINK_PRIMARY_BINDING.json','PRIMARY_PID_DEDUCTION.md','PRIMARY_SOURCE_BINDING.json','NEW_CALIBRATION_BINDING.json']]
captured={}
for path in dict.fromkeys(paths):
    data=gate_data if path==AUDIT/'FINAL_PUBLICATION_GATE.json' else path.read_bytes()
    rel=str(path.relative_to(ROOT)); saved=SNAP/rel
    saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(data)
    captured[rel]=pin(data)
checks={rel:captured[str((AUDIT/rel).relative_to(ROOT))]==value for rel,value in gate['reviewed_inputs'].items()}
if len(checks)!=45 or not all(checks.values()): raise RuntimeError('Accepted gate drift')
author_receipt=json.loads((AUTHOR/'AUTHOR_RECEIPT.json').read_bytes())
for rel,value in author_receipt['review_files'].items():
    if captured[str((AUTHOR/rel).relative_to(ROOT))]!=value: raise RuntimeError('Author input drift: '+rel)
if captured[str((AUTHOR/'native_transport.py').relative_to(ROOT))]['sha256']!='954d909ee6a8388c36d93bfa74387b24e9383a90c113d6f8eece89a0fa54f32b': raise RuntimeError('Adapter not assigned SHA')
if captured[str((AUTHOR/'run_native_transport.py').relative_to(ROOT))]['sha256']!='16ac53b7127971de17c0948783fbc23ccc6854c7720e7e63cbd585305df7bf3b': raise RuntimeError('Bootstrap not assigned SHA')
report={'captured_utc':datetime.now(timezone.utc).isoformat(),'inputs':captured,'gate45':checks,'gate45_match':all(checks.values()),'native29_count':sum(n.startswith('native/') for n in checks),'live_writes':0}
(HERE/'INPUT_BINDING.json').write_text(json.dumps(report,indent=2)+'\n')
(HERE/'RESEARCH_LOG.md').write_text('# Native transport review3 research log\n\n'+report['captured_utc']+' — Captured '+str(len(captured))+' inputs. All 45 accepted publication pins and author freeze match. Review completion estimate: 15%; operational readiness estimate: 80%, with no live lifecycle established. No shared reviewed source changed.\n')
print(json.dumps({'captured':len(captured),'gate45_match':all(checks.values()),'native29':report['native29_count']}))
