"""Apply frozen reviewed metadata patches using the existing metadata-only tool."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'zenodo_deposit_tool'))
import zenodo
import metadata_updates as updates
from baseline import PacedClient, snapshot
from native_views import normalized_draft, normalized_draft_files
from preview_preservation import repair_owned_preview, validate_display_payload, legacy_native_target, public_unchanged

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

class BoundClient(PacedClient):
    """Only the selected existing paper's edit/update/publish endpoints may write."""
    def __init__(self, record_id, baseline, resume=None):
        super().__init__('production', zenodo.token_for('production'))
        self.record_id = record_id
        self.baseline = baseline
        self.first_deposit = True
        self.first_native = True
        self.actions = []
        self.native_normalizations = []
        self.resume = resume

    def request(self, method, url, *args, **kwargs):
        if method != 'GET':
            path = urlsplit(url).path
            root = f'/api/deposit/depositions/{self.record_id}'
            if (method, path) not in {('POST', root+'/actions/edit'), ('PUT', root), ('POST', root+'/actions/publish'),
                                     ('PUT', f'/api/records/{self.record_id}/draft')}:
                raise RuntimeError('Prohibited mutation route')
            if path == f'/api/records/{self.record_id}/draft':
                payload=args[0] if args else kwargs.get('payload')
                file_argument=args[1] if len(args)>1 else kwargs.get('file')
                validate_display_payload(payload,self.baseline,file_argument)
            self.actions.append({'method': method, 'path': path, 'requested_utc': datetime.now(timezone.utc).isoformat()})
        return super().request(method, url, *args, **kwargs)

    def update(self, record_id, metadata):
        if record_id != self.record_id:
            raise RuntimeError('Cannot update another record')
        result = super().update(record_id, metadata)
        session = json.loads(updates.snapshot_path(record_id,'production').read_text())
        try:
            repair = repair_owned_preview(self,record_id,self.baseline,
                                          HERE/'patches'/f'{record_id}.json',session,
                                          HERE/'receipts'/str(record_id))
        except Exception as exc:
            # The surrounding legacy mutate_and_read recovers DepositError by
            # reading once; a preserving-repair failure must instead halt.
            raise RuntimeError(f'Legacy PUT completed; preserving draft repair/verification stopped: {exc}') from exc
        self.native_normalizations.append({k:v for k,v in repair.items() if k not in {'draft','native_staged'}})
        return result

    def publish(self,record_id):
        if record_id != self.record_id:
            raise RuntimeError('Cannot publish another record')
        public_unchanged(self,record_id,self.baseline)
        session=json.loads(updates.snapshot_path(record_id,'production').read_text())
        draft=self.native_get(record_id,draft=True)
        updates.verify_native_preserved({key:draft[key] for key in ('metadata','custom_fields','access','pids')},
                                        session,changed=True)
        if {key:draft[key] for key in ('metadata','custom_fields','access','pids')} != session['native_staged']:
            raise RuntimeError('Pending native state changed immediately before publication')
        return super().publish(record_id)

    def get(self, record_id):
        record = super().get(record_id)
        if self.first_deposit:
            self.first_deposit = False
            b = self.baseline
            if self.resume:
                updates.verify_metadata(record, self.resume['target_metadata'], self.resume)
                if record['state'] != 'inprogress':
                    raise RuntimeError('Recovery requires this owned pending metadata edit')
            elif (record_id != self.record_id or record['state'] != 'done' or
                record['metadata'] != b['metadata'] or updates.file_snapshot(record) != b['files'] or
                updates.record_doi(record) != b['doi'] or record.get('conceptrecid') != b['conceptrecid']):
                raise RuntimeError('Reviewed public deposition baseline changed before edit')
        return record

    def native_get(self, record_id, draft=False):
        record = super().native_get(record_id, draft=draft)
        if draft:
            original = {'id':str(record_id),'pids':self.baseline['native']['pids']}
            record, note = normalized_draft(record, original)
            if note:
                self.native_normalizations.append(note)
            if record.get('is_draft') is not True:
                raise RuntimeError('Expected selected existing draft representation')
            b=self.baseline
            if (any(record[key] != b['identity'][key] for key in ('id','pids','versions')) or
                record['parent']['id'] != b['identity']['parent_id'] or
                record['parent']['pids'] != b['identity']['parent_pids'] or
                any(record[key] != b['native'][key] for key in ('access','custom_fields'))):
                raise RuntimeError('Draft identity/PIDs/access/custom fields changed')
            reviewed_patch=json.loads((HERE/'patches'/f'{record_id}.json').read_text())['metadata']
            expected=legacy_native_target({'metadata':b['native']['metadata']},reviewed_patch,record_id)
            from native_metadata import canonical
            if canonical(record['metadata']) != canonical(expected):
                raise RuntimeError('Draft rich metadata differs from frozen reviewed target')
        file_view, omitted = normalized_draft_files(record, self.baseline['native_files'])
        if file_view != self.baseline['native_files']:
            raise RuntimeError('Native files/preview/order/access changed')
        if omitted:
            self.native_normalizations.append({'kind':'generated_file_links_omitted_in_draft','files':omitted})
        if self.first_native:
            self.first_native = False
            if self.resume:
                updates.verify_native_preserved({k:record[k] for k in ('metadata','custom_fields','access','pids')},self.resume,changed=True)
                if not draft:
                    raise RuntimeError('Recovery requires owned draft view')
            elif draft or record_id != self.record_id:
                raise RuntimeError('Refusing an existing draft or different record')
            b = self.baseline
            if not self.resume and any(record[k] != b['native'][k] for k in ('metadata','pids','access','custom_fields')):
                raise RuntimeError('Reviewed native baseline changed before edit')
            identity_now = {'id':record['id'], 'pids':record['pids'], 'parent_id':record['parent']['id'],
                            'parent_pids':record['parent']['pids'], 'versions':record['versions']}
            if any(identity_now[k] != b['identity'][k] for k in identity_now):
                raise RuntimeError('Record/concept/version identity changed before edit')
        return record

