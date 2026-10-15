#!/usr/bin/env python3
"""Reproducible engineering probes, not manuscript or mathematical acceptance.
Authenticate this harness/templates independently. Use -I -S -B; repeat with -O.
No original is changed. All mutation/reseal/build fixtures are temporary.
"""
import argparse
from collections import Counter
import datetime
import hashlib
import importlib.util
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


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--original-base', type=Path, required=True)
    p.add_argument('--templates', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--full-sources', action='store_true')
    p.add_argument('--repo', type=Path)
    args = p.parse_args()
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, 'use -I -S -B')
    base, engine = args.original_base.resolve(), args.templates.resolve()
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    records = []
    def record(name, kind, **data):
        records.append(dict(name=name, classification=kind, **data))
    code = {n: (engine / n).read_bytes() for n in ('check_originals.py', 'verify_package.py', 'build_verification.py')}
    with tempfile.TemporaryDirectory(prefix='PR872 template engineering probes ') as td:
        top = Path(td)
        trusted = top / 'trusted code'
        trusted.mkdir()
        for name, raw in code.items():
            (trusted / name).write_bytes(raw)
        module_spec = importlib.util.spec_from_file_location('reviewed_engine', trusted / 'check_originals.py')
        mod = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(mod)
        template = top / 'baseline assembly'
        template.mkdir()
        shutil.copytree(base / 'source', template / 'source')
        (template / 'root_evidence').mkdir()
        shutil.copyfile(base / 'SOURCE_MANIFEST.json', template / 'root_evidence/SOURCE_MANIFEST.json')
        for name, raw in code.items():
            (template / name).write_bytes(raw)
        (template / 'README.md').write_text('ENGINEERING FIXTURE ONLY; no paper or acceptance.\n')
        def seal(folder):
            rows = []
            for item in sorted(folder.rglob('*')):
                if item.is_file() and item.name != 'package_index.json':
                    raw = item.read_bytes()
                    rows.append(dict(path=item.relative_to(folder).as_posix(), bytes=len(raw), sha256=sha(raw)))
            data = dump(dict(schema='random-property-t-verification-v1', problem_id='30006628', files=rows))
            (folder / 'package_index.json').write_bytes(data)
            return sha(data)
        index_pin = seal(template)
        mod.original_inputs(template)
        record('authenticate frozen baseline', 'positive_control', files=15, outer=14, members=26)
        serial = 0
        def fixture():
            nonlocal serial
            serial += 1
            folder = top / ('mutation ' + str(serial))
            shutil.copytree(template, folder)
            return folder
        def run(name, folder, extra=(), timeout=30):
            return subprocess.run([sys.executable, *flags, str(trusted / name), *map(str, extra)],
                                  cwd=folder, capture_output=True, timeout=timeout)
        def check_rejection(proc, fragment):
            need(proc.returncode == 1 and not proc.stderr, 'unexpected rejection process: ' + repr(proc.stderr))
            data = json.loads(proc.stdout)
            need(data.get('status') == 'REJECTED' and fragment in data.get('reason', ''),
                 'wrong rejection: ' + repr(data) + ' expected ' + fragment)
            return data['reason']
        def reject(name, script, folder, extra, fragment, kind='ordinary_expected_rejection'):
            reason = check_rejection(run(script, folder, extra), fragment)
            record(name, kind, reason=reason)
        def original_reject(name, folder, fragment):
            reject(name, 'check_originals.py', folder, ['--root', folder, '--verify-only'], fragment)
        def portable_reject(name, folder, pin, fragment, full=False, kind='ordinary_expected_rejection'):
            extra = [pin, '--root', folder] + (['--full'] if full else [])
            reject(name, 'verify_package.py', folder, extra, fragment, kind)
        # Full diagnostics are run once per harness, internally in both child modes.
        proc = run('verify_package.py', template, [index_pin, '--root', template, '--full'], timeout=700)
        need(proc.returncode == 0 and not proc.stderr, 'finite replay baseline')
        full = json.loads(proc.stdout)
        replay = full['full_replay']
        need(len(replay['receipts']) == 14 and Counter(x['kind'] for x in replay['receipts']) == {'positive': 6, 'negative': 8}, 'default receipt count')
        record('portable full finite replay', 'positive_control', result=full)
        for row in json.loads((base / 'SOURCE_MANIFEST.json').read_bytes())['files']:
            folder = fixture()
            path = folder / 'source' / row['path']
            raw = path.read_bytes()
            path.write_bytes(bytes([raw[0] ^ 1]) + raw[1:])
            original_reject('frozen corruption ' + row['path'], folder, 'pin mismatch:')
        for kind in ('extra file', 'empty directory', 'missing', 'leaf symlink', 'internal directory symlink', 'FIFO', 'directory leaf', 'changed bytes'):
            folder = fixture()
            path = folder / 'README.md'
            if kind == 'extra file':
                (folder / 'EXTRA').write_text('extra')
                fragment = 'unlisted file:'
            elif kind == 'empty directory':
                (folder / 'EMPTY').mkdir()
                fragment = 'unlisted directory:'
            elif kind == 'internal directory symlink':
                shutil.rmtree(folder / 'source')
                (folder / 'source').symlink_to(template / 'source', target_is_directory=True)
                fragment = 'nonregular inventory entry:'
            else:
                path.unlink()
                if kind == 'missing': fragment = 'missing inventory file'
                elif kind == 'leaf symlink':
                    path.symlink_to(template / 'README.md'); fragment = 'nonregular inventory entry:'
                elif kind == 'FIFO':
                    os.mkfifo(path); fragment = 'nonregular inventory entry:'
                elif kind == 'directory leaf':
                    path.mkdir(); fragment = 'unlisted directory:'
                else:
                    path.write_text('wrong bytes'); fragment = 'byte count mismatch:'
            portable_reject('closed inventory ' + kind, folder, index_pin, fragment)
        for kind in ('duplicate keys', 'nonfinite', 'overflow number', 'duplicate path', 'traversal', 'absolute', 'backslash', 'dot', 'empty', 'boolean bytes', 'wrong schema', 'wrong problem', 'file directory collision', 'missing startup'):
            folder = fixture()
            obj = json.loads((folder / 'package_index.json').read_bytes())
            if kind == 'duplicate keys':
                raw = dump(obj).replace(b'"problem_id": "30006628",', b'"problem_id": "30006628", "problem_id": "30006628",')
                fragment = 'duplicate JSON key:'
            elif kind == 'nonfinite':
                raw = dump(obj).replace(b'"problem_id": "30006628"', b'"problem_id": NaN')
                fragment = 'nonfinite JSON constant:'
            elif kind == 'overflow number':
                raw = dump(obj).replace(b'\"problem_id\": \"30006628\"', b'\"problem_id\": 1e999')
                fragment = 'nonfinite JSON number'
            else:
                if kind == 'duplicate path': obj['files'].append(obj['files'][0]); fragment = 'duplicate inventory path'
                elif kind in ('traversal', 'absolute', 'backslash', 'dot', 'empty'):
                    obj['files'][0]['path'] = {'traversal': '../evil', 'absolute': '/evil', 'backslash': 'a\\b', 'dot': 'a/./b', 'empty': 'a//b'}[kind]
                    fragment = 'unsafe relative path'
                elif kind == 'boolean bytes': obj['files'][0]['bytes'] = True; fragment = 'invalid pinned byte count'
                elif kind == 'wrong schema': obj['schema'] = 'other'; fragment = 'portable index identity/schema'
                elif kind == 'wrong problem': obj['problem_id'] = 'other'; fragment = 'portable index identity/schema'
                elif kind == 'file directory collision':
                    obj['files'].append(dict(path='source', bytes=0, sha256=sha(b''))); fragment = 'file/directory inventory collision'
                elif kind == 'missing startup':
                    obj['files'] = [r for r in obj['files'] if r['path'] != 'verify_package.py']; fragment = 'portable inventory required files'
                raw = dump(obj)
            (folder / 'package_index.json').write_bytes(raw)
            portable_reject('artificially resealed index ' + kind, folder, sha(raw), fragment,
                            kind='artificially_resealed_parser_rejection')
        # Tampered checker must never run even with --full.
        folder = fixture()
        marker = top / 'CHECKER_MARKER_MUST_NOT_EXIST'
        (folder / 'check_originals.py').write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n')
        portable_reject('substituted checker marker', folder, index_pin, 'byte count mismatch:', full=True,
                        kind='startup_rejection_before_execution')
        need(not marker.exists(), 'checker marker executed')
        for kind in ('index FIFO', 'startup FIFO', 'changed startup marker', 'changed index marker', 'output inside', 'nonempty output', 'output symlink'):
            folder = fixture()
            pin = index_pin
            startup_pin = sha(code['verify_package.py'])
            out = top / ('builder output ' + str(serial))
            if kind == 'index FIFO':
                (folder / 'package_index.json').unlink(); os.mkfifo(folder / 'package_index.json'); fragment = 'nonregular input:'
            elif kind == 'startup FIFO':
                (folder / 'verify_package.py').unlink(); os.mkfifo(folder / 'verify_package.py'); fragment = 'nonregular inventory entry:'
            elif kind in ('changed startup marker', 'changed index marker'):
                marker = top / (kind + ' MUST_NOT_EXIST')
                (folder / 'verify_package.py').write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n')
                newpin = seal(folder)
                if kind == 'changed startup marker': pin = newpin; fragment = 'startup verifier external pin mismatch'
                else: fragment = 'external index pin mismatch'
            elif kind == 'output inside': out = folder / 'out'; fragment = 'output must be outside assembly'
            elif kind == 'nonempty output':
                out.mkdir(); (out / 'keep').write_text('preserve'); fragment = 'output must be fresh or empty'
            else:
                target = top / ('real output ' + str(serial)); target.mkdir(); out.symlink_to(target, target_is_directory=True)
                fragment = 'output directory leaf alias'
            reject('builder ' + kind, 'build_verification.py', folder, [folder, pin, startup_pin, out], fragment,
                   'startup_rejection_before_execution' if 'marker' in kind or 'FIFO' in kind else 'ordinary_expected_rejection')
            if 'marker' in kind: need(not marker.exists(), 'builder startup marker executed')
        folder = fixture()
        reject('incomplete source arguments', 'check_originals.py', folder,
               ['--root', folder, '--catalog', top / 'unused'], 'supply all four source locations or none')
        (top / 'unused PDF directory').mkdir()
        for kind in ('FIFO', 'leaf symlink'):
            supplied = top / ('supplied catalog ' + kind)
            if kind == 'FIFO': os.mkfifo(supplied)
            else: supplied.symlink_to(template / 'README.md')
            extra = ['--root', folder, '--catalog', supplied, '--problems', top / 'unused1', '--reports', top / 'unused2', '--pdf-dir', top / 'unused PDF directory', '--verify-only']
            reject('source catalog ' + kind, 'check_originals.py', folder, extra, 'nonregular input:')
        # Artificially replace the frozen manifest trust anchor to reach ZIP parser branches.
        # These are semantic guard tests, never attacks succeeding against the fixed pin.
        def reseal_original(folder):
            manifest = json.loads((folder / 'root_evidence/SOURCE_MANIFEST.json').read_bytes())
            for row in manifest['files']:
                raw = (folder / 'source' / row['path']).read_bytes()
                row.update(bytes=len(raw), sha256=sha(raw), git_blob=hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest())
            raw = dump(manifest)
            (folder / 'root_evidence/SOURCE_MANIFEST.json').write_bytes(raw)
            return sha(raw)
        def refresh_outer(folder):
            path = folder / 'source/PUBLICATION_MANIFEST.json'
            outer = json.loads(path.read_bytes())
            for row in outer['files']:
                raw = (folder / 'source' / row['path']).read_bytes()
                row.update(bytes=len(raw), sha256=sha(raw))
            path.write_bytes(dump(outer))
        archive, extname, _ = mod.BUNDLES[0]
        for kind in ('FIFO mode', 'device mode', 'symlink mode', 'executable mode', 'duplicate member', 'extra member', 'traversal member'):
            folder = fixture()
            path = folder / 'source' / archive
            extpath = folder / 'source' / extname
            ext = json.loads(extpath.read_bytes())
            with zipfile.ZipFile(path) as z:
                items = [(i.filename, z.read(i)) for i in z.infolist()]
            first_name, first_data = items[0]
            if kind == 'extra member':
                items.append(('extra/file.txt', b'extra'))
                ext['members'].append(dict(path='extra/file.txt', bytes=5, sha256=sha(b'extra')))
            if kind == 'traversal member':
                items[0] = ('../evil', first_data)
                ext['members'][0]['path'] = '../evil'
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as z:
                for i, (name, raw) in enumerate(items):
                    info = zipfile.ZipInfo(name)
                    mode = stat.S_IFREG | 0o644
                    if i == 0:
                        mode = {'FIFO mode': stat.S_IFIFO | 0o600, 'device mode': stat.S_IFCHR | 0o600,
                                'symlink mode': stat.S_IFLNK | 0o777, 'executable mode': stat.S_IFREG | 0o755}.get(kind, mode)
                    info.external_attr = mode << 16
                    z.writestr(info, raw)
                if kind == 'duplicate member':
                    # zipfile warns to stderr on duplicate; silence only fixture-authoring warning.
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', UserWarning)
                        z.writestr(first_name, first_data)
            raw = buffer.getvalue()
            path.write_bytes(raw)
            ext['zip'].update(bytes=len(raw), sha256=sha(raw))
            extpath.write_bytes(dump(ext))
            refresh_outer(folder)
            saved = mod.SOURCE_MANIFEST_SHA256
            mod.SOURCE_MANIFEST_SHA256 = reseal_original(folder)
            try:
                mod.original_inputs(folder)
                raise RuntimeError('resealed unsafe ZIP accepted')
            except ValueError as exc:
                expected = ('unsafe relative path' if kind == 'traversal member' else
                            'archive member count' if kind == 'extra member' else
                            'archive member set' if kind == 'duplicate member' else 'nonregular or unsafe ZIP metadata')
                need(expected in str(exc), 'wrong resealed ZIP rejection: ' + str(exc))
                record('resealed ZIP ' + kind, 'artificially_resealed_parser_rejection', reason=str(exc))
            finally:
                mod.SOURCE_MANIFEST_SHA256 = saved
        # Root directory aliases are an explicit allowed policy; inside-tree aliases are rejected.
        alias = top / 'root directory alias'
        alias.symlink_to(template, target_is_directory=True)
        proc = run('verify_package.py', template, [index_pin, '--root', alias])
        need(proc.returncode == 0 and not proc.stderr, 'documented root alias policy')
        record('root directory alias', 'positive_control', permitted=True)
        builds = []
        for suffix in ('one', 'two'):
            out = top / ('fixture rebuild ' + suffix)
            proc = run('build_verification.py', template, [template, index_pin, sha(code['verify_package.py']), out], timeout=700)
            need(proc.returncode == 0 and not proc.stderr, 'fixture builder failed: ' + proc.stdout.decode())
            result = json.loads(proc.stdout)
            builds.append((out / 'verification.zip').read_bytes())
            with zipfile.ZipFile(io.BytesIO(builds[-1])) as z:
                need(len(z.infolist()) == len(json.loads((template / 'package_index.json').read_bytes())['files']) + 1, 'dynamic member count')
                need(all(i.date_time == (2026, 10, 15, 0, 0, 0) and i.external_attr >> 16 == stat.S_IFREG | 0o644 for i in z.infolist()), 'canonical ZIP metadata')
            record('fixture deterministic build ' + suffix, 'positive_control', sha256=result['sha256'], bytes=result['bytes'])
        need(builds[0] == builds[1], 'fixture rebuild bytes differ')
        record('byte-identical same-runtime rebuild', 'positive_control', sha256=sha(builds[0]))
        if args.full_sources:
            need(args.repo is not None, '--repo required with --full-sources')
            repo = args.repo.resolve()
            locations = {'catalog': repo / 'unsolved_math_prioritization/catalog.json',
                         'problems': repo / 'unsolved_math_prioritization/cache/problems.json',
                         'reports': repo / 'unsolved_math_prioritization/cache/research_results.json',
                         'pdf-dir': base / 'private_sources'}
            extra = [index_pin, '--root', template, '--full']
            for name, value in locations.items(): extra += ['--' + name, value]
            proc = run('verify_package.py', template, extra, timeout=700)
            need(proc.returncode == 0 and not proc.stderr, 'optional full source replay failed: ' + proc.stdout.decode())
            result = json.loads(proc.stdout)
            replay = result['full_replay']
            need(len(replay['receipts']) == 20 and Counter(x['kind'] for x in replay['receipts']) == {'positive': 8, 'negative': 12}, 'full source receipt counts')
            record('optional original provenance replay', 'positive_control', result=result)
            # All three corpus leaves and each of six PDF leaves get FIFO and alias probes.
            _, members, _ = mod.original_inputs(template)
            pins = json.loads(members['random_property_t_30006628/sources.json'])
            source_data = dict(catalog=locations['catalog'], problems=locations['problems'], reports=locations['reports'], pdf_dir=locations['pdf-dir'])
            for key in ('catalog', 'problems', 'reports'):
                for kind in ('FIFO', 'symlink'):
                    path = top / ('source leaf ' + key + ' ' + kind)
                    if kind == 'FIFO': os.mkfifo(path)
                    else: path.symlink_to(source_data[key])
                    data = dict(source_data, **{key: path})
                    try:
                        mod.supplied_inputs(members, data)
                        raise RuntimeError('unsafe source accepted')
                    except ValueError as exc:
                        need('nonregular input:' in str(exc), 'source guard rejection')
                        record(key + ' ' + kind, 'ordinary_expected_rejection', reason=str(exc))
            for row in pins['primary_sources']:
                for kind in ('FIFO', 'symlink'):
                    folder = top / ('PDF input ' + str(serial) + row['filename'] + kind)
                    folder.mkdir()
                    for item in pins['primary_sources']:
                        target = folder / item['filename']
                        if item['filename'] == row['filename']:
                            if kind == 'FIFO': os.mkfifo(target)
                            else: target.symlink_to(locations['pdf-dir'] / item['filename'])
                        else: shutil.copyfile(locations['pdf-dir'] / item['filename'], target)
                    try:
                        mod.supplied_inputs(members, dict(source_data, pdf_dir=folder))
                        raise RuntimeError('unsafe PDF accepted')
                    except ValueError as exc:
                        need('nonregular input:' in str(exc), 'PDF guard rejection')
                        record(row['filename'] + ' ' + kind, 'ordinary_expected_rejection', reason=str(exc))
    result = dict(status='PASS', timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  harness_mode='optimized' if sys.flags.optimize else 'normal',
                  template_sha256={n: sha(v) for n, v in code.items()},
                  original_source_manifest_sha256=mod.SOURCE_MANIFEST_SHA256,
                  classification_counts=dict(Counter(r['classification'] for r in records)), records=records,
                  full_sources=args.full_sources, no_publication_acceptance=True,
                  probe_scope='Engineering fixture only. Resealed parser probes deliberately change trusted pins, not successful external-pin attacks. Diagnostic receipts are not asymptotic proof.')
    args.output.write_bytes(dump(result))
    print(json.dumps({k: result[k] for k in ('status', 'harness_mode', 'classification_counts', 'full_sources')}, sort_keys=True))


if __name__ == '__main__':
    main()
