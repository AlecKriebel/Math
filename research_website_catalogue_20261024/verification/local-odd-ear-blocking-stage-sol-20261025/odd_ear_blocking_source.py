"""Exact read-only consumer for two separately approved original editions.

Native objects remain literal. Only the returned resolver view is temporary.
"""
from pathlib import Path, PurePosixPath
from io import BytesIO
import gzip, hashlib, json, re, stat, tarfile, zipfile
from bosonic_source import contained_file, digest
from published_assets import safe_relative

OEB_IDS = {'23576280','23331258'}
STATUSES = {'23576280':'PASS','23331258':'PASS'}
PINS = {'23576280': {'publication': 'aee88f21d1609b9c0c38454281e1a862d381c3a491462cc4a26b827348bdac5b', 'promotion': '9e6e4de0a4733572cd9743deb5b1338ee64b426259e010c696f3f629d419fd6f', 'science': '1135fe54724927c75d2e03e4fa15b61fc294bd90611c3a92f273c4e18a1a6e7e', 'editorial': '457ad0f27dfca04b13e6eb57e9fa45031d4cde26ce5290e222299ff4022a91f7', 'editorial_manifest': '4dd9e8617a31c57a53610c587e01fa5097bba20b3d873981a09196d1e388da80', 'editorial_seal': '4b4507f80ac47bcf721309e0c3917ed2dc48b489ab8d4e06f71c9e31fd971aa5', 'public_copy': '085f17250b882ebaf7065d3ef8fa62936fc6031647c4353e7873a5bd4c3316b1', 'source_pins': {'SOURCE_READY_MANIFEST.json': 'ba0443c2a5f8001b9916a217c113bd38247695093c12b8cead3aef421c9ae388', 'SOURCE_READY_SEAL.json': '78a83dd556f77e4b6c003fa16465b64d3a7d8079f1d4d85f450683930b86e56b', 'SOURCE_MANIFEST.json': '5087982cf536dc9065569fe3faabfa7c3a4a245ff979fb2e3c9031b0d3652a92', 'SOURCE_SEAL.json': 'df61e1d94ae9994619a6afba0166c83cabc175d63513bca8cda03bbcfcfd57c0', 'archive-members.json': 'e3fc450856544f0b9383089185b7c88f712be93c015da0b3898dfee16e628ed0'}}, '23331258': {'publication': '526de0fb685c39bf2f327892635c44938e84b4e9dd462edb9d0aabb7c6650be6', 'promotion': 'bbf4754395e0987511983f3368b44950386d9bc54d9c6749a596dea19d958976', 'science': '5ddd08a3c3eda941ece10ccf650a0ad0fe5ef4615d1832f6bda442b14242abb6', 'editorial': 'c4732399b108494c5146b0486c00c8651e769071a9a8bad71edfa2c47105b747', 'editorial_manifest': '8f37f19a3ad6a8d9992a931cfb2546103f238a68b54cbd3c7a00d9238dcdcf4d', 'editorial_seal': 'e9ab83b4d4350ee31dea09278f96f663cc68b6ae21d555978de83d1bdfdd3103', 'public_copy': '5c44c22d0843e5313e8b677a1136eaef3022009b0380b28a9043d7cd2132660b', 'source_pins': {'SOURCE_READY_MANIFEST.json': '04d695c6b28667593e38b353c9c828bf1fa368e61a038a2ecd624ccbaaeab277', 'SOURCE_READY_SEAL.json': 'c0f6319840cecc469656cd76b93e1c4ddcf881629a07e27232334c00976495bc', 'SOURCE_MANIFEST.json': '30554d3d03bada5c1a095dfa841406d2c16f65cf2c0ed464f455ce1f6a4740ea', 'SOURCE_SEAL.json': '73263edb102271553c240908868d0153db79775cbcf1a94c476cf2c259702e08', 'archive-members.json': '36579a24878fa328493efdd8e4f510e60e378b5fbcb47b208a6dbdc4f7a206cd'}, 'tar_addendum': '34e560a6b37c74a03776dbbe8dadd43dc75746ff1de14e3a1f4249596abf3cd6'}}
VERSIONS = {'23576280':'1.0.0','23331258':'1.0'}
DATES = {'23576280':'2026-10-22','23331258':'2026-10-12'}
ASSET_ORDER = {'23576280':['initial-odd-ear-prefix-source-and-verification.zip','initial-odd-ear-prefix.pdf'],
               '23331258':['three-terminal-shortest-path-blocking-v1.0.pdf','three-terminal-bsp-source-verification-v1.0.zip']}
