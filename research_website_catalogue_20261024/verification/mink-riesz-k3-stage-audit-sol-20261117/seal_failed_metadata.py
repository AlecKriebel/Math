"""Finite metadata seal for the closed failed audit, without rerunning its reader."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-stage-audit-sol-20261117')

def stamp():
    return datetime.now(timezone.utc).isoformat()

def pin(p):
    st = p.lstat()
    assert stat.S_ISREG(st.st_mode)
    b = p.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest(), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def put(name, obj):
    (A / name).write_text(json.dumps(obj, indent=2) + '\n')

def main():
    assert Path(__file__).resolve() == A / 'seal_failed_metadata.py'
    assert not (A / 'FINAL.json').exists() and not (A / 'MANIFEST.json').exists()
    started = stamp()
    inputs = json.loads((A / 'CLOSURE_INPUTS.json').read_text())
    assert all(pin(A / r) == v for r, v in inputs['original_failed_files'].items())
    result = json.loads((A / 'CLOSURE_RESULT.json').read_text())
    assert result['original_audit_exit'] == 1 and result['original_audit_completion_percent'] == 60
    assert result['all_original_and_protected_inputs_stage_native_public_before_after_exact']
    assert json.loads((A / 'CLOSURE_EXECUTION.json').read_text())['exit_code'] == 0
    assert (A / 'CLOSURE.stdout.txt').read_bytes() == (A / 'CLOSURE.stderr.txt').read_bytes() == b''
    assert (A / 'SEAL.stdout.txt').read_bytes() == (A / 'SEAL.stderr.txt').read_bytes() == b''
    assert not (A / 'SEAL_EXECUTION.json').exists()
    put('SEAL_EXECUTION.json', {'schema': 'single-failed-audit-metadata-seal-normal-completion-v1',
        'UTC_start': started, 'UTC_data_end': stamp(), 'invocations': 1,
        'exit_code_at_normal_completion': 0, 'external_tool_exit_observation_required': True,
        'original_audit_exit_remains': 1, 'coverage_percent_remains': 60,
        'original_reader_or_producer_execution': False, 'follow_up': None})
    (A / 'MANIFEST.json').write_bytes(b'')
    (A / 'FINAL.json').write_bytes(b'')
    rows, dirs = [], []
    def hidden(r):
        return any(x.startswith('.') for x in Path(r).parts if x != '.')
    def walk(p):
        st = p.lstat()
        assert stat.S_ISDIR(st.st_mode)
        children = sorted(p.iterdir(), key=lambda x: x.name)
        rel = p.relative_to(A).as_posix()
        dirs.append({'path': rel, 'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children, 'hidden': hidden(rel)})
        for c in children:
            if stat.S_ISDIR(c.lstat().st_mode):
                walk(c)
            else:
                assert stat.S_ISREG(c.lstat().st_mode)
                r = c.relative_to(A).as_posix()
                if r in ['MANIFEST.json', 'FINAL.json']:
                    continue
                v = pin(c)
                rows.append({'path': r, **v, 'empty': v['bytes'] == 0, 'hidden': hidden(r)})
    walk(A)
    assert len(dirs) == 1 and dirs[0]['path'] == '.'
    manifest = {'schema': 'finite-original-failed-stage-audit-manifest-v1', 'UTC': stamp(), 'root': str(A),
        'regular_files': len(rows) + 2, 'child_directories': len(dirs) - 1, 'payload_files': rows, 'directories': dirs,
        'exact_already_created_terminal_recursive_hash_exclusions': ['MANIFEST.json', 'FINAL.json'],
        'terminal_modes': {x: pin(A / x)['mode'] for x in ['MANIFEST.json', 'FINAL.json']},
        'other_exclusions': [], 'all_hidden_empty_ignored_modes_and_topology_included': True,
        'external_terminal_pins_required': True}
    put('MANIFEST.json', manifest)
    put('FINAL.json', {'schema': 'original-failed-stage-audit-truthful-final-v1', 'UTC': stamp(),
        'status': 'ORIGINAL_AUDIT_FAILED_CUSTODY_CLOSED_FROZEN', 'original_audit_exit': 1,
        'completion_percent_assigned_original_audit_only': 60, 'original_failure_line': 316,
        'original_reader': pin(A / 'audit_private.py'), 'literal_stderr': pin(A / 'AUDIT.stderr.txt'),
        'distinct_closing_guard_exit': 0, 'all_original_nine_files_and_protected_inputs_exact': True,
        'root_diagnosis': result['root_diagnosis'], 'manifest': pin(A / 'MANIFEST.json'),
        'regular_files': len(rows) + 2, 'child_directories': len(dirs) - 1, 'root_mode': dirs[0]['mode'],
        'original_audit_rerun_or_repair': False, 'producer_or_science_execution': False,
        'no_PASS_retroclaim': True, 'follow_up': None, 'AA': None, 'actual_publication_date': None,
        'actual_UI_live_production_or_future_action_authority': False, 'frozen': True})

if __name__ == '__main__':
    main()
