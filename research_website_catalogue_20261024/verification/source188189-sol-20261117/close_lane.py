#!/usr/bin/env python3
"""Freeze acquisition-lane receipts after independent custody verification.

This reads source objects as hashes/topology only and executes no source code.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat

LANE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/source188189-sol-20261117')


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def hashes(path):
    digest, md5, size = hashlib.sha256(), hashlib.md5(), 0
    with path.open('rb') as stream:
        while True:
            data = stream.read(1024 * 1024)
            if not data:
                break
            digest.update(data)
            md5.update(data)
            size += len(data)
    return {'bytes': size, 'sha256': digest.hexdigest(), 'md5': md5.hexdigest()}


def namespace(root, exclusions=()):
    output = []
    def visit(path):
        relative = path.relative_to(root).as_posix()
        if relative in exclusions:
            return
        info = path.lstat()
        item = {'path': relative, 'mode_octal': oct(stat.S_IMODE(info.st_mode))}
        if stat.S_ISDIR(info.st_mode):
            children = sorted(path.iterdir(), key=lambda p: p.name)
            item.update({'kind': 'directory', 'empty': not children})
            output.append(item)
            for child in children:
                visit(child)
        elif stat.S_ISREG(info.st_mode):
            item.update({'kind': 'file', **hashes(path)})
            output.append(item)
        else:
            raise ValueError('Unexpected link or special object: ' + str(path))
    visit(root)
    return sorted(output, key=lambda e: e['path'])


def new_json(path, data):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def main():
    independent = LANE / 'custody-verification' / 'FINAL.json'
    if not independent.is_file():
        raise ValueError('Independent custody verification final is required')
    independent_data = json.loads(independent.read_text())
    if hashes(independent)['sha256'] != '43139d039da02aa8cac5e84516ccb80cce7a4491768a4718968e6fac6a1814df':
        raise ValueError('Independent custody final differs from reported frozen pin')
    if (independent_data['status'] != 'PASS'
            or independent_data['completion_percent'] != 100
            or independent_data['first_run_exit_code'] != 0
            or independent_data['first_run_execution_count'] != 1
            or not independent_data['source_trees_unchanged']
            or independent_data['follow_up'] is not None
            or not independent_data['quiescent']):
        raise ValueError('Independent custody PASS and quiescence required')
    external = json.loads((LANE / 'EXTERNAL_SOURCE_PINS.json').read_text())
    sources = []
    for pin in external['records']:
        root = Path(pin['source_root'])
        manifest_path, final_path = root / 'SOURCE_MANIFEST.json', root / 'SOURCE_FINAL.json'
        if hashes(manifest_path) != pin['manifest'] or hashes(final_path) != pin['final']:
            raise ValueError('External source control pins changed')
        manifest = json.loads(manifest_path.read_text())
        actual = namespace(root, ('SOURCE_MANIFEST.json', 'SOURCE_FINAL.json'))
        if actual != manifest['entries']:
            raise ValueError('Source payload namespace changed after closure')
        complete = namespace(root)
        sources.append({'record_id': pin['record_id'], 'source_root': str(root),
            'source_manifest': hashes(manifest_path), 'source_final': hashes(final_path),
            'actual_total_files_including_two_control_files': sum(e['kind'] == 'file' for e in complete),
            'actual_directories_including_root': sum(e['kind'] == 'directory' for e in complete),
            'published_asset_count': pin['published_asset_count'],
            'archive_member_count': pin['archive_member_count'],
            'embedded_pdf_count': pin['embedded_pdf_count'],
            'outer_controlling_manuscript': pin['outer_controlling_manuscript']})
    completed = timestamp()
    with (LANE / 'RESEARCH_LOG.md').open('a') as log:
        log.write(f'- {completed}: Independent source-custody verification frozen; full source payload namespace and external control pins independently rehashed again at lane closure. Acquisition and custody goal completion estimate: 100%. Scientific review remains unstarted. All lane/source operations quiescent after this closure; follow-up operations null.\n')
    new_json(LANE / 'COMPLETION.json', {'completed_utc': completed,
        'status': 'source_acquisition_and_custody_complete',
        'completion_percent': 100, 'scientific_review_started': False,
        'native_scientific_programs_executed': False,
        'network_mutations': False, 'outreach': False,
        'independent_verification_final': {'path': str(independent), **hashes(independent)},
        'source_pins': sources, 'followup_operations': None})
    entries = namespace(LANE, ('MANIFEST.json', 'FINAL.json'))
    manifest = {'schema': 'finite-lane-manifest-v1', 'created_utc': completed,
        'root': str(LANE), 'scope': 'Every lane payload object including root, hidden files, ignored files and empty directories; only MANIFEST.json and FINAL.json are excluded control files.',
        'excluded_control_files': ['MANIFEST.json', 'FINAL.json'],
        'entries': entries,
        'payload_file_count': sum(e['kind'] == 'file' for e in entries),
        'directory_count_including_root': sum(e['kind'] == 'directory' for e in entries)}
    new_json(LANE / 'MANIFEST.json', manifest)
    final = {'closed_utc': completed, 'status': 'source_only_complete',
        'completion_percent': 100, 'source_records': [23203270, 23203081],
        'manifest': {'path': str(LANE / 'MANIFEST.json'), **hashes(LANE / 'MANIFEST.json')},
        'actual_total_lane_files_including_two_control_files': manifest['payload_file_count'] + 2,
        'directory_count_including_root': manifest['directory_count_including_root'],
        'source_pins': sources,
        'scientific_review': 'unstarted; no opinion or result supplied',
        'followup_operations': None, 'quiescent': True}
    new_json(LANE / 'FINAL.json', final)
    print(json.dumps({'final': hashes(LANE / 'FINAL.json'),
        'manifest': hashes(LANE / 'MANIFEST.json'),
        'actual_total_lane_files_including_two_control_files': final['actual_total_lane_files_including_two_control_files'],
        'directory_count_including_root': final['directory_count_including_root'],
        'source_pins': sources}, indent=2))


if __name__ == '__main__':
    main()
