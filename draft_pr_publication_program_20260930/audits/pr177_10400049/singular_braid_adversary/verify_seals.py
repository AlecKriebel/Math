"""Read-only verification of retained files and exact safe-public allowlist."""
from hashlib import sha256
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    root=Path(__file__).resolve().parent
    manifests=('FIRST_INVENTORY.json','FINAL_INVENTORY.json')
    for name in manifests:
        path=root/name
        data=json.loads(path.read_text())
        for entry in data['entries']:
            target=root/entry['path']
            require(target.is_file(),'missing retained file: '+entry['path'])
            body=target.read_bytes()
            require(sha256(body).hexdigest()==entry['sha256'],'hash mismatch: '+entry['path'])
            require(len(body)==entry['bytes'],'byte mismatch: '+entry['path'])
            require(format(target.stat().st_mode&0o777,'04o')==entry['mode']=='0444',
                    'mode mismatch: '+entry['path'])
    final=json.loads((root/'FINAL_INVENTORY.json').read_text())
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    listed={entry['path'] for entry in final['entries']}
    require(actual==listed|{'FINAL_INVENTORY.json'},'unlisted or missing file')
    public=json.loads((root/'SAFE_PUBLIC_ALLOWLIST.json').read_text())
    entries={entry['path']:entry for entry in final['entries']}
    for entry in public['entries']:
        require(entry['path'] in entries,'public item unlisted')
        require(not entry['path'].startswith('private_'),'private item is public')
        require(entry['sha256']==entries[entry['path']]['sha256'],'allowlist hash mismatch')
        require(entry['bytes']==entries[entry['path']]['bytes'],'allowlist byte mismatch')
    require(format((root/'FINAL_INVENTORY.json').stat().st_mode&0o777,'04o')=='0444',
            'inventory envelope writable')
    return {'status':'PASS','retained_regular_files':len(actual),
            'public_allowlisted_files':len(public['entries']),
            'first_and_final_entries_verified':sum(len(json.loads((root/n).read_text())['entries']) for n in manifests),
            'optimization_level':sys.flags.optimize}


if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
