#!/usr/bin/env python3
"""ROOT-invoked self-only closure; never closes external source inputs."""
import argparse
import datetime
import json
from pathlib import Path
import family_custody as c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-report-sha256',required=True)
    args = parser.parse_args()
    if c.identity(c.ROOT/'REPORT.md')['sha256'] != args.expected_report_sha256:
        raise ValueError('report digest')
    if (c.ROOT/'SELF_MANIFEST.json').exists():
        raise ValueError('already closed; read only verifier required')
    c.external_check()
    files,dirs = c.members()
    rows = []
    for p in files:
        identity = c.identity(p)
        rows.append({'path':str(p.relative_to(c.ROOT)),'bytes':identity['bytes'],
                     'sha256':identity['sha256'],'full_mode':'0444'})
    value = {'schema':'pr51-modular-geometry-adversary-self-only-closure/v1',
             'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'scope':'This family only, fifteen readonly exact external science inputs; no native/merge/publication authority.',
             'payload_file_count':len(rows),'self_excluded_count':1,'files':rows,
             'directories':[{'path':'.' if p == c.ROOT else str(p.relative_to(c.ROOT)),
                             'full_mode':'0555'} for p in dirs]}
    mf = c.ROOT/'SELF_MANIFEST.json'
    with mf.open('x') as f:
        json.dump(value,f,sort_keys=True,indent=2)
        f.write('\n')
    for p in files+[mf]:
        p.chmod(0o444)
    for p in sorted(dirs,key=lambda p:len(p.parts),reverse=True):
        p.chmod(0o555)
    print(json.dumps(c.verify(c.identity(mf)['sha256']),sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
