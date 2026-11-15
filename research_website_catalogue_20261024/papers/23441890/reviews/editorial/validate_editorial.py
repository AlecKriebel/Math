"""Read-only editorial contract validator; no source/scientific program execution.

Run python3 -E -B validate_editorial.py [--preseal] [--negative-controls].
Negative cases alter only in-memory copies. This does not verify a live page.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

P = Path(__file__).resolve().parent
B = P.parents[1]
BASE = B.parents[1]
AUTHORITY = BASE/'verification/root-clearance-23441890-20261114.json'
AUTHORITY_HASH = 'c09a3b765eabc0b98f61dd2f4bafe1f831ccefb0d6b5dc848e109ffa33dfa7c5'
ROOT_REVIEW_HASH = '4074c0fd7a82b7e586a9f8b2e03907ccab385c749218c00a56f4184478e59769'
GATES = ['production_integration_authorized', 'publication_clearance', 'ready_to_publish',
         'rendered_copy_verified', 'local_http_verified', 'deployed', 'live_verified',
         'browser_verified', 'native_verified', 'canonical_verified']


class ContractError(Exception):
    pass


def need(x, label):
    if not x:
        raise ContractError(label)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def public_sections(text):
    return {m[1]: m[2].strip() for m in re.finditer(
        r'^## ([^\n]+)\n\n([\s\S]*?)(?=^## |\Z)', text, re.M)}


def contract(state, authority, ready, record, latest, versions, tex):
    pub, prom, metadata = state['pub'], state['prom'], state['meta']
    body = state['body']
    sections = public_sections(body)
    expected_abstract = ' '.join(tex.split('\\begin{abstract}\n', 1)[1].split(
        '\\end{abstract}', 1)[0].strip().replace('\\Z', '\\mathbb Z').split())
    need(pub['abstract'] == sections.get('Original abstract') == expected_abstract,
         'full original abstract')
    result = sections.get('The precise result', '')
    for token, label in [
        ('including a right affine germ at $0$', 'right germ at0'),
        ('initial ray at $-\\infty$', 'initial affine ray'),
        ('one automorphism', 'one fixed alpha'),
        ('both Dlab bi-orders', 'both source orders'),
        ('every injective homomorphism', 'every abstract injective embedding'),
        ('every $u\\in A$', 'every ambient conjugator'),
        ('abstract group embedding', 'no order-preserving restriction'),
        ('Positive ambient slopes are unrestricted', 'unrestricted ambient slopes'),
        ('For any multiplicative subgroup $H\\le\\mathbb R_{>0}$', 'arbitrary positive-real H'),
        ('D_H(I),\\quad D_{H*}(I),\\quad D_{*H}(I),\\quad\\overline D_H(I),\\qquad D_H,\\quad D_{H*},\\quad D_{*H},\\quad\\overline D_H', 'all eight standard families'),
        ('For every automorphism $\\beta$', 'full arbitrary-beta countermodel'),
        ('with **no condition at $-\\infty$**', 'genuine larger B boundary'),
        ('E(\\beta(f))=v^{-1}E(f)v', 'countermodel conjugation direction'),
        ('\\phi_n\\beta^n(f)\\phi_n^{-1}', 'complete bilateral cell construction'),
        ('v(x)=\\begin{cases}x/2,&x<0,\\\\x,&x\\ge0.', 'exact implementing map'),
        ('e(\\alpha(f))\\ne u^{-1}e(f)u', 'full nonimplementation formula')]:
        need(token in result, label)
    need(pub['title'] == record['metadata']['title'] and body.startswith('# '+pub['title']+'\n'), 'exact original title')
    need(pub['publication_date'] == metadata['schema']['datePublished'] == '2026-10-17', 'original date')
    need(pub['version'] == metadata['schema']['version'] == record['metadata']['version'] == '1.0.0', 'exact native version')
    need(pub['doi'] == '10.5281/zenodo.23441890' and metadata['citation']['citation_doi'] == pub['doi'], 'exact DOI')
    need(pub['author'] == 'Alec Kriebel' and pub['orcid'] == 'https://orcid.org/0009-0001-9320-500X', 'author and ORCID')
    need(record['metadata']['license'] == {'id': 'cc-by-4.0'} and
         pub['license'] == pub['code_license'] == 'CC BY 4.0', 'actual code/prose CC BY license')
    sb = pub['source_binding']
    need([x['original_api_file_object']['key'] for x in sb['all_assets_in_original_order']] ==
         ['source-and-verification.zip', 'paper.pdf'], 'native ZIP-before-PDF order')
    need(sb['whole_original_source_ready'] == prom['whole_original_source_ready'] == ready,
         'whole original READY and historical flags')
    for key, expected in [('whole_native_record', record), ('whole_native_latest_record', latest),
                          ('whole_native_versions', versions)]:
        need(sb[key] == expected, 'whole native API object '+key)
    need(prom['whole_original_native_record'] == record and
         prom['whole_original_native_latest_record'] == latest and
         prom['whole_original_native_versions'] == versions, 'promotion whole API schemas')
    need(sb['all_assets_in_original_order'] == ready['all_assets_in_original_order'], 'whole native asset objects')
    need(sb['whole_original_native_transport_objects'] == prom['whole_original_native_transport_objects'] ==
         authority['whole_native_transport_objects'], 'all six complete actual transport objects')
    need(prom['whole_root_scientific_clearance_record'] == authority and prom['reviews'] == authority['reviews'],
         'whole exact root authority and literal verdicts')
    for lane in ['scope', 'analytic', 'adversarial']:
        need(pub['review_metadata']['whole_original_review_verdicts'][lane] ==
             authority['reviews'][lane]['verdict_original'], 'literal custom verdict '+lane)
    need(prom['scientific_status'] == pub['review_metadata']['scientific_status'] == authority['status'],
         'custom root scientific status')
    need(prom['status'] == 'PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED', 'private editorial status')
    for obj in [prom, pub['review_metadata'], state['adapter'], state['requirements']]:
        need(all(obj.get(k) is False for k in GATES), 'all current publishing gates closed')
        need(all(obj.get(k) is None for k in ['canonical_url', 'native_sheet_aa_url', 'AA']), 'null canonical and AA')
        need(obj.get('root_copy_and_config_adoption_required') is True, 'root copy/config adoption required')
    need(pub['canonical_url'] is None and pub['AA'] is None and metadata['canonical_url'] is None
         and metadata['citation']['citation_pdf_url'] is None and metadata['schema']['url'] is None
         and metadata['seo']['open_graph_url'] is None, 'no invented current canonical or local PDF URL')
    need(pub['proposed_canonical_url'] == prom['proposed_canonical_url'] == metadata['proposed_canonical_url']
         and pub['proposed_canonical_url'].endswith('/'+pub['slug']+'/'), 'separate consistent proposed canonical')
    need(pub['follow_up'] is None and prom['follow_up'] is None and state['sections']['follow_up'] is None,
         'follow-up omitted')
    need('## Follow' not in body and 'Related questions include' not in body, 'no generic follow-up section')
    for key, heading in [('plain_language', 'The idea in plain English'), ('result', 'The precise result'),
                         ('why_it_works', 'Why the result holds'), ('limitations', 'Scope and limitations')]:
        need('\n\n'.join(pub[key]) == sections[heading], 'public copy/config consistency '+key)
    for key, heading in [('background', 'Background and prior work'),
                         ('collaboration', 'Collaborate on this result')]:
        need(pub[key] == sections[heading], 'public copy/config consistency '+key)
    need(state['sections']['sections'] == sections, 'complete public section object')
    need(pub['ai_disclosure'] == sections['Status and AI use'] and 'used extensively' in pub['ai_disclosure']
         and 'not independent human peer review' in pub['ai_disclosure']
         and 'No formal proof-assistant verification' in pub['ai_disclosure'], 'honest concise AI/unrefereed/formal disclosure')
    need('Dlab' in sections['Background and prior work'] and 'Zenkov' in sections['Background and prior work']
         and 'Gong' in sections['Background and prior work'] and 'earlier one-tail' in sections['Background and prior work']
         and 'original non-inner' in sections['Background and prior work'] and 'not a certification' in sections['Background and prior work'],
         'classical credit and distinct Lean antecedent')
    need('Historical first priority remains unestablished' in sections['Scope and limitations']
         and 'No claim about the present open status' in sections['Scope and limitations'], 'honest priority/openness limit')
    need('would be welcome' in pub['collaboration'] and 'actual contributions' in pub['collaboration'], 'passive contribution-based collaboration')
    need('<iframe src="paper.pdf"' in body and 'complete six-page paper PDF' in body
         and '<a href="paper.pdf" download>' in body and '<a href="source-and-verification.zip" download>' in body,
         'accessible unchanged reader and explicit complete downloads')
    need(pub['pdf_filename'] == 'paper.pdf' and pub['pdf_pages'] == 6
         and pub['supplement_filename'] == 'source-and-verification.zip', 'exact complete reader/archive names')
    need([x['name'] for x in metadata['schema']['encoding']] == ['source-and-verification.zip', 'paper.pdf'], 'schema native asset order')
    need(metadata['citation']['citation_publication_date'] == '2026/10/17'
         and metadata['citation']['citation_version'] == '1.0.0', 'citation date/version')
    need(110 <= len(pub['description']) <= 180 and metadata['seo']['description'] == pub['description'], 'descriptive consistent SEO')
    need(not re.search(r'SHA256|checkpoint|manifest|November 14|2026-11-1[45]|closure checks', body, re.I),
         'no private audit/hash/count/log narrative in public copy')
    return True


def replace_public(state, old, new):
    need(old in state['body'], 'negative fixture target exists')
    state['body'] = state['body'].replace(old, new)
    for key in ['plain_language', 'result', 'why_it_works', 'limitations']:
        state['pub'][key] = [x.replace(old, new) for x in state['pub'][key]]
    for key in ['background', 'collaboration', 'ai_disclosure']:
        state['pub'][key] = state['pub'][key].replace(old, new)
    if old in state['pub']['abstract']:
        state['pub']['abstract'] = state['pub']['abstract'].replace(old, new)
    state['sections']['sections'] = public_sections(state['body'])


def main():
    need(sys.flags.ignore_environment and sys.dont_write_bytecode, 'run python3 -E -B')
    need(set(sys.argv[1:]) <= {'--preseal', '--negative-controls'}, 'supported arguments')
    authority = load(AUTHORITY)
    need(sha(AUTHORITY) == AUTHORITY_HASH and sha(Path(authority['root_review']['path'])) == ROOT_REVIEW_HASH,
         'exact root clearance and review')
    for entry in load(P/'PROTECTED_INPUTS.json')['files']:
        path = Path(entry['path'])
        need(path.is_file() and path.stat().st_size == entry['bytes'] and sha(path) == entry['SHA256'],
             'unchanged protected input '+str(path))
    ready = load(B/'sources/SOURCE_READY.json')
    need(sha(B/'sources/SOURCE_READY.json') == authority['source_ready_sha256'], 'frozen READY hash')
    for obj in authority['whole_native_transport_objects']:
        path = Path(obj['path'])
        need(sha(path) == obj['sha256'] and load(path) == obj['original'], 'actual complete transport')
    for asset in ready['all_assets_in_original_order']:
        data = Path(asset['path']).read_bytes()
        need(len(data) == asset['bytes'] and hashlib.sha256(data).hexdigest() == asset['sha256']
             and hashlib.md5(data).hexdigest() == asset['md5'], 'native unchanged complete asset')
    with zipfile.ZipFile(B/'sources/source-and-verification.zip') as archive:
        infos = archive.infolist()
        need(len(infos) == 16 and sum(x.file_size for x in infos) == 227895, 'whole native ZIP count/bytes')
        for info in infos:
            need(archive.read(info) == (B/'sources/published-source'/info.filename).read_bytes(), 'complete original ZIP payload equality')
    need((B/'sources/paper.pdf').read_bytes() ==
         (B/'sources/published-source/kourovka-21-149/paper.pdf').read_bytes(), 'embedded complete reader identity')
    record, latest, versions = [load(B/'sources'/name) for name in ['record.raw.json', 'latest.raw.json', 'versions.raw.json']]
    tex = Path(ready['controlling_TeX']['path']).read_text()
    state = {'pub': load(B/'publication.json'), 'prom': load(B/'promotion.json'),
             'meta': load(P/'SCHOLARLY_METADATA.json'), 'body': (P/'PUBLIC_COPY.md').read_text(),
             'sections': load(P/'public-sections.json'), 'adapter': load(P/'SCHEMA_ADAPTER.json'),
             'requirements': load(P/'PUBLICATION_REQUIREMENTS.json')}
    contract(state, authority, ready, record, latest, versions, tex)
    need(state['prom']['publication_sha256'] == sha(B/'publication.json'), 'publication config hash')
    bib = (P/'citation.bib').read_text()
    need(all(x in bib for x in ['Kriebel, Alec', state['pub']['title'], '1.0.0', '10.5281/zenodo.23441890', 'day = {17}']), 'complete BibTeX')
    negatives = []
    if '--negative-controls' in sys.argv:
        cases = [
            ('abstract_omission', lambda d: replace_public(d, 'This extends a one-tail mechanism used in prior work. ', '')),
            ('missing_right_germ0', lambda d: replace_public(d, 'including a right affine germ at $0$', 'with no germ condition at $0$')),
            ('missing_initial_affine_ray', lambda d: replace_public(d, 'initial ray at $-\\infty$', 'ray with no eventual affine condition')),
            ('order_preserving_only_embedding', lambda d: replace_public(d, 'every injective homomorphism', 'every order-preserving injective homomorphism')),
            ('rank_one_only_H', lambda d: replace_public(d, 'For any multiplicative subgroup $H\\le\\mathbb R_{>0}$', 'For any cyclic subgroup $H\\le\\mathbb R_{>0}$')),
            ('dropped_reflected_family', lambda d: replace_public(d, ',\\quad D_{*H},', ',')),
            ('weakened_arbitrary_beta', lambda d: replace_public(d, 'For every automorphism $\\beta$', 'For some automorphism $\\beta$')),
            ('MIT_default', lambda d: d['pub'].__setitem__('code_license', 'MIT')),
            ('reversed_native_assets', lambda d: d['pub']['source_binding']['all_assets_in_original_order'].reverse()),
            ('invented_current_canonical', lambda d: d['prom'].__setitem__('canonical_url', d['prom']['proposed_canonical_url'])),
            ('generic_PASS_normalization', lambda d: d['pub']['review_metadata']['whole_original_review_verdicts']['scope'].__setitem__('status', 'PASS')),
            ('historical_unread_flag_rewritten', lambda d: d['pub']['source_binding']['whole_original_source_ready'].__setitem__('target_mathematics_scientifically_read', True)),
            ('publication_gate_opened', lambda d: d['prom'].__setitem__('ready_to_publish', True)),
            ('public_audit_narrative', lambda d: replace_public(d, '[All research](/research/)',
                 '[All research](/research/)\n\nCheckpoint manifest SHA256 on November 14.')),
        ]
        for name, mutation in cases:
            altered = copy.deepcopy(state)
            mutation(altered)
            try:
                contract(altered, authority, ready, record, latest, versions, tex)
            except ContractError as err:
                negatives.append({'case': name, 'rejected': True, 'reason': str(err)})
            else:
                raise ContractError('negative control accepted: '+name)
    if '--preseal' not in sys.argv:
        manifest = load(P/'MANIFEST.json')
        for entry in manifest['files']:
            path = Path(entry['path'])
            need(path.resolve().is_relative_to(P) or path in [B/'publication.json', B/'promotion.json'],
                 'only owned editorial/config paths in final manifest')
            need(path.stat().st_size == entry['bytes'] and sha(path) == entry['SHA256'], 'sealed owned artifact')
        exclusions = {'MANIFEST.json', 'SEAL.json', 'VALIDATION.json'}
        actual_owned = {str(x) for x in P.rglob('*') if x.is_file() and x.name not in exclusions}
        actual_owned.update([str(B/'publication.json'), str(B/'promotion.json')])
        need(actual_owned == {x['path'] for x in manifest['files']}, 'complete owned editorial/config set')
        seal = load(P/'SEAL.json')
        need(sha(P/'MANIFEST.json') == seal['MANIFEST_SHA256'], 'terminal manifest seal')
        need(sha(P/'VALIDATION.json') == seal['VALIDATION_SHA256'], 'terminal validation seal')
    print(json.dumps({'status': 'PASS_PRIVATE_EDITORIAL_CONTRACT_ONLY',
                      'record_id': 23441890, 'protected_inputs_unchanged': len(load(P/'PROTECTED_INPUTS.json')['files']),
                      'original_source_files_unchanged': 32, 'whole_native_ZIP_payloads': 16,
                      'literal_native_transport_objects': 6, 'negative_controls': negatives,
                      'publication_authorized': False, 'rendered_or_browser_or_live_verified': False,
                      'source_programs_reexecuted': 0, 'network_requests': 0, 'writes_by_validator': 0},
                     indent=2))


if __name__ == '__main__':
    main()
