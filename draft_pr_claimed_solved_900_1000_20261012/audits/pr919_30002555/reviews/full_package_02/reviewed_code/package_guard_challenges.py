#!/usr/bin/env python3
"""Exercise actual closed-package rejection and assertion execution safeguards."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
MODES = {'normal': ([], None), 'O': (['-O'], None), 'OO': (['-OO'], None),
         'environment_2': ([], '2')}


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bundle', type=Path, required=True)
    ap.add_argument('--python', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    bundle = args.bundle.absolute()
    pin = sha(bundle/'PACKAGE_MANIFEST.json')
    temporary = HERE/'tmp/guard_challenges'
    temporary.mkdir(parents=True, exist_ok=True)
    require(not temporary.is_symlink(), 'Unsafe test work directory')
    rows = []
    with tempfile.TemporaryDirectory(dir=temporary, prefix='closed_inventory_') as td:
        temp = Path(td)
        def env_for(mode):
            flags, optimize = MODES[mode]
            env = dict(os.environ, TMPDIR=str(temp), PYTHONDONTWRITEBYTECODE='1')
            env.pop('PYTHONOPTIMIZE', None)
            if optimize is not None:
                env['PYTHONOPTIMIZE'] = optimize
            return flags, env
        def invoke(root, expected, mode, tail=()):
            flags, env = env_for(mode)
            return subprocess.run([str(args.python), *flags, str(root/'verify_package.py'),
                    '--expected-manifest', expected, '--integrity-only', *map(str, tail)],
                    capture_output=True, text=True, env=env, cwd=temp, timeout=8)
        def json_edit(root, edit):
            path = root/'PACKAGE_MANIFEST.json'
            data = json.loads(path.read_text())
            edit(data)
            path.write_text(json.dumps(data, indent=2)+'\n')
            return sha(path)
        def replace_fifo(root, name):
            path = root/name
            path.unlink()
            os.mkfifo(path)
        cases = [
            ('missing_file', lambda r: (r/'note.tex').unlink()),
            ('extra_regular', lambda r: (r/'extra.txt').write_text('unexpected')),
            ('extra_pdf_source', lambda r: (r/'copied-source.pdf').write_bytes(b'%PDF-1.7')),
            ('extra_csv_corpus', lambda r: (r/'source-corpus.csv').write_text('title,body\n')),
            ('extra_empty_directory', lambda r: (r/'empty').mkdir()),
            ('extra_fifo', lambda r: os.mkfifo(r/'unlisted_fifo')),
            ('manifest_fifo', lambda r: replace_fifo(r, 'PACKAGE_MANIFEST.json')),
            ('expected_note_fifo', lambda r: replace_fifo(r, 'note.tex')),
            ('expected_proof_fifo', lambda r: replace_fifo(r, 'original_packet/public/PROOF.md')),
            ('internal_symlink', lambda r: ((r/'note.tex').unlink(), (r/'note.tex').symlink_to(bundle/'note.tex'))),
            ('root_alias', lambda r: None),
            ('extra_socket', lambda r: None),
            ('expected_file_becomes_directory', lambda r: ((r/'note.pdf').unlink(), (r/'note.pdf').mkdir())),
            ('semantic_proof_change', lambda r: (r/'original_packet/public/PROOF.md').write_text('False theorem.\n')),
            ('substitute_external_anchor', lambda r: None),
            ('invalid_external_anchor', lambda r: None),
            ('boolean_pr', lambda r: json_edit(r, lambda m: m.update(pr=True))),
            ('integer_problem_id', lambda r: json_edit(r, lambda m: m.update(problem_id=30002555))),
            ('boolean_schema', lambda r: json_edit(r, lambda m: m.update(schema_version=True))),
            ('extra_metadata_key', lambda r: json_edit(r, lambda m: m.update(unreviewed='added'))),
            ('missing_scope', lambda r: json_edit(r, lambda m: m.pop('scope'))),
            ('boolean_record_bytes', lambda r: json_edit(r, lambda m: m['files']['note.tex'].update(bytes=True))),
            ('negative_record_bytes', lambda r: json_edit(r, lambda m: m['files']['note.tex'].update(bytes=-1))),
            ('invalid_record_hash', lambda r: json_edit(r, lambda m: m['files']['note.tex'].update(sha256='bad'))),
            ('record_extra_key', lambda r: json_edit(r, lambda m: m['files']['note.tex'].update(extra=True))),
            ('parent_traversal_record', lambda r: json_edit(r, lambda m: m['files'].update({'../escape': m['files'].pop('note.tex')}))),
            ('absolute_record', lambda r: json_edit(r, lambda m: m['files'].update({'/escape': m['files'].pop('note.tex')}))),
            ('self_listed_manifest', lambda r: json_edit(r, lambda m: m['files'].update({'PACKAGE_MANIFEST.json': m['files']['note.tex']}))),
            ('wrong_original_head', lambda r: json_edit(r, lambda m: m.update(original_pr_head='0'*40))),
            ('wrong_original_manifest_pin', lambda r: json_edit(r, lambda m: m.update(original_packet_manifest_sha256='0'*64))),
            ('duplicate_json_key', lambda r: None),
            ('nonfinite_json', lambda r: None),
            ('truncated_json', lambda r: (r/'PACKAGE_MANIFEST.json').write_text('{')),
            ('separate_pdf_mismatch', lambda r: None),
            ('separate_pdf_fifo', lambda r: None),
        ]
        for label, mutate in cases:
            root = temp/'packet'
            shutil.copytree(bundle, root)
            returned = mutate(root)
            expected = returned if type(returned) is str and len(returned) == 64 else pin
            selected = root
            tail = []
            sock = None
            if label == 'root_alias':
                selected = temp/'alias'
                selected.symlink_to(root, target_is_directory=True)
            elif label == 'extra_socket':
                sock = socket.socket(socket.AF_UNIX)
                # macOS limits Unix-socket path length; use this case's own cwd.
                previous = Path.cwd()
                os.chdir(root)
                try:
                    sock.bind('unlisted_socket')
                finally:
                    os.chdir(previous)
            elif label == 'substitute_external_anchor':
                expected = '0'*64
            elif label == 'invalid_external_anchor':
                expected = 'True'
            elif label == 'duplicate_json_key':
                path = root/'PACKAGE_MANIFEST.json'
                text = path.read_text()
                path.write_text(text.replace('{', '{"pr": 919,', 1))
                expected = sha(path)
            elif label == 'nonfinite_json':
                path = root/'PACKAGE_MANIFEST.json'
                path.write_text(path.read_text().replace('"schema_version": 1', '"schema_version": NaN', 1))
                expected = sha(path)
            elif label == 'truncated_json':
                expected = sha(root/'PACKAGE_MANIFEST.json')
            elif label in ('separate_pdf_mismatch', 'separate_pdf_fifo'):
                separate = temp/'separate.pdf'
                if label.endswith('fifo'):
                    os.mkfifo(separate)
                else:
                    separate.write_bytes(b'%PDF-wrong')
                tail = ['--pdf', separate]
            for mode in MODES:
                proc = invoke(selected, expected, mode, tail)
                require(proc.returncode != 0, 'Hostile case accepted: '+label+'/'+mode)
                rows.append({'case': label, 'mode': mode, 'rejected': True,
                             'exit_code': proc.returncode,
                             'stderr_sha256': hashlib.sha256(proc.stderr.encode()).hexdigest()})
            if sock is not None:
                sock.close()
            if selected != root:
                selected.unlink()
            if tail:
                Path(tail[1]).unlink()
            shutil.rmtree(root)

        for mode in MODES:
            proc = invoke(bundle, pin, mode, ['--pdf', bundle/'note.pdf'])
            require(proc.returncode == 0 and json.loads(proc.stdout)['status'] == 'PASS_INTEGRITY',
                    'Unchanged positive rejected: '+mode)
            rows.append({'case': 'unchanged_integrity', 'mode': mode, 'passed': True})

        false_script = temp/'deliberately_false_assert.py'
        false_script.write_text('assert False, "deliberate mathematical guard fixture"\nprint("UNSAFE_PASS")\n')
        launcher = temp/'isolated_launch.py'
        launcher.write_text('import os,subprocess,sys\nenv=dict(os.environ)\n'
                            'for name in ("PYTHONOPTIMIZE","PYTHONPATH","PYTHONHOME"):env.pop(name,None)\n'
                            'p=subprocess.run([sys.executable,"-I","-B",sys.argv[1],sys.argv[2]],env=env)\n'
                            'raise SystemExit(p.returncode)\n')
        for mode in MODES:
            flags, env = env_for(mode)
            proc = subprocess.run([str(args.python), *flags, str(launcher),
                    str(bundle/'run_checked.py'), str(false_script)], env=env,
                    cwd=temp, text=True, capture_output=True, timeout=8)
            require(proc.returncode != 0 and 'AssertionError' in proc.stderr
                    and 'UNSAFE_PASS' not in proc.stdout, 'Disabled child assertion: '+mode)
            observation = json.loads(proc.stderr.splitlines()[0])
            require(observation['child_optimization'] == 0 and observation['child_isolated'] == 1,
                    'False-child execution flags wrong')
            rows.append({'case': 'genuinely_false_child_assertion', 'mode': mode,
                         'rejected': True, 'child_optimization': 0, 'child_isolated': 1})
    require(sha(bundle/'PACKAGE_MANIFEST.json') == pin, 'Original bundle changed')
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
              'package_manifest_sha256': pin, 'hostile_inventory_cases': len(cases),
              'hostile_inventory_runs': len(cases)*len(MODES), 'positive_runs': len(MODES),
              'false_assertion_child_runs': len(MODES), 'all_bounded_no_timeouts': True,
              'original_bundle_unchanged': True, 'rows': rows,
              'scope': 'Actual structural/metadata/FIFO rejection plus isolated active-assertion execution. Full mathematical replay is separately recorded.'}
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