LICENSES = {'23576280':'CC BY 4.0 for manuscript/prose; MIT for authored code',
            '23331258':'CC BY 4.0 for authored manuscript, proofs, code and audits in the deposit'}

def require(ok, tag):
    if not ok:
        raise ValueError('odd_ear_blocking:'+tag)

def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x,y) for x,y in zip(a,b))
    return a == b

def normalize_oeb_abstract(rid, text):
    require(rid in OEB_IDS, 'unsupported_ID')
    if rid == '23576280':
        for old,new in [(r'Seb\H{o}','Sebő'),('Benchetrit--','Benchetrit–'),(r'\(',''),(r'\)',''),(r'\beta','β'),(r'\ge','≥')]:
            text = text.replace(old,new)
    return ' '.join(text.split())

def approved_material_note(paper):
    paper = Path(paper)
    require(paper.name in OEB_IDS, 'unsupported_ID')
    path = contained_file(paper,'reviews/editorial/PUBLIC_COPY.md')
    require(digest(path) == PINS[paper.name]['public_copy'], 'approved_complete_public_copy')
    text = path.read_text()
    require(text.count('## Supporting materials\n\n') == 1, 'one_approved_material_section')
    section = text.split('## Supporting materials\n\n',1)[1].split('\n\n## Background and prior work',1)[0]
    paragraphs = section.split('\n\n')
    require(len(paragraphs) == 2 and paragraphs[0].startswith('[Complete unchanged source and verification ZIP]('), 'approved_material_note_shape')
    return paragraphs[1]

def validate_oeb_assets(paper, rid, raw, api):
    require(rid in OEB_IDS, 'unsupported_ID')
    require(type(raw.get('all_assets')) is list and len(raw['all_assets']) == 2, 'native_all_assets_list')
    require(not {'files','assets','actual_assets','all_actual_assets'} & raw.keys(), 'no_source_aliases')
    require(all(type(x) is dict and set(x) == {'original_api_file_object','path','bytes','md5','sha256'} for x in raw['all_assets']), 'exact_native_asset_fields')
    require(type(api['files']) is list and same([x['original_api_file_object'] for x in raw['all_assets']],api['files']), 'whole_API_file_objects_and_order')
    names = []
    for item in raw['all_assets']:
        require(set(item) == {'original_api_file_object','path','bytes','md5','sha256'}, 'exact_native_asset_fields')
        obj = item['original_api_file_object']
        name = safe_relative(obj['key'],basename=True)
        names.append(name)
        require(item['path'] == str(Path(paper)/'sources'/name), 'actual_asset_path')
        require(type(item['bytes']) is int and type(obj['size']) is int and item['bytes'] == obj['size'] > 0, 'integer_asset_sizes')
        require(re.fullmatch('[0-9a-f]{64}',item['sha256']) and re.fullmatch('[0-9a-f]{32}',item['md5']), 'native_lowercase_hashes')
        require(obj['checksum'] == 'md5:'+item['md5'], 'actual_API_MD5')
    require(names == ASSET_ORDER[rid], 'exact_record_specific_asset_order')
    return raw['all_assets']

