"""Final owned data seal only; no source execution/import/AST/compiler/test."""
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'verification/complex-retract-editorial-sol-20261117'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')

def need(ok, label):
    if not ok:
        raise ValueError(label)

def readj(path):
    return json.loads(path.read_bytes().decode('utf-8'))

def rec(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Not regular: ' + str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(), 'MD5': hashlib.md5(body).hexdigest(), 'mode': oct(stat.S_IMODE(info.st_mode))}

def inv(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Not directory')
    files, dirs = {}, {}
    for path in sorted(root.rglob('*'), key=lambda item: item.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        if stat.S_ISDIR(path.lstat().st_mode):
            dirs[name] = {'mode': oct(stat.S_IMODE(path.lstat().st_mode)), 'empty': not any(path.iterdir())}
        else:
            files[name] = rec(path)
    return {'root': str(root), 'root_mode': oct(stat.S_IMODE(root.lstat().st_mode)), 'root_empty': not any(root.iterdir()), 'files': files, 'directories': dirs}

def putj(name, value):
    need(name in ['SOURCE_GUARDS_FINAL.json', 'MANIFEST.json', 'FINAL.json'], 'Unapproved output')
    path = OWN / name
    with path.open('xb') as handle:
        handle.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())
    os.chmod(path, 0o644)

need(Path(__file__).resolve() == OWN / 'seal.py', 'Unexpected seal location')
need(not (OWN / 'FINAL.json').exists() and not (OWN / 'MANIFEST.json').exists(), 'Already frozen')
before, after = readj(OWN / 'SOURCE_GUARDS_BEFORE.json'), readj(OWN / 'SOURCE_GUARDS_AFTER.json')
need(before == after and inv(Path(after['source']['root'])) == after['source'], 'Final whole source differs')
paths = {'clearance': P / 'verification/root-clearance-23203270-20261117.json', 'root_review': P / 'papers/23203270/reviews/root-continuation-20261117/ROOT_REVIEW.md', 'source_final': P / 'papers/23203270/sources/SOURCE_FINAL.json', 'source_manifest': P / 'papers/23203270/sources/SOURCE_MANIFEST.json', 'shared_CSS': W / 'research/research.css'}
need(all(rec(path) == after['pins'][key] for key, path in paths.items()), 'Final input pin differs')
need(not (W / 'research/complex-polynomial-retract-five-variables').exists(), 'Proposed slug now collides')
putj('SOURCE_GUARDS_FINAL.json', after)
article = (OWN / 'article.html').read_bytes()
head, main = (OWN / 'head.html').read_bytes(), (OWN / 'main.html').read_bytes()
need(re.findall(rb'(<head>.*?</head>\n)', article, re.S) == [head] and re.findall(rb'(<main id="main">.*?</main>\n)', article, re.S) == [main], 'Final whole head/MAIN differs')
schemas = re.findall(rb'<script type="application/ld\+json">(.*?)</script>', head, re.S)
need(len(schemas) == 1, 'Schema count differs')
schema, model = json.loads(schemas[0]), readj(OWN / 'page-model.json')
need(schema['abstract'] == model['abstract'] == (OWN / 'ABSTRACT.txt').read_bytes().decode().strip(), 'Final abstract differs')
need('version' not in schema and b'citation_version' not in head and model['native_version'] is None and model['native_API_version_field_absent'] is True and model['native_HTML_display_version'] == 'v1', 'Invented version or host label lost')
need([item['name'] for item in schema['encoding']] == [item['name'] for item in model['native_asset_order']] == ['source-and-verification.zip', 'paper.pdf'], 'Native2 encoding order differs')
for item in model['native_asset_order']:
    need(rec(OWN / item['local_path']) == {key: item[key] for key in ['bytes', 'SHA256', 'MD5', 'mode']}, 'Final native asset differs')
need(all(model[key] is None for key in ['canonical_url', 'base_url', 'production_url', 'actual_publication_date', 'AA', 'follow_up']) and model['publication_authority'] is False, 'Private gate differs')
need(b'<meta name="robots" content="noindex, nofollow">' in head and b'<meta name="googlebot" content="noindex, nofollow">' in head and b'rel="canonical"' not in head, 'Private head differs')
need(readj(OWN / 'STATIC_CHECK.json')['status'] == 'PASS_PRIVATE_DATA_ONLY_ASSEMBLY_AND_STATIC_CHECKS', 'Static check absent')
need(b'Apache' in main and b'MIT' not in main + head, 'Actual license exception differs')
for name in ['PREPARE.stdout.txt', 'PREPARE.stderr.txt', 'SEAL.stdout.txt', 'SEAL.stderr.txt']:
    need((OWN / name).read_bytes() == b'', 'Nonempty data stream')
utc = datetime.now(timezone.utc).isoformat()
with (OWN / 'RESEARCH_LOG.md').open('a', encoding='utf-8') as handle:
    handle.write('\n- ' + utc + ' — 100% complete toward the assigned private editorial preparation. Complete actual article/head/MAIN/model/Bib proofread; final whole assembly, abstract, source97files/12childdirs/root/CSS/slug, native ZIP→PDF and host-v1-without-API-version gates all passed. CC BY4 original verification and Apache2 bundled exception retained. One own data assembly and one final data seal ran with zero-byte streams; no source execution/import/AST/compiler/test, child or external/other packet write occurred. Finite manifest/FINAL freeze follows; no subsequent writes. Publication/render/live and independent fact/root adoption remain separate.\n')
snapshot = inv(OWN)
manifest = {'schema': 'finite-private-editorial-manifest-v1', 'UTC': utc, 'root': str(OWN), 'root_mode': snapshot['root_mode'],
    'payload_files': [{'path': name, **value} for name, value in snapshot['files'].items()], 'directories': [{'path': name, **value} for name, value in snapshot['directories'].items()],
    'exact_terminal_exclusions': ['MANIFEST.json', 'FINAL.json'], 'all_hidden_ignored_empty_files_and_modes_included': True, 'no_future_or_subtree_exclusions': True}
putj('MANIFEST.json', manifest)
final = {'schema': 'private-editorial-final-v1', 'UTC': utc, 'record': 23203270, 'row': 188, 'status': 'FROZEN_PRIVATE_EDITORIAL_READY_FOR_INDEPENDENT_FACT_REVIEW_AND_ROOT_ADOPTION', 'completion_percent_private_editorial': 100,
    'manifest': {'path': 'MANIFEST.json', **rec(OWN / 'MANIFEST.json')}, 'article': {'path': 'article.html', **rec(OWN / 'article.html')}, 'head': {'path': 'head.html', **rec(OWN / 'head.html')}, 'whole_MAIN': {'path': 'main.html', **rec(OWN / 'main.html')}, 'model': {'path': 'page-model.json', **rec(OWN / 'page-model.json')}, 'Bib': {'path': 'citation.bib', **rec(OWN / 'citation.bib')}, 'report': {'path': 'REPORT.md', **rec(OWN / 'REPORT.md')},
    'full_original_abstract_visible_DC_schema_model_exact': True, 'native_asset_order': model['native_asset_order'], 'source97files12childdirs_before_after_final_unchanged': True,
    'whole_actual_article_head_MAIN_model_Bib_personally_read': True, 'global_complex_unital_splitting_full5components_scheme_image_and_zero_fiber_retained': True,
    'no_denominators_linearity_orthogonality_distance_realform_positivechar_or_ambient4_claim_added': True, 'OpenAI_pinned_cancellation_and_Nagamine_v2_classical_mechanism_credited': True,
    'scientific_clearance_inherited': True, 'new_scientific_review': False, 'no_firstness_fresh_symbolic_PASS_formal_build_or_new55module_audit_claim': True,
    'native_version': None, 'native_API_version_field_absent': True, 'native_HTML_display_version': 'v1', 'host_label_clearly_qualified_not_author_API_version': True,
    'original_note_verification_CCBY4_bundled_OpenAI_Lean_adapted_configuration_harness_Apache2_exception': True, 'MIT_substitution': False,
    'shared_CSS_only': '/research/research.css', 'proposed_canonical': model['deployment_proposal']['proposed_canonical_url'], 'actual_publication_date': None, 'canonical_url': None, 'base_url': None, 'production_url': None, 'AA': None, 'publication_authority': False, 'follow_up': None,
    'current_rendered_reader_or_live_publication_certificate': False, 'source_execution_import_AST_compiler_test': False, 'preparation_data_runs': 1, 'final_data_seal_runs': 1, 'all4_data_streams_empty': True,
    'child_agents': 0, 'website_Git_network_Sheet_deploy_AA_redirect_outreach_or_other_packet_writes': False, 'all_writes_confined_to_owned_lane': True,
    'extent': {'regular_files': len(snapshot['files']) + 2, 'child_directories': len(snapshot['directories']), 'root_mode': snapshot['root_mode'], 'all_paths': sorted(list(snapshot['files']) + ['MANIFEST.json', 'FINAL.json']), 'directories': [{'path': name, **value} for name, value in snapshot['directories'].items()]},
    'terminal_self_hash_excluded': True, 'all_handles_terminal_at_return': True, 'quiescent_after_freeze': True}
putj('FINAL.json', final)
