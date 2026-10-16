#!/usr/bin/env python3
"""PR623-only native transport. No create/update/delete/edit/version operations.

The repository kit owns manifests, final verification, summaries and receipts.
This module is a fail-closed transport for recovered own draft 23356540.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit

ROOT = Path('/Users/alec/Documents/Math')
KIT_PATH = ROOT / 'zenodo_deposit_tool' / 'zenodo.py'
sys.dont_write_bytecode = True  # Importing the kit must not write shared bytecode caches.
sys.path.insert(0, str(KIT_PATH.parent))
import zenodo

HERE = Path(__file__).resolve().parent
MANIFEST = ROOT / 'draft_pr_claimed_solved_600_700_20261012/audits/pr623_30001184/publication/zenodo-deposit.json'
RECORD_ID = 23356540
DOI = '10.5281/zenodo.23356540'
BASE = 'https://zenodo.org'
REC = BASE + f'/api/records/{RECORD_ID}'
DRAFT = REC + '/draft'
NATIVE_ACCEPT = 'application/vnd.inveniordm.v1+json'
MANIFEST_SHA = '0612ed1a8d1259168698cff199897acd80d0417061e55574f9819b32da1c7af0'
KIT_SHA = 'a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'
NATIVE_METADATA_SHA = '16618fd47db1114769cd8e0b82d969ad949990552ebeac89c5551e21be4a3148'
FILE_PINS = {
    'gns_generation_counterexample.pdf': (79172, '05c6bcaee280209a52493a6d7b330a31041ed33d6ffae2bfdcd2d46f888b912d'),
    'gns_verification.zip': (226383, 'a00be1239cba9b64012c2010f03f06d30e6716cf56adf52b15c5d6f3b2e66a7c'),
}


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise zenodo.DepositError(message)


def utc():
    return datetime.now(timezone.utc).isoformat()


def pinned_inputs():
    require(zenodo.digest(KIT_PATH, 'sha256') == KIT_SHA, 'Reviewed kit changed; re-review required')
    require(zenodo.digest(MANIFEST, 'sha256') == MANIFEST_SHA, 'Reviewed manifest changed; refusing native recovery')
    metadata, files = zenodo.load_manifest(MANIFEST)
    require({f['name']: (f['size'], f['sha256']) for f in files} == FILE_PINS,
            'Reviewed PDF/ZIP bytes or names changed; refusing native recovery')
    return metadata, files


def legacy_projection(record):
    """An explicitly reversible view of the exact pinned native metadata.

    Native metadata is first hashed in full (including vocabulary annotations),
    so this projection cannot conceal an extra or rich field. It is never PUT.
    """
    native = record.get('metadata')
    require(isinstance(native, dict) and canonical_sha(native) == NATIVE_METADATA_SHA,
            'Native metadata differs from the exact recovered draft snapshot')
    require(record.get('custom_fields') == {}, 'Unsupported native custom fields')
    require(set(native) == {'title', 'description', 'publication_date', 'version', 'publisher',
                           'resource_type', 'creators', 'subjects', 'related_identifiers', 'rights'},
            'Unsupported native metadata fields')
    require(native['publisher'] == 'Zenodo', 'Unexpected native publisher')
    resource = native['resource_type']
    require(isinstance(resource, dict) and set(resource) == {'id', 'title'}
            and resource['id'] == 'publication-preprint', 'Unsupported resource type shape')
    rights = native['rights']
    require(isinstance(rights, list) and len(rights) == 1 and rights[0].get('id') == 'cc-by-4.0',
            'Unsupported native license shape')
    creators = []
    for creator in native['creators']:
        require(set(creator) == {'person_or_org', 'affiliations'}, 'Unsupported creator fields')
        person = creator['person_or_org']
        require(set(person) == {'type', 'name', 'given_name', 'family_name', 'identifiers'}
                and person['type'] == 'personal'
                and person['name'] == person['family_name'] + ', ' + person['given_name'],
                'Unsupported creator name/type/identifier representation')
        identifiers = person['identifiers']
        require(len(identifiers) == 1 and set(identifiers[0]) == {'scheme', 'identifier'}
                and identifiers[0]['scheme'] == 'orcid', 'Unsupported creator identifiers')
        affiliations = creator['affiliations']
        require(len(affiliations) == 1 and set(affiliations[0]) == {'name'}, 'Unsupported affiliations')
        creators.append({'name': person['name'], 'affiliation': affiliations[0]['name'],
                         'orcid': identifiers[0]['identifier']})
    subjects = native['subjects']
    require(all(isinstance(item, dict) and set(item) == {'subject'} for item in subjects),
            'Unsupported controlled subjects')
    relations = []
    for item in native['related_identifiers']:
        require(set(item) == {'identifier', 'scheme', 'relation_type'}, 'Unsupported related identifier fields')
        relation = item['relation_type']
        require(set(relation) == {'id', 'title'} and relation['id'] in {'issupplementedby', 'references'},
                'Unsupported native relation type')
        relations.append({'identifier': item['identifier'], 'scheme': item['scheme'],
                          'relation': {'issupplementedby': 'isSupplementedBy', 'references': 'references'}[relation['id']]})
    access = record.get('access')
    require(isinstance(access, dict) and access.get('record') == 'public' and access.get('files') == 'public'
            and access.get('embargo') == {'active': False, 'reason': None}, 'Unexpected access or embargo')
    require(set(access) <= {'record', 'files', 'embargo', 'status'}, 'Unsupported access fields')
    result = {key: native[key] for key in ('title', 'description', 'publication_date', 'version')}
    result.update(upload_type='publication', publication_type='preprint', access_right='open',
                  license=rights[0]['id'], creators=creators, keywords=[item['subject'] for item in subjects],
                  related_identifiers=relations)
    return result


class NativeOwnDraftClient(zenodo.ZenodoClient):
    def __init__(self, token, metadata, files, *, allow_writes=False, journal_path=None):
        super().__init__('production', token)
        self.metadata = deepcopy(metadata)
        self.files = {entry['name']: entry for entry in files}
        require({name: (f['size'], f['sha256']) for name, f in self.files.items()} == FILE_PINS,
                'Transport accepts only the exact reviewed two files')
        self.allow_writes = allow_writes
        self.journal_path = journal_path or HERE / 'runtime/native-23356540-journal.json'
        if self.journal_path.exists():
            self.journal = zenodo.read_json(self.journal_path)
            require(self.journal.get('id') == RECORD_ID and self.journal.get('manifest_sha256') == MANIFEST_SHA
                    and self.journal.get('file_pins') == {k: list(v) for k, v in FILE_PINS.items()}
                    and isinstance(self.journal.get('operations'), dict), 'Invalid recovery journal')
        else:
            self.journal = {'id': RECORD_ID, 'manifest_sha256': MANIFEST_SHA,
                            'file_pins': {k: list(v) for k, v in FILE_PINS.items()}, 'operations': {}}
        allowed_operations = {'publish'} | {kind + ':' + name for name in self.files for kind in ('initialize', 'content', 'commit')}
        require(set(self.journal['operations']) <= allowed_operations and all(
                isinstance(value, dict) and value.get('phase') in {'attempted', 'response_received', 'verified'}
                and isinstance(value.get('started_utc'), str) for value in self.journal['operations'].values()),
                'Unsupported recovery journal operation/phase')
        self.last_pending = {}
        self._active_write = None

    def pin_id(self, deposit_id):
        require(type(deposit_id) is int and deposit_id == RECORD_ID, 'Only recovered own draft 23356540 is allowed')

    def safe_url(self, url, expected):
        require(isinstance(url, str), 'Missing native endpoint link')
        if url.startswith('/') and not url.startswith('//'):
            url = BASE + url
        parsed = urlsplit(url)
        require(parsed.scheme == 'https' and parsed.netloc == 'zenodo.org' and not parsed.query
                and not parsed.fragment and url == expected, 'Unexpected native endpoint/host/ID')
        return url

    def request(self, method, url, payload=None, file=None, accept='application/json'):
        """Allowlist before calling kit transport; no alternate API/redirect routes."""
        allowed = {('GET', DRAFT), ('GET', REC), ('GET', DRAFT + '/files'), ('GET', REC + '/files')}
        allowed |= {('POST', DRAFT + '/files'), ('POST', DRAFT + '/actions/publish')}
        for name in self.files:
            for prefix in (DRAFT, REC):
                endpoint = prefix + '/files/' + quote(name, safe='')
                allowed.add(('GET', endpoint))
            endpoint = DRAFT + '/files/' + quote(name, safe='')
            allowed |= {('PUT', endpoint + '/content'), ('POST', endpoint + '/commit')}
        self.safe_url(url, url)
        require((method, url) in allowed, 'Native method/endpoint is not allowlisted')
        if method != 'GET':
            require(self.allow_writes, 'This runner is read-only unless explicitly enabled for own draft')
            require(self._active_write == (method, url), 'Native mutation requires durable operation intent')
        return self._wire_request(method, url, payload=payload, file=file, accept=accept)

    def _wire_request(self, method, url, payload=None, file=None, accept='application/json'):
        # Kit request serializes JSON lists too, despite its dict type annotation.
        return super().request(method, url, payload=payload, file=file, accept=accept)

    def save_journal(self):
        self.journal['updated_utc'] = utc()
        try:
            zenodo.save_state(self.journal_path, self.journal)
        except OSError as exc:
            raise zenodo.DepositError('Cannot durably save native recovery journal; no further mutation permitted') from exc

    def operation(self, key, method, url, payload=None, file=None):
        require(self.allow_writes, 'Native mutations are disabled')
        previous = self.journal['operations'].get(key)
        require(previous is None, f'Native {key} was already attempted; no automatic mutating retry')
        self.journal['operations'][key] = {'phase': 'attempted', 'started_utc': utc()}
        self.save_journal()  # Durable intent BEFORE every request.
        self._active_write = (method, url)
        try:
            response = self.request(method, url, payload=payload, file=file)
        finally:
            self._active_write = None
        self.validate_write_response(key, response)
        self.journal['operations'][key]['phase'] = 'response_received'
        self.save_journal()
        return response

    def validate_write_response(self, key, response):
        require(isinstance(response, dict) and not response.get('errors'), 'Native mutation returned errors or malformed acknowledgment')
        if key.startswith(('content:', 'commit:')):
            name = key.split(':', 1)[1]
            require(response.get('key') == name and response.get('status') ==
                    ('completed' if key.startswith('commit:') else 'pending'),
                    'Native file mutation acknowledgment has wrong key/status')
            endpoint = DRAFT + '/files/' + quote(name, safe='')
            for kind, suffix in (('self', ''), ('content', '/content'), ('commit', '/commit')):
                self.safe_url(response.get('links', {}).get(kind), endpoint + suffix)
            if key.startswith('commit:'):
                self.require_file_match(response, self.files[name])
        elif key.startswith('initialize:'):
            require(isinstance(response.get('entries'), list) and
                    any(item.get('key') == key.split(':', 1)[1] for item in response['entries'] if isinstance(item, dict)),
                    'Native initialization acknowledgment omitted expected key')
        elif key == 'publish':
            require(type(response.get('id')) in (int, str) and str(response['id']) == str(RECORD_ID),
                    'Publication acknowledgment has wrong record ID')
        else:
            raise zenodo.DepositError('Unknown native journal operation')

    def confirmed(self, key):
        require(key in self.journal['operations'], 'Missing operation intent')
        self.journal['operations'][key].update(phase='verified', verified_utc=utc())
        self.save_journal()

    def create(self, metadata):
        raise zenodo.DepositError('Creation is prohibited: recover existing draft 23356540 only')

    def edit(self, deposit_id):
        raise zenodo.DepositError('Metadata edit is prohibited')

    def discard(self, deposit_id):
        raise zenodo.DepositError('Discard/delete is prohibited')

    def native_get(self, deposit_id, draft=False):
        self.pin_id(deposit_id)
        return self.request('GET', DRAFT if draft else REC, accept=NATIVE_ACCEPT)

    def file_list(self, draft=True):
        endpoint = (DRAFT if draft else REC) + '/files'
        response = self.request('GET', endpoint)
        require(response.get('enabled') is True and isinstance(response.get('entries'), list), 'Invalid native file collection')
        self.safe_url(response.get('links', {}).get('self'), endpoint)
        entries = {}
        for item in response['entries']:
            require(isinstance(item, dict), 'Invalid native file entry')
            name = item.get('key')
            require(name in self.files and name not in entries, 'Unexpected or duplicate native filename')
            require(item.get('status') in {'pending', 'completed'}, 'Unexpected native file status')
            require(item.get('metadata') in (None, {}), 'Unsupported native file metadata')
            expected = endpoint + '/' + quote(name, safe='')
            links = item.get('links', {})
            self.safe_url(links.get('self'), expected)
            self.safe_url(links.get('content'), expected + '/content')
            if draft:
                self.safe_url(links.get('commit'), expected + '/commit')
            require(set(links) <= {'self', 'content', 'commit'}, 'Unexpected native file links')
            if item['status'] == 'completed':
                self.require_file_match(item, self.files[name])
            else:
                require(draft, 'Published record contains a pending file')
                # Initialized pending files may have no hash or byte count.
                require(item.get('checksum') in (None, '') and item.get('size') in (None, 0),
                        'Pending file unexpectedly exposes checksum/size; reconcile before continuing')
            entries[name] = item
        order = response.get('order')
        require(isinstance(order, list) and len(set(order)) == len(order) and set(order) <= set(entries), 'Unexpected native file order')
        require(response.get('default_preview') is None or response.get('default_preview') in entries, 'Unexpected default preview')
        return entries

    def require_file_match(self, remote, local):
        size = remote.get('size')
        # Official docs historically show integer-valued float sizes.
        require(type(size) in (int, float) and size >= 0 and size == local['size'], 'Native file size differs')
        require(remote.get('checksum') == 'md5:' + local['md5'], 'Native committed checksum differs')

    def remote_sha256(self, name, draft=True):
        url = (DRAFT if draft else REC) + '/files/' + quote(name, safe='') + '/content'
        self.safe_url(url, url)
        return self._wire_digest(url, self.files[name]['size'])

    def _wire_digest(self, url, expected_size):
        """Authenticated bounded binary read. No redirects and no response body log."""
        conn = http.client.HTTPSConnection('zenodo.org', timeout=120)
        try:
            conn.request('GET', urlsplit(url).path, headers={'Authorization': 'Bearer ' + self.token,
                         'Accept': 'application/octet-stream', 'User-Agent': zenodo.USER_AGENT})
            response = conn.getresponse()
            require(response.status == 200, 'Native content read did not return HTTP 200; no retry or commit')
            digest = hashlib.sha256()
            size = 0
            while True:
                block = response.read(zenodo.CHUNK)
                if not block:
                    break
                size += len(block)
                require(size <= expected_size, 'Native content exceeds reviewed size')
                digest.update(block)
            require(size == expected_size, 'Native content has wrong byte count')
            return digest.hexdigest()
        except (OSError, http.client.HTTPException) as exc:
            raise zenodo.DepositError('Native content read failed; bytes/outcome unconfirmed') from exc
        finally:
            conn.close()

    def get(self, deposit_id):
        self.pin_id(deposit_id)
        try:
            record = self.native_get(deposit_id, draft=True)
            draft = True
        except zenodo.DepositError as draft_error:
            try:
                record = self.native_get(deposit_id, draft=False)
                draft = False
            except zenodo.DepositError:
                raise zenodo.DepositError('Neither known draft nor published record can be read; no mutation retry') from draft_error
        require(record.get('id') in (str(RECORD_ID), RECORD_ID) and type(record.get('id')) in (str, int), 'Different native record ID')
        require(type(record.get('is_draft')) is bool and type(record.get('is_published')) is bool, 'Invalid native publication flags')
        require((record['is_draft'], record['is_published'], record.get('status')) ==
                ((True, False, 'draft') if draft else (False, True, 'published')), 'Native state is not an initial draft or confirmed publication')
        links = record.get('links', {})
        self.safe_url(links.get('self'), DRAFT if draft else REC)
        self.safe_url(links.get('files'), (DRAFT if draft else REC) + '/files')
        self.safe_url(links.get('self_html'), BASE + (f'/uploads/{RECORD_ID}' if draft else f'/records/{RECORD_ID}'))
        if draft:
            self.safe_url(links.get('publish'), DRAFT + '/actions/publish')
        metadata = legacy_projection(record)
        require(set(metadata) == set(self.metadata), 'Projected metadata field set differs')
        zenodo.verify({'metadata': metadata, 'files': []}, self.metadata, [])
        pids = record.get('pids')
        require(isinstance(pids, dict) and set(pids) <= {'doi'}, 'Unsupported native persistent identifiers')
        doi = None
        if pids:
            pid = pids['doi']
            require(isinstance(pid, dict) and set(pid) <= {'identifier', 'provider', 'client'}
                    and pid.get('identifier') == DOI and pid.get('provider') == 'datacite'
                    and pid.get('client') in (None, 'datacite'), 'Unexpected native DOI/provider')
            doi = pid['identifier']
        require(draft or doi == DOI, 'Published record has no expected version DOI')
        entries = self.file_list(draft)
        embedded = record.get('files')
        require(isinstance(embedded, dict) and embedded.get('enabled') is True
                and type(embedded.get('count')) is int and embedded['count'] == len(entries)
                and isinstance(embedded.get('entries'), dict) and set(embedded['entries']) == set(entries),
                'Native record/file-collection mismatch')
        require(embedded.get('total_bytes') == sum(x.get('size') or 0 for x in entries.values()), 'Native total byte count differs')
        pending = {name: value for name, value in entries.items() if value['status'] == 'pending'}
        for name in pending:
            require('initialize:' + name in self.journal['operations'], 'Foreign/unjournaled pending upload; refusing to overwrite')
        self.last_pending = pending
        completed = []
        for name, item in entries.items():
            if item['status'] == 'completed':
                require(self.remote_sha256(name, draft) == self.files[name]['sha256'], 'Native remote SHA-256 differs')
                completed.append({'filename': name, 'checksum': item['checksum'], 'filesize': self.files[name]['size']})
        # Only verified completed files are shown to kit. Journaled pending names
        # are handed to upload(), which never repeats already attempted writes.
        result = {'id': RECORD_ID, 'submitted': not draft, 'state': 'unsubmitted' if draft else 'done',
                  'metadata': metadata, 'files': completed,
                  'links': {'bucket': DRAFT + '/files', 'html': links['self_html']}}
        if doi:
            result['doi'] = doi
        return result

    def update(self, deposit_id, metadata):
        self.pin_id(deposit_id)
        require(metadata == self.metadata, 'Metadata writes are not supported')
        return self.get(deposit_id)  # Exact saved metadata: verify and skip PUT.

    def upload(self, bucket, entry):
        self.safe_url(bucket, DRAFT + '/files')
        name = entry.get('name')
        require(name in self.files and entry == self.files[name], 'Unexpected local upload entry')
        require(entry['path'].stat().st_size == entry['size']
                and zenodo.digest(entry['path'], 'sha256') == entry['sha256'], 'Local file changed before native upload')
        # Re-read full metadata/state/file guard immediately before mutating.
        require(self.get(RECORD_ID)['submitted'] is False, 'Cannot upload to a published record')
        entries = self.file_list(True)
        item = entries.get(name)
        if item and item['status'] == 'completed':
            return item
        init = 'initialize:' + name
        content = 'content:' + name
        commit = 'commit:' + name
        error = None
        if not item:
            try:
                self.operation(init, 'POST', DRAFT + '/files', payload=[{'key': name}])
            except zenodo.DepositError as exc:
                error = exc
            # A lost initialization response may still have registered the key.
            entries = self.file_list(True)
            item = entries.get(name)
            require(item is not None and item['status'] == 'pending',
                    'Initialization outcome unconfirmed; intent saved, no mutating retry')
        require(init in self.journal['operations'], 'Pending key was not initialized by this recovery runner')
        self.confirmed(init)
        if content not in self.journal['operations']:
            try:
                self.operation(content, 'PUT', DRAFT + '/files/' + quote(name, safe='') + '/content', file=entry['path'])
            except zenodo.DepositError as exc:
                error = exc
        # A validated HTTP acknowledgment permits reversible commit. A lost
        # response requires independent staged-content SHA-256; if native GET
        # cannot expose pending bytes, stop with durable intent and never PUT again.
        phase = self.journal['operations'][content]['phase']
        if phase == 'attempted':
            require(self.remote_sha256(name, True) == entry['sha256'], 'Pending native content SHA-256 differs; no commit')
        self.confirmed(content)
        if commit not in self.journal['operations']:
            try:
                self.operation(commit, 'POST', DRAFT + '/files/' + quote(name, safe='') + '/commit')
            except zenodo.DepositError as exc:
                error = exc
        entries = self.file_list(True)
        item = entries.get(name)
        require(item is not None and item['status'] == 'completed',
                'Commit outcome unconfirmed; intent saved, no mutating retry')
        self.require_file_match(item, entry)
        require(self.remote_sha256(name, True) == entry['sha256'], 'Committed native content SHA-256 differs')
        self.confirmed(commit)
        return item

    def publish(self, deposit_id):
        self.pin_id(deposit_id)
        # Kit verifies before calling. Recheck at the transport boundary too.
        record = self.get(deposit_id)
        require(not record['submitted'], 'Known record is already published')
        zenodo.verify(record, self.metadata, list(self.files.values()))
        return self.operation('publish', 'POST', DRAFT + '/actions/publish')


@contextmanager
def runner_lock(path):
    import fcntl
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        os.chmod(path, 0o600)
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise zenodo.DepositError('Another local native recovery command is running') from exc
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check', 'preflight', 'stage', 'inspect', 'publish'))
    parser.add_argument('--confirm-id', type=int)
    parser.add_argument('--execute-own-draft', action='store_true')
    parser.add_argument('--check-doi', action='store_true')
    args = parser.parse_args()
    try:
        metadata, files = pinned_inputs()
        args.manifest, args.sandbox = MANIFEST, False
        if args.command == 'check':
            print(json.dumps(zenodo.run(args), indent=2))
            return 0
        if args.command in {'stage', 'publish'}:
            require(args.execute_own_draft and args.confirm_id == RECORD_ID,
                    'Mutation requires --execute-own-draft --confirm-id 23356540')
        place, state = zenodo.local_state(MANIFEST, 'production')
        require(state is not None and state.get('id') == RECORD_ID, 'Existing kit state must pin recovered draft 23356540; no creation permitted')
        with runner_lock(HERE / 'runtime/native-23356540.lock'):
            client = NativeOwnDraftClient(zenodo.token_for('production'), metadata, files,
                                         allow_writes=args.execute_own_draft)
            if args.command == 'preflight':
                record = client.get(RECORD_ID)
                result = {'environment': 'production', 'id': RECORD_ID, 'metadata_verified': True,
                          'submitted': record['submitted'], 'completed_files': [x['filename'] for x in record['files']],
                          'pending_files': sorted(client.last_pending), 'verified_utc': utc(),
                          'note': 'Read-only transport check; this is not a ready-to-publish or publication receipt'}
            else:
                result = zenodo.run(args, client=client)
            print(json.dumps(result, indent=2))
        return 0
    except zenodo.DepositError as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
