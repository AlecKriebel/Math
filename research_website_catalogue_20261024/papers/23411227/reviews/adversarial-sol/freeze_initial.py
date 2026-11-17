"""Finite data-only source-first seal; no scientific/native/foreign program execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

O = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23411227/reviews/adversarial-sol')
S = O.parent.parent/'sources'

def need(test, message):
    if not test:
        raise RuntimeError(message)

def pin(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'Nonordinary file: '+str(path))
    body = path.read_bytes()
    return {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest(),
            'mode': oct(stat.S_IMODE(info.st_mode))}

for name in ['SOURCE_PINS.json', 'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json']:
    need(not (O/name).exists(), 'Refusing existing source-first terminal output: '+name)
references = ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json', 'SOURCE_READY.json',
    'record.response.body', 'files-23411227.response.body',
    'assets/rank-two-fano-note.pdf', 'assets/rank-two-fano-verification.zip',
    'published-source/container-001/tree/note.tex']
source_pins = [{**{'path':str(S/name)}, **pin(S/name)} for name in references]
need(source_pins[0]['SHA256'] == '46a1f71e118fff3101c7f0af2158658847ad338172d7bd6d119ba041c8613886', 'Source FINAL changed')
need(source_pins[1]['SHA256'] == '3bd41786837658193a0258d1f1a70dc719f0e321647ed885294e9947f64a1e7b', 'Source manifest changed')
need(source_pins[5]['SHA256'] == '38b4897c731fe9916a7ae8eaf3cb6c62352631f24776b9b93f9af61807ab0060', 'Actual PDF changed')
need(source_pins[7]['SHA256'] == '58fc08b947c20e4d00fb6a379a109e8489aa6a22b1f2161587980ada95c318bc', 'Controlling TeX changed')
record = json.loads((S/'record.response.body').read_bytes())
files = json.loads((S/'files-23411227.response.body').read_bytes())
facts = {'record':23411227, 'row':172, 'source_references':source_pins,
    'metadata_original':record['metadata'], 'native_record_file_order':record['files'],
    'native_files_wrapper_original':files, 'created':record['created'],
    'modified':record['modified'], 'updated':record['updated'],
    'status':record['status'], 'state':record['state'], 'submitted':record['submitted'],
    'is_published':record.get('is_published','ABSENT'),
    'printed_version_personally_read':'1.0.0', 'printed_date_personally_read':'16 October 2026',
    'rights':'Native record cc-by-4.0; no separate LICENSE/COPYING filename found; no MIT split inferred',
    'actual_prior_whole_custody_receipt':pin(O/'SOURCE_CUSTODY.json')}
(O/'SOURCE_PINS.json').write_text(json.dumps(facts, indent=2)+'\n')
payload, directories = [], []
for path in sorted(O.rglob('*')):
    info = path.lstat()
    relative = str(path.relative_to(O))
    if stat.S_ISDIR(info.st_mode):
        directories.append({'path':relative, 'mode':oct(stat.S_IMODE(info.st_mode))})
    else:
        payload.append({'path':relative, **pin(path)})
now = datetime.now(timezone.utc).isoformat()
manifest = {'schema':'actual-source-first-result-manifest-v1', 'UTC':now,
    'root':str(O), 'files_including_two_terminal_controls':len(payload)+2,
    'directories':directories, 'payloads':payload,
    'exact_root_terminal_exclusions':['INITIAL_MANIFEST.json','INITIAL_SEAL.json']}
(O/'INITIAL_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
seal = {'schema':'actual-independent-adversarial-source-first-seal-v1', 'UTC':now,
    'record':23411227, 'row':172, 'status':'SOURCE_ONLY_INITIAL_AND_ACTUAL_HAND_RESULTS_FROZEN',
    'INITIAL':pin(O/'INITIAL.md'), 'independent_results':pin(O/'INDEPENDENT_RESULTS.md'),
    'manifest':pin(O/'INITIAL_MANIFEST.json'), 'source_pins':pin(O/'SOURCE_PINS.json'),
    'actual_regular_files':len(payload)+2, 'child_directories':len(directories),
    'all388_TeX_lines_all5_PDF_pages_all5_fresh_pixels_personally_read':True,
    'actual_independent_derivations_and_controls_completed_before_support_foreign_opinions':True,
    'original_scientific_program_executions':0, 'foreign_proof_support_archived_current_peer_root_bodies_opened':False,
    'peer_coordination':False, 'source_first_completion_percent':100,
    'full_adversarial_review_estimate_percent':55, 'findings_withheld_until_root_gate':True,
    'publication_authority':False, 'AA':None, 'canonical_url':None, 'follow_up':None}
(O/'INITIAL_SEAL.json').write_text(json.dumps(seal, indent=2)+'\n')
print(json.dumps({'INITIAL_SEAL':pin(O/'INITIAL_SEAL.json'),
                 'INITIAL':pin(O/'INITIAL.md'), 'manifest':pin(O/'INITIAL_MANIFEST.json'),
                 'actual_files':len(payload)+2, 'child_directories':len(directories),
                 'source_first_ready':True}))
