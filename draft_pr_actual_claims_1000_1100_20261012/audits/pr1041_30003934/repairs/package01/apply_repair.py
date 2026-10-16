#!/usr/bin/env python3
"""One-time local editorial/package repair; never performs remote operations."""
import sys
sys.dont_write_bytecode = True
import datetime, difflib, hashlib, json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
ROOT = AUDIT / 'preprint_v1_0'
def sha(data): return hashlib.sha256(data).hexdigest()
def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')
def replace(name, old, new):
    path = ROOT / name
    data = path.read_text()
    if data.count(old) != 1: raise RuntimeError('Unique replacement failed: '+name)
    path.write_text(data.replace(old, new))

baseline = json.loads((HERE/'BASELINE_PINS.json').read_text())
for row in baseline['files']:
    path = AUDIT/row['path']
    if len(path.read_bytes()) != row['bytes'] or sha(path.read_bytes()) != row['sha256']:
        raise RuntimeError('Input drift: '+row['path'])

history_names = ['PREPARATION_REPORT.md','PDF_QA.json','BUILD_RECEIPT.json',
                 'INTEGRITY_QA.json','VERIFICATION_RECEIPT.json','ARCHIVE_SHA256.json',
                 'CURRENT_INTEGRITY.json','EVIDENCE_COPY_MANIFEST.json','STATUS.json']
for name in history_names:
    dst = ROOT/'history/initial_preparation'/name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/name, dst)
dump(ROOT/'history/initial_preparation/INPUT_SCOPE.json', {
    'scope':'Exact pre-repair preparation records for the unchanged NEW_WHOLE_01 candidate; every path and status in these records retains its historical scope.',
    'original_candidate_files': [r for r in baseline['files'] if r['group']=='candidate'],
    'first_whole_review':'evidence/reviews/package_01/FINAL_INPUT_PINS.json',
    'tex_sha256':sha((ROOT/'paper.tex').read_bytes()),
    'pdf_sha256':sha((ROOT/'output/pdf/paper.pdf').read_bytes()),
    'archive_sha256':sha((ROOT/'supportkit-v1.0.tar.gz').read_bytes())})
(ROOT/'history/initial_preparation/README.md').write_text(
    '# Initial preparation history\n\nThese are unchanged records from the candidate reviewed by NEW_WHOLE_01. '
    'Their pending status, input paths, hashes, page checks and receipts describe that frozen input only. '
    'INPUT_SCOPE.json identifies its 85 candidate files. The current kit state is ../../STATUS.json; '
    'current build and layout receipts are at the package root. No historical verdict or pin has been retargeted.\n')

replace('paper.tex',
    'The accompanying preparation package remains pending a new complete manuscript/package review.',
    'The accompanying support package preserves the dated AI review history and the exact input scope of each review; its current kit state is recorded in \\texttt{STATUS.json}.')
old = (HERE/'baseline/paper.tex').read_text()
new = (ROOT/'paper.tex').read_text()
delta = ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='before/paper.tex',tofile='after/paper.tex'))
(HERE/'TEX_DISCLOSURE_DIFF.patch').write_text(delta)
replacement = ('The accompanying support package preserves the dated AI review history and the exact input scope of each review; its current kit state is recorded in \\texttt{STATUS.json}.')
if new.replace(replacement,'The accompanying preparation package remains pending a new complete manuscript/package review.') != old:
    raise RuntimeError('Mathematical source changed')

replace('README.md',
    '**Current status: content prepared; PENDING_NEW_WHOLE_01; publication_ready=false.** The underlying complete proof was accepted in the root mathematical audit after two fresh mathematical review families. That acceptance does not replace the pending new complete manuscript/package adversarial review. No external submission, publication, DOI creation, Git operation, or service mutation is performed by this package.',
    'The underlying complete proof was accepted in the root mathematical audit after two fresh mathematical review families. The support package preserves dated independent and adversarial AI review history, with each verdict limited to its frozen input. `evidence/reviews/package_01/` records the first complete manuscript/package review, which found zero P0–P3 issues on its unchanged inputs. The root subsequently recorded an editorial release-wording issue; the repair and subsequent review state are tracked in `STATUS.json`. These records are unrefereed AI review evidence.')
