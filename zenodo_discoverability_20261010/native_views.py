"""One source-verified draft/public PID representation exception.

Zenodo's legacy metadata deserializer replaces draft pids with DOI only.
Invenio's publish component restores REQUIRED public PIDs, including OAI.
Accept only that exact missing-OAI draft view; full original public PIDs are
still required at every public boundary and after publication.
"""
import copy

def normalized_draft_files(record, original_files):
    """Draft serialization omits generated per-file links; protect all else."""
    files = record['files']
    if record.get('is_draft') is not True:
        return files, []
    view = copy.deepcopy(files)
    omitted = []
    for name, entry in view.get('entries', {}).items():
        original = original_files.get('entries', {}).get(name, {})
        if 'links' not in entry and 'links' in original:
            entry['links'] = copy.deepcopy(original['links'])
            omitted.append(name)
    return view, omitted

def normalized_draft(record, original):
    expected = original['pids']
    actual = record['pids']
    oai = expected.get('oai')
    omission = {k:v for k,v in expected.items() if k != 'oai'}
    if (record.get('is_draft') is True and oai == {
            'identifier': f'oai:zenodo.org:{original["id"]}', 'provider':'oai'}
            and actual == omission and 'doi' in actual):
        normalized = copy.deepcopy(record)
        normalized['pids'] = copy.deepcopy(expected)
        return normalized, {'field':'pids.oai','kind':'required_public_oai_omitted_in_draft',
                            'original_public_oai':oai, 'raw_draft_pids':actual}
    return record, None
