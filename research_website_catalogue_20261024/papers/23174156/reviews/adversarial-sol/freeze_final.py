"""Finite data-only closure. No scientific code, acquisition, or Git execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O = P / 'papers/23174156/reviews/adversarial-sol'
S = P / 'papers/23174156/sources'
Q = P / 'papers/23174156/reviews/scope-sol'
C = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr95_10400120')
K = C / 'priority_conjecture_history_20261005'
Y = C / 'priority_later_version_followup_20261005'

def pin(path):
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('Expected ordinary file: ' + str(path))
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(path.stat().st_mode))}

def check(path, expected):
    item = pin(path)
    if item['SHA256'] != expected:
        raise RuntimeError('Pin mismatch: ' + str(path))
    return item

for name in ['FINAL.json', 'MANIFEST.json', 'PRIMARY_PINS.json']:
    if (O / name).exists():
        raise RuntimeError('Refusing to overwrite closure file: ' + name)
initial_pin = check(O / 'INITIAL_SEAL.json', 'a2437879774834cea41fba7e1c456c4d4ce7f574f54beeaf9969a4a8f9e9cad5')
initial = json.loads((O / 'INITIAL_SEAL.json').read_text())
for old in initial['files']:
    actual = pin(O / old['path'])
    if any(actual[k] != old[k] for k in ['bytes', 'SHA256', 'mode']):
        raise RuntimeError('Original INITIAL payload changed: ' + old['path'])
source_manifest = check(S / 'SOURCE_MANIFEST.json', 'fdff8a4219c2b4b72f7395079fab6945ab2736784c712a359015c08ff40a35dc')
source_final = check(S / 'SOURCE_FINAL.json', '153bc99484999f9e5bca8623ee88e9935cf2c42557626112161f8f372a5a4827')
sm = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
expected = {x['path']: x for x in sm['files']}
expected.update({'SOURCE_MANIFEST.json': source_manifest, 'SOURCE_FINAL.json': source_final})
if sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_file()) != sorted(expected):
    raise RuntimeError('Source file extent differs')
for rel, old in expected.items():
    actual = pin(S / rel)
    if any(actual[k] != old[k] for k in ['bytes', 'SHA256', 'mode']):
        raise RuntimeError('Source file changed: ' + rel)
source_dirs = sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_dir())
if source_dirs != sorted(x['path'] for x in sm['directories']):
    raise RuntimeError('Source directory extent differs')
for old in sm['directories']:
    path = S / old['path']
    if path.is_symlink() or oct(stat.S_IMODE(path.stat().st_mode)) != old['mode']:
        raise RuntimeError('Source directory changed: ' + old['path'])
receipt_pin = check(O / 'native-run/RECEIPT.json', 'ae6033e0347ddfe7c838fba03da8b97b9645bcec581ebd217a589f66da496572')
receipt = json.loads((O / 'native-run/RECEIPT.json').read_text())
if receipt['exit_code'] != 1 or receipt['artifacts']:
    raise RuntimeError('Native receipt no longer describes retained failed attempt')
for old in receipt['streams']:
    if pin(Path(old['path'])) != old:
        raise RuntimeError('Literal native stream changed')

raw = [
    (Q/'primaries/hansen-takata-v2.pdf', 'a00c189a481c1c7f5ccb14968e4d3b29abe7e560d3bb416f13ba56ae795e609e', 'https://arxiv.org/pdf/math/0209403v2', 'math/0209403v2;2Feb2003;61pages'),
    (Q/'primaries/ohtsuki-problems.pdf', '33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd', 'https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf', 'GTM4 nominal2002;published1Jun2004;200pages'),
    (Q/'primaries/guadagnini-pilo-v1.pdf', '9dad5e47a2c787824e05cb97cd12c037c2a49dff9ea38bc7b22aee513aca29b0', 'https://arxiv.org/pdf/hep-th/9612090v1', 'hep-th/9612090v1;9Dec1996;22pages'),
    (K/'sources/kuriya_institutional.html', '860acb9213f10a9ad9165ea81e97d6fb18f6694cac48926be9ac50a93294427e', 'https://www2.math.kyushu-u.ac.jp/coe/staff/staff_sub/kuriya.html', 'historical official HTML cached5Oct2026;Shift_JIS'),
    (K/'sources/kuriya_kyushu_report.pdf', 'e46f2b85da39c1de6a1e0158a6ca573c3e2352535018789a923d5a0d2ec44f68', 'https://www2.math.kyushu-u.ac.jp/coe/report/pdf3/report-6.pdf', 'historical institutional report;99physical four-up pages;printed121 atphysical32'),
    (Y/'private_sources/kubo_yokoyama_v2.pdf', '05a138182c138c4c1cb794166250349c9021540e85dc958c6bf5b6806b2b7381', 'https://arxiv.org/pdf/2108.09300v2', '2108.09300v2;15Apr2022;37physicalpages')
]
raw_pins = []
for path, sha, url, edition in raw:
    item = check(path, sha)
    item.update({'source_URL': url, 'edition': edition, 'access': 'existing pinned raw local body; no new GET in this lane'})
    raw_pins.append(item)
reference_paths = [Q/'PRIMARY_ACQUISITION.json',
    Q/'primaries/hansen-takata-v2.txt', Q/'primaries/ohtsuki-problems.txt',
    Q/'primaries/guadagnini-pilo-v1.txt', K/'sources/kuriya_kyushu_report.txt',
    K/'receipts/kuriya_institutional.html.retrieval.json',
    K/'receipts/kuriya_kyushu_report.pdf.retrieval.json',
    Y/'private_sources/kubo_yokoyama_v2.txt', Y/'processes/retrieval_kubo_yokoyama_v2.json']
if (K/'sources/kuriya_kyushu_report.txt').read_bytes() != b'\f' * 99:
    raise RuntimeError('Report raw text is not exactly99 form-feed bytes')
primary = {'schema': 'raw-primary-reference-pins-v1', 'raw_bodies': raw_pins,
           'raw_extracts_and_acquisition_receipts': [pin(x) for x in reference_paths],
           'new_GETs': 0, 'foreign_review_reports_opened': False,
           'critical_actual_reading_and_page_locators': 'PRIMARY_READINGS.md'}
(O/'PRIMARY_PINS.json').write_text(json.dumps(primary, indent=2)+'\n')
payload = []
directories = []
for path in sorted(O.rglob('*')):
    if path.is_symlink():
        raise RuntimeError('Unexpected symlink in review')
    if path.is_dir():
        directories.append({'path': str(path.relative_to(O)), 'mode': oct(stat.S_IMODE(path.stat().st_mode))})
    else:
        item = pin(path)
        item['path'] = str(path.relative_to(O))
        payload.append(item)
now = datetime.now(timezone.utc).isoformat()
manifest = {'schema': 'finite-adversarial-review-manifest-v1', 'UTC': now,
            'root': str(O), 'ordinary_files_including_two_terminal_controls': len(payload)+2,
            'child_directories': directories, 'files': payload,
            'exact_root_terminal_exclusions': ['MANIFEST.json', 'FINAL.json']}
(O/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
final = {'schema': 'finite-adversarial-review-final-v1', 'UTC': now, 'record': 23174156,
         'row': 169, 'status': 'COMPLETE_FROZEN_FINDINGS_WITHHELD_PENDING_ROOT_GATE',
         'completion_percent_review': 100, 'INITIAL_SEAL': initial_pin,
         'all_initial_14_files_unchanged': True, 'REPORT': pin(O/'REPORT.md'),
         'MANIFEST': pin(O/'MANIFEST.json'), 'PRIMARY_PINS': pin(O/'PRIMARY_PINS.json'),
         'source_guard': {'all_bytes_modes_and_extent_match': True,
                          'files': len(expected), 'child_directories': len(source_dirs),
                          'manifest': source_manifest, 'final': source_final},
         'native_ordinary_invocations': 1, 'native_successful_reproductions': 0,
         'native_receipt': receipt_pin, 'no_retries_installs_or_environment_changes': True,
         'extent': {'files': len(payload)+2, 'child_directories': len(directories)},
         'publication_authority': False, 'AA': None, 'canonical_url': None,
         'followup': None, 'immutable_after_this_seal': True}
(O/'FINAL.json').write_text(json.dumps(final, indent=2)+'\n')
print(json.dumps({'FINAL': pin(O/'FINAL.json'), 'MANIFEST': pin(O/'MANIFEST.json'),
                  'REPORT': pin(O/'REPORT.md'), 'extent': final['extent'],
                  'completion_percent_review': 100, 'writes_cease_now': True}))
