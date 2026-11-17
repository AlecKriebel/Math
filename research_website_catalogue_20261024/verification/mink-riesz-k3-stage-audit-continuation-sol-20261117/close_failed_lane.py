"""Distinct passive closing custody for the retained failed audit; never reruns it."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import stat

A = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mink-riesz-k3-stage-audit-continuation-sol-20261117')
P = A.parent.parent
S = P / 'verification/mink-riesz-k3-stage-sol-20261117'
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
D = P / 'verification/root-mink-riesz-k3-audit-pdf-fragment-diagnosis-20261117.json'
E = P / 'verification/root-mink-riesz-k3-audit-head-diagnosis-20261117.json'
O = P / 'verification/mink-riesz-k3-stage-audit-sol-20261117'

def now():
    return datetime.now(timezone.utc).isoformat()

def need(value, label):
    if not value:
        raise AssertionError(label)

def load(path):
    return json.loads(path.read_text())

def pin(path):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'regular file ' + str(path))
    b = path.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest(), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def tree(root):
    files, dirs, seen = {}, {}, set()
    def walk(path, rel):
        st = path.lstat()
        need(stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'real unique directory ' + str(path))
        seen.add((st.st_dev, st.st_ino))
        children = sorted(path.iterdir(), key=lambda x: x.name)
        dirs[rel] = {'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children}
        for child in children:
            r = child.relative_to(root).as_posix()
            st = child.lstat()
            if stat.S_ISDIR(st.st_mode):
                walk(child, r)
            else:
                need(stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'real unique file ' + str(child))
                seen.add((st.st_dev, st.st_ino))
                files[r] = pin(child)
    walk(root, '.')
    return {'root': str(root), 'files': files, 'directories': dirs,
            'regular_files': len(files), 'child_directories': len(dirs) - 1}

def native(root):
    git = root / '.git'
    head = (git / 'HEAD').read_text()
    packed = git / 'packed-refs'
    lines = [x for x in packed.read_text().splitlines(keepends=True)
             if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?', x)]
    branch = head.strip().removeprefix('ref: ')
    need(head.startswith('ref: refs/heads/'), 'native branch ' + str(root))
    loose = git / branch
    refs = {x.split()[1]: x.split()[0] for x in lines}
    resolved = loose.read_text().strip() if loose.exists() else refs[branch]
    return {'HEAD': pin(git / 'HEAD'), 'index': pin(git / 'index'), 'config': pin(git / 'config'),
            'HEAD_text': head, 'local_loose_heads': tree(git / 'refs/heads'),
            'packed_local_heads': {'file_mode': pin(packed)['mode'], 'raw_lines': lines},
            'resolved_native_HEAD': resolved,
            'optional_worktree_config': pin(git / 'config.worktree') if (git / 'config.worktree').exists() else None}

def capture(expected, originals):
    protected = {'schema': expected['schema'], 'roots': {r: tree(Path(r)) for r in expected['roots']},
                 'controls': {r: pin(Path(r)) for r in expected['controls']},
                 'public': tree(W / 'public'), 'native_M': native(M), 'native_W': native(W)}
    return {'protected': protected, 'stage': tree(S),
            'original_failed_files': {r: pin(A / r) for r in originals}, 'root_diagnosis': pin(D),
            'prior_failed': tree(O), 'prior_root_diagnosis': pin(E)}

def put(name, value):
    p = A / name
    need(p.parent == A and not p.exists(), 'fresh own closure output ' + name)
    p.write_text(json.dumps(value, indent=2) + '\n')

def main():
    need(Path(__file__).resolve() == A / 'close_failed_lane.py', 'fixed closure source')
    need(not (A / 'CLOSURE_RESULT.json').exists(), 'one distinct closure invocation')
    started = now()
    original = load(A / 'BEFORE.json')
    inputs = load(A / 'CLOSURE_INPUTS.json')
    need(len(inputs['original_failed_files']) == 11, 'exact eleven original failed-lane files')
    need(inputs['original_failed_files']['audit_private.py'] ==
         {'bytes': 44562, 'SHA256': '1923a70e3eb716920f96b12facbae4fa0b12337eac320da650fd558f4c7d88fb', 'mode': '0644'}, 'original failed reader fixed pin')
    before = capture(original['protected'], inputs['original_failed_files'])
    need(before['protected'] == original['protected'] and before['stage'] == original['stage'] and
         before['prior_failed'] == original['prior_failed'] and before['prior_root_diagnosis'] == original['root_diagnosis'],
         'all protected inputs native controls public and stage unchanged since failed reader start')
    need(before['original_failed_files'] == inputs['original_failed_files'], 'all original failed files exact')
    need(before['root_diagnosis'] == {'bytes': 2165, 'SHA256': '700257c3ce91aa281fe730fdd5a360763fef974dfbb10e95512f9fd32063f49a', 'mode': '0644'}, 'external root diagnosis pin')
    need(load(A / 'EXECUTION.json')['exit_code'] == 1, 'original audit remains failed')
    put('CLOSURE_BEFORE.json', {'UTC': now(), 'snapshot': before})
    after = capture(original['protected'], inputs['original_failed_files'])
    need(after == before, 'distinct closing guard whole before/after exact')
    put('CLOSURE_AFTER.json', {'UTC': now(), 'snapshot': after})
    put('CLOSURE_RESULT.json', {'schema': 'distinct-failed-audit-closing-custody-only-v1',
                              'UTC_start': started, 'UTC_end': now(), 'status': 'CUSTODY_ONLY_PASS_ORIGINAL_AUDIT_FAILED',
                              'original_audit_exit': 1, 'original_audit_completion_percent': 60,
                              'original_failure_line': 372, 'original_failed_files': before['original_failed_files'],
                              'root_diagnosis': {'path': str(D), 'pin': before['root_diagnosis']},
                              'prior_root_diagnosis': {'path': str(E), 'pin': before['prior_root_diagnosis']},
                              'all_original_and_protected_inputs_stage_native_public_before_after_exact': True,
                              'original_audit_rerun_import_AST_compile_or_repair': False,
                              'stage_payload_or_producer_or_science_execution': False,
                              'follow_up': None, 'publication_or_future_action_authority': False})
    need(not (A / 'CLOSURE_REPORT.md').exists(), 'fresh closure report')
    (A / 'CLOSURE_REPORT.md').write_text(
        'The original audit remains one failed exit 1, at line 372, with incomplete coverage estimated at 60%. '
        'Its eleven original files, including the entire 629-line reader, literal 1221-byte error, empty stdout, '
        'initial BEFORE and execution receipt, remain unchanged. No PASS is retroactively claimed.\n\n'
        'Under explicit root disposition, this distinct passive closing guard verifies the complete original '
        'protected boundary against the retained initial snapshot and again before/after: all twelve input '
        'roots, root adoption/clearance buffers, native Math/website controls, complete website public tree '
        'and whole frozen 1635-file/770-directory stage. Inherited modes including 0600/0666 are exact. '
        'The root diagnosis pin is checked; it establishes a reader HTML/PDF fragment type assumption and '
        'authorizes a separate corrected audit. No original reader or producer was executed, imported, '
        'AST-parsed, compiled, repaired or rerun. No scientific, publication or actual UI certificate. '
        'follow_up null; no later action authority.\n')

if __name__ == '__main__':
    main()
