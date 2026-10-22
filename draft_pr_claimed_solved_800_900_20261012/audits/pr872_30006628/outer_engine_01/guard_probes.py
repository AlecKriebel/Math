#!/usr/bin/env python3
"""Focused PR872 outer-wrapper probes; temporary fixture is not a publication package."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def row(name, raw):
    return {'path': name, 'bytes': len(raw), 'sha256': sha(raw)}


def archive(blobs, bad_mode=False, reverse=False, corrupt=False):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        for position, name in enumerate(sorted(blobs, reverse=reverse)):
            info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | (0o755 if bad_mode and position == 0 else 0o644)) << 16
            data = blobs[name] + (b'x' if corrupt and position == 0 else b'')
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buf.getvalue()


def fixture(base, wrapper):
    p = base / 'preprint'
    portable = {name: (p / name).read_bytes() for name in (
        'note.tex', 'README.md', 'metadata.json', 'CURRENT_PRIORITY.md',
        'check_originals.py', 'verify_package.py', 'build_verification.py')}
    portable['note.pdf'] = (p / 'output/pdf/note.pdf').read_bytes()
    source_manifest = (base / 'SOURCE_MANIFEST.json').read_bytes()
    portable['root_evidence/SOURCE_MANIFEST.json'] = source_manifest
    originals = {}
    for r in json.loads(source_manifest)['files']:
        raw = (base / 'source' / r['path']).read_bytes()
        if len(raw) != r['bytes'] or sha(raw) != r['sha256']:
            raise ValueError('fixture original source mismatch')
        originals[r['path']] = raw
        portable['source/' + r['path']] = raw
    portable['package_index.json'] = encoded({
        'schema': 'random-property-t-verification-v1', 'problem_id': '30006628',
        'files': [row(name, portable[name]) for name in sorted(portable)]})
    pre = {name: portable[name] for name in (
        'note.tex', 'README.md', 'metadata.json', 'CURRENT_PRIORITY.md',
        'check_originals.py', 'verify_package.py', 'build_verification.py', 'package_index.json')}
    pre['output/pdf/note.pdf'] = portable['note.pdf']
    pre['zenodo-deposit.json'] = (p / 'zenodo-deposit.json').read_bytes()
    pre['verification.zip'] = archive(portable)
    blobs = {name: raw for name, raw in originals.items() if name not in ('README.md', 'PUBLICATION_MANIFEST.json')}
    blobs.update({'README.md': b'Synthetic wrapper guard fixture.\n',
                  'RESEARCH_LOG.md': b'Synthetic fixture, not publication acceptance.\n',
                  'CURRENT_PUBLICATION.json': encoded({'zenodo_metadata': json.loads(pre['metadata.json'])}),
                  'verify_current_publication.py': wrapper.read_bytes()})
    blobs.update({'publication_20261015/preprint/' + n: raw for n, raw in pre.items()})
    blobs.update({'publication_20261015/verification_package/' + n: raw for n, raw in portable.items()})
    return blobs, portable


def write_fixture(root, blobs):
    for name, raw in blobs.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return reseal(root)


def reseal(root):
    rows = []
    for p in sorted(root.rglob('*')):
        if p.is_file() and p.name != 'PUBLICATION_MANIFEST.json':
            rows.append(row(p.relative_to(root).as_posix(), p.read_bytes()))
    # The frozen inner PUBLICATION_MANIFEST.json must remain in the outer index.
    frozen = root / 'publication_20261015/verification_package/source/PUBLICATION_MANIFEST.json'
    rows.append(row(frozen.relative_to(root).as_posix(), frozen.read_bytes()))
    rows.sort(key=lambda r: r['path'])
    data = encoded({'schema': 'random-property-t-current-publication-v1',
                    'problem_id': '30006628', 'files': rows})
    (root / 'PUBLICATION_MANIFEST.json').write_bytes(data)
    return sha(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--wrapper', type=Path, default=Path(__file__).resolve().with_name('verify_current_publication.py'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    blobs, portable = fixture(args.base, args.wrapper)
    records = []
    work = Path(__file__).resolve().parent / 'private_work'
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='outer guard probes ', dir=work) as td:
        td = Path(td)
        def execute(label, mode, mutate=None, extras=(), full=False, expected=None):
            root = td / (mode + ' ' + label)
            root.mkdir()
            pin = write_fixture(root, blobs)
            if mutate:
                pin = mutate(root, pin)
            flags = ['-I', '-S', '-B'] + (['-O'] if mode == 'optimized' else [])
            command = [sys.executable, *flags, str(root / 'verify_current_publication.py'), pin]
            if full:
                command.append('--full')
            command.extend(extras)
            child_env = dict(os.environ)
            child_env['TMPDIR'] = str(td)
            proc = subprocess.run(command, cwd=td, env=child_env, capture_output=True, timeout=90)
            try:
                data = json.loads(proc.stdout)
            except ValueError as exc:
                raise ValueError(label + ' did not return JSON: ' + repr(proc.stdout) + repr(proc.stderr)) from exc
            if expected is None:
                ok = proc.returncode == 0 and not proc.stderr and data.get('status') == 'PASS'
                if full:
                    replay = data['inner_verifier_result']['full_replay']
                    ok = ok and len(replay['receipts']) == 14 and replay['historical_wrapper_executed'] is False
            else:
                ok = (proc.returncode == 1 and not proc.stderr and data.get('status') == 'REJECTED'
                      and expected in data.get('reason', ''))
            if not ok:
                raise ValueError(label + ': ' + repr(data) + repr(proc.stderr))
            records.append({'label': label, 'mode': mode, 'expected': 'PASS' if expected is None else 'REJECTED',
                            'exit_code': proc.returncode, 'stdout_sha256': sha(proc.stdout),
                            'observed_reason': data.get('reason'), 'expectation_matched': True,
                            'finite_receipts': 14 if full else 0,
                            'positive_counts': {k: data[k] for k in ('outer_file_count', 'portable_member_count',
                                'original_file_count', 'preserved_root_original_count') if k in data}})
        def edit(root, name, raw):
            (root / name).write_bytes(raw)
            return reseal(root)
        for mode in ('normal', 'optimized'):
            execute('closed fixture', mode)
            execute('full relocated finite replay', mode, full=True)
            execute('dynamic published receipt', mode,
                    lambda r, p: edit(r, 'PUBLICATION_RECEIPT.json', encoded({'synthetic': True})))
            execute('external pin mismatch', mode, lambda r, p: '0' * 64, expected='external outer manifest pin mismatch')
            def duplicate(root, pin):
                raw = (root / 'PUBLICATION_MANIFEST.json').read_bytes()
                raw = raw.replace(b'{', b'{"schema":"bad",', 1)
                (root / 'PUBLICATION_MANIFEST.json').write_bytes(raw)
                return sha(raw)
            execute('duplicate JSON key', mode, duplicate, expected='duplicate JSON key')
            def boolean(root, pin):
                doc = json.loads((root / 'PUBLICATION_MANIFEST.json').read_bytes())
                doc['files'][0]['bytes'] = True
                raw = encoded(doc)
                (root / 'PUBLICATION_MANIFEST.json').write_bytes(raw)
                return sha(raw)
            execute('boolean inventory size', mode, boolean, expected='invalid pinned byte count')
            def unsafe(root, pin):
                doc = json.loads((root / 'PUBLICATION_MANIFEST.json').read_bytes())
                doc['files'][0]['path'] = '../escape'
                raw = encoded(doc)
                (root / 'PUBLICATION_MANIFEST.json').write_bytes(raw)
                return sha(raw)
            execute('unsafe inventory path', mode, unsafe, expected='unsafe relative path')
            def extra(root, pin):
                (root / 'extra.txt').write_bytes(b'unlisted')
                return pin
            execute('unlisted file', mode, extra, expected='unlisted file')
            def empty(root, pin):
                (root / 'extra empty directory').mkdir()
                return pin
            execute('unlisted empty directory', mode, empty, expected='unlisted directory')
            def missing(root, pin):
                (root / 'README.md').unlink()
                return pin
            execute('missing file', mode, missing, expected='missing inventory file')
            def alias(root, pin):
                (root / 'README.md').unlink()
                (root / 'README.md').symlink_to(root / 'RESEARCH_LOG.md')
                return pin
            execute('leaf symlink', mode, alias, expected='nonregular inventory entry')
            def fifo(root, pin):
                (root / 'README.md').unlink()
                os.mkfifo(root / 'README.md')
                return pin
            execute('FIFO before read', mode, fifo, expected='nonregular inventory entry')
            def verifier_mutant(root, pin):
                marker = root / 'MUST_NOT_EXECUTE.txt'
                raw = ('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text(\'executed\')\n').encode()
                (root / 'publication_20261015/preprint/verify_package.py').write_bytes(raw)
                (root / 'publication_20261015/verification_package/verify_package.py').write_bytes(raw)
                return reseal(root)
            execute('changed inner code before execution', mode, verifier_mutant, expected='pin mismatch: portable verify_package.py')
            if (td / (mode + ' changed inner code before execution') / 'MUST_NOT_EXECUTE.txt').exists():
                raise ValueError('untrusted inner verifier executed')
            execute('resealed metadata mismatch', mode,
                    lambda r, p: edit(r, 'CURRENT_PUBLICATION.json', encoded({'zenodo_metadata': {}})),
                    expected='current metadata copies differ')
            execute('resealed original root mismatch', mode,
                    lambda r, p: edit(r, 'PROOF.md', b'changed original'), expected='preserved root original mismatch')
            execute('resealed portable copy mismatch', mode,
                    lambda r, p: edit(r, 'publication_20261015/preprint/README.md', b'changed preprint'),
                    expected='preprint/portable copy mismatch')
            for label, options, reason in (
                    ('ZIP executable mode', {'bad_mode': True}, 'verification ZIP unsafe metadata'),
                    ('ZIP reverse order', {'reverse': True}, 'verification ZIP closed sorted member set'),
                    ('ZIP altered member', {'corrupt': True}, 'verification ZIP declared size mismatch')):
                execute(label, mode, lambda r, p, opts=options: edit(
                    r, 'publication_20261015/preprint/verification.zip', archive(portable, **opts)), expected=reason)
            execute('partial source options', mode, extras=('--catalog', '/nonexistent'),
                    expected='supply all four source locations or none')
            execute('sources require full', mode,
                    extras=('--catalog', '/a', '--problems', '/b', '--reports', '/c', '--pdf-dir', '/d'),
                    expected='source replay requires --full')
    result = {'status': 'PASS', 'scope': 'Focused synthetic-fixture outer wrapper validation; not final package, mathematical or priority acceptance.',
              'wrapper_sha256': sha(args.wrapper.read_bytes()), 'python': sys.version,
              'positive_runs': sum(r['expected'] == 'PASS' for r in records),
              'expected_rejections': sum(r['expected'] == 'REJECTED' for r in records),
              'full_replay_runs': sum(r['finite_receipts'] > 0 for r in records),
              'records': records, 'fixture_artifacts_retained': False}
    args.output.write_bytes(encoded(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