def run_one(record_id):
    approved = json.loads((HERE/'APPROVED_PROPOSALS.json').read_text())
    entry = next(r for r in approved['records'] if r['id'] == record_id)
    patch_path = HERE/'patches'/f'{record_id}.json'
    if hashlib.sha256(patch_path.read_bytes()).hexdigest() != entry['patch_sha256']:
        raise RuntimeError('Reviewed patch changed; obtain a new content audit before applying')
    dest = HERE/'receipts'/str(record_id)
    if (dest/'after.json').exists():
        print(f'Already verified {record_id}; skipped', flush=True)
        return
    before = json.loads((dest/'before.json').read_text())
    if not before['legacy_compatible']:
        raise RuntimeError('Use reviewed preserving native route for this record')
    resume = None
    session_path = updates.snapshot_path(record_id,'production')
    if session_path.exists():
        saved = json.loads(session_path.read_text())
        if saved['phase'] not in updates.FINAL_PHASES:
            recovered_preview = dest/'preview_repair_recovery.json'
            if not (dest/'first_staging_guard_stop.json').exists() and not recovered_preview.exists():
                raise RuntimeError('Unreconciled existing session; inspect before recovery')
            patch = json.loads(patch_path.read_text())['metadata']
            if (saved['original_metadata'] != updates.editable_metadata({'metadata':before['metadata']}) or
                saved['target_metadata'] != {**saved['original_metadata'],**patch} or
                saved['native_original'] != before['native']):
                raise RuntimeError('Pending session is not the exact reviewed original/target')
            if recovered_preview.exists():
                guard = json.loads(recovered_preview.read_text())
                if (guard.get('id') != record_id or guard.get('patch_sha256') != entry['patch_sha256'] or
                    guard.get('baseline_sha256') != hashlib.sha256((dest/'before.json').read_bytes()).hexdigest() or
                    guard.get('native_staged') != saved.get('native_staged') or saved['phase'] != 'staged' or
                    guard.get('verified_complete_draft_files_and_original_public_identity') is not True):
                    raise RuntimeError('Preview recovery receipt does not bind the reviewed staged session')
                resume = saved
            else:
                resume = reconcile_owned_oai(record_id, before, saved, dest, session_path)
    client = BoundClient(record_id, before, resume=resume)
    args = argparse.Namespace(command='update-metadata', record_id=record_id,
                              patch=patch_path, sandbox=False, confirm_id=record_id)
    stage = updates.run_metadata(args, client)
    save(dest/'stage.json', stage)
    if stage['state'] != 'ready_to_publish_metadata':
        raise RuntimeError('Unexpected staging outcome; inspect without retrying')
    args.command = 'publish-metadata'
    published = updates.run_metadata(args, client)
    save(dest/'publish.json', published)
    after = snapshot(client, record_id)
    patch = json.loads(patch_path.read_text())['metadata']
    if before['identity'] != after['identity']:
        raise RuntimeError('Version/concept/DOI identity or complete version list changed')
    for field in ('doi','conceptrecid','files'):
        if before[field] != after[field]:
            raise RuntimeError(f'Protected {field} changed')
    if before['native_files'] != after['native_files']:
        raise RuntimeError('Native file settings changed during metadata edit')
    session = json.loads(session_path.read_text())
    if after['native'] != session['native_staged']:
        raise RuntimeError('Final native metadata differs from staged canonical snapshot')
    for field in ('publication_date','version','license','access_right','title'):
        if before['metadata'].get(field) != after['metadata'].get(field):
            raise RuntimeError(f'Protected metadata.{field} changed')
    updates.verify_metadata({'id':record_id, 'submitted':True, 'state':'done',
                             'doi':after['doi'], 'metadata':after['metadata'],
                             'files':[{'filename':f['name'],'checksum':f['md5'],'filesize':f['size']}
                                      for f in after['files']]},
                            {**updates.editable_metadata({'metadata':before['metadata']}),**patch},
                            {'id':record_id,'doi':before['doi'],'files':before['files']})
    after['verification'] = {'same_record_doi_concept_version_history_files': True,
                             'original_date_version_license_access_title_preserved': True,
                             'reviewed_patch_sha256':entry['patch_sha256'], 'mutation_routes':client.actions}
    after['verification']['draft_representation_normalizations'] = client.native_normalizations
    save(dest/'after.json', after)
    print(f'Published and verified {record_id}: {after["metadata"]["title"]}', flush=True)

