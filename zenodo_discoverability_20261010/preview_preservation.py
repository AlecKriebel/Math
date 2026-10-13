"""Restore only a reviewed owned draft's legacy-induced preview loss.

No record/version creation, PID/access changes, or file upload/content operation.
All original/target/session and raw public/draft state gates precede one PUT.
"""
import copy
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

from baseline import identity
from native_views import normalized_draft, normalized_draft_files
import zenodo
import metadata_updates as legacy

HERE = Path(__file__).resolve().parent

def display_file_options(files):
    """Only original writable display options, never entries or file contents."""
    enabled = files['enabled']
    preview = files.get('default_preview')
    order = files['order']
    if type(enabled) is not bool or not isinstance(order, list):
        raise RuntimeError('Invalid original file display configuration')
    if preview is not None and (not isinstance(preview, str) or not preview or
                                preview not in files.get('entries', {})):
        raise RuntimeError('Original preview is not an existing file')
    if any(not isinstance(key, str) or key not in files.get('entries', {}) for key in order):
        raise RuntimeError('Original file display order is invalid')
    return copy.deepcopy({'enabled':enabled, 'default_preview':preview, 'order':order})

def validate_display_payload(payload, baseline, file_argument=None):
    if (file_argument is not None or not isinstance(payload,dict) or
        set(payload) != {'metadata','custom_fields','files'} or
        not isinstance(payload['metadata'],dict) or
        payload['custom_fields'] != baseline['native']['custom_fields'] or
        payload['files'] != display_file_options(baseline['native_files'])):
        raise RuntimeError('Native preview PUT may carry only original display options and reviewed metadata')

def legacy_native_target(original, patch, record_id):
    """Existing translator plus two exact already-reviewed legacy corrections.

    Keep the general native route unchanged; these exceptions bind only the
    frozen name-order correction and software-to-preprint correction on their
    selected original legacy-compatible records.
    """
    from native_metadata import translate
    translated_patch=copy.deepcopy(patch)
    rename=None
    if record_id == 22770864 and 'creators' in translated_patch:
        rename=translated_patch.pop('creators')
        if rename != [{'name':'Kriebel, Alec','affiliation':'Independent Researcher',
                       'orcid':'0009-0001-9320-500X'}]:
            raise RuntimeError('Unexpected frozen creator correction')
        creator=original['metadata']['creators']
        if (len(creator)!=1 or creator[0]['person_or_org']['name']!='Alec, Kriebel' or
            creator[0]['person_or_org'].get('type')!='personal' or
            creator[0]['person_or_org'].get('family_name')!='Alec' or
            creator[0]['person_or_org'].get('given_name')!='Kriebel' or
            creator[0].get('affiliations')!=[{'name':'Independent Researcher'}] or
            creator[0]['person_or_org'].get('identifiers') !=
                [{'identifier':'0009-0001-9320-500X','scheme':'orcid'}]):
            raise RuntimeError('Original creator does not match reviewed name-order correction')
    retype=None
    if record_id == 22929556:
        retype={key:translated_patch.pop(key) for key in ('upload_type','publication_type') if key in translated_patch}
        if retype and (retype!={'upload_type':'publication','publication_type':'preprint'} or
                       original['metadata']['resource_type']['id']!='software'):
            raise RuntimeError('Unexpected frozen resource-type correction')
    target=translate(original,translated_patch)
    if rename:
        target['creators']=copy.deepcopy(original['metadata']['creators'])
        person=target['creators'][0]['person_or_org']
        person.update(name='Kriebel, Alec',family_name='Kriebel',given_name='Alec')
    if retype:target['resource_type']={'id':'publication-preprint'}
    return target

def raw_native(client, record_id, draft=False):
    suffix = '/draft' if draft else ''
    return client.request('GET', client.base + f'/api/records/{record_id}{suffix}',
                          accept='application/vnd.inveniordm.v1+json')

def reviewed_session(record_id, baseline, patch_path, session):
    patch = json.loads(patch_path.read_text())['metadata']
    approved = json.loads((HERE/'APPROVED_PROPOSALS.json').read_text())
    entry = next((row for row in approved['records'] if row['id'] == record_id),None)
    if entry is None:
        raise RuntimeError('Preview repair record lacks a frozen reviewed proposal')
    digest = hashlib.sha256(patch_path.read_bytes()).hexdigest()
    if digest != entry['patch_sha256']:
        raise RuntimeError('Preview repair patch differs from frozen reviewed metadata')
    original = legacy.editable_metadata({'metadata':baseline['metadata']})
    if (session.get('id') != record_id or session.get('environment') != 'production' or
        session.get('phase') not in {'update_requested','staged'} or
        session.get('original_metadata') != original or
        session.get('target_metadata') != {**original,**patch} or
        session.get('native_original') != baseline['native'] or
        session.get('files') != baseline['files'] or session.get('doi') != baseline['doi'] or
        session.get('patch_fields') != list(patch)):
        raise RuntimeError('Preview repair is not this exact owned reviewed metadata session')
    if baseline.get('id') != record_id or baseline['identity']['id'] != str(record_id):
        raise RuntimeError('Preview repair baseline belongs to another record')
    return patch, digest

