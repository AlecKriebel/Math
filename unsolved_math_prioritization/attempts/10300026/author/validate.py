"""Validate bounded public metadata, not mathematical correctness."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: invoke through isolated bootstrap')
import json
from pathlib import Path
root = Path(__file__).resolve().parent
status = json.loads((root / 'STATUS.json').read_text(encoding='utf-8'))
if status['problem_id'] != 10300026 or status['problem_number'] != 'AMR-102-0026':
    raise SystemExit('REJECT: wrong problem identity')
if status['status'] != 'UNRESOLVED_IN_THIS_AUDIT':
    raise SystemExit('REJECT: disposition changed')
if status['full_solution'] is not False or status['new_mathematical_result_claimed'] is not False:
    raise SystemExit('REJECT: unsupported success claim')
if status['substantive_approaches'] != 4 or status['independent_audit_status'] != 'PENDING':
    raise SystemExit('REJECT: accounting changed')
metadata = json.loads((root / 'VERIFICATION_METADATA.json').read_text(encoding='utf-8'))
if metadata['statement_sha256'] != 'df1623ec850b43d288ee3b733ef4c0108852280687e2cd09c89c79a18659b6df':
    raise SystemExit('REJECT: statement digest')
if metadata['review_sha256'] != 'd539a48fb43e8d346651b0e11607b0e6315c856cdaec3d0d156d348c4d77aca2':
    raise SystemExit('REJECT: review digest')
if not metadata['statement_match'] or not metadata['review_match']:
    raise SystemExit('REJECT: input mismatch')
print(json.dumps({'metadata_validation': 'PASS', 'problem_id': 10300026, 'mathematical_proof_checked': False, 'full_solution': False}, sort_keys=True))
