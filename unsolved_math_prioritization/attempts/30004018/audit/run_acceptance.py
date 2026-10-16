#!/usr/bin/env python3
"""Run source-free acceptance checks; originals are read-only inputs.

Usage: run_acceptance.py ORIGINAL_PACKET OUTPUT_JSON [SOURCE_PDF_DIRECTORY]
The output contains complete subprocess stdout/stderr and exact return codes.
Temporary mutation packets contain authored files only, never source documents.
"""
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_frozen import EXPECTED, verify

PDF_PINS = {
    'owr52_2018.pdf': (756610, 'b33ed36eaa470877bc6cfb5b45b1019564f568925ea9d94e8dc7ee355879976e'),
    'hps1712.00664v4.pdf': (404925, '1c8bb4b2f5481a68a3024114cbd94a15cad9bff0d02010eff53a17488b632ac4'),
    'hps_author.pdf': (556643, '34a0b69fd3074ea7360576138007ec225a3c08d3e2b6f08aedeb5ae148a3af95'),
    'cs_categoryo.pdf': (454056, '31be45045f6a3e6c7c6226f81572831591509246e64b2ead161d5d973bc4a6f2'),
    'ghss2203.00529v2.pdf': (726131, 'ae9d629d21c0174bf27049684fbede994f83e91dfde3bccf9f8a8bdc902a4e3e'),
    'hirota2603.01390v1.pdf': (379972, '2a21dc12bac85e8ee6861488c255be0921561d44ca25d0849a84d7ff93bb5ca9'),
    'hirota2603.01390_current.pdf': (406666, '2526e144536fab7afbe762d49f6b51cf3c8ac1c26424bc4455afe10f0209ce4e'),
}
MUTATIONS = [
    'exterior-sign', 'wrong-weight', 'wrong-parity', 'class-implies-object',
    'wrong-moment', 'drop-total-arrow', 'action-rank-is-algebra-rank', 'omit-Koszul-sign',
]


def check(test, label):
    if not test:
        raise RuntimeError(label)


def run(command, display_command, expected_returncode):
    p = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    check(p.returncode == expected_returncode,
          f'{display_command}: return code {p.returncode}, expected {expected_returncode}; {p.stdout}; {p.stderr}')
    return {'command': display_command, 'returncode': p.returncode,
            'expected_returncode': expected_returncode, 'stdout': p.stdout, 'stderr': p.stderr}


def snapshot(packet):
    return {'directory_mode': oct(stat.S_IMODE(packet.stat().st_mode)),
            'files': {name: dict(info, mode=oct(stat.S_IMODE((packet / name).stat().st_mode)))
                      for name, info in verify(packet).items()}}


