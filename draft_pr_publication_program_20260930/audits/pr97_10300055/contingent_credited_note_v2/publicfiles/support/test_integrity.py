#!/usr/bin/env python3
"""Run normal/optimized positive and hostile-path integrity controls."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time
import warnings
import zipfile
sys.dont_write_bytecode = True
from safe_output import fresh_output, copy_new, write_new, exclusive_binary, json_bytes, Journal

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    code = root/'check_integrity.py'
    archive = Path(args.archive).absolute()
    output = fresh_output(args.output_dir, root)
    records = []
    custody = Journal(output/'PROCESS_RECEIPTS.json')
    def run(label, options, reason=None):
        for optimized in (False, True):
            command = [sys.executable, '-E', '-B'] + (['-O'] if optimized else [])
            command += [str(code)] + options
            started = dt.datetime.now(dt.timezone.utc).isoformat()
            tick = time.monotonic()
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            accepted = (proc.returncode == 0 and b'"status": "PASS"' in out) if reason is None else (
                proc.returncode != 0 and reason.encode() in err)
            record = dict(label=label, optimized=optimized, command=command,
                          cwd=os.getcwd(), pid=proc.pid, started_utc=started,
                          finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                          wall_seconds=time.monotonic()-tick, exit_code=proc.returncode,
                          expected_reason=reason, accepted=accepted,
                          stdout=out.decode(errors='replace'), stderr=err.decode(errors='replace'),
                          stdout_sha256=sha(out), stderr_sha256=sha(err))
            if options[0] == '--zip':
                record['tested_archive_sha256'] = sha(Path(options[1]).read_bytes())
            records.append(record)
            custody.save(records)
            if not accepted:
                raise RuntimeError('Integrity control failed: '+label)
    run('valid_directory', ['--root', str(root)])
    run('valid_zip', ['--zip', str(archive)])
    with zipfile.ZipFile(archive) as z:
        contents = [(i.filename, z.read(i)) for i in z.infolist()]
    variants = [
        ('traversal', '../escaped.txt', 'Empty, dot, or traversing member component'),
        ('absolute', '/escaped.txt', 'Absolute member name'),
        ('windows_absolute', 'C:/escaped.txt', 'Absolute member name'),
        ('backslash', 'folder\\escaped.txt', 'Unsafe member name'),
        ('dot_component', './escaped.txt', 'Empty, dot, or traversing member component'),
        ('empty_component', 'folder//escaped.txt', 'Empty, dot, or traversing member component'),
        ('duplicate', 'README.md', 'Duplicate ZIP member'),
        ('extra_safe_file', 'unexpected.txt', 'ZIP closure mismatch')]
    for label, name, reason in variants:
        dest = output/(label+'.zip')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with exclusive_binary(dest) as stream:
                with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                    for old, data in contents:
                        z.writestr(old, data)
                    z.writestr(name, b'controlled payload')
        run(label, ['--zip', str(dest)], reason)
        dest.unlink()
    dest = output/'zip_symlink.zip'
    with exclusive_binary(dest) as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for old, data in contents:
                z.writestr(old, data)
            info = zipfile.ZipInfo('linked')
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, b'../../outside')
    run('zip_symlink', ['--zip', str(dest)], 'ZIP symlink')
    dest.unlink()
    dest = output/'tampered.zip'
    with exclusive_binary(dest) as stream:
        with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for old, data in contents:
                z.writestr(old, data+b'\nTAMPERED' if old == 'README.md' else data)
    run('tampered_digest', ['--zip', str(dest)], 'Digest/size mismatch')
    dest.unlink()
    ancestor = output/'escaping_ancestor'
    ancestor.symlink_to(root.parent.parent, target_is_directory=True)
    run('escaping_ancestor_symlink', ['--root', str(ancestor/'credited_verification_candidate_v2')],
        'Symlink in root or ancestor')
    ancestor.unlink()
    payload = output/'symlink_payload'
    payload.mkdir()
    copy_new(root/'MANIFEST.json', payload/'MANIFEST.json')
    link = payload/'linked'
    link.symlink_to(root.parent.parent/'credited_verification_candidate_v2/CANDIDATE.md')
    run('payload_symlink', ['--root', str(payload)], 'Payload symlink')
    link.unlink()
    (payload/'MANIFEST.json').unlink()
    payload.rmdir()
    result = dict(status='PASS', process_runs=len(records),
                  positive_runs=sum(r['expected_reason'] is None for r in records),
                  rejection_runs=sum(r['expected_reason'] is not None for r in records),
                  checker_sha256=sha(code.read_bytes()), archive_sha256=sha(archive.read_bytes()),
                  manifest_sha256=sha((root/'MANIFEST.json').read_bytes()),
                  explicit_guards_active_under_optimization=True,
                  publication_authorized=False,
                  scope='Payload/path integrity controls only, not theorem or priority acceptance')
    write_new(output/'RESULT.json', json_bytes(result))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
