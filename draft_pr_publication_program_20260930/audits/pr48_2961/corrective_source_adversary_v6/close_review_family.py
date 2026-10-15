"""UNEXECUTED ROOT-only own evidence freeze; no production/candidate loading."""
import argparse
import json
import os
import stat
from pathlib import Path
import review_evidence_common as c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--personally-read-complete-source', action='store_true')
    parser.add_argument('--ready-sha256', required=True)
    args = parser.parse_args()
    c.need(args.execute and args.personally_read_complete_source and __debug__ and c.F.name == 'corrective_source_adversary_v6', 'ROOT explicit complete own evidence reading')
    c.need(not (c.F / 'SELF_MANIFEST.json').exists(), 'Absent own evidence self')
    body = c.raw(c.F / 'READY.json')
    c.need(c.sha(body) == args.ready_sha256, 'Exact own ready pin')
    ready = c.parse(body)
    c.need(ready['schema'] == 'pr48-v6-independent-review-readiness/v1' and ready['production_executed'] is False and ready['future_acceptance_approved'] is False, 'Review only readiness')
    c.check_fixed()
    names = ready['payload_names']
    c.topology(c.F, names, ready['directory_names'], 0o644)
    for row in ready['payload_rows_except_READY']:
        c.check(row)
    c.need({Path(z['path']).relative_to(c.F.relative_to(c.R)).as_posix() for z in ready['payload_rows_except_READY']} == set(names) - {'READY.json'}, 'Complete own nonself-ready body index')
    rows = [{k: v for k, v in c.ref(c.F / name).items() if k != 'full_mode'} for name in names]
    for row, name in zip(rows, names):
        row['path'] = name
    result = dict(schema='pr48-v6-independent-review-evidence-closure/v1', source_only=True, self_excluded=['SELF_MANIFEST.json'], files_count=len(rows), files=rows, file_modes=[dict(path=n, full_mode=0o444) for n in sorted(names + ['SELF_MANIFEST.json'])], directory_modes=[dict(path=n, full_mode=0o755) for n in ready['directory_names']], verdict_status='PASS_SOURCE_ONLY', production_executed=False, future_acceptance_approved=False)
    os.umask(0o022)
    with (c.F / 'SELF_MANIFEST.json').open('xb') as stream:
        stream.write((json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    for name in names + ['SELF_MANIFEST.json']:
        (c.F / name).chmod(0o444)
    c.topology(c.F, names + ['SELF_MANIFEST.json'], ready['directory_names'], 0o444)
    for row in rows:
        content = c.raw(c.F / row['path'])
        c.need(len(content) == row['bytes'] and c.sha(content) == row['sha256'], 'Own source bytes unchanged by evidence freeze')
    print(json.dumps(dict(status='PASS_V6_REVIEW_EVIDENCE_CLOSURE_ONLY', payload_count=len(rows), self_manifest_sha256=c.sha(c.raw(c.F / 'SELF_MANIFEST.json')), production_executed=False, future_acceptance_approved=False)))

if __name__ == '__main__':
    main()
