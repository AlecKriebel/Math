#!/usr/bin/env python3
"""Record consumed file inputs and final outputs; no Git or service operations."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import platform
import sys

root=Path(__file__).resolve().parent
original=root.parent/'original_submission/files/unsolved_math_prioritization/attempts/30000229'
now=datetime.now(timezone.utc).isoformat()

def entry(path,role):
    path=Path(path).absolute()
    data=path.read_bytes()
    return {'path':str(path),'role':role,'bytes':len(data),'sha256':sha256(data).hexdigest()}

inputs=[]
for name in ('COUNTEREXAMPLE.md','verify.py','source_record.json','README.md'):
    inputs.append(entry(original/name,'original candidate read; checker inspected but not executed'))
for name in ('REVIEW.md','independent_checks.py'):
    inputs.append(entry(original/'independent_review'/name,'historical comparison only; opened after independent checkpoint; not executed'))
inputs.append(entry('/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1009.11318/skills/pdf/SKILL.md','read-only PDF skill instructions'))
for path in sorted((root/'sources').iterdir()):
    inputs.append(entry(path,'downloaded primary source or extracted/rendered source page used in inspection'))
inputs.append(entry(sys.executable,'standard-library exact checker Python executable'))
inputs.append(entry('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3','bundled Python executable used for PDF extraction'))
inputs.append(entry('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/bin/pdftoppm','PDF page rendering executable'))
manifest={'recorded_at_utc':now,'cwd':str(root),'scope':'All consumed on-disk original, historical, source, rendered-page, skill and executable inputs. The shared conversation/environment and tool documentation are not represented as files.','inputs':inputs,'source_receipts':'SOURCE_RECEIPTS.json'}
(root/'INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
runtime={'recorded_at_utc':now,'python_executable':sys.executable,'python_version':sys.version,'platform':platform.platform(),'normal_replay':'python3 exact_mesh_checks.py --output exact_mesh_results.json > exact_mesh_stdout.json','optimized_replay':'python3 -O exact_mesh_checks.py --output exact_mesh_results_optimized.json > exact_mesh_stdout_optimized.json','exit_codes':{'ordinary':0,'optimized':0},'mutations_outside_audit_directory':False,'git_or_service_mutations':False,'external_individual_communications':False}
(root/'RUNTIME_RECEIPT.json').write_text(json.dumps(runtime,indent=2)+'\n')
outputs=[]
for path in sorted(root.rglob('*')):
    if path.is_file() and path.name!='OUTPUT_MANIFEST.json':
        e=entry(path,'audit output');e['relative_path']=str(path.relative_to(root));outputs.append(e)
out={'recorded_at_utc':now,'root':str(root),'self_hash_exclusion':'OUTPUT_MANIFEST.json is excluded from its own list to avoid a recursive digest. All other final on-disk outputs, including INPUT_MANIFEST.json, are listed.','outputs':outputs}
(root/'OUTPUT_MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
for e in outputs:
    p=Path(e['path'])
    if sha256(p.read_bytes()).hexdigest()!=e['sha256']:raise ValueError('Output changed while manifesting: '+str(p))
print(json.dumps({'status':'PASS','input_files':len(inputs),'output_files':len(outputs),'root':str(root)}))