replace('README.md',
    '`publication/zenodo.json` is a prepared metadata wrapper, not an uploaded record or DOI reservation.',
    '`publication/zenodo.json` supplies publication metadata. The external `zenodo-deposit.json` wrapper exactly embeds that metadata and names the supplied PDF and support archive for the repository tool; it is locally prepared only. Its preparation does not create an uploaded record or reserve a DOI.')
replace('SUPPLEMENT.md',
    'The fresh flow, game, and priority families retain their authored derivations/reports, code/receipts where applicable, independence checkpoints, input/final/output pins, logs, and source receipt/catalogue metadata.',
    'The fresh flow, game, priority and first complete manuscript/package review retain their authored derivations/reports, code/receipts where applicable, independence checkpoints, input/final/output pins, logs, and source receipt/catalogue metadata. The first complete review is frozen at `evidence/reviews/package_01/`: its clean zero-issue verdict applies to its pinned original input, before the root release-wording repair. Its legitimate exact-test stdout/stderr streams are retained; raw source bodies, extracts, renderings and disposable replay directories remain excluded.')
replace('SUPPLEMENT.md',
    'Candidate archive and build/verification receipts are kept outside its self-reference domain.',
    'The candidate archive, external `zenodo-deposit.json` wrapper and root build/verification/archive-hash receipts are kept outside its self-reference domain. The wrapper names the archive, so excluding it prevents archive self-reference; its exact metadata equality and both supplied-file hashes are checked externally. Unchanged initial preparation reports, PDF checks, receipts and input pins live under `history/initial_preparation/` with explicitly historical scope. Root `PREPARATION_REPORT.md`, `PDF_QA.json`, and build receipts describe the editorially repaired inputs.')
replace('SUPPLEMENT.md',
    'all raw/rawprivate material, PDFs other than the authored paper, extracted `.txt`, page images, caches, rendering intermediates, and citation-discovery response dumps are excluded.',
    'all raw/rawprivate material, PDFs other than the authored paper, extracted source text (including `fullsource.txt` outside raw folders), page images, caches, rendering intermediates, disposable replay trees, and citation-discovery response dumps are excluded. Only explicitly copied, pinned authored test stdout/stderr `.txt` streams from the first complete review are distributed; these contain no source bodies.')
replace('SUPPLEMENT.md',
    'The root accepted the underlying full theorem; NEW_WHOLE_01 review of this exact manuscript/package is pending. `publication_ready=false` until that review and root decision.',
    'The root accepted the underlying full theorem. The dated complete AI review history records a clean NEW_WHOLE_01 verdict on its frozen inputs and a later root editorial release-wording observation. Every verdict remains limited to its exact input hashes; the current kit state and subsequent review disposition are in `STATUS.json`.')
replace('EVIDENCE_INDEX.md',
    'This index distinguishes theorem evidence, finite checks, historical records, and pending review.',
    'This index distinguishes theorem evidence, finite checks, and dated review history with exact frozen input scopes.')
replace('EVIDENCE_INDEX.md','NEW_WHOLE_01 review pending.','Review input scopes and current kit state are recorded separately.')
replace('EVIDENCE_INDEX.md',
    '| `RESEARCH_LOG.md`, `PREPARATION_REPORT.md` | UTC preparation checkpoints and limits; no readiness promotion before NEW_WHOLE_01. |',
    '| `evidence/reviews/package_01/` | Unchanged authored first complete AI review: clean zero P0–P3 findings on its pinned pre-repair inputs, with independence, source scopes, exact checks and terminal output pins. |\n'
    '| `evidence/root/ROOT_PREPRINT_REVIEW_01.json` | Root final-readiness observation on the same frozen candidate; one editorial release-wording issue, preserved unchanged. |\n'
    '| `history/initial_preparation/` | Byte-identical initial preparation report, PDF QA, machine status, manifests and receipts, with their exact historical input scope. |\n'
    '| `RESEARCH_LOG.md`, `PREPARATION_REPORT.md`, `PDF_QA.json` | UTC preparation/repair checkpoints, current repair report and current PDF layout check. Read `STATUS.json` for current kit state. |')

metadata = json.loads((ROOT/'publication/zenodo.json').read_text())
metadata['notes'] = metadata['notes'].replace(
    'Prepared local metadata only; no upload, DOI reservation, release, or submission has occurred. Current manuscript/package review is PENDING_NEW_WHOLE_01 and publication_ready=false.',
    'The support package preserves dated independent/adversarial AI review history and each review\'s exact frozen input scope; its current kit state is recorded in STATUS.json. The repository deposit wrapper is locally prepared only and does not imply upload, DOI reservation, release, or submission.')