def verify_oeb_archive(paper, rid, archive, inventory, selected_pdf, tar_addendum=None):
    paper = Path(paper)
    require(rid in OEB_IDS and type(inventory['files']) is list, 'native_archive_files_schema')
    expected = 12 if rid == '23576280' else 50
    require(len(inventory['files']) == inventory['safe_all_depth_members'] == expected and inventory['nested_archives'] == [], 'original_ZIP_only_inventory_preserved')
    table = {x['member']:x for x in inventory['files']}
    require(len(table) == expected, 'unique_outer_inventory')
    payloads = {}
    with zipfile.ZipFile(BytesIO(archive.read_bytes())) as z:
        require(len(z.infolist()) == expected, 'complete_outer_ZIP')
        for entry in z.infolist():
            name = safe_relative(entry.filename)
            mode = entry.external_attr >> 16
            require(name == entry.filename and name not in payloads and not entry.is_dir() and not(entry.flag_bits & 1) and stat.S_IFMT(mode) in (0,stat.S_IFREG), 'safe_unique_regular_outer_member')
            data = z.read(entry)
            row = table[name]
            require(row['archive_chain'] == [] and row['path'] == 'published-source/'+name and type(row['bytes']) is int and row['bytes'] == len(data) == entry.file_size, 'native_outer_member_mapping_size')
            require(row['sha256'] == hashlib.sha256(data).hexdigest() and row['CRC32'] == f'{entry.CRC:08x}' and row['mode'] == mode, 'actual_outer_CRC_hash_mode')
            require(contained_file(paper,'sources/'+row['path']).read_bytes() == data, 'unchanged_existing_outer_body')
            require(len(data) <= 10000000, 'bounded_member')
            payloads[name] = data
    pdfs = [name for name in payloads if name.lower().endswith('.pdf')]
    if rid == '23576280':
        require(pdfs == ['paper.pdf'] and payloads['paper.pdf'] == selected_pdf.read_bytes(), 'one_embedded_identical_reader')
        require(not any(name.lower().endswith(('.zip','.tar','.gz')) for name in payloads), 'no_nested_archive_odd_ear')
        return {'occurrences':12,'containers':1,'embedded_PDFs':1}
    require(not pdfs and tar_addendum is not None, 'blocking_no_embedded_reader_and_additive_tar')
    require([n for n in payloads if n.lower().endswith(('.zip','.tar','.gz'))] == ['original_packet/AUTHOR_FREEZE.tar.gz'], 'one_exact_nested_tar')
    add = tar_addendum
    compressed = payloads['original_packet/AUTHOR_FREEZE.tar.gz']
    tar_path = contained_file(paper,'sources/published-source/original_packet/AUTHOR_FREEZE.tar.gz')
    require(add['archive'] == str(tar_path) and add['archive_bytes'] == len(compressed) == 12052 and add['archive_sha256'] == hashlib.sha256(compressed).hexdigest(), 'original_additive_tar_container')
    expanded = gzip.decompress(compressed)
    require(len(expanded) == add['uncompressed_tar_bytes'] == 51200 and hashlib.sha256(expanded).hexdigest() == add['uncompressed_tar_sha256'], 'full_gzip_CRC_decompression')
    records = {x['original_tar_member']:x for x in add['regular_members']}
    require(type(add['regular_members']) is list and len(records) == len(add['regular_members']) == 7, 'seven_distinct_tar_occurrences')
    seen, bodies, directories = set(), 0, 0
    with tarfile.open(fileobj=BytesIO(expanded),mode='r:') as t:
        for member in t.getmembers():
            path = PurePosixPath(member.name)
            require(not path.is_absolute() and '..' not in path.parts and '\\' not in member.name and member.name not in seen and (member.isdir() or member.isfile()), 'safe_unique_tar_member')
            seen.add(member.name)
            if member.isdir():
                directories += 1
                continue
            data = t.extractfile(member).read()
            row = records[member.name]
            relative = str(path.relative_to('three_terminal_30000347'))
            outer = 'original_packet/frozen_packet/'+relative
            existing = contained_file(paper,'sources/published-source/'+outer)
            require(type(row['bytes']) is int and row['bytes'] == len(data) and row['sha256'] == hashlib.sha256(data).hexdigest(), 'tar_body_integer_size_and_hash')
            require(row['existing_exact_original_member'] == str(existing) and row['byteidentical_to_existing_outer_member'] is True and payloads[outer] == existing.read_bytes() == data, 'qualified_tar_to_existing_outer_identity')
            require(not member.name.lower().endswith('.pdf'), 'no_nested_reader')
            bodies += 1
    require(bodies == add['tar_regular_member_count'] == 7 and directories == 2 and add['total_recursive_regular_member_occurrences'] == 57 and add['nested_archives_all_formats'] == 1, 'complete_50_plus_7_without_deduplication')
    return {'occurrences':57,'containers':2,'embedded_PDFs':0}

