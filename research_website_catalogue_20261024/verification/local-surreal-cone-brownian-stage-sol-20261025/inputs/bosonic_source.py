"""Authenticated, read-only adapter for the original Zenodo 23203100 layout.

No replacement receipt is persisted. PublishedAssets receives an ephemeral view
only after raw API, receipt, deposited assets, review and root bindings agree.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT_CLEARANCE_SHA256 = 'e186543476c3a507b7ba5fc59df50432963efce03d6791015eb8f48becb61ca6'


def contained_file(root, relative):
    relative = PurePosixPath(relative)
    if relative.is_absolute() or not relative.parts or any(x in ('', '.', '..') for x in relative.parts):
        raise ValueError('Invalid contained source path')
    current = Path(root)
    if current.is_symlink():
        raise ValueError('Symlink source root')
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlink in source path')
    resolved = current.resolve(strict=True)
    if not resolved.is_relative_to(Path(root).resolve()) or not resolved.is_file():
        raise ValueError('Source is not a contained regular file')
    return resolved


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bosonic_source_view(paper, config, gate):
    """Return (unchanged raw list, derived asset receipt, original asset root)."""
    if Path(paper).name != '23203100':
        raise ValueError('Adapter is restricted to Zenodo 23203100')
    binding = config['source_binding']
    assert binding['record_id'] == gate['record_id'] == '23203100'
    assert gate['publication_sha256'] == digest(contained_file(paper, 'publication.json'))
    assert gate['status'] == 'PASS' and gate['disposition_by'] == 'root'
    assert binding['receipt_path'] == gate['source_receipt_path'] == 'sources/record/transport_receipts.json'
    assert binding['record_path'] == binding['metadata_path'] == gate['metadata_path'] == 'sources/record/zenodo_record.json'
    assert binding['receipt_schema'] == gate['source_receipt_schema'] == 'transport_receipt_list'
    assert binding['asset_root'] == 'sources/assets' and binding['embedded_assets'] == []
    raw_path = contained_file(paper, binding['receipt_path'])
    record_path = contained_file(paper, binding['record_path'])
    raw = json.loads(raw_path.read_bytes())
    api = json.loads(record_path.read_bytes())
    assert type(raw) is list and len(raw) == 3
    assert [x['saved'] for x in raw] == ['record/zenodo_record.json', 'assets/zenodo-upload-kit.zip', 'assets/paper.pdf']
    assert all(x['status'] == 200 and x['url'] == x['final_url'] for x in raw)
    assert digest(raw_path) == binding['receipt_sha256'] == binding['source_receipt_sha256'] == gate['source_receipt_sha256']
    assert digest(record_path) == binding['record_sha256'] == binding['metadata_sha256'] == gate['metadata_sha256'] == raw[0]['sha256']
    assert record_path.stat().st_size == raw[0]['bytes']
    assert raw[0]['url'] == 'https://zenodo.org/api/records/23203100'
    metadata = api['metadata']
    assert str(api['id']) == '23203100' and str(api['conceptrecid']) == binding['concept_record_id'] == '23203099'
    assert all(config[k] == metadata[k] for k in ('title', 'doi', 'publication_date'))
    assert config['author'] == 'Alec Kriebel' and metadata['creators'][0]['name'] == 'Kriebel, Alec'
    assert metadata['creators'][0]['orcid'] == '0009-0001-9320-500X'
    assert config['version'] is binding['zenodo_version'] is binding['manuscript_version'] is None and 'version' not in metadata
    assert config['publication_date'] == binding['manuscript_date'] == binding['zenodo_publication_date'] == '2026-10-06'
    assert api['created'] == binding['record_created_utc'] == '2026-10-07T04:42:47.312983+00:00'
    assert api['updated'] == binding['record_updated_utc']
    programme = Path(paper).parents[1]
    clearance_path = contained_file(programme, gate['root_clearance_file'])
    assert gate['root_clearance_file'] == config['review_metadata']['root_clearance_file'] == 'verification/root-clearance-23203100-20261025.json'
    assert digest(clearance_path) == gate['root_clearance_sha256'] == config['review_metadata']['root_clearance_sha256'] == ROOT_CLEARANCE_SHA256
    clearance = json.loads(clearance_path.read_bytes())
    assert clearance == gate['root_clearance_record'] and clearance['status'] == 'PASS'
    assert clearance['approved_scope'] == gate['approved_scope'] and clearance['scope_gate_resolution'] == gate['scope_gate_resolution']
    assert clearance['source_receipt_sha256'] == digest(raw_path)
    assert all(digest(contained_file(paper, rel)) == item['sha256'] for rel, item in clearance['source_receipts'].items())
    assert set(gate['reviews']) == set(clearance['reviews']) == {'scope', 'analytic', 'adversarial', 'upstream_analytic', 'upstream_adversarial'}
    for role, item in gate['reviews'].items():
        authority = clearance['reviews'][role]
        assert authority['report'] == 'papers/23203100/' + item['report']
        assert authority['verdict'] == 'papers/23203100/' + item['verdict_file']
        assert digest(contained_file(paper, item['report'])) == item['sha256'] == authority['report_sha256']
        verdict_path = contained_file(paper, item['verdict_file'])
        assert digest(verdict_path) == item['verdict_sha256'] == authority['verdict_sha256']
        assert json.loads(verdict_path.read_bytes()) == item['verdict']
    assert len(api['files']) == len(binding['files']) == 2 and gate['source_files'] == binding['files']
    assert {x['key'] for x in api['files']} == {x['filename'] for x in binding['files']} == {'paper.pdf', 'zenodo-upload-kit.zip'}
    for item in binding['files']:
        name = item['filename']
        receipt_item = raw[item['receipt_index']]
        api_item = next(x for x in api['files'] if x['key'] == name)
        assert item['source_relative_path'] == 'sources/assets/' + name
        assert item['receipt_saved_path'] == receipt_item['saved'] == 'assets/' + name
        assert item['url'] == receipt_item['url'] == api_item['links']['self']
        assert item['api_checksum'] == receipt_item['record_checksum'] == api_item['checksum'] == 'md5:' + item['md5']
        path = contained_file(paper, item['source_relative_path'])
        data = path.read_bytes()
        assert len(data) == item['bytes'] == receipt_item['bytes'] == receipt_item['record_bytes'] == api_item['size']
        assert hashlib.md5(data).hexdigest() == item['md5'] == receipt_item['md5']
        key = 'pdf_sha256' if name == config['pdf_filename'] else 'supplement_sha256'
        assert digest(path) == item['sha256'] == receipt_item['sha256'] == binding[key] == gate[key] == clearance[key]
    return raw, {'record_id': '23203100', 'files': binding['files']}, contained_file(paper, 'sources/assets/paper.pdf').parent
