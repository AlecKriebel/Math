"""Owned finite data-only custody seal; no scientific programs are imported."""
import hashlib
import html
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/even-minkowski-editorial-sol-20261117'
S = P / 'papers/23203081/sources'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
TERMINALS = ['FINAL.json', 'MANIFEST.json']

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_bytes().decode('utf-8'))

def rec(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def inv(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Not directory: ' + str(root))
    files, dirs = {}, {}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            dirs[name] = {'mode': oct(stat.S_IMODE(info.st_mode)), 'empty': not any(path.iterdir())}
        else:
            files[name] = rec(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)),
            'root_empty': not any(root.iterdir()), 'files': files, 'directories': dirs}

def putj(name, value):
    need(name in ['SOURCE_GUARDS_FINAL.json'] + TERMINALS, 'Unexpected output')
    path = OWN / name
    if name in TERMINALS:
        need(rec(path)['bytes'] == 0, 'Terminal placeholder differs')
    with path.open('wb' if name in TERMINALS else 'xb') as handle:
        handle.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())
    os.chmod(path, 0o644)

def only(pattern, text):
    found = re.findall(pattern, text, re.S)
    need(len(found) == 1, 'Nonunique expression')
    return found[0]

need(not any((OWN / name).exists() for name in TERMINALS + ['SOURCE_GUARDS_FINAL.json']), 'Terminal already exists')
before = readj(OWN / 'SOURCE_GUARDS_BEFORE.json')
after = readj(OWN / 'SOURCE_GUARDS_AFTER.json')
need(before == after and (OWN / 'SOURCE_GUARDS_BEFORE.json').read_bytes() == (OWN / 'SOURCE_GUARDS_AFTER.json').read_bytes(), 'Before/after guard differs')
need(inv(S) == before['source'], 'Source changed before seal')
need((len(before['source']['files']), len(before['source']['directories'])) == (51, 12), 'Source extent differs')
paths = {'clearance': P / 'verification/root-clearance-23203081-20261117.json',
         'root_review': P / 'papers/23203081/reviews/root-continuation-20261117/ROOT_REVIEW.md',
         'source_final': S / 'SOURCE_FINAL.json', 'source_manifest': S / 'SOURCE_MANIFEST.json',
         'shared_CSS': W / 'research/research.css'}
need(set(paths) == set(before['pins']), 'Pin set differs')
for key, path in paths.items():
    need(rec(path) == before['pins'][key], 'Pin changed: ' + key)
need(not (W / 'research/even-minkowski-uniqueness').exists() and before['proposed_slug_absent'] is True, 'Slug collision')
clearance = readj(paths['clearance'])
need(clearance['verdict'] == 'PASS' and clearance['follow_up'] is None and clearance['publication_authority'] is False, 'Inherited clearance differs')
putj('SOURCE_GUARDS_FINAL.json', before)

