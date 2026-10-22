#!/usr/bin/env python3
"""Authenticate the ENTIRE PR952 operations inventory before any dependency execution.

No external operation runs on import. The entry point, interpreter, standard
library and external inventory pin are trust roots; this is not an OS sandbox.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError('Invoke with Python -I -S -B before loading this file')
import argparse,base64,hashlib,json,os,re,stat,subprocess
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr952_10400145'
HEAD='989a532ae1d50894190d010a0a02ba8c3d71ee05'
KEY='10400145'
PR=952
MAX_FILE=128*1024*1024
KIT='zenodo_deposit_tool/zenodo.py'
HELPERS=['accept_pr952.py','merge_pr952.py','run_pr952_zenodo.py','append_pr952_tracker.py','update_pr952_publication_ledger.py','finalize_pr952_and_gate_next.py']


def need(ok, label):
    if not ok:
        raise RuntimeError('PR952 guard: ' + label)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe(name):
    return (type(name) is str and bool(name) and '\\' not in name and '\0' not in name
            and not PurePosixPath(name).is_absolute()
            and PurePosixPath(name).as_posix() == name
            and all(x not in ('', '.', '..') for x in name.split('/')))

def strict_json(raw):
    def pairs(items):
        result = {}
        for k, v in items:
            need(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def bad(value):
        raise RuntimeError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)

def fingerprint(raw):
    return {'bytes': len(raw), 'sha256': sha(raw)}

def validate_pin(pin):
    need(type(pin) is dict and set(pin) == {'bytes', 'sha256'}
         and type(pin['bytes']) is int and 0 <= pin['bytes'] <= MAX_FILE
         and type(pin['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}', pin['sha256']) is not None,
         'fingerprint schema/cap')

def read_regular(path, cap=MAX_FILE, pin=None):
    """Anchor every repository ancestor; reject FIFO/symlink before reading."""
    path = Path(path)
    try:
        name = path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise RuntimeError('File outside trusted repository root') from error
    need(safe(name), 'unsafe repository file name')
    if pin is not None:
        validate_pin(pin)
        cap = pin['bytes']
    need(type(cap) is int and 0 <= cap <= MAX_FILE, 'read cap')
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(ROOT, flags | os.O_DIRECTORY)
    try:
        parts = name.split('/')
        for part in parts[:-1]:
            next_fd = os.open(part, flags | os.O_DIRECTORY, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        file_fd = os.open(parts[-1], flags, dir_fd=fd)
        try:
            info = os.fstat(file_fd)
            need(stat.S_ISREG(info.st_mode) and info.st_size <= cap,
                 'nonregular or oversized file: ' + name)
            if pin is not None:
                need(info.st_size == pin['bytes'], 'file size changed: ' + name)
            chunks = []
            total = 0
            while total <= cap:
                block = os.read(file_fd, min(1024 * 1024, cap + 1 - total))
                if not block:
                    break
                chunks.append(block)
                total += len(block)
            raw = b''.join(chunks)
            need(len(raw) <= cap, 'file grew beyond cap: ' + name)
            if pin is not None:
                need(fingerprint(raw) == pin, 'file fingerprint changed: ' + name)
            return raw
        finally:
            os.close(file_fd)
    finally:
        os.close(fd)

def validate_inventory(mapping):
    need(type(mapping) is dict and mapping.get('schema') == 'pr952-operations-v1'
         and type(mapping.get('pr')) is int and mapping['pr'] == PR
         and mapping.get('problem_id') == KEY
         and mapping.get('original_pr_head') == HEAD, 'inventory target/schema')
    records = mapping.get('files')
    expected = {P.relative_to(ROOT).as_posix() + '/' + name for name in HELPERS} | {KIT}
    need(type(records) is dict and set(records) == expected, 'entire seven-file operations inventory required')
    for name, pin in records.items():
        need(safe(name), 'inventory path')
        validate_pin(pin)
        need(0 < pin['bytes'] <= 4 * 1024 * 1024, 'operational dependency size cap')
    need(records[KIT]['sha256']=='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca','unchanged standard kit SHA256')
    return records

def capture_inventory(external_pin):
    need(type(external_pin) is str and re.fullmatch('[0-9a-f]{64}', external_pin) is not None,
         'external operations-inventory pin required')
    raw = read_regular(A / 'publication/workflow/OPERATIONS_INVENTORY.json', 1024 * 1024)
    need(sha(raw) == external_pin, 'externally pinned operations inventory changed')
    mapping = strict_json(raw)
    records = validate_inventory(mapping)
    captured = {name: read_regular(ROOT / name, pin=pin) for name, pin in records.items()}
    return {'inventory_sha256': external_pin, 'inventory': mapping, 'captured': captured}

def entry(action):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operations-sha256', required=True)
    if action == 'accept':
        parser.add_argument('--freeze', required=True)
        parser.add_argument('--review', action='append', required=True)
    if action == 'zenodo':
        parser.add_argument('action', choices=['stage', 'publish', 'inspect'])
    args = parser.parse_args()
    context = capture_inventory(args.operations_sha256)
    # Every repository dependency is authenticated BEFORE a copied-byte worker
    # starts. -I -S -B gives an actual optimization0 worker even if this trusted
    # entry point was invoked with -O/-OO/PYTHONOPTIMIZE.
    bundle = {'action': action, 'args': vars(args),
              'inventory_sha256': context['inventory_sha256'], 'inventory': context['inventory'],
              'captured': {name: base64.b64encode(raw).decode('ascii') for name, raw in context['captured'].items()}}
    bootstrap = ('import argparse,base64,json,sys; '
                 'b=json.loads(sys.stdin.buffer.read()); '
                 'c={"inventory_sha256":b["inventory_sha256"],"inventory":b["inventory"],'
                 '"captured":{n:base64.b64decode(v,validate=True) for n,v in b["captured"].items()}}; '
                 'p=sys.argv[1]; n={"__name__":"_pr952_authenticated_core_","__file__":p,"__package__":None}; '
                 'exec(compile(c["captured"][sys.argv[2]],p,"exec",dont_inherit=True,optimize=0),n); '
                 'n["operation"](b["action"],argparse.Namespace(**b["args"]),c)')
    core = str((P / 'accept_pr952.py').relative_to(ROOT))
    result = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', bootstrap,
                             str(P / 'accept_pr952.py'), core], cwd=ROOT,
                            input=json.dumps(bundle).encode())
    raise SystemExit(result.returncode)

if __name__=='__main__':
    entry('native')
