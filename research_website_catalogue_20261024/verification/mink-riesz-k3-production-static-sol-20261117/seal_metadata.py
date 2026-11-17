"""Finite metadata seal only; this audit rejects execution of the original helper."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-production-static-sol-20261117')

def now():
    return datetime.now(timezone.utc).isoformat()

def load(name):
    return json.loads((A / name).read_text())

def pin(path):
    st = path.lstat()
    assert stat.S_ISREG(st.st_mode)
    b = path.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest(), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def put(name, obj):
    (A / name).write_text(json.dumps(obj, indent=2) + '\n')

def main():
    assert Path(__file__).resolve() == A / 'seal_metadata.py'
    assert not (A / 'FINAL.json').exists() and not (A / 'MANIFEST.json').exists()
    started = now()
    result, execution = load('CUSTODY_RESULT.json'), load('EXECUTION.json')
    assert result['status'] == 'CUSTODY_EXACT_HELPER_REMAINS_UNFIT_FOR_EXECUTION'
    assert result['complete_before_after_exact'] and result['runtime_absent']
    assert execution['invocations'] == 1 and execution['exit_code'] == 0
    assert execution['production_helper_invocations_import_AST_compile_help_or_tests'] == 0
    assert pin(A / 'capture_custody.py') == {'bytes': 10531, 'SHA256': 'cf726d598d399cd1796d28c0849ce6d44989857f4b0c18d48e312e6a86290722', 'mode': '0644'}
    assert (A / 'CUSTODY.stdout.txt').read_bytes() == (A / 'CUSTODY.stderr.txt').read_bytes() == b''
    assert (A / 'SEAL.stdout.txt').read_bytes() == (A / 'SEAL.stderr.txt').read_bytes() == b''
    before, after = load('BEFORE.json'), load('AFTER.json')
    assert {k: v for k, v in before.items() if k != 'UTC'} == {k: v for k, v in after.items() if k != 'UTC'}
    assert 'EVERY opaque Git call, including successful calls' in (A / 'FINDINGS.md').read_text()
    assert 'UNFIT_FOR_EXECUTION' in (A / 'REPORT.md').read_text()
    existing = {p.name: pin(p) for p in sorted(A.iterdir())}
    assert 'SEAL_EXECUTION.json' not in existing
    put('SEAL_EXECUTION.json', {'schema': 'independent-production-static-metadata-normal-completion-v1',
        'UTC_start': started, 'UTC_data_end': now(), 'invocations': 1, 'exit_code_at_normal_completion': 0,
        'external_tool_exit_observation_required': True, 'production_helper_execution': False,
        'helper_disposition': 'UNFIT_FOR_EXECUTION', 'follow_up': None})
    (A / 'MANIFEST.json').write_bytes(b'')
    (A / 'FINAL.json').write_bytes(b'')
    rows, dirs, seen = [], [], set()
    def hidden(r):
        return any(x.startswith('.') for x in Path(r).parts if x != '.')
    def walk(path):
        st = path.lstat()
        assert stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen
        seen.add((st.st_dev, st.st_ino))
        children = sorted(path.iterdir(), key=lambda p: p.name)
        r = path.relative_to(A).as_posix()
        dirs.append({'path': r, 'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children, 'hidden': hidden(r)})
        for child in children:
            st = child.lstat()
            if stat.S_ISDIR(st.st_mode):
                walk(child)
            else:
                assert stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen
                seen.add((st.st_dev, st.st_ino))
                r = child.relative_to(A).as_posix()
                if r not in ['FINAL.json', 'MANIFEST.json']:
                    v = pin(child)
                    rows.append({'path': r, **v, 'empty': v['bytes'] == 0, 'hidden': hidden(r)})
    walk(A)
    assert len(dirs) == 1 and all(pin(A / r) == v for r, v in existing.items())
    put('MANIFEST.json', {'schema': 'finite-independent-production-static-audit-manifest-v1', 'UTC': now(),
        'root': str(A), 'root_mode': dirs[0]['mode'], 'regular_files': len(rows) + 2, 'child_directories': len(dirs) - 1,
        'payload_files': rows, 'directories': dirs,
        'exact_already_created_terminal_recursive_hash_exclusions': ['MANIFEST.json', 'FINAL.json'],
        'terminal_modes': {r: pin(A / r)['mode'] for r in ['MANIFEST.json', 'FINAL.json']},
        'other_exclusions': [], 'all_hidden_empty_ignored_modes_and_topology_included': True,
        'no_future_subtree_or_basename_exclusions': True, 'external_terminal_pins_required': True})
    source = before['snapshot']['source_preparation']['files']['release_three.py']
    put('FINAL.json', {'schema': 'independent-production-static-audit-final-v1', 'UTC': now(),
        'status': 'STATIC_REVIEW_COMPLETE_HELPER_UNFIT_FOR_EXECUTION_FROZEN',
        'completion_percent_assigned_static_audit_only': 100, 'helper': source, 'helper_lines': 1279,
        'helper_disposition': 'UNFIT_FOR_EXECUTION', 'concrete_findings': 1, 'finding_source_line': 484,
        'finding': 'Opaque Git stdout omitted, including success followed by parse failure',
        'required_correction': 'Durably retain whole actual stdout for EVERY opaque Git call including success before later parsing; not only nonzero exits',
        'independent_adversarial_source_review': True, 'production_helper_modes_import_AST_compile_help_or_tests': 0,
        'passive_custody_reader_invocations': 1, 'passive_custody_reader_exit': 0,
        'complete_preparation_stage_successful_audit_source_native_public_config_before_after_exact': True,
        'raw_index_summary': result['raw_index'], 'runtime_absent': True,
        'initial_read_path_discovery_errors_retained_separately': 2,
        'manifest': pin(A / 'MANIFEST.json'), 'report': pin(A / 'REPORT.md'), 'findings': pin(A / 'FINDINGS.md'),
        'regular_files': len(rows) + 2, 'child_directories': len(dirs) - 1, 'root_mode': dirs[0]['mode'],
        'follow_up': None, 'AA': None, 'actual_publication_date': None,
        'execution_publication_UI_live_production_science_copy_or_future_action_authority': False,
        'M_W_source_runtime_ignore_Git_network_Sheet_deploy_redirect_or_contact_mutation': False, 'frozen': True})

if __name__ == '__main__':
    main()