article = (OWN / 'article.html').read_text()
head = (OWN / 'head.html').read_text()
main = (OWN / 'main.html').read_text()
need(all(text.encode() == (OWN / name).read_bytes() for name, text in [('article.html', article), ('head.html', head), ('main.html', main)]), 'Byte/newline representation differs')
model = readj(OWN / 'page-model.json')
bib = (OWN / 'citation.bib').read_text()
abstract = (OWN / 'ABSTRACT.txt').read_text().removesuffix('\n')
schema = json.loads(only(r'<script type="application/ld\+json">(.*?)</script>', head))
need(only(r'(<head>.*?</head>\n)', article) == head and only(r'(<main id="main">.*?</main>\n)', article) == main, 'Whole HEAD/MAIN differ')
need(html.unescape(only(r'<p id="abstract-text">(.*?)</p>', main)) == abstract == schema['abstract'] == model['abstract'], 'Abstract differs')
need(html.unescape(only(r'<meta name="DC.description" content="(.*?)">', head)) == abstract, 'DC abstract differs')
need(model['native_version'] is None and model['native_API_version_field_absent'] is True and model['native_HTML_display_version'] == 'v1', 'Version differs')
need('display edition only' in model['host_edition_qualification'] and 'version' not in schema and 'citation_version' not in head and re.search(r'^\s*version\s*=', bib, re.M) is None, 'Author version invented')
need('version' not in readj(S / 'native-metadata/record-api.json')['metadata'], 'Native API version changed')
need('Version v1</span>' in (S / 'native-metadata/record-page.html').read_text(), 'Native host label changed')
need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']) and model['publication_authority'] is False, 'Private field differs')
need('noindex, nofollow' == model['robots'] and '<meta name="robots" content="noindex, nofollow">' in head and '<meta name="googlebot" content="noindex, nofollow">' in head, 'Private robots differs')
need(re.search(r'<link[^>]+rel="canonical"', head) is None and 'url' not in schema and 'mainEntityOfPage' not in schema, 'Actual canonical present')
need(model['deployment_proposal']['proposed_canonical_url'] == 'https://aleckriebel.com/research/even-minkowski-uniqueness/', 'Proposal differs')
need(re.findall(r'<link rel="stylesheet" href="([^"]+)">', head) == ['/research/research.css'] and '<style' not in article and ' style=' not in article, 'Shared CSS only differs')
names = ['paper.pdf', 'source-and-verification.zip', 'README.md']
need([item['name'] for item in model['native_asset_order']] == names and [item['name'] for item in schema['encoding']] == names, 'Native order differs')
need([item['contentUrl'] for item in schema['encoding']] == ['assets/' + name for name in names], 'Encoding path differs')
need(re.findall(r'<a href="(assets/[^"]+)" download>', only(r'<ol id="native-assets">(.*?)</ol>', main)) == ['assets/' + name for name in names], 'Visible native order differs')
for item in model['native_asset_order']:
    expected = {key: item[key] for key in ['bytes', 'SHA256', 'MD5', 'mode']}
    need(rec(OWN / item['local_path']) == expected == rec(S / 'zenodo-files' / item['name']), 'Original asset differs')
need('MIT' not in main + head and 'Apache' not in main + head and 'CC BY 4.0' in main and model['rights']['owned_contribution'] == 'CC BY 4.0', 'Rights differs')
need(readj(OWN / 'STATIC_CHECK.json')['status'] == 'PASS_PRIVATE_DATA_ONLY_ASSEMBLY_AND_STATIC_CHECKS', 'Static check failed')
for name in ['PREPARE.stdout.txt', 'PREPARE.stderr.txt', 'SEAL.stdout.txt', 'SEAL.stderr.txt']:
    need(rec(OWN / name)['bytes'] == 0, 'Nonempty operation stream: ' + name)
utc = datetime.now(timezone.utc).isoformat()
with (OWN / 'RESEARCH_LOG.md').open('a') as handle:
    handle.write('\n- ' + utc + ' — 100% complete toward the private editorial handoff. Final data-only seal reauthenticated the unchanged51sourcefiles/12childdirs, all root/source/CSS pins, exact article/wholeHEAD/wholeMAIN/abstract/model/Bib and3originalassets in native PDF→ZIP→README order. One saved/read own preparer and one saved/read own seal ran; all four streams are empty. Complete personal copy review and static checks passed. No fresh science, native program/import/AST/compiler/test, new literature/formal/human/priority certificate, rendering/live certificate, other packet/stage/production/Git/network/Sheet/AA/deploy/redirect/outreach or child work occurred. Finite manifest covers hidden/empty/modes/topology, excluding only exactly created FINAL.json and MANIFEST.json controls. Frozen for independent fact review/root adoption; no further writes.\n')
for name in TERMINALS:
    with (OWN / name).open('xb'):
        pass
    os.chmod(OWN / name, 0o644)