def odd_ear_blocking_source_view(paper, config, gate):
    paper = Path(paper)
    rid = paper.name
    require(rid in OEB_IDS, 'unsupported_ID')
    pin = PINS[rid]
    programme = paper.parents[1]
    cp, gp = contained_file(paper,'publication.json'), contained_file(paper,'promotion.json')
    require(digest(cp) == pin['publication'] and digest(gp) == pin['promotion'], 'exact_config_bytes')
    require(same(json.loads(cp.read_bytes()),config) and same(json.loads(gp.read_bytes()),gate), 'whole_passed_objects_equal_actual_types')
    b = config['source_binding']
    science_path = contained_file(programme,'verification/root-clearance-'+rid+'-20261025.json')
    editorial_path = contained_file(programme,'verification/root-editorial-'+rid+'-20261025.json')
    require(digest(science_path) == pin['science'] and digest(editorial_path) == pin['editorial'], 'separate_pinned_current_authorities')
    science, editorial = json.loads(science_path.read_bytes()), json.loads(editorial_path.read_bytes())
    require(same(science,gate['root_clearance_record']) and gate['approved_scope'] == science['approved_scope'] and gate['disposition_by'] == 'root' and gate['status'] == science['status'] == STATUSES[rid], 'whole_original_root_exact_literal_status')
    require(gate['root_clearance_file'] == config['review_metadata']['root_clearance_file'] == str(science_path.relative_to(programme)) and gate['root_clearance_sha256'] == config['review_metadata']['root_clearance_sha256'] == pin['science'], 'exact_scientific_path_hash')
    require(editorial['status'] == 'ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE' and editorial['private_staging_authorized'] is True and editorial['production_integration_authorized'] is False, 'private_editorial_stage_authority_only')
    require(gate['publication_sha256'] == pin['publication'], 'publication_gate_hash')
    ed = paper/'reviews/editorial'
    mf, sf = contained_file(ed,'MANIFEST.json'), contained_file(ed,'SEAL.json')
    require(digest(mf) == pin['editorial_manifest'] and digest(sf) == pin['editorial_seal'], 'exact_original_editorial_seal_manifest')
    sealed, manifest = json.loads(sf.read_bytes()), json.loads(mf.read_bytes())
    require(sealed['manifest']['sha256'] == pin['editorial_manifest'] and sealed['publication']['sha256'] == pin['publication'] and sealed['promotion']['sha256'] == pin['promotion'], 'native_editorial_seal_bindings')
    owned = 0
    for row in manifest['files']:
        path = Path(row['path'])
        if path.is_relative_to(ed) or path in (cp,gp):
            actual = contained_file(paper,str(path.relative_to(paper)))
            require(type(row['bytes']) is int and actual.stat().st_size == row['bytes'] and digest(actual) == row['sha256'], 'original_editorial_owned_file')
            owned += 1
    require(owned == (32 if rid == '23576280' else 36), 'owned_only_no_old_mutable_baseline_following')
    originals = {}
    for key in ('source_receipt','metadata','raw_record','transport_receipt','initial_intake_receipt'):
        path = contained_file(paper,b[key+'_path'])
        require(b[key+'_path'] == gate[key+'_path'] and digest(path) == b[key+'_sha256'] == gate[key+'_sha256'], 'actual_'+key+'_binding')
        originals[key] = json.loads(path.read_bytes())
        if key in ('source_receipt','metadata','raw_record'):
            require(science[key+'_path'] == 'papers/'+rid+'/'+b[key+'_path'] and science[key+'_sha256'] == b[key+'_sha256'], 'exact_scientific_source_interface')
    raw, meta, api = originals['source_receipt'], originals['metadata'], originals['raw_record']
    require(same(raw,b['source_receipt_original']) and same(raw,gate['source_receipt_original']) and same(meta,b['metadata_original']), 'whole_original_native_receipt_metadata')
    require(same(raw['all_assets'],b['all_assets']) and same(raw['all_assets'],gate['all_assets']) and same(api['files'],b['published_file_objects']) and same(api['files'],gate['published_file_objects']), 'complete_actual_file_objects')
    expected_gate_ID = rid if rid == '23576280' else int(rid)
    require(raw['record_id'] == meta['record_id'] == b['record_id'] == int(rid) and same(gate['record_id'],expected_gate_ID) and str(api['id']) == rid and api['status'] == 'published', 'actual_record_identity_and_native_promotion_ID_type')
    require(all(config[k] == meta[k] == api['metadata'][k] for k in ('title','doi','publication_date','version')) and config['version'] == b['version'] == b['zenodo_version'] == b['manuscript_version'] == gate['version'] == VERSIONS[rid] and config['publication_date'] == b['manuscript_date'] == b['zenodo_publication_date'] == DATES[rid], 'exact_record_specific_version_declaration')
    require(api['created'] == raw['created'] == meta['created'] == b['record_created_utc'] and api['updated'] == meta['updated'] == b['record_updated_utc'] and str(api['conceptrecid']) == b['concept_record_id'] == meta['conceptrecid'], 'separate_actual_creation_update_concept')
    require(config['author'] == 'Alec Kriebel' and api['metadata']['creators'][0]['name'] == 'Kriebel, Alec' and api['metadata']['creators'][0]['orcid'] == '0009-0001-9320-500X' and api['metadata']['license']['id'] == 'cc-by-4.0' and config['license_url'] == 'https://creativecommons.org/licenses/by/4.0/' and config['license'] == LICENSES[rid], 'actual_author_and_distinct_code_licenses')
    require(set(gate['reviews']) == set(science['reviews']) == {'scope','analytic','adversarial'}, 'three_whole_native_family_roles')
    for role, item in gate['reviews'].items():
        original = science['reviews'][role]
        require(same(item['root_authority_entry'],original) and original['report'] == 'papers/'+rid+'/'+item['report'] and original['verdict'] == 'papers/'+rid+'/'+item['verdict_file'], 'whole_root_review_entry')
        require(digest(contained_file(paper,item['report'])) == item['report_sha256'] == original['report_sha256'], 'complete_original_scientific_report')
        path = contained_file(paper,item['verdict_file'])
        require(digest(path) == item['verdict_sha256'] == original['verdict_sha256'] and same(json.loads(path.read_bytes()),item['verdict']), 'whole_custom_verdict_no_status_coercion')
    for key in ('root_review','root_custody_receipt'):
        require(digest(contained_file(programme,science[key])) == science[key+'_sha256'], 'actual_root_final_evidence')
    flags = ('rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received')
    require(all(gate[k] is False and config['review_metadata'][k] is False for k in flags) and config['review_metadata']['rendered'] is False and config['review_metadata']['deployed'] is False, 'original_false_gates_unchanged')
    require(all(config[k] is None and gate[k] is None for k in ('canonical_url','AA','follow_up')) and science['follow_up'] is None and editorial['follow_up'] is None, 'original_null_gates_unchanged')
    for key in ('transport_receipt','initial_intake_receipt'):
        events = originals[key]
        require(type(events) is list and len(events) == (4 if key == 'transport_receipt' else 1) and same(events,b[key+'_original']) and same(events,gate[key+'_original']), 'whole_separate_actual_4_plus_1_transports')
        for event in events:
            require(set(event) == {'requested_url','started_utc','completed_utc','status','final_url','headers','path','bytes','sha256'} and event['status'] == 200 and type(event['headers']) is dict and event['headers'] and type(event['bytes']) is int, 'native_transport_objects_no_invented_fields')
            path = contained_file(paper,str(Path(event['path']).relative_to(paper)))
            require(path.stat().st_size == event['bytes'] and digest(path) == event['sha256'], 'actual_transport_payload')
    require([Path(x['path']).name for x in originals['transport_receipt'][-2:]] == ASSET_ORDER[rid], 'actual_transport_asset_order')
    for name, expected in pin['source_pins'].items():
        require(digest(contained_file(paper,'sources/'+name)) == expected, 'pinned_native_source_custody')
    for name in ('SOURCE_READY_MANIFEST.json','SOURCE_MANIFEST.json'):
        for row in json.loads((paper/'sources'/name).read_bytes())['files']:
            path = Path(row['path'])
            relative = str(path.relative_to(paper)) if path.is_absolute() else 'sources/'+str(path)
            path = contained_file(paper,relative)
            require(type(row['bytes']) is int and path.stat().st_size == row['bytes'] and digest(path) == row['sha256'], 'all_original_source_manifest_bindings')
    tex = contained_file(paper,b['source_tex_path'])
    require(digest(tex) == b['source_tex_sha256'] == science['source_tex_sha256'] and 'papers/'+rid+'/'+b['source_tex_path'] == science['source_tex_path'], 'sole_current_controlling_TeX')
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex.read_text(),re.S).group(1)
    require(abstract == b['abstract_tex'] == contained_file(paper,'reviews/editorial/ORIGINAL_ABSTRACT.tex').read_text() and normalize_oeb_abstract(rid,abstract) == config['abstract'], 'whole_original_abstract_only_declared_normalization')
    bib = contained_file(paper,b['prepared_bibtex_path'])
    require(bib.read_text() == config['prepared_bibtex'] and digest(bib) == b['prepared_bibtex_sha256'] and config['additional_assets'] == [], 'exact_prepared_BibTeX_one_reader')
    selected = []
    for item in validate_oeb_assets(paper,rid,raw,api):
        obj = item['original_api_file_object'];name = obj['key'];path = contained_file(paper,'sources/'+name);data = path.read_bytes()
        label = 'pdf' if name == config['pdf_filename'] else 'supplement'
        require(len(data) == item['bytes'] and hashlib.md5(data).hexdigest() == item['md5'] and digest(path) == item['sha256'] == b[label+'_sha256'] == gate[label+'_sha256'] == science[label+'_sha256'], 'actual_complete_asset_hash_size_API_binding')
        selected.append({'name':name,'url':obj['links']['self'],'bytes':item['bytes'],'sha256':item['sha256'],'zenodo_checksum':obj['checksum']})
    inventory = json.loads((paper/'sources/archive-members.json').read_bytes())
    add = None
    if rid == '23331258':
        path = contained_file(paper,b['tar_custody_addendum_path'])
        require(digest(path) == b['tar_custody_addendum_sha256'] == gate['tar_custody_addendum_sha256'] == pin['tar_addendum'], 'separate_pinned_tar_custody_addendum')
        add = json.loads(path.read_bytes())
        require(same(add,b['tar_custody_addendum_original']) and same(add,gate['tar_custody_addendum_original']) and same(inventory,b['recursive_archive_inventory_original']) and same(inventory,gate['recursive_archive_inventory_original']), 'whole_native_inventory_and_additive_tar')
    stats = verify_oeb_archive(paper,rid,paper/'sources'/config['supplement_filename'],inventory,paper/'sources'/config['pdf_filename'],add)
    require(stats == {'occurrences':b['archive_regular_member_occurrences'],'containers':b['archive_container_count'],'embedded_PDFs':b['archive_embedded_pdf_count']}, 'exact_final_archive_occurrences_containers_reader')
    if rid == '23576280':
        require((paper/'sources/published-source/LICENSE-CODE.txt').read_text().startswith('MIT License') and 'CC BY 4.0' in (paper/'sources/published-source/LICENSE-PROSE.txt').read_text(), 'actual_separate_MIT_code_CC_BY_prose_notices')
    else:
        require('Authored manuscript, proofs, code and audits in this deposit are licensed under\nCreative Commons Attribution 4.0 International' in (paper/'sources/published-source/README.md').read_text(), 'actual_CC_BY_code_audit_notice')
    require(approved_material_note(paper) in (paper/'reviews/editorial/PUBLIC_COPY.md').read_text(), 'complete_approved_material_license_note')
    return raw, {'record_id':rid,'files':selected}, paper/'sources'
