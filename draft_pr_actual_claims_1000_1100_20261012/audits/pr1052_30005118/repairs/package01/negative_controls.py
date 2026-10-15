#!/usr/bin/env python3
"""Bounded P3 repair controls; no mathematics or hostile-files policy tests."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

AUDIT = Path(__file__).resolve().parents[2]
ROOT = AUDIT / 'preprint_v1_0'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    spec = importlib.util.spec_from_file_location('repair_verifier', ROOT/'verify_support.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    canonical = json.loads((ROOT/'.zenodo.json').read_text())
    wrapper = json.loads((ROOT/'metadata.json').read_text())
    descriptor = json.loads((ROOT/'zenodo-deposit.json').read_text())
    results = []
    scratch = Path(__file__).resolve().parent/'private/scratch'
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='controls-', dir=scratch) as temp:
        work = Path(temp)
        module.ROOT = work
        members = json.loads((ROOT/'SUPPORT_ALLOWLIST.json').read_text())['members']
        for name in members + ['zenodo-deposit.json', 'pr1052_support_v1_0.zip', 'pr1052_support_v1_0.zip.sha256']:
            dest = work/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/name, dest)

        def write_surfaces(z, w, d):
            for name, data in [('.zenodo.json', z), ('metadata.json', w), ('zenodo-deposit.json', d)]:
                (work/name).write_text(json.dumps(data, indent=2)+'\n')

        def reject(label, call):
            try:
                call()
            except (ValueError, KeyError, TypeError) as exc:
                results.append({'control': label, 'rejected': True, 'reason': str(exc)})
            else:
                raise RuntimeError('invalid control accepted: '+label)

        write_surfaces(canonical, wrapper, descriptor)
        require(module.verify_metadata() == canonical, 'current metadata not accepted')
        require(module.verify_upload_if_present() == 'present, metadata and both upload files verified', 'current strict bindings not accepted')
        variants = []
        for label, value in [('undated_matching_notes', 'This metadata is prepared locally; no deposit or publication occurred.'), ('wrong_matching_notes_date', 'Prepared locally on 2026-10-13 before deposit or publication.')]:
            z = copy.deepcopy(canonical)
            z['notes'] = z['notes'].rsplit('Prepared locally on ', 1)[0]+value
            w = copy.deepcopy(wrapper); w['metadata'] = z
            d = copy.deepcopy(descriptor); d['metadata'] = z
            variants.append((label, z, w, d))
        for label, key, value in [('wrong_stage', 'stage', 'PENDING_NEW_WHOLE_01'), ('wrong_snapshot_date', 'preparation_snapshot_date', '2026-10-13'), ('publication_flag_true', 'publication_ready', True), ('issues_flag_true', 'all_issues_resolved', True)]:
            w = copy.deepcopy(wrapper); w[key] = value
            variants.append((label, canonical, w, descriptor))
        w = copy.deepcopy(wrapper); w.pop('stage')
        variants.append(('missing_stage', canonical, w, descriptor))
        z = copy.deepcopy(canonical); z['notes'] += ' changed'
        variants.append(('bare_metadata_mismatch', z, wrapper, descriptor))
        w = copy.deepcopy(wrapper); w['metadata']['notes'] += ' changed'
        variants.append(('wrapped_metadata_mismatch', canonical, w, descriptor))
        for label, z, w, d in variants:
            write_surfaces(z, w, d)
            reject(label, module.verify_metadata)
        write_surfaces(canonical, wrapper, descriptor)
        for index, name in [(0, 'pdf'), (1, 'zip')]:
            for key, value in [('bytes', descriptor['files'][index]['bytes']+1), ('sha256', '0'*64)]:
                d = copy.deepcopy(descriptor); d['files'][index][key] = value
                write_surfaces(canonical, wrapper, d)
                reject(name+'_wrong_'+key, module.verify_upload_if_present)
        d = copy.deepcopy(descriptor); d['metadata']['notes'] += ' changed'
        write_surfaces(canonical, wrapper, d)
        reject('external_metadata_mismatch', module.verify_upload_if_present)

        # Recompute the manifest to isolate the metadata gate from file hashing.
        build_receipts = []
        for label, z, w, d in variants[:3]:
            write_surfaces(z, w, d)
            m = json.loads((ROOT/'SUPPORT_MANIFEST.json').read_text())
            for e in m['entries']:
                data = (work/e['path']).read_bytes()
                e['bytes'] = len(data); e['sha256'] = hashlib.sha256(data).hexdigest()
            (work/'SUPPORT_MANIFEST.json').write_text(json.dumps(m, indent=2)+'\n')
            argv = [sys.executable, '-I', '-B'] + (['-O'] if sys.flags.optimize else []) + ['build_support.py', '--output', '_runs/rejected.zip']
            proc = subprocess.run(argv, cwd=work, capture_output=True, timeout=60)
            require(proc.returncode != 0 and not (work/'_runs/rejected.zip').exists(), 'bad-stage metadata built: '+label)
            build_receipts.append({'control': label, 'argv': ['python3', '-I', '-B'] + (['-O'] if sys.flags.optimize else []) + ['build_support.py', '--output', '_runs/rejected.zip'], 'exit_code': proc.returncode, 'stdout': proc.stdout.decode(), 'stderr': proc.stderr.decode(), 'archive_not_created': True})
    print(json.dumps({'all_checks_passed': True, 'accepted_current_metadata_and_strict_two_file_binding_controls': 2, 'metadata_and_binding_rejections': results, 'bad_metadata_build_rejections_with_valid_manifest': build_receipts}, sort_keys=True))


if __name__ == '__main__':
    main()
