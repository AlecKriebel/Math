#!/usr/bin/env python3
"""Disposable-copy rejection probes for the already externally bound r2 bytes.

Test-only repinning reaches syntax and semantic checks; it is not substitution of
the reviewed external acceptance pin. No input package file is modified.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2] / 'work/pr838_revision_r2'
INNER = ROOT / 'publication_20261015/verification_package'
PRIVATE = HERE / 'private/disposable'
PIN = 'acbefb678d34b701ae1df67c6d6896c013b195c08220007d0389fa3aa2feb659'
OUTER_PIN = '2881defd3d6a349f346ac5ea9cedf0fa8b71bacad159cbe5c1e0b031229a55b5'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def repin_row(root, manifest, member):
    obj = json.loads((root / manifest).read_bytes())
    row = next(r for r in obj['files'] if r['path'] == member)
    raw = (root / member).read_bytes()
    row.update(bytes=len(raw), sha256=sha(raw))
    write_json(root / manifest, obj)
    return sha((root / manifest).read_bytes())


def main():
    results = []
    for optimized in (False, True):
        flags = ['-I', '-S', '-B'] + (['-O'] if optimized else [])
        with tempfile.TemporaryDirectory(dir=PRIVATE, prefix='probes with spaces ') as td:
            work = Path(td)

            def run_case(name, command, expected, marker=None):
                run = subprocess.run([sys.executable, *flags, *command], cwd='/',
                                     capture_output=True, text=True, timeout=4,
                                     env=dict(os.environ, TMPDIR=str(PRIVATE)))
                ok = run.returncode != 0 and expected in run.stderr
                marker_absent = marker is None or not marker.exists()
                row = {'name': name, 'optimized': optimized, 'expected': expected,
                       'returncode': run.returncode, 'rejected_as_expected': ok,
                       'untrusted_execution_marker_absent': marker_absent,
                       'error_tail': run.stderr.strip().splitlines()[-1:]}
                results.append(row)
                if not ok or not marker_absent:
                    raise RuntimeError(json.dumps(row) + '\n' + run.stdout + run.stderr)

            def clone(name, outer=False):
                path = work / name
                shutil.copytree(ROOT if outer else INNER, path)
                return path

            def portable(path, pin=PIN, full=False):
                return [str(path / 'verify_package.py'), pin] + (['--full'] if full else [])

            p = clone('wrong pin')
            run_case('portable_wrong_external_pin', portable(p, '0' * 64), 'external index pin')
            p = clone('extra regular file'); (p / 'unlisted.txt').write_text('unlisted')
            run_case('portable_extra_regular_file', portable(p), 'closed inventory')
            p = clone('extra empty directory'); (p / 'unlisted-empty').mkdir()
            run_case('portable_extra_empty_directory', portable(p), 'closed inventory')
            p = clone('symlink file'); (p / 'README.md').unlink(); (p / 'README.md').symlink_to(INNER / 'README.md')
            run_case('portable_member_symlink', portable(p), 'nonregular member')
            p = clone('symlink directory'); (p / 'unlisted-directory').symlink_to(INNER, target_is_directory=True)
            run_case('portable_directory_symlink', portable(p), 'nonregular member')
            p = clone('fifo index'); (p / 'package_index.json').unlink(); os.mkfifo(p / 'package_index.json')
            run_case('portable_fifo_index_no_blocking_read', portable(p), 'regular file required')
            p = clone('fifo member'); (p / 'README.md').unlink(); os.mkfifo(p / 'README.md')
            run_case('portable_fifo_member_no_blocking_read', portable(p), 'nonregular member')
            for label, raw, expected in [
                ('duplicate_key', b'{"schema":1,"schema":2}', 'duplicate JSON key'),
                ('nonfinite', b'{"schema":NaN}', 'nonfinite JSON constant'),
            ]:
                p = clone(label); (p / 'package_index.json').write_bytes(raw)
                run_case('portable_' + label, portable(p, sha(raw)), expected)
            for i, bad in enumerate(['../outside.md', '/absolute.md', 'x//bad.md',
                                     'x/./bad.md', 'x\\bad.md', 'C:bad.md', '.']):
                p = clone('unsafe path ' + str(i)); obj = json.loads((p / 'package_index.json').read_bytes())
                obj['files'][0]['path'] = bad; write_json(p / 'package_index.json', obj)
                run_case('portable_unsafe_path_' + str(i), portable(p, sha((p / 'package_index.json').read_bytes())), 'safe paths')
            p = clone('bool bytes'); obj = json.loads((p / 'package_index.json').read_bytes())
            obj['files'][0]['bytes'] = True; write_json(p / 'package_index.json', obj)
            run_case('portable_bool_not_integer_byte_count', portable(p, sha((p / 'package_index.json').read_bytes())), 'byte count')
            p = clone('duplicate path'); obj = json.loads((p / 'package_index.json').read_bytes())
            obj['files'].append(obj['files'][0]); write_json(p / 'package_index.json', obj)
            run_case('portable_duplicate_inventory_path', portable(p, sha((p / 'package_index.json').read_bytes())), 'unique inventory')
            p = clone('wrong problem'); obj = json.loads((p / 'package_index.json').read_bytes())
            obj['problem_id'] = 10000037; write_json(p / 'package_index.json', obj)
            run_case('portable_wrong_problem_identity', portable(p, sha((p / 'package_index.json').read_bytes())), 'package identity')
            p = clone('replay result mismatch')
            target = 'root_evidence/' + ('ROOT_ORIGINAL_DATA_INTEGRITY_O.json' if optimized else 'ROOT_ORIGINAL_DATA_INTEGRITY.json')
            obj = json.loads((p / target).read_bytes()); obj['archive_member_total'] = 14; write_json(p / target, obj)
            changed_pin = repin_row(p, 'package_index.json', target)
            run_case('portable_replayed_result_drift', portable(p, changed_pin, True), 'original integrity replay result drift')

            # Builder probes authenticate before subprocess execution. Marker code
            # would write only within this disposable copy if it were reached.
            builder = str(INNER / 'build_verification.py')
            def build(p, out, pin=PIN):
                return [builder, '--from-package', str(p), '--trusted-index-sha256', pin,
                        '--output-root', str(out)]
            p = clone('builder substituted verifier'); marker = p / 'executed-marker'
            (p / 'verify_package.py').write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n')
            run_case('builder_substituted_verifier_before_execution', build(p, work / 'output 1'), 'trusted input verifier binding failed', marker)
            p = clone('builder fifo index'); (p / 'package_index.json').unlink(); os.mkfifo(p / 'package_index.json')
            run_case('builder_fifo_index_no_blocking_read', build(p, work / 'output 2'), 'nonregular input')
            p = clone('builder fifo verifier'); (p / 'verify_package.py').unlink(); os.mkfifo(p / 'verify_package.py')
            run_case('builder_fifo_verifier_no_blocking_read', build(p, work / 'output 3'), 'nonregular input')
            p = clone('builder symlink verifier'); (p / 'verify_package.py').unlink(); (p / 'verify_package.py').symlink_to(INNER / 'verify_package.py')
            run_case('builder_symlink_verifier', build(p, work / 'output 4'), 'nonregular input')
            p = clone('builder inside output')
            run_case('builder_output_inside_input', build(p, p / 'new output'), 'outside the intact input package')
            p = clone('builder existing output'); out = work / 'already occupied'; out.mkdir(); (out / 'keep').write_text('keep')
            run_case('builder_nonempty_output', build(p, out), 'fresh or empty directory')
            p = clone('builder unlisted payload'); (p / 'unexpected').mkdir()
            run_case('builder_closed_inventory_before_rebuild', build(p, work / 'output 5'), 'input package binding failed')

            p = clone('outer extra directory', True); (p / 'unexpected').mkdir()
            run_case('outer_extra_directory', [str(p / 'verify_publication.py'), OUTER_PIN], 'closed inventory')
            p = clone('outer metadata mismatch', True)
            member = 'publication_20261015/preprint/metadata.json'; obj = json.loads((p / member).read_bytes())
            obj['title'] += ' altered'; write_json(p / member, obj)
            altered_pin = repin_row(p, 'PUBLICATION_MANIFEST.json', member)
            run_case('outer_metadata_crosscopy_mismatch', [str(p / 'verify_publication.py'), altered_pin], 'exact current metadata')
            p = clone('outer zip altered', True)
            member = 'publication_20261015/preprint/verification.zip'
            import zipfile
            with zipfile.ZipFile(p / member, 'a') as z:
                z.writestr('extra.md', b'unlisted')
            altered_pin = repin_row(p, 'PUBLICATION_MANIFEST.json', member)
            run_case('outer_zip_closed_inventory', [str(p / 'verify_publication.py'), altered_pin], 'archive closed inventory')
            p = clone('outer pdf mismatch', True)
            member = 'publication_20261015/preprint/output/pdf/note.pdf'; raw = (p / member).read_bytes()
            (p / member).write_bytes(raw + b'\n')
            altered_pin = repin_row(p, 'PUBLICATION_MANIFEST.json', member)
            run_case('outer_pdf_crosscopy_mismatch', [str(p / 'verify_publication.py'), altered_pin], 'PDF identity')
    record = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'probe_count': len(results), 'all_expected_rejections': True,
              'normal_and_optimized': True,
              'test_only_index_repinning': 'Used solely to reach independent guards. Original pins/inputs never changed.',
              'concurrent_hostile_filesystem_tested': False, 'results': results}
    write_json(HERE / 'PROBE_EVIDENCE.json', record)
    print(json.dumps({'probes': len(results), 'all_expected_rejections': True}))


if __name__ == '__main__':
    main()