dump(ROOT/'publication/zenodo.json',metadata)
dump(ROOT/'zenodo-deposit.json',{'metadata':metadata,'files':[
    {'path':'output/pdf/paper.pdf','name':'paper.pdf'},
    {'path':'supportkit-v1.0.tar.gz','name':'supportkit-v1.0.tar.gz'}]})
status=json.loads((ROOT/'STATUS.json').read_text())
status['new_whole_package_review']='PENDING_NEW_WHOLE_02'
status['all_issues_resolved']=False
status['first_whole_package_review']={
    'review':'NEW_WHOLE_01','verdict':'PASS_COMPLETE_CURRENT_MANUSCRIPT_AND_PACKAGE',
    'findings':0,'frozen_input_scope':'evidence/reviews/package_01/FINAL_INPUT_PINS.json',
    'verdict_path':'evidence/reviews/package_01/VERDICT.json'}
status['root_release_wording_issue']='ROOT-P3-RELEASE-WORDING-01; editorial repair awaiting NEW_WHOLE_02 and root decision'
dump(ROOT/'STATUS.json',status)

manifest=json.loads((ROOT/'EVIDENCE_COPY_MANIFEST.json').read_text())
base=AUDIT/'reviews/package_01'
pins=json.loads((base/'OUTPUT_PINS.json').read_text())
for row in pins['files']:
    data=(base/row['path']).read_bytes()
    if len(data)!=row['bytes'] or sha(data)!=row['sha256']:raise RuntimeError('Frozen package_01 output drift')
names=[row['path'] for row in pins['files']]+['OUTPUT_PINS.json']
for name in sorted(names):
    if '/' in name:raise RuntimeError('Unexpected terminal output path')
    source='reviews/package_01/'+name; target='evidence/'+source
    src=AUDIT/source; dst=ROOT/target;dst.parent.mkdir(parents=True,exist_ok=True)
    data=src.read_bytes();dst.write_bytes(data)
    manifest['files'].append({'source_path':source,'package_path':target,'group':'frozen_package_01',
        'bytes':len(data),'sha256':sha(data),'copy_policy':'byte-identical authored record; frozen first whole review scope preserved; raw/private/replay/render material excluded'})
source='ROOT_PREPRINT_REVIEW_01.json';target='evidence/root/'+source
data=(AUDIT/source).read_bytes();(ROOT/target).write_bytes(data)
manifest['files'].append({'source_path':source,'package_path':target,'group':'root_release_wording_snapshot',
    'bytes':len(data),'sha256':sha(data),'copy_policy':'unchanged dated root frozen-input observation'})
manifest['policy'] += ' Includes pinned authored package_01 terminal records and legitimate exact-test stdout/stderr only; excludes raw/private/replay/extracted/render/tmp/caches/fullsource.txt and all source bodies even outside raw folders.'
manifest['first_preparation_copy_records_preserved']=53
manifest['appended_first_whole_review_records']=41
dump(ROOT/'EVIDENCE_COPY_MANIFEST.json',manifest)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(HERE/'RESEARCH_LOG.md').write_text('# Editorial package repair log\n\n'
    f'- {baseline["timestamp_utc"]}: Baseline pinned all 85 candidate files, all 11 originals, root records, complete family records and frozen first-review inputs/outputs before edits. Repair completion estimate: 5%.\n'
    f'- {now}: Replaced only the Section 7 pending-review sentence and related durable README/supplement/index/metadata wording. Mathematical TeX recovered exactly by reversing that single replacement. Copied 41 unchanged first-review terminal records and the root observation; preserved the original 53 copy-map records and historical preparation bytes. Machine state PENDING_NEW_WHOLE_02, publication_ready=false and all_issues_resolved=false. Repair completion estimate: 45%; compilation, page viewing and final integrity remain.\n')
dump(HERE/'APPLY_RECEIPT.json',{'timestamp_utc':now,'completion_percent':45,
    'mathematical_source_unchanged_except_one_disclosure_sentence':True,
    'tex_diff':'TEX_DISCLOSURE_DIFF.patch','first_review_records_appended':41,
    'original_copy_records_retained':53,'historical_preparation_records':history_names,
    'first_review_and_originals_unchanged':True,'external_operations':False})
print('Applied editorial changes and 42 unchanged evidence copies; source math unchanged; pending NEW_WHOLE_02.')
