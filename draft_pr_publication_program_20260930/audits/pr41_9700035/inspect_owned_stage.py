"""ROOT verifies every staged selected blob before committing its merge."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
PREFIX = 'unsolved_math_prioritization/attempts/9700035/'


def git(*args): return subprocess.check_output(['git', *args], cwd=R)


def main():
    overlay = json.loads((A / 'integration_check.json').read_bytes())
    rows = overlay['canonical_overlay_files']
    assert len(rows) == 556
    expected = {PREFIX + z['path']: z for z in rows}
    queue = 'unsolved_math_prioritization/QUEUE.md'
    changed = set(filter(None, git('diff','--cached','--name-only','-z').decode().split('\0')))
    assert changed == set(expected) | {queue}
    entries = git('ls-files','--stage','-z','--',PREFIX,queue).decode().split('\0')
    seen = set(); maximum = 0
    for entry in filter(None, entries):
        fields, name = entry.split('\t'); mode, blob, stage = fields.split()
        assert name in changed and name not in seen and mode == '100644' and stage == '0'
        seen.add(name); raw = (R / name).read_bytes(); maximum = max(maximum,len(raw))
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == blob
        if name != queue:
            row = expected[name]
            assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        else: assert hashlib.sha256(raw).hexdigest() == overlay['whole_queue_after_sha256']
    assert seen == changed and maximum <= 104857600
    assert git('rev-parse','HEAD').decode().strip() == '521770c746b2fd48e00ac6dd908afe5085daf4ab'
    assert git('rev-parse','MERGE_HEAD').decode().strip() == '292b95ca601f166e6d246e609cf7ed5ca5653e25'
    result = {'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
              'status':'PASS','canonical_blobs':556,'queue_blobs':1,'maximum_blob_bytes':maximum,
              'all_exact_staged_bytes_and_regular_modes':True,'unrelated_staged_paths':[]}
    with (A/'ROOT_OWNED_STAGE_VERIFICATION.json').open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__': main()
