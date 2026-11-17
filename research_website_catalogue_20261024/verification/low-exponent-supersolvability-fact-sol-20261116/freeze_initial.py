"""Data-only private copy-contract custody seal; no writer or scientific execution."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'verification/low-exponent-supersolvability-fact-sol-20261116'
S = P / 'papers/23331709/sources'
R = P / 'papers/23331709/reviews/root'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    mode = path.lstat().st_mode
    need(stat.S_ISREG(mode), 'Nonordinary file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': oct(stat.S_IMODE(mode))}

def save(name, obj):
    target = O / name
    need(not target.exists(), 'Refusing repeat seal/output: ' + name)
    target.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

authority = P / 'verification/root-clearance-23331709-20261116.json'
ap, rp = pin(authority), pin(R / 'ROOT_REVIEW.md')
need(ap['bytes'] == 2388 and ap['SHA256'] == '94df1cd5e29413a1db22e5e25ccc290e5a649c22b1d3aa21b2be0ef88b887144', 'Authority differs')
need(rp['bytes'] == 13216 and rp['SHA256'] == 'd51e3987044d14fec0f83cb984b3961abfe975bc939f9396e82f1951c6dc5dac', 'Root report differs')
mp, fp = pin(S / 'SOURCE_MANIFEST.json'), pin(S / 'SOURCE_FINAL.json')
need(mp['bytes'] == 27746 and mp['SHA256'] == 'bb80fc71825c75c727cd9f842d6fe38759cdfd6c1cd2d02c5f6ac9b4aa0444c6', 'Source manifest differs')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_bytes())
expected = {x['path']: {k: x[k] for k in ('bytes', 'SHA256', 'mode')} for x in sm['files']}
need(len(expected) == len(sm['files']), 'Duplicate source name')
expected.update({'SOURCE_MANIFEST.json': mp, 'SOURCE_FINAL.json': fp})
files, dirs = {}, {}
for path in S.rglob('*'):
    info = path.lstat()
    rel = path.relative_to(S).as_posix()
    if stat.S_ISREG(info.st_mode):
        files[rel] = pin(path)
    else:
        need(stat.S_ISDIR(info.st_mode), 'Source symlink/special node')
        dirs[rel] = oct(stat.S_IMODE(info.st_mode))
need(files == expected and len(files) == 120, 'Source byte/mode/extent differs')
need(dirs == {x['path']: x['mode'] for x in sm['directories']} and len(dirs) == 17, 'Source directory topology differs')
tex_path = S / 'published-source/container-001/tree/low_exponent_supersolvability.tex'
tex = tex_path.read_text()
need(tex.count('\n') == 132, 'Controlling TeX line count differs')
record = json.loads((S / 'record.response.body').read_bytes())
wrapper = json.loads((S / 'files-23331709.response.body').read_bytes())
ready = json.loads((S / 'SOURCE_READY.json').read_bytes())
need(record['id'] == 23331709, 'Record differs')
asset_pins = []
for asset in ready['native_assets']:
    path = S / asset['asset']['path']
    actual = pin(path)
    need(all(actual[k] == asset['asset'][k] for k in ('bytes', 'SHA256', 'mode')), 'Asset differs')
    md5 = hashlib.md5(path.read_bytes()).hexdigest()
    need('md5:' + md5 == asset['native_MD5'], 'Native MD5 differs')
    asset_pins.append({'name': asset['name'], 'path': str(path), **actual, 'MD5': md5})
need([x['name'] for x in asset_pins] == ['low_exponent_supersolvability.pdf', 'low_exponent_verification.zip'], 'Asset order differs')
pages = [{'path': str(R / 'page-images' / ('page-' + str(n) + '.png')),
          **pin(R / 'page-images' / ('page-' + str(n) + '.png'))} for n in range(1, 6)]
now = datetime.now(timezone.utc).isoformat()
save('SOURCE_EXPECTATIONS.json', {'schema': 'independent-source-first-private-copy-contract-v1', 'UTC': now,
    'record': 23331709, 'row': 167, 'source_manifest': mp, 'source_FINAL': fp,
    'all120_source_files_17_child_directories_match': True,
    'root_clearance': {'path': str(authority), **ap}, 'root_report': {'path': str(R / 'ROOT_REVIEW.md'), **rp},
    'controlling_TeX': {'path': str(tex_path), **pin(tex_path)},
    'native_metadata_exact': record['metadata'], 'native_asset_pins_ordered': asset_pins,
    'raw_metadata': [{'path': str(S / x), **pin(S / x)} for x in ('record.response.body', 'files-23331709.response.body')],
    'native_custom_order': wrapper['order'], 'native_default_preview': wrapper['default_preview'],
    'native_version': '1.0', 'printed_numeric_version': None, 'printed_date': '13 October 2026',
    'root_PDF_text_read': {'path': str(R / 'published-pdf.txt'), **pin(R / 'published-pdf.txt')},
    'root_original_pages_personally_inspected': pages, 'full132_TeX_all5_PDF_pages_personally_read': True,
    'raw_original_abstract_TeX': tex.split('\\begin{abstract}', 1)[1].split('\\end{abstract}', 1)[0].strip(),
    'expected_full_abstract_plain': (O / 'ABSTRACT_EXPECTED.txt').read_text().strip(),
    'writer_draft_helper_model_findings_opened': False, 'informed_root_cleared_fact_copy_role': True,
    'new_scientific_review_or_program_execution': False, 'publication_authority': False, 'follow_up': None})
owned = {}
for path in O.iterdir():
    need(stat.S_ISREG(path.lstat().st_mode), 'Unexpected initial directory/special node')
    owned[path.name] = pin(path)
need(set(owned) == {'INITIAL.md', 'RESEARCH_LOG.md', 'ABSTRACT_EXPECTED.txt', 'freeze_initial.py',
     'freeze.stdout.txt', 'freeze.stderr.txt', 'SOURCE_EXPECTATIONS.json'}, 'Initial extent differs')
save('INITIAL_MANIFEST.json', {'schema': 'finite-independent-copy-contract-manifest-v1', 'UTC': now,
    'root': str(O), 'root_mode': oct(stat.S_IMODE(O.stat().st_mode)), 'whole_files_including_controls': 9,
    'child_directories': [], 'files': [{'path': k, **v} for k, v in sorted(owned.items())],
    'exact_root_terminal_exclusions': ['INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'], 'ignored_empty_files_included': True})
save('INITIAL_SEAL.json', {'schema': 'independent-fact-copy-source-contract-seal-v1', 'UTC': now,
    'record': 23331709, 'row': 167, 'status': 'SOURCE_EXPECTATIONS_FROZEN_BEFORE_WRITER',
    'whole_files': 9, 'child_directories': 0, 'INITIAL': pin(O / 'INITIAL.md'),
    'source_expectations': pin(O / 'SOURCE_EXPECTATIONS.json'), 'manifest': pin(O / 'INITIAL_MANIFEST.json'),
    'source_contract_complete_percent': 100, 'whole_fact_copy_estimate_percent': 30,
    'writer_opened': False, 'publication_authority': False, 'AA': None, 'follow_up': None})
