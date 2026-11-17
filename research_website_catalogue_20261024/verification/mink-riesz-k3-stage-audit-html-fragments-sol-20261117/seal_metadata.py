"""Seal only this successful independent audit's finite administrative namespace."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-stage-audit-html-fragments-sol-20261117')

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
    result = load('RESULTS.json')
    execution = load('EXECUTION.json')
    assert result['status'] == 'PASS_TYPED_FRAGMENT_PRIVATE_STAGE_AUDIT_ONLY'
    assert result['checks_passed'] == len(result['checks']) == 58461
    assert execution['invocations'] == 1 and execution['exit_code'] == 0
    assert execution['prior_two_reader_exits_remain'] == [1, 1]
    assert pin(A / 'audit_private.py') == {'bytes': 48481, 'SHA256': 'ab46590f2eb64fc1ce1cb38fa08d21cd191b0dd9a29012361037e3461013dc27', 'mode': '0644'}
    assert (A / 'AUDIT.stdout.txt').read_bytes() == (A / 'AUDIT.stderr.txt').read_bytes() == b''
    assert (A / 'SEAL.stdout.txt').read_bytes() == (A / 'SEAL.stderr.txt').read_bytes() == b''
    before, after = load('BEFORE.json'), load('AFTER.json')
    assert {k: v for k, v in before.items() if k != 'UTC'} == {k: v for k, v in after.items() if k != 'UTC'}
    assert result['follow_up'] is None and result['AA'] is None and result['actual_publication_date'] is None
    assert not result['future_action_authority'] and not result['actual_UI_render_live_or_production_certificate']
    existing = {p.name: pin(p) for p in sorted(A.iterdir())}
    assert 'SEAL_EXECUTION.json' not in existing
    put('SEAL_EXECUTION.json', {'schema': 'successful-private-audit-metadata-normal-completion-v1',
        'UTC_start': started, 'UTC_data_end': now(), 'invocations': 1, 'exit_code_at_normal_completion': 0,
        'external_tool_exit_observation_required': True, 'reader_invocations_remain': 1,
        'old_failed_reader_exits_remain': [1, 1], 'producer_or_science_execution': False, 'follow_up': None})
    (A / 'MANIFEST.json').write_bytes(b'')
    (A / 'FINAL.json').write_bytes(b'')
    rows, dirs, seen = [], [], set()
    def hidden(r):
        return any(c.startswith('.') for c in Path(r).parts if c != '.')
    def walk(p):
        st = p.lstat()
        assert stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen
        seen.add((st.st_dev, st.st_ino))
        children = sorted(p.iterdir(), key=lambda x: x.name)
        r = p.relative_to(A).as_posix()
        dirs.append({'path': r, 'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children, 'hidden': hidden(r)})
        for c in children:
            st = c.lstat()
            if stat.S_ISDIR(st.st_mode):
                walk(c)
            else:
                assert stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen
                seen.add((st.st_dev, st.st_ino))
                r = c.relative_to(A).as_posix()
                if r not in ['MANIFEST.json', 'FINAL.json']:
                    v = pin(c)
                    rows.append({'path': r, **v, 'empty': v['bytes'] == 0, 'hidden': hidden(r)})
    walk(A)
    assert all(pin(A / r) == v for r, v in existing.items())
    assert len(dirs) == 1 and dirs[0]['path'] == '.'
    put('MANIFEST.json', {'schema': 'finite-independent-typed-fragment-stage-audit-manifest-v1', 'UTC': now(),
        'root': str(A), 'root_mode': dirs[0]['mode'], 'regular_files': len(rows) + 2,
        'child_directories': len(dirs) - 1, 'payload_files': rows, 'directories': dirs,
        'payload_file_mode_counts': dict(Counter(r['mode'] for r in rows)),
        'hidden_payload_files': sum(r['hidden'] for r in rows), 'empty_payload_files': [r['path'] for r in rows if r['empty']],
        'exact_already_created_terminal_recursive_hash_exclusions': ['MANIFEST.json', 'FINAL.json'],
        'terminal_modes': {x: pin(A / x)['mode'] for x in ['MANIFEST.json', 'FINAL.json']},
        'other_exclusions': [], 'all_hidden_empty_ignored_modes_and_topology_included': True,
        'no_future_subtree_or_basename_exclusions': True, 'external_terminal_pins_required': True})
    put('FINAL.json', {'schema': 'independent-typed-fragment-stage-audit-final-v1', 'UTC': now(),
        'status': 'PASS_PRIVATE_STATIC_STAGE_AUDIT_ONLY_FROZEN', 'completion_percent_assigned_audit_only': 100,
        'reader_exit': 0, 'reader_invocations': 1, 'reader': pin(A / 'audit_private.py'), 'checks_passed': 58461,
        'prior_failed_reader_exits': [1, 1], 'prior_failed_audit_completion_percent': [60, 60],
        'prior_failed_finite_files_childdirs': [[28, 0], [30, 0]], 'no_prior_failure_retroPASS': True,
        'stage_files_childdirs': [1635, 770], 'baseline_files_childdirs_index_XML': [790, 381, 130, 131],
        'candidate_files_childdirs_index_XML': [803, 387, 133, 134], 'projection': '13A2M/15Gitpaths/6newdirs',
        'whole_accepted_articles_except_independent_HEAD_spans': [8, 7, 7], 'native_assets_exact': 7,
        'old130whole_HTML_concat_data_rawJSON_typed_and131whole_fullparsed_XML_prefix': True,
        'independent_complete_index_XML_forward_reverse_span_counts': [3, 1],
        'old_file_modes_0644_0600_0666_and_all_directory_modes_exact': True,
        'all_protected_inputs_native_public_stage_both_failed_lanes_and_diagnoses_before_after_exact': True,
        'HTML_ID_checks_only_HTML_PDF_viewer_native_bytes_path_header_only': True,
        'manifest': pin(A / 'MANIFEST.json'), 'report': pin(A / 'REPORT.md'), 'criteria': pin(A / 'CRITERIA.md'),
        'regular_files': len(rows) + 2, 'child_directories': len(dirs) - 1, 'root_mode': dirs[0]['mode'],
        'follow_up': None, 'AA': None, 'actual_publication_date': None,
        'new_science_copy_actual_UI_render_live_production_or_future_action_authority': False,
        'producer_science_or_original_reader_rerun_import_AST_compile_help': False,
        'W_source_Git_network_Sheet_deploy_redirect_outreach_mutation': False, 'frozen': True})

if __name__ == '__main__':
    main()
