#!/usr/bin/env python3
"""Freeze this verifier packet only; no source-tree mutation or program replay."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/source188189-sol-20261117/custody-verification')


def pin(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'md5': hashlib.md5(data).hexdigest()}


def put(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def main():
    read = json.loads((ROOT / 'CLOSURE_CODE_READ_RECEIPT.json').read_bytes())
    assert read['sha256'] == pin(Path(__file__))['sha256']
    assert not (ROOT / 'MANIFEST.json').exists() and not (ROOT / 'FINAL.json').exists()
    assert not (ROOT / 'FAILURE.json').exists()
    result = json.loads((ROOT / 'RESULT.json').read_bytes())
    process = json.loads((ROOT / 'FIRST_RUN_RECEIPT.json').read_bytes())
    assert result['status'] == 'PASS' and result['follow_up'] is None
    assert process['exit_code'] == 0 and process['execution_count'] == 1
    assert pin(ROOT / 'FIRST_RUN.stdout.txt') == process['stdout']
    assert pin(ROOT / 'FIRST_RUN.stderr.txt') == process['stderr']
    assert process['stderr']['bytes'] == 0
    when = datetime.now(timezone.utc).isoformat()
    with (ROOT / 'RESEARCH_LOG.md').open('a') as log:
        log.write(f'- {when}: Sole first run PASS, 6282 checks, exit 0 and empty stderr preserved literally. Source trees unchanged. Record 23203270: 95 payload files, 97 files including controls; record 23203081: 49 payload files, 51 files including controls; each 13 directories including root, 12 child directories. No mathematical interpretation or source-program execution. Completion estimate: 100%; follow-up operations null; quiescent after packet closure.\n')
    payload = []
    for child in sorted(ROOT.iterdir(), key=lambda item: item.name):
        info = child.lstat()
        assert stat.S_ISREG(info.st_mode), 'Verifier packet must contain only regular files'
        child.chmod(0o444)
        payload.append({'path': child.name, 'kind': 'file',
                        'mode_octal': oct(stat.S_IMODE(child.stat().st_mode)), **pin(child)})
    manifest = {'closed_utc': when,
        'scope': 'Complete finite verification payload; excludes MANIFEST.json and FINAL.json controls',
        'payload_file_count': len(payload), 'child_directory_count': 0,
        'root_mode_octal': oct(stat.S_IMODE(ROOT.stat().st_mode)), 'entries': payload}
    put(ROOT / 'MANIFEST.json', manifest)
    final = {'closed_utc': when, 'status': 'PASS', 'completion_percent': 100,
        'scope': 'Independent source custody verification only; no mathematical review',
        'checks_passed': result['checks_passed'], 'first_run_exit_code': 0,
        'first_run_execution_count': 1, 'first_run_stdout': process['stdout'],
        'first_run_stderr': process['stderr'],
        'manifest': {'path': 'MANIFEST.json', **pin(ROOT / 'MANIFEST.json')},
        'result': {'path': 'RESULT.json', **pin(ROOT / 'RESULT.json')},
        'payload_file_count': len(payload), 'total_files_including_controls': len(payload) + 2,
        'child_directory_count': 0,
        'source_counts': [{'record_id': item['record_id'],
            'payload_files_excluding_manifest_final': item['payload_file_count'],
            'actual_files_including_manifest_final': item['full_file_count_including_controls'],
            'directories_including_root': item['payload_directory_count_including_root'],
            'child_directories_excluding_root': item['payload_directory_count_including_root'] - 1,
            'archive_members': item['archive_member_count'],
            'embedded_pdfs': item['embedded_pdf_count'],
            'source_manifest': item['manifest_pin'], 'source_final': item['final_pin']}
            for item in result['records']],
        'source_trees_unchanged': True, 'follow_up': None, 'quiescent': True}
    put(ROOT / 'FINAL.json', final)
    (ROOT / 'MANIFEST.json').chmod(0o444)
    (ROOT / 'FINAL.json').chmod(0o444)
    print(json.dumps({'status': 'PASS', 'final': pin(ROOT / 'FINAL.json'),
                      'manifest': pin(ROOT / 'MANIFEST.json'),
                      'result': pin(ROOT / 'RESULT.json'),
                      'packet_total_files': len(payload) + 2,
                      'packet_child_directories': 0,
                      'source_counts': final['source_counts'],
                      'follow_up': None, 'quiescent': True}, indent=2))


if __name__ == '__main__':
    main()