def reconcile_owned_oai(record_id, before, saved, dest, session_path):
            # Keep the raw first attempt in its public receipt. Reconcile only the
            # source-proven draft-OAI omission in this task's saved canonical view.
            raw = json.loads((dest/'first_staging_guard_stop.json').read_text())
            staged = raw.get('native_staged')
            if not staged or saved.get('native_staged') is None:
                raise RuntimeError('Recovery requires an inspected native staged snapshot')
            shaped = {**staged,'id':str(record_id),'is_draft':True}
            normalized, note = normalized_draft(shaped,{'id':str(record_id),'pids':before['native']['pids']})
            if not note:
                raise RuntimeError('Recovery exception does not match missing draft OAI')
            canonical_staged = {k:normalized[k] for k in staged}
            if saved['native_staged'] not in (staged,canonical_staged):
                raise RuntimeError('Saved staged view differs from its inspected raw receipt')
            saved['native_staged'] = canonical_staged
            saved['draft_representation_normalization'] = note
            zenodo.save_state(session_path,saved)
            return saved

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('record_ids', type=int, nargs='+')
    args = parser.parse_args()
    for record_id in args.record_ids:
        try:
            run_one(record_id)
        except Exception as exc:
            # Do not print request headers or secret configuration.
            save(HERE/'receipts'/str(record_id)/'application_error.json',
                 {'id':record_id,'error':str(exc),'utc':datetime.now(timezone.utc).isoformat(),
                  'automatic_mutation_retry':False})
            raise