snapshot = inv(OWN)
need(all(snapshot['files'][name]['bytes'] == 0 and snapshot['files'][name]['mode'] == '0o644' for name in TERMINALS), 'Created terminal placeholders differ')
snapshot['files'] = {key: value for key, value in snapshot['files'].items() if key not in TERMINALS}
expected_names = ['ABSTRACT.txt', 'PREPARE.stderr.txt', 'PREPARE.stdout.txt', 'RESEARCH_LOG.md', 'REPORT.md', 'SEAL.stderr.txt', 'SEAL.stdout.txt', 'SOURCE_GUARDS_AFTER.json', 'SOURCE_GUARDS_BEFORE.json', 'SOURCE_GUARDS_FINAL.json', 'STATIC_CHECK.json', 'article.html', 'assets/README.md', 'assets/paper.pdf', 'assets/source-and-verification.zip', 'citation.bib', 'head.html', 'main.html', 'page-model.json', 'prepare.py', 'seal.py']
need(sorted(snapshot['files']) == sorted(expected_names) and set(snapshot['directories']) == {'assets'}, 'Unexpected owned extent')
need(snapshot['root_mode'] == '0o755' and all(item['mode'] == '0o644' for item in snapshot['files'].values()) and snapshot['directories'] == {'assets': {'mode': '0o755', 'empty': False}}, 'Owned modes/topology differs')
manifest = {'schema': 'private-editorial-finite-manifest-v1', 'UTC': utc, 'root': str(OWN), 'root_mode': snapshot['root_mode'], 'root_empty': snapshot['root_empty'],
            'payload_file_count': len(snapshot['files']), 'final_regular_file_count': len(snapshot['files']) + 2, 'child_directory_count': len(snapshot['directories']),
            'exact_created_terminal_exclusions': TERMINALS, 'no_prefix_or_future_exclusions': True,
            'files': [{'path': key, **value, 'hidden': any(part.startswith('.') for part in Path(key).parts), 'empty': value['bytes'] == 0} for key, value in snapshot['files'].items()],
            'directories': [{'path': key, **value, 'hidden': any(part.startswith('.') for part in Path(key).parts)} for key, value in snapshot['directories'].items()]}
putj('MANIFEST.json', manifest)
final = {'schema': 'private-editorial-final-v1', 'UTC': utc, 'status': 'PASS_PRIVATE_EDITORIAL_FROZEN', 'completion_percent': 100,
         'record_id': '23203081', 'sheet_row': 189, 'root': str(OWN), 'scientific_clearance_inherited': True,
         'new_scientific_verdict': False, 'new_literature_or_formal_or_human_or_priority_certificate': False,
         'whole_article_head_MAIN_full_abstract_model_Bib_personally_read': True, 'static_checks': 'PASS',
         'smooth_positive_even_scope_n_ge2_p_in_0_1_with_zero_retained': True, 'arbitrary_full_dimensional_symmetric_equal_unnormalized_measure_scope_only_0_lt_p_lt_1': True,
         'no_volume_one_normalization_scale_c_power_n_minus_p_even_center_retained': True, 'local_endpoint_open_positivity_and_n_plus_1_coefficient_retained': True,
         'singular_equal_volume_boxes_distinguished_from_smooth_positive_data': True, 'native_asset_order': names,
         'native_version': None, 'host_display_edition': 'v1, explicitly qualified; not an author API version', 'owned_rights': 'CC BY 4.0; third-party rights retained',
         'actual_canonical': None, 'base_url': None, 'production_url': None, 'actual_publication_date': None, 'AA': None, 'follow_up': None,
         'proposed_canonical_url': model['deployment_proposal']['proposed_canonical_url'], 'publication_authority': False, 'robots': 'noindex, nofollow',
         'rendered_or_live_certificate': False, 'native_scientific_execution_import_AST_compiler_or_test': False,
         'external_communication_child_stage_website_Git_network_Sheet_AA_deploy_redirect_or_other_packet_writes': False,
         'source_extent': {'files': 51, 'child_directories': 12, 'all_bytes_modes_topology_unchanged': True},
         'manifest': {'path': 'MANIFEST.json', **rec(OWN / 'MANIFEST.json')},
         'artifacts': {name: rec(OWN / name) for name in ['article.html', 'head.html', 'main.html', 'ABSTRACT.txt', 'page-model.json', 'citation.bib', 'REPORT.md', 'SOURCE_GUARDS_BEFORE.json', 'SOURCE_GUARDS_AFTER.json', 'SOURCE_GUARDS_FINAL.json', 'STATIC_CHECK.json']},
         'assets': [{key: value for key, value in item.items() if key in ['name', 'local_path', 'bytes', 'SHA256', 'MD5', 'mode']} for item in model['native_asset_order']],
         'finite_extent': {'regular_files': len(snapshot['files']) + 2, 'child_directories': len(snapshot['directories']), 'root_mode': snapshot['root_mode'], 'all_paths': sorted(list(snapshot['files']) + list(snapshot['directories']) + TERMINALS), 'exact_created_terminal_exclusions': TERMINALS, 'terminal_modes': {'FINAL.json': '0o644', 'MANIFEST.json': '0o644'}, 'FINAL_self_hash_excluded': True},
         'frozen_after_final_write': True, 'next_step': 'Independent fact review and root adoption; no publication authority'}
putj('FINAL.json', final)
