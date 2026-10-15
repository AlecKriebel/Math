"""Freeze a final source pin receipt and syntax-check without integration.

Writes only its own FINAL_SOURCE_PINS.json. This is not ROOT approval.
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

def main():
    own = Path(__file__).resolve().parent
    out = own / 'FINAL_SOURCE_PINS.json'
    if out.exists(): raise RuntimeError('Final source receipt already exists; preserve it')
    entries = []
    for name in ('.gitignore', 'inspect_readonly.py', 'integrate_attributed_prior_result.py',
                 'prepare_source_bindings.py', 'SOURCE_BINDINGS.json', 'READONLY_INSPECTION.json',
                 'SYNTAX_CHECK.json', 'REPORT.md', 'HELPER_INTERFACE.md', 'RESEARCH_LOG.md', 'finalize_source_packet.py'):
        p = own / name
        b = p.read_bytes()
        if name.endswith('.py'): compile(b, str(p), 'exec')
        entries.append({'path': name, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                        'in_memory_syntax_compile_passed': True if name.endswith('.py') else None})
    value = {'schema': 'pr55-partial-integration-operation-final-source-pins/v1',
             'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_finalizer_pid': os.getpid(),
             'source_only': True, 'integration_helper_executed': False, 'ROOT_disposition_authority': False,
             'Git_native_PR_paper_Zenodo_DOI_tracker_mutation': False, 'new_central_proof_attempts': 0,
             'operational_SOURCE_preparation_percent': 100, 'integration_operations_by_this_agent_percent': 0,
             'original_target_novel_discovery_percent': 0, 'dated_program_percent': 4.040404, 'files': entries}
    out.write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(value, indent=2))

if __name__ == '__main__': main()
