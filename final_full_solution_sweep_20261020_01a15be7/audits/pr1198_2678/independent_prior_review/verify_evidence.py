"""Read-only closure checks of the retained PR1198 publication evidence.

This authenticates evidence relationships, not continuous topology theorems.
No provider calls, extraction, external programs, or writes are performed.
"""
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_sources'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(name):
    return json.loads((PRIVATE / name).read_bytes())


def main():
    record = read('record.json')
    require(record == read('concept_record.json'), 'Concept API differs')
    require(record['id'] == 23165876 and record['conceptrecid'] == '23127198', 'Wrong family')
    require(record['state'] == 'done' and record['submitted'] is True, 'Not published')
    require(record['doi'] == '10.5281/zenodo.23165876'
            and record['conceptdoi'] == '10.5281/zenodo.23127198', 'DOI mismatch')
    metadata = record['metadata']
    require(metadata['version'] == '1.1' and metadata['publication_date'] == '2026-10-05', 'Wrong version')
    require(metadata['title'] == 'Asymmetric Hyperbolic Knots Detect Mapping Classes of 3-Manifolds: A Written Proof for a Problem of the K3 List', 'Title mismatch')
    require(metadata['creators'] == [{'name':'Ferudun, Alper','affiliation':'Mercury Software GmbH'}], 'Creator mismatch')
    records = json.loads((HERE / 'PRIMARY_RETRIEVALS.json').read_bytes())
    version = next(x for x in records if x['name'] == 'version_doi')
    concept = next(x for x in records if x['name'] == 'concept_doi')
    require(version['status'] == 404, 'Observed version DOI outcome changed')
    require(concept['status'] == 200 and concept['final_url'] == 'https://zenodo.org/records/23165876', 'Concept does not bind exact version')
    vr = read('version_registry.json')['data']['attributes']
    cr = read('concept_registry.json')['data']['attributes']
    require(vr['state'] == 'findable' and cr['state'] == 'findable', 'Registry state')
    require(vr['doi'] == record['doi'] and cr['doi'] == record['conceptdoi'], 'Registry DOI mismatch')
    require(any(x['relationType'] == 'IsVersionOf' and x['relatedIdentifier'] == record['conceptdoi'] for x in vr['relatedIdentifiers']), 'Missing version-to-concept relation')
    require(any(x['relationType'] == 'HasVersion' and x['relatedIdentifier'] == record['doi'] for x in cr['relatedIdentifiers']), 'Missing concept-to-version relation')
    for attrs in [vr, cr]:
        require(attrs['titles'] == [{'title':metadata['title']}]
                and attrs['version'] == '1.1' and attrs['creators'][0]['name'] == 'Ferudun, Alper', 'Registry metadata mismatch')
    inventory = []
    require({x['key'] for x in record['files']} == {'KP-1.19-paper.pdf','KP-1.19-source.zip','KP-1.19-verification-report.md'}, 'Inventory mismatch')
    for item in record['files']:
        raw = (PRIVATE / item['key']).read_bytes()
        require(len(raw) == item['size'] and 'md5:'+hashlib.md5(raw).hexdigest() == item['checksum'], 'File checksum mismatch')
        inventory.append({'name':item['key'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    require(hashlib.sha256((PRIVATE/'KP-1.19-paper.pdf').read_bytes()).hexdigest() == '2c4973940aa4fc9e4eb89854a5b42b1147392b55ba268a2b460d0455a160c243', 'PR paper pin differs')
    with zipfile.ZipFile(PRIVATE/'KP-1.19-source.zip') as archive:
        require(archive.testzip() is None, 'Archive CRC failure')
        names = [item.filename for item in archive.infolist() if not item.is_dir()]
        require(len(names) == 20 and 'main.tex' in names and 'references.bib' in names
                and 'reproducibility/README.md' in names, 'Source/support members missing')
        require(archive.read('verification_report.md') == (PRIVATE/'KP-1.19-verification-report.md').read_bytes(), 'Two report copies differ')
        tex = archive.read('main.tex').decode()
        require('version 1.1: October 5, 2026' in tex and metadata['title'] in tex, 'Source version/title mismatch')
    bindings = json.loads((HERE/'PR_BINDINGS.json').read_bytes())
    require(bindings['head'] == '3586a64988bc5aba234c8cb27b44fa14505e6d2c'
            and len(bindings['complete_paths']) == 8 and bindings['no_QUEUE_changed'], 'PR binding failure')
    for item in bindings['complete_paths']:
        raw = (HERE/'inputs'/Path(item['path']).name).read_bytes()
        require(len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256'], 'PR input pin failure')
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == item['blob'], 'Git blob pin failure')
    print(json.dumps({'status':'passed','existing_published_record':23165876,'version':'1.1',
      'concept_doi_resolved_to_exact_version':True,'version_doi_observed_404_retained':True,
      'registry_reciprocal_family_links':True,'all_three_payloads_size_md5_verified':True,
      'source_archive_members':20,'source_archive_crc_clean':True,'same_report_inside_and_outside_zip':True,
      'all_eight_PR_inputs_bound':True,'inventory':inventory,
      'limit':'No live-state check or full classical-proof/continuous-topology certification is implied by these evidence checks.'},indent=2))


if __name__ == '__main__':
    main()
