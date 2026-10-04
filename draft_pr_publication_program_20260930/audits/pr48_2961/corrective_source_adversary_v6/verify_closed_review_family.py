"""UNEXECUTED ROOT separate readback of own evidence only."""
import argparse
import json
import stat
import review_evidence_common as c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-manifest-sha256', required=True)
    args = parser.parse_args()
    body = c.raw(c.F / 'SELF_MANIFEST.json')
    c.need(c.sha(body) == args.self_manifest_sha256, 'Literal actual own self pin')
    value = c.parse(body)
    keys = {'schema', 'source_only', 'self_excluded', 'files_count', 'files', 'file_modes', 'directory_modes', 'verdict_status', 'production_executed', 'future_acceptance_approved'}
    c.need(set(value) == keys and value['schema'] == 'pr48-v6-independent-review-evidence-closure/v1' and value['source_only'] is True and value['self_excluded'] == ['SELF_MANIFEST.json'] and value['verdict_status'] == 'PASS_SOURCE_ONLY' and value['production_executed'] is False and value['future_acceptance_approved'] is False, 'Exact closed own review schema')
    names = [c.safe(z['path']) for z in value['files']]
    c.need(type(value['files_count']) is int and len(names) == value['files_count'] and names == sorted(set(names)), 'Exact typed distinct payload')
    dirs = [z['path'] for z in value['directory_modes']]
    c.topology(c.F, names + ['SELF_MANIFEST.json'], dirs, 0o444)
    c.need(value['file_modes'] == [dict(path=n, full_mode=0o444) for n in sorted(names + ['SELF_MANIFEST.json'])] and all(z['full_mode'] == 0o755 for z in value['directory_modes']), 'Complete frozen fullmode domains')
    for row in value['files']:
        c.need(set(row) == {'path', 'bytes', 'sha256'} and type(row['bytes']) is int, 'Typed fullbody descriptor')
        b = c.raw(c.F / row['path'])
        c.need(len(b) == row['bytes'] and c.sha(b) == row['sha256'], 'Every closed own body')
    c.check_fixed()
    print(json.dumps(dict(status='PASS_V6_REVIEW_EVIDENCE_SEPARATE_READBACK_ONLY', payload_count=len(names), self_manifest_sha256=args.self_manifest_sha256, production_executed=False, future_acceptance_approved=False)))

if __name__ == '__main__':
    main()