def main():
    if len(sys.argv) not in (3, 4):
        raise RuntimeError(__doc__)
    packet, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    check(os.getuid() == os.geteuid() == 1000, 'runner requires actual/effective UID 1000')
    check(packet not in output.parents, 'output must be outside original packet')
    receipt = {'status': 'RUNNING', 'checked_on_utc_date': '2026-10-08',
               'uid': os.getuid(), 'euid': os.geteuid(), 'python': sys.version,
               'original_packet': 'frozen_v2', 'external_pin_scope': 'all six files including original manifest',
               'before': snapshot(packet), 'read_only_probes': [], 'runs': [],
               'pin_negative_controls': [], 'source_pdf_checks': []}
    check(receipt['before']['directory_mode'] == '0o555', 'original directory not mode 555')
    check(all(x['mode'] == '0o444' for x in receipt['before']['files'].values()),
          'original files not mode 444')
    probes = [('create_new_file', packet / '.independent_audit_write_probe',
               os.O_WRONLY | os.O_CREAT | os.O_EXCL),
              ('open_existing_for_append', packet / 'MATHEMATICAL_AUDIT.md', os.O_WRONLY | os.O_APPEND)]
    for label, path, flags in probes:
        try:
            fd = os.open(path, flags, 0o600)
        except OSError as exc:
            check(exc.errno in (errno.EACCES, errno.EPERM, errno.EROFS), 'wrong denial errno')
            receipt['read_only_probes'].append({'operation': label, 'denied': True,
                                                'errno': exc.errno, 'error': os.strerror(exc.errno)})
        else:
            os.close(fd)
            if label == 'create_new_file':
                path.unlink()
            raise RuntimeError('read-only probe unexpectedly permitted: ' + label)
    modes = [([], 'normal'), (['-O'], '-O'), (['-OO'], '-OO')]
    for flags, label in modes:
        receipt['runs'].append(run([sys.executable, *flags, '-B', str(packet / 'check_examples.py')],
                                   ['python3', *flags, '-B', 'frozen_v2/check_examples.py'], 0))
        receipt['runs'].append(run([sys.executable, *flags, '-B', str(HERE / 'independent_checks.py')],
                                   ['python3', *flags, '-B', 'independent_checks.py'], 0))
        for mutation in MUTATIONS:
            receipt['runs'].append(run([sys.executable, *flags, '-B', str(HERE / 'independent_checks.py'),
                                       '--mutation', mutation],
                                      ['python3', *flags, '-B', 'independent_checks.py', '--mutation', mutation], 1))
    with tempfile.TemporaryDirectory(prefix='duflo_authored_pin_controls_') as temporary:
        for mutation in ('modified_body', 'body_and_internal_manifest', 'missing_file', 'extra_file', 'symlink'):
            copied = Path(temporary) / mutation
            shutil.copytree(packet, copied)
            copied.chmod(0o755)
            for p in copied.iterdir():
                p.chmod(0o644)
            body = copied / 'MATHEMATICAL_AUDIT.md'
            if mutation in ('modified_body', 'body_and_internal_manifest'):
                body.write_bytes(body.read_bytes() + b'\nMUTATED AUDIT INPUT\n')
                if mutation == 'body_and_internal_manifest':
                    manifest = json.loads((copied / 'MANIFEST.json').read_text())
                    data = body.read_bytes()
                    manifest['files']['MATHEMATICAL_AUDIT.md'] = {
                        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                    (copied / 'MANIFEST.json').write_text(json.dumps(manifest))
            elif mutation == 'missing_file':
                (copied / 'README.md').unlink()
            elif mutation == 'extra_file':
                (copied / 'extra.txt').write_text('extra authored test fixture')
            else:
                body.unlink()
                body.symlink_to(packet / 'MATHEMATICAL_AUDIT.md')
            for flags, label in modes:
                entry = run([sys.executable, *flags, '-B', str(HERE / 'verify_frozen.py'), str(copied)],
                            ['python3', *flags, '-B', 'verify_frozen.py', 'mutation_fixture:' + mutation], 1)
                entry['mutation'] = mutation
                receipt['pin_negative_controls'].append(entry)
    if len(sys.argv) == 4:
        source_directory = Path(sys.argv[3])
        for name, expected in PDF_PINS.items():
            p = source_directory / name
            check(p.is_file() and not p.is_symlink(), 'source PDF missing or symlinked: ' + name)
            data = p.read_bytes()
            actual = (len(data), hashlib.sha256(data).hexdigest())
            check(actual == expected, 'source PDF pin mismatch: ' + name)
            receipt['source_pdf_checks'].append({'file': name, 'bytes': actual[0], 'sha256': actual[1], 'match': True})
    receipt['after'] = snapshot(packet)
    check(receipt['after'] == receipt['before'], 'original packet changed')
    receipt.update(status='PASS', original_packet_unchanged=True, positive_runs=6,
                   mathematical_negative_runs=24, external_pin_negative_runs=15,
                   source_retrieval_scope='Existing local PDF bytes independently rehashed; no new PDF download claimed.',
                   limitations=['No machine verification of imported representation-theoretic theorems.',
                                'No proof or counterexample for full-category-O k>=2 equality.',
                                'No certificate of comprehensive literature coverage, openness, or novelty.'])
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'uid', 'positive_runs', 'mathematical_negative_runs',
                                            'external_pin_negative_runs', 'original_packet_unchanged')}, sort_keys=True))


if __name__ == '__main__':
    main()