def public_unchanged(client, record_id, baseline):
    record = raw_native(client, record_id)
    versions = client.request('GET', client.base + f'/api/records/{record_id}/versions?size=100',
                              accept='application/vnd.inveniordm.v1+json')
    if (record.get('is_draft') is not False or not record.get('is_published') or
        identity(record, versions) != baseline['identity'] or
        record['files'] != baseline['native_files'] or
        any(record[key] != baseline['native'][key] for key in ('metadata','pids','access','custom_fields'))):
        raise RuntimeError('Public record or complete version registry changed before preview repair')
    return record

def checked_draft(client, record_id, baseline, session, expected_metadata):
    # The legacy endpoint is the pending draft; public state is verified separately.
    deposit = client.get(record_id)
    if deposit.get('state') != 'inprogress' or not deposit.get('submitted'):
        raise RuntimeError('Preview repair requires an existing owned pending metadata draft')
    legacy.verify_metadata(deposit, session['target_metadata'], session)
    if deposit.get('conceptrecid') != baseline['conceptrecid']:
        raise RuntimeError('Pending draft concept identity changed')
    raw = raw_native(client, record_id, draft=True)
    if raw.get('is_draft') is not True or str(raw.get('id')) != str(record_id):
        raise RuntimeError('Preview repair did not read the selected existing draft')
    view, normalization = normalized_draft(raw, {'id':str(record_id),'pids':baseline['native']['pids']})
    for key in ('id','pids','versions'):
        if view[key] != baseline['identity'][key]:
            raise RuntimeError('Pending draft record/PIDs/version identity changed')
    if (view['parent']['id'] != baseline['identity']['parent_id'] or
        view['parent']['pids'] != baseline['identity']['parent_pids']):
        raise RuntimeError('Pending draft parent identity changed')
    native = {key:view[key] for key in ('metadata','custom_fields','access','pids')}
    legacy.verify_native_preserved(native, session, changed=True)
    # Late import avoids a cycle with native_metadata's display-config helper.
    from native_metadata import canonical
    if canonical(raw['metadata']) != canonical(expected_metadata):
        raise RuntimeError('Pending rich metadata differs from exact reviewed native target')
    file_view, omitted = normalized_draft_files(raw, baseline['native_files'])
    return raw, native, file_view, {'pid':normalization,'omitted_generated_links':omitted}

def repair_owned_preview(client, record_id, baseline, patch_path, session, receipt_dir):
    """Verify all state; repair original-string→None preview with one native PUT.

    Returns the verified draft even when no repair is needed. No mutation retry.
    The caller holds the selected legacy record's lock throughout.
    """
    patch, digest = reviewed_session(record_id, baseline, patch_path, session)
    public = public_unchanged(client, record_id, baseline)
    from native_metadata import canonical
    target = legacy_native_target(public, patch, record_id)
    raw, native, files, normalizations = checked_draft(client, record_id, baseline, session, target)
    original_files = baseline['native_files']
    if files == original_files:
        return {'id':record_id,'state':'preview_already_preserved','draft':raw,'native_staged':native,
                'patch_sha256':digest,'normalizations':normalizations,'mutations':0}
    preview = original_files.get('default_preview')
    restored_view = copy.deepcopy(files)
    restored_view['default_preview'] = preview
    if (not isinstance(preview, str) or not preview or files.get('default_preview') is not None or
        restored_view != original_files):
        raise RuntimeError('Draft file difference is not solely original preview lost to None')
    pre_path = receipt_dir/'preview_repair_pre.json'
    if pre_path.exists():
        raise RuntimeError('Preview repair was already requested; inspect receipts without mutation retry')
    payload = {'metadata':copy.deepcopy(raw['metadata']),
               'custom_fields':copy.deepcopy(baseline['native']['custom_fields']),
               'files':display_file_options(original_files)}
    validate_display_payload(payload,baseline)
    pre = {'id':record_id,'utc':datetime.now(timezone.utc).isoformat(),'patch_sha256':digest,
           'public':public,'draft':raw,'session':copy.deepcopy(session),'payload':payload,
           'normalizations':normalizations,'phase':'repair_requested','automatic_mutation_retry':False}
    zenodo.save_state(pre_path, pre)  # Durable before the only mutation.
    client.request('PUT', client.base + f'/api/records/{record_id}/draft', payload,
                   accept='application/vnd.inveniordm.v1+json')
    after, after_native, after_files, after_normalizations = checked_draft(
        client, record_id, baseline, session, target)
    if after_files != original_files or canonical(after['metadata']) != canonical(raw['metadata']):
        raise RuntimeError('Preview restoration read-back did not preserve complete draft state')
    public_unchanged(client, record_id, baseline)
    post = {'id':record_id,'utc':datetime.now(timezone.utc).isoformat(),'patch_sha256':digest,
            'draft':after,'native_staged':after_native,'normalizations':after_normalizations,
            'phase':'preview_restored','full_files_and_public_identity_preserved':True,
            'automatic_mutation_retry':False}
    zenodo.save_state(receipt_dir/'preview_repair_post.json', post)
    return {'id':record_id,'state':'preview_restored','draft':after,'native_staged':after_native,
            'patch_sha256':digest,'normalizations':after_normalizations,'mutations':1}
