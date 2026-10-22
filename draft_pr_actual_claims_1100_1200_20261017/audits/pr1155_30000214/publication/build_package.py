#!/usr/bin/env python3
"""Deterministically build an offline source archive and portable upload kit.

The PDF is a frozen input, never recompiled. No network or deposit operation is
performed. All output destinations are preflighted before the first write.
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import stat
import tempfile
import zipfile

sys.dont_write_bytecode = True
_script = Path(os.path.abspath(__file__))
_helper = _script.parent / 'verification/package_common.py'
for _input in (_script, _helper):
    for _component in reversed([_input, *_input.parents]):
        if _component.is_symlink():
            raise ValueError('symlink ancestor/member: ' + str(_component))
    if not _input.exists() or not stat.S_ISREG(_input.lstat().st_mode):
        raise ValueError('missing/nonregular input: ' + str(_input))
sys.path.insert(0, str(_helper.parent))
from package_common import (HERE, KIT, PDF, PREFIX, PUBLICATION_MEMBERS, SOURCE,
                            audit_root, byte_pin, encoded, load, member_name,
                            need, output_path, pin, read, read_allowlist,
                            verify_audit, verify_manifest, verify_pdf_qa)


def archive_bytes(members):
    folded = set()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            member_name(name)
            need(name.casefold() not in folded, 'case-colliding archive member: ' + name)
            folded.add(name.casefold())
            entry = zipfile.ZipInfo(name, (2026, 10, 17, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buffer.getvalue()


def atomic_bytes(path, data):
    path = output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.' + path.name + '.', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        output_path(path)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    need(len(sys.argv) == 1, 'builder accepts no command-line arguments')
    destinations = [HERE / 'output' / SOURCE, HERE / 'output' / KIT, HERE / 'PACKAGE_RECEIPT.json']
    for destination in destinations:
        output_path(destination)
    allowed = read_allowlist()
    verify_audit(allowed)
    verify_manifest(allowed)
    qa = verify_pdf_qa()
    metadata_bytes = read(HERE / 'zenodo-metadata.json')
    deposit_bytes = read(HERE / 'zenodo-deposit.json')
    metadata = load(HERE / 'zenodo-metadata.json')
    deposit = load(HERE / 'zenodo-deposit.json')
    need(isinstance(metadata, dict) and isinstance(deposit, dict)
         and set(deposit) == {'metadata', 'files'} and deposit['metadata'] == metadata,
         'deposit metadata contract mismatch')
    need(deposit['files'] == [{'path': 'output/pdf/' + PDF}, {'path': 'output/' + SOURCE}],
         'deposit payload path contract mismatch')
    replay_bytes = read(HERE / 'verification/REPLAY_RECEIPT.json')
    replay = load(HERE / 'verification/REPLAY_RECEIPT.json')
    result = subprocess.run([sys.executable, '-B', str(HERE / 'verification/verify_all.py')],
                            capture_output=True, timeout=300)
    need(result.returncode == 0 and result.stderr == b'',
         'portable verification failed: ' + result.stderr.decode('utf-8', errors='replace'))
    need(result.stdout == replay_bytes and json.loads(result.stdout) == replay,
         'complete frozen replay receipt mismatch')
    need(replay.get('status') == 'PASS' and len(replay['runs']) == 2
         and len(replay['actual_wrong_result_failures']) == 6, 'incomplete frozen replay')
    members = {}
    for name in PUBLICATION_MEMBERS:
        member_name(name)
        need(name not in members, 'duplicate publication member: ' + name)
        members[name] = read(HERE / name)
    for name, wanted in sorted(allowed.items()):
        data = read(audit_root() / name)
        need(byte_pin(data) == wanted, 'audit member changed during packaging: ' + name)
        archived_name = PREFIX + '/' + name
        need(archived_name not in members, 'duplicate authored archive member')
        members[archived_name] = data
    # Recheck the pinned PDF/source using the byte snapshots actually archived.
    need(byte_pin(members['main.tex']) == qa['source']
         and byte_pin(members['output/pdf/' + PDF]) == qa['pdf'], 'PDF/source changed during packaging')
    need(members['zenodo-metadata.json'] == metadata_bytes
         and members['zenodo-deposit.json'] == deposit_bytes
         and members['verification/REPLAY_RECEIPT.json'] == replay_bytes,
         'metadata/replay changed during packaging')
    manifest = {name: byte_pin(data) for name, data in sorted(members.items())}
    members['SOURCE_MANIFEST.json'] = encoded(manifest)
    source_bytes = archive_bytes(members)
    portable = {'metadata': metadata, 'files': [{'path': PDF}, {'path': SOURCE}]}
    kit_bytes = archive_bytes({PDF: members['output/pdf/' + PDF], SOURCE: source_bytes,
                              'README.md': members['README.md'],
                              'zenodo-metadata.json': metadata_bytes,
                              'zenodo-deposit.json': encoded(portable)})
    final_files = {
        'main.tex': members['main.tex'], 'output/pdf/' + PDF: members['output/pdf/' + PDF],
        'output/' + SOURCE: source_bytes, 'output/' + KIT: kit_bytes,
        'zenodo-metadata.json': metadata_bytes, 'zenodo-deposit.json': deposit_bytes,
    }
    receipt = {'files': {name: byte_pin(data) for name, data in sorted(final_files.items())},
               'source_members': manifest, 'source_members_including_manifest': len(members),
               'kit_members': 5, 'operative_paper_pages': qa['pages'],
               'verification': 'One stdlib finite-incidence/threshold program; 2 byte-exact complete positive outputs and 6 actual mathematical mutation failures across normal and optimized Python. Optional NumPy and historical family programs are separate and are not run by the default verifier.',
               'source_body_custody_checks': 'Optional and excluded from offline verification; third-party bodies are not distributed.'}
    # All inputs and both in-memory archives are complete before output writes.
    for destination in destinations:
        output_path(destination)
    atomic_bytes(destinations[0], source_bytes)
    atomic_bytes(destinations[1], kit_bytes)
    atomic_bytes(destinations[2], encoded(receipt))
    print(json.dumps({name: value for name, value in receipt.items() if name != 'source_members'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
