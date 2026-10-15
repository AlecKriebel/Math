#!/usr/bin/env python3
"""Guard PR464 publication using the unchanged repository Zenodo upload kit.

Default is the kit's entirely local check. inspect is externally read-only.
stage/publish require --apply; publish also requires the verified draft ID.
Each uncertain operation is saved before dispatch and never blindly retried.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import common as c


def kit_cli(context, mode, confirm_id=None):
    args = [sys.executable, str(context['kit']), mode, str(c.PACKAGE / 'deposit.json')]
    if mode == 'inspect':
        args.append('--check-doi')
    if mode == 'publish':
        args += ['--confirm-id', str(confirm_id)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    c.require(result.returncode == 0, 'Repository Zenodo kit did not confirm success; inspect saved draft read-only before another write')
    summary = json.loads(result.stdout)
    c.require(type(summary) is dict and summary.get('environment') == 'production'
              and summary.get('title') == context['metadata']['title'], 'Zenodo production/title identity differs')
    records = summary.get('files')
    c.require(type(records) is list and len(records) == len(c.UPLOADS)
              and {x['name']: x for x in records} == c.expected_public_files(context), 'Zenodo files differ from accepted package')
    if mode != 'check':
        c.require(summary.get('metadata_normalizations') == [], 'Canonical metadata changed during Zenodo serialization')
    summary['canonical_metadata_sha256'] = c.sha(c.safe_file(c.PACKAGE, 'metadata.json').read_bytes())
    summary['accepted_input_manifest_sha256'] = context['gate']['review_input_manifest_sha256']
    summary['unchanged_repository_kit_sha256'] = context['gate']['zenodo_kit_sha256']
    return summary


class PublicRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        c.require(parsed.scheme == 'https' and parsed.hostname == 'zenodo.org'
                  and parsed.port in (None, 443) and not parsed.username, 'Public download redirected outside Zenodo')
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def public_readback(context, published):
    record_id = published.get('id')
    c.require(type(record_id) is int and record_id > 0
              and published.get('state') == 'published'
              and published.get('doi') == '10.5281/zenodo.' + str(record_id), 'Published record identity absent')
    opener = build_opener(PublicRedirects())
    headers = {'User-Agent': 'Math-PR464-Public-Readback/1.0', 'Accept': 'application/json'}
    with opener.open(Request('https://zenodo.org/api/records/' + str(record_id), headers=headers), timeout=60) as response:
        c.require(response.status == 200, 'Public record unavailable')
        body = response.read(2_000_001)
        c.require(len(body) <= 2_000_000, 'Oversized public record response')
        record = json.loads(body)
    expected = c.expected_public_files(context)
    c.require(record.get('id') == record_id and record.get('doi') == published['doi']
              and record.get('metadata', {}).get('title') == context['metadata']['title'], 'Public record identity/title changed')
    files = record.get('files')
    c.require(type(files) is list and len(files) == len(expected)
              and {x.get('key') for x in files} == set(expected), 'Unexpected actual public file list')
    verified = []
    for name, spec in expected.items():
        request = Request('https://zenodo.org/records/' + str(record_id) + '/files/' + quote(name, safe='') + '?download=1',
                          headers={'User-Agent': headers['User-Agent']})
        digest = hashlib.sha256()
        count = 0
        with opener.open(request, timeout=60) as response:
            c.require(response.status == 200, 'Actual public file unavailable')
            while True:
                block = response.read(1_048_576)
                if not block:
                    break
                count += len(block)
                c.require(count <= spec['size'], 'Public download exceeds accepted size')
                digest.update(block)
        c.require(count == spec['size'] and digest.hexdigest() == spec['sha256'], 'Actual public download differs from accepted file')
        verified.append(dict(spec))
    receipt = {'verified_at_utc': c.now(), 'verified': True, 'authenticated': False,
               'id': record_id, 'doi': published['doi'], 'record_url': published['record_url'],
               'files': verified, 'public_bytes_downloaded_and_hashed': True,
               'canonical_metadata_confirmed_by_unchanged_kit_inspect': True}
    c.dump('ZENODO_PUBLIC_FILE_READBACK.json', receipt)
    return receipt


def run(mode='check', apply=False, confirm_id=None):
    c.require(mode in {'check', 'inspect', 'stage', 'publish'}, 'Unsupported Zenodo operation')
    c.require(not apply or mode in {'stage', 'publish'}, '--apply is meaningful only for explicit writes')
    c.require(mode not in {'stage', 'publish'} or apply, 'Explicit --apply required for Zenodo writes')
    context = c.validate_gate()
    if mode != 'check':
        c.live_eligibility()
    if mode == 'check':
        return kit_cli(context, 'check')
    if mode in {'stage', 'publish'}:
        operation_name = 'ZENODO_' + mode.upper() + '_OPERATION.json'
        previous = c.AUDIT / operation_name
        if previous.exists():
            prior = c.read_json(c.AUDIT, operation_name)
            c.require(prior.get('state') == 'read_only_preflight',
                      'A prior Zenodo write exists; use inspect read-only rather than repeating the write')
        if mode == 'publish':
            stage = c.read_json(c.AUDIT, 'ZENODO_STAGE_RECEIPT.json')
            c.require(type(confirm_id) is int and confirm_id > 0 and stage.get('id') == confirm_id
                      and stage.get('state') == 'ready_to_publish' and stage.get('environment') == 'production'
                      and stage.get('canonical_metadata_sha256') == c.sha(c.safe_file(c.PACKAGE, 'metadata.json').read_bytes())
                      and stage.get('accepted_input_manifest_sha256') == context['gate']['review_input_manifest_sha256'],
                      'Exact confirmed production draft/accepted metadata absent')
            inspected = kit_cli(context, 'inspect')
            c.require(inspected.get('id') == confirm_id and inspected.get('state') == 'ready_to_publish',
                      'Draft is no longer the exact unpublished accepted deposit')
        c.validate_gate()
        c.live_eligibility()
        operation = {'prepared_at_utc': c.now(), 'operation': mode, 'state': mode + '_attempted_once',
                     'pr': c.PR, 'environment': 'production', 'confirm_id': confirm_id,
                     'accepted_input_manifest_sha256': context['gate']['review_input_manifest_sha256'],
                     'canonical_metadata_sha256': c.sha(c.safe_file(c.PACKAGE, 'metadata.json').read_bytes())}
        c.dump(operation_name, operation)
        try:
            summary = kit_cli(context, mode, confirm_id)
        except (RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
            operation['state'] = 'outcome_unconfirmed'
            c.dump(operation_name, operation)
            raise
        operation.update(state='kit_confirmed_' + summary.get('state', ''), confirmed_at_utc=c.now(), id=summary.get('id'))
        c.dump(operation_name, operation)
    else:
        summary = kit_cli(context, 'inspect')
    c.require(summary.get('state') in {'ready_to_publish', 'published'} and type(summary.get('id')) is int
              and summary['id'] > 0, 'Zenodo kit did not confirm the expected state')
    if summary['state'] == 'ready_to_publish':
        c.dump('ZENODO_STAGE_RECEIPT.json', summary)
    else:
        # Both direct publish and read-only recovery independently inspect the
        # same saved draft through the original kit before claiming acceptance.
        inspected = kit_cli(context, 'inspect')
        c.require(inspected.get('state') == 'published' and inspected.get('id') == summary['id']
                  and inspected.get('doi') == summary.get('doi'), 'Published state readback differs')
        c.dump('ZENODO_PUBLISH_RECEIPT.json', inspected)
        public_readback(context, inspected)
        c.validate_publication(context)
        summary = inspected
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('check', 'inspect', 'stage', 'publish'), default='check')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--confirm-id', type=int)
    args = parser.parse_args()
    print(json.dumps(run(args.mode, args.apply, args.confirm_id), indent=2))


if __name__ == '__main__':
    main()
