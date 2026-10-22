#!/usr/bin/env python3
"""Disposable negative controls for the priority packet's custody interface."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def rehash(root):
    p = root / 'MANIFEST.json'
    d = json.loads(p.read_text())
    for row in d['files']:
        file = root / row['path']
        row.update(bytes=file.stat().st_size, sha256=sha(file))
    write_json(p, d)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--packet-root', required=True)
    p.add_argument('--intake-root', required=True)
    p.add_argument('--primary-root', required=True)
    p.add_argument('--expected-manifest-sha256', required=True)
    p.add_argument('--expected-checker-sha256', required=True)
    p.add_argument('--scratch', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    source = Path(a.packet_root).resolve(strict=True)
    intake = Path(a.intake_root).resolve(strict=True)
    primary = Path(a.primary_root).resolve(strict=True)
    scratch = Path(a.scratch).absolute()
    scratch.mkdir(exist_ok=False)
    if sha(source / 'MANIFEST.json') != a.expected_manifest_sha256:
        raise ValueError('original manifest bootstrap pin failed')
    if sha(source / 'verify_priority.py') != a.expected_checker_sha256:
        raise ValueError('original checker bootstrap pin failed')
    jobs = []
    for optimized in (False, True):
        for full in (False, True):
            jobs.append(('positive_' + str(optimized) + '_' + str(full),
                         source, intake, primary, full, optimized,
                         a.expected_manifest_sha256, True))

    negatives = [
        'packet_bytes', 'extra_file', 'missing_file', 'packet_symlink',
        'packet_hardlink', 'packet_fifo', 'root_symlink', 'ancestor_symlink',
        'input_bytes', 'input_symlink', 'external_bytes', 'external_fifo',
        'manifest_duplicate_key', 'manifest_traversal', 'manifest_duplicate_path',
        'manifest_nonfinite', 'rehashed_firstness', 'rehashed_wrong_problem',
        'rehashed_chronology', 'rehashed_mislabeled_article',
        'rehashed_wrong_authorship', 'rehashed_source_count',
        'rehashed_bad_passage', 'checker_pin',
    ]
    for name in negatives:
        case = scratch / name
        case.mkdir()
        packet = case / 'packet'
        shutil.copytree(source, packet)
        ri, rp = intake, primary
        full = name in ('external_bytes', 'external_fifo', 'rehashed_bad_passage')
        update_manifest_pin = False
        if name == 'packet_bytes':
            with (packet / 'REPORT.md').open('a') as f:
                f.write('alteration\n')
        elif name == 'extra_file':
            (packet / 'unexpected.txt').write_text('extra\n')
        elif name == 'missing_file':
            (packet / 'REPORT.md').unlink()
        elif name in ('packet_symlink', 'packet_hardlink', 'packet_fifo'):
            dst = packet / 'REPORT.md'
            dst.unlink()
            if name == 'packet_symlink':
                dst.symlink_to(source / 'REPORT.md')
            elif name == 'packet_hardlink':
                donor = case / 'disposable_hardlink_target'
                shutil.copyfile(source / 'REPORT.md', donor)
                os.link(donor, dst)
            else:
                os.mkfifo(dst)
        elif name == 'root_symlink':
            link = case / 'rootlink'
            link.symlink_to(packet, target_is_directory=True)
            packet = link
        elif name == 'ancestor_symlink':
            link = case / 'ancestor'
            link.symlink_to(case, target_is_directory=True)
            packet = link / 'packet'
        elif name in ('input_bytes', 'input_symlink'):
            ri = case / 'intake'
            rows = json.loads((source / 'INPUT_BINDINGS.json').read_text())['files']
            for row in rows:
                dst = ri / row['path']
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(intake / row['path'], dst)
            dst = ri / 'SELECTED_PUBLIC_RECORD.json'
            if name == 'input_bytes':
                with dst.open('a') as f:
                    f.write(' ')
            else:
                dst.unlink()
                dst.symlink_to(intake / 'SELECTED_PUBLIC_RECORD.json')
        elif name in ('external_bytes', 'external_fifo'):
            rp = case / 'primary'
            rp.mkdir()
            rows = json.loads((source / 'EXTERNAL_BINDINGS.json').read_text())['files']
            for row in rows:
                shutil.copyfile(primary / row['path'], rp / row['path'])
            dst = rp / 'RS_journal.pdf'
            if name == 'external_bytes':
                with dst.open('ab') as f:
                    f.write(b' ')
            else:
                dst.unlink()
                os.mkfifo(dst)
        elif name.startswith('manifest_'):
            path = packet / 'MANIFEST.json'
            d = json.loads(path.read_text())
            if name == 'manifest_duplicate_key':
                path.write_text(path.read_text().replace('{', '{"schema": "duplicate",', 1))
            elif name == 'manifest_nonfinite':
                path.write_text(path.read_text().replace('30001478', 'NaN', 1))
            elif name == 'manifest_traversal':
                d['files'][0]['path'] = '../outside'
                write_json(path, d)
            else:
                d['files'].append(d['files'][0].copy())
                write_json(path, d)
            update_manifest_pin = True
        elif name.startswith('rehashed_'):
            file, key, value = {
                'rehashed_firstness': ('VERDICT.json', 'novelty_or_firstness_claimed', True),
                'rehashed_wrong_problem': ('VERDICT.json', 'problem', 1),
                'rehashed_chronology': ('ORIGINAL_AUDIT_COMPARISON.json', 'timestamp_utc',
                                       '2000-01-01T00:00:00+00:00'),
                'rehashed_mislabeled_article': ('PRIMARY_SOURCES.json', None, None),
                'rehashed_wrong_authorship': ('PRIMARY_SOURCES.json', None, None),
                'rehashed_source_count': ('PRIMARY_SOURCES.json', 'valid_pdf_retrievals', 23),
                'rehashed_bad_passage': ('PASSAGE_LOCATORS.json', None, None),
            }[name]
            path = packet / file
            d = json.loads(path.read_text())
            if key:
                d[key] = value
            elif name == 'rehashed_bad_passage':
                d['pages'][0]['extracted_page_sha256'] = '0' * 64
            else:
                target = 'NS_accepted' if name == 'rehashed_mislabeled_article' else 'Homological'
                for row in d['sources']:
                    if row['name'] == target:
                        row['reading_scope' if target == 'NS_accepted' else 'version'] = 'Wrong'
            write_json(path, d)
            rehash(packet)
            update_manifest_pin = True
        elif name == 'checker_pin':
            with (packet / 'verify_priority.py').open('a') as f:
                f.write('\n')
        mf = sha(packet / 'MANIFEST.json') if update_manifest_pin else a.expected_manifest_sha256
        jobs.append((name, packet, ri, rp, full, False, mf, False))

    def run(job):
        name, packet, ri, rp, full, optimized, mf, expected = job
        cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else [])
        cmd += [str(packet / 'verify_priority.py'), '--packet-root', str(packet),
                '--intake-root', str(ri), '--expected-manifest-sha256', mf,
                '--expected-checker-sha256', a.expected_checker_sha256]
        if full:
            cmd += ['--primary-root', str(rp)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        success = r.returncode == 0
        result = json.loads(r.stdout)
        return {'name': name, 'expected_success': expected, 'success': success,
                'pass': success == expected, 'checker_result': result}
    results = list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(run, jobs))
    summary = {'status': 'PASS' if all(x['pass'] for x in results) else 'FAIL',
               'positive_controls': 4, 'negative_controls': len(negatives),
               'results': results, 'original_manifest_unchanged':
               sha(source / 'MANIFEST.json') == a.expected_manifest_sha256,
               'original_checker_unchanged':
               sha(source / 'verify_priority.py') == a.expected_checker_sha256}
    write_json(Path(a.output), summary)
    print(json.dumps({k: v for k, v in summary.items() if k != 'results'}, sort_keys=True))
    if summary['status'] != 'PASS':
        sys.exit(1)


if __name__ == '__main__':
    main()
