#!/usr/bin/env python3
"""Challenge the submission envelope in disposable copies, including special files."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--package', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source = args.package.absolute()
    pin = digest(source/'PACKAGE_MANIFEST.json')
    receipts = []
    # Keep Unix-domain socket paths below macOS's address-length limit.
    with tempfile.TemporaryDirectory(prefix='p906-', dir='/tmp') as td:
        temp = Path(td)
        def invoke(root, mode, anchor=pin, pdf=None):
            env = dict(os.environ)
            env.pop('PYTHONOPTIMIZE', None)
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            cmd = [sys.executable, '-I', '-B', *mode, str(root/'verify_package.py'),
                   '--integrity-only', '--expected-manifest', anchor]
            if pdf is not None:
                cmd += ['--pdf', str(pdf)]
            return subprocess.run(cmd, cwd=temp, env=env, capture_output=True,
                                  text=True, timeout=20)
        for mode in [[], ['-O'], ['-OO']]:
            label = mode[0] if mode else 'normal'
            positive = invoke(source, mode, pdf=source/'note.pdf')
            require(positive.returncode == 0, 'Pristine package rejected in '+label)
            require(json.loads(positive.stdout)['external_anchor_checked'] is True,
                    'Trusted anchor not checked')
            receipts.append({'mode': label, 'case': 'pristine before', 'passed': True})
            names = ['missing payload', 'extra file', 'extra directory', 'modified paper',
                     'resigned original proof', 'FIFO manifest', 'FIFO listed payload',
                     'FIFO unlisted payload', 'socket listed payload', 'socket unlisted payload',
                     'listed file symlink', 'listed directory symlink', 'package root symlink',
                     'wrong external anchor', 'separate PDF corrupt', 'separate PDF symlink',
                     'separate PDF FIFO']
            for number, name in enumerate(names):
                root = temp/('case-'+label+'-'+str(number))
                shutil.copytree(source, root)
                active_root = root
                pdf = None
                anchor = pin
                sock = None
                if name == 'missing payload':
                    (root/'README.md').unlink()
                elif name == 'extra file':
                    (root/'unexpected.txt').write_text('unexpected\n')
                elif name == 'extra directory':
                    (root/'unexpected').mkdir()
                elif name == 'modified paper':
                    with (root/'note.tex').open('ab') as f:
                        f.write(b'\n% altered claim\n')
                elif name == 'resigned original proof':
                    proof = root/'original_packet/author/PROOF.md'
                    proof.write_bytes(proof.read_bytes()+b'\nAltered mathematical claim.\n')
                    manifest_path = root/'PACKAGE_MANIFEST.json'
                    m = json.loads(manifest_path.read_text())
                    m['files']['original_packet/author/PROOF.md'] = {
                        'bytes': proof.stat().st_size, 'sha256': digest(proof)}
                    manifest_path.write_text(json.dumps(m, indent=2)+'\n')
                    # Even a caller who supplies this replacement envelope cannot
                    # override the separately hard-coded original proof anchor.
                    anchor = digest(manifest_path)
                elif name.startswith('FIFO'):
                    path = root/({'FIFO manifest':'PACKAGE_MANIFEST.json',
                                 'FIFO listed payload':'README.md',
                                 'FIFO unlisted payload':'extra_fifo'}[name])
                    if path.exists(): path.unlink()
                    os.mkfifo(path)
                elif name.startswith('socket'):
                    path = root/('README.md' if 'listed' in name and 'unlisted' not in name
                                 else 'extra_socket')
                    if path.exists(): path.unlink()
                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    sock.bind(str(path))
                elif name == 'listed file symlink':
                    (root/'README.md').unlink()
                    (root/'README.md').symlink_to(source/'README.md')
                elif name == 'listed directory symlink':
                    shutil.rmtree(root/'original_packet/author')
                    (root/'original_packet/author').symlink_to(source/'original_packet/author',
                                                             target_is_directory=True)
                elif name == 'package root symlink':
                    active_root = temp/('root-link-'+label)
                    active_root.symlink_to(root, target_is_directory=True)
                elif name == 'wrong external anchor':
                    anchor = '0'*64
                elif name.startswith('separate PDF'):
                    pdf = temp/('separate-'+label+'-'+str(number)+'.pdf')
                    if name == 'separate PDF corrupt': pdf.write_bytes(b'wrong pdf')
                    elif name == 'separate PDF symlink': pdf.symlink_to(source/'note.pdf')
                    else: os.mkfifo(pdf)
                try:
                    result = invoke(active_root, mode, anchor=anchor, pdf=pdf)
                    require(result.returncode != 0 and 'RuntimeError' in result.stderr,
                            'Challenge did not fail through an explicit guard: '+name+' '+label)
                    receipts.append({'mode': label, 'case': name, 'rejected': True,
                                     'guard': result.stderr.strip().splitlines()[-1]})
                finally:
                    if sock is not None: sock.close()
            spec = importlib.util.spec_from_file_location('guard_verifier_'+label,
                                                          source/'verify_package.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Exercise the intended comparator boundary, including bool-as-int.
            for actual, expected in [(True, 1.0), (1, True), (float('nan'), 1.0),
                                     (float('inf'), 1.0), (1.1, 1.0)]:
                try:
                    module.equivalent(actual, expected)
                except RuntimeError:
                    pass
                else:
                    raise RuntimeError('Comparator accepted invalid value')
            # The checks above are invoked in this harness's own mode. Separate
            # subprocess probes confirm the same imported helper in every mode.
            probe = ('import importlib.util; '
                     's=importlib.util.spec_from_file_location("v",'+repr(str(source/'verify_package.py'))+'); '
                     'v=importlib.util.module_from_spec(s); s.loader.exec_module(v); '
                     'v.equivalent(True,1.0)')
            proc = subprocess.run([sys.executable, '-I', '-B', *mode, '-c', probe],
                                  cwd=temp, capture_output=True, text=True, timeout=20)
            require(proc.returncode != 0 and 'Boolean' not in proc.stderr and
                    'Numerical replay mismatch' in proc.stderr,
                    'Boolean/numeric separation failed in '+label)
            receipts.append({'mode': label, 'case':'bool-as-float helper subprocess',
                             'rejected': True})
            positive = invoke(source, mode, pdf=source/'note.pdf')
            require(positive.returncode == 0, 'Pristine package changed in '+label)
            receipts.append({'mode':label, 'case':'pristine after', 'passed':True})
    require(digest(source/'PACKAGE_MANIFEST.json') == pin, 'Original envelope changed')
    output = {'utc':datetime.now(timezone.utc).isoformat(), 'status':'PASS',
              'package_manifest_sha256':pin, 'modes':['normal','-O','-OO'],
              'rejected_package_cases_per_mode':17,
              'rejected_bool_helper_cases_per_mode':1,
              'positive_package_cases_per_mode':2, 'receipt_count':len(receipts),
              'receipts':receipts,
              'scope':'Finite integrity/comparator challenges, not analytic proof certification.'}
    args.output.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='receipts'}, indent=2))

if __name__ == '__main__': main()
