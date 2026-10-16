"""Bounded administrative authoring; preserve exact preterminal identities."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

sys.dont_write_bytecode = True
F = Path(__file__).resolve().parent
A = F.parents[1]
C = A / 'preprint_v1_0'

def record(p):
    raw = p.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')

def main():
    freeze = json.loads((F/'INPUT_FREEZE.json').read_text())
    changed = {'preprint_v1_0/' + n for n in (
        'README.md', 'code/verify_kit.py', 'MANIFEST.json',
        'DEPOSIT_BINDING.json', 'pr1098_support_v1_0.zip')}
    for row in freeze['entries']:
        p = F/'before'/row['path'] if row['path'] in changed else A/row['path']
        if record(p) != {k: row[k] for k in ('bytes', 'sha256')}:
            raise ValueError('before/protected input mismatch: ' + row['path'])
    selected = []
    review_names = {
        'package_01': ['VERDICT.json', 'OUTPUT_SEAL.json', 'OUTPUT_PINS.json',
                       'REPORT.md', 'INDEPENDENT_DERIVATION_FROZEN.md'],
        'package_02': ['VERDICT.json', 'OUTPUT_SEAL.json', 'OUTPUT_PINS.json',
                       'REPORT.md', 'INDEPENDENT_DERIVATION.md']}
    for review, names in review_names.items():
        for name in names:
            selected.append((A/'reviews'/review/name,
                             C/'terminal/evidence'/review/name))
    for name in ('ROOT_WHOLE_PACKAGE_REVIEW_01.json', 'ROOT_WHOLE_PACKAGE_REVIEW_02.json'):
        selected.append((A/name, C/'terminal/evidence'/name))
    for name in ('README.md', 'code/verify_kit.py', 'MANIFEST.json', 'DEPOSIT_BINDING.json'):
        selected.append((F/'before/preprint_v1_0'/name, C/'terminal/before'/name))
    for name in ('OUTPUT_PINS.json', 'PREPARATION_SEAL.json'):
        selected.append((C/name, C/'terminal/before'/name))
    copies = []
    for source, target in selected:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if source.read_bytes() != target.read_bytes():
            raise ValueError('authored interface copy')
        copies.append({'source': str(source.relative_to(A)),
                       'destination': str(target.relative_to(C)),
                       'disposition': 'EXACT_AUTHORED_COPY', **record(source)})
    save(F/'COPY_LEDGER.json', {'entries': copies,
         'omitted_old_ZIP': {'source': 'preprint_v1_0/pr1098_support_v1_0.zip',
         'durable_local_before': 'finalization/terminal_admin_20261016/before/preprint_v1_0/pr1098_support_v1_0.zip',
         **record(F/'before/preprint_v1_0/pr1098_support_v1_0.zip'),
         'disposition': 'OMITTED_FROM_PUBLIC_PAYLOAD',
         'reason': 'Exact old closed archive retained durably and locally, individually ignored; no old archive is redistributed or recursively imported.'}})
    stages = []
    for review, names in review_names.items():
        pinned = json.loads((A/'reviews'/review/'OUTPUT_PINS.json').read_text())['entries']
        for row in pinned:
            stages.append({'review': review, **row,
                'disposition': 'EXACT_AUTHORED_COPY' if row['path'] in names else 'OMITTED',
                **({'destination': 'terminal/evidence/'+review+'/'+row['path']} if row['path'] in names else {
                    'reason': 'Selected portable authored interfaces only; no raw execution/compiler streams, source bodies, pixels, runtime or duplicate historical control payload imported. Full original review stays exact in the research audit.'})})
    save(C/'terminal/REVIEW_STAGE_SELECTION.json', {'entries': stages,
         'scope': 'Individual selection of every output pinned by each completed whole review; seal and pinfile are additional exact authored interfaces. Omission never claims replay.'})
    status = {
        'schema_version': 1, 'checkpoint_date_utc': '2026-10-16',
        'stage': 'TERMINAL_ADMIN_COMPLETE_PENDING_ROOT_FINAL_INTEGRITY',
        'new_complete_whole_reviews_completed': 2,
        'minimum_new_complete_whole_reviews_required': 2,
        'latest_whole_review': 'NEW_INDEPENDENT_COMPLETE_WHOLE_PACKAGE_02',
        'latest_review_complete': True,
        'latest_review_actionable_findings': {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0},
        'latest_whole_review_ROOT_adopted': True,
        'further_whole_package_review_currently_required': False,
        'terminal_administrative_reconciliation_complete': True,
        'ROOT_final_terminal_integrity': 'REQUIRED_UNADOPTED',
        'ROOT_final_terminal_integrity_adopted': False,
        'publication_ready': False, 'issues_resolved': False, 'published': False,
        'services_held_after_pr': 1032,
        'full_result_physical_simple_oriented_realization_remaining_method_priority_worldwide_openness': 'UNKNOWN',
        'exact_scope_math_adopted': True,
        'reviewed_preterminal_support_archive': record(F/'before/preprint_v1_0/pr1098_support_v1_0.zip'),
        'unchanged_paper': record(C/'paper.pdf'),
        'evidence_root': 'terminal/evidence',
        'historical_preparation_status': 'STATUS.json',
        'scope': 'Current administrative state. The two whole reviews adopted the unchanged paper and preterminal payload. This administrative payload update requires external ROOT final integrity, presently unadopted. Earlier statuses, seals, pins, reports and metadata checkpoint notes retain their exact dated meaning.'}
    save(F/'TERMINAL_STATUS.json', status)
    shutil.copyfile(F/'TERMINAL_STATUS.json', C/'TERMINAL_STATUS.json')
    readme = (F/'before/preprint_v1_0/README.md').read_text()
    readme = readme.replace('## Downloads and a clean reproduction',
        '## Current terminal state — 16 October 2026 UTC\n\n'
        'TERMINAL_STATUS.json is the current workflow record. Two new complete\n'
        'whole-package reviews have completed, meeting the minimum of two. The\n'
        'latest, whole02, found zero actionable P0/P1/P2/P3 issues and was adopted\n'
        'by ROOT. No further complete whole review is currently required. These\n'
        'reviews apply to the unchanged paper and the preterminal support archive\n'
        'identified in that record. This administrative payload update still\n'
        'requires an external ROOT final integrity review, which is **unadopted**.\n'
        'Publication readiness, issues-resolved and published remain **false**;\n'
        'all ordered external actions remain held after PR #1032.\n\n'
        'Selected exact authored review reports, independent derivations, verdicts,\n'
        'seals, pinfiles and ROOT adoptions are in terminal/evidence/. They are\n'
        'dated evidence, not new human peer review or priority certification. The\n'
        'first reviewer accurately qualified its fixture ORIGINAL redirection;\n'
        'whole02 separately ran 116 actual unchanged external commands with\n'
        'ROOT and ORIGINAL unmodified. Both actual PDFs matched the canonical\n'
        'seven-page paper, and all seven pages were viewed. No new PDF build or\n'
        'render was needed for this unchanged source. The semantic verifier checks\n'
        'the current status against both dated verdict/seal/pin/adoption chains.\n\n'
        '## Downloads and a clean reproduction')
    readme = readme.replace('STATUS.json records that past checkpoint. It does not',
        'STATUS.json, the preparation seal/report/pins and the metadata notes\n'
        'record that past checkpoint. TERMINAL_STATUS.json supersedes their\n'
        'workflow count for current use without rewriting them. That history does not')
    readme = readme.replace('PR bytes remain unchanged. No person was contacted.',
        'PR bytes remain unchanged. No person was contacted.\n\n'
        'terminal/before/ retains the exact preterminal authored README, verifier,\n'
        'manifest and deposit binding as historical interfaces. Its old manifest\n'
        'and binding describe the old archive, not the current download. The old\n'
        'ZIP remains durably local to the research audit and is deliberately not\n'
        'redistributed. terminal/PREPARATION_PIN_RESOLUTION.json resolves every\n'
        'one of the 123 old preparation pins individually to unchanged portable bytes,\n'
        'an exact before interface, or an explicitly omitted local preparation output\n'
        'or old ZIP identity. The 18 undistributed preparation helpers, reports and\n'
        'validation records remain exact at their original local audit paths.\n'
        'terminal/REVIEW_STAGE_SELECTION.json likewise states each selected or\n'
        'omitted review output; pinfiles do not imply omitted programs or raw\n'
        'streams are present or replayed. Source bodies and pixels remain omitted.')
    (C/'README.md').write_text(readme)
    rows = []
    portable_original = {r['path'] for r in json.loads((F/'before/preprint_v1_0/MANIFEST.json').read_text())['entries']}
    for row in json.loads((C/'OUTPUT_PINS.json').read_text())['entries']:
        name = row['path']
        if name == 'pr1098_support_v1_0.zip':
            rows.append({**row, 'disposition': 'KNOWN_OLD_ZIP_OMITTED',
                'reason': 'Exact old ZIP retained durably in the local audit before/ folder; omitted from this public payload to avoid recursively redistributing an obsolete archive.'})
        elif name in ('README.md', 'code/verify_kit.py', 'MANIFEST.json', 'DEPOSIT_BINDING.json'):
            rows.append({**row, 'disposition': 'EXACT_BEFORE_INTERFACE', 'resolved_path': 'terminal/before/'+name})
        elif name not in portable_original and name != 'paper.pdf':
            rows.append({**row, 'disposition': 'UNCHANGED_LOCAL_PREPARATION_OUTPUT_OMITTED',
                'reason': 'Exact dated preparation output retained unchanged at its original local audit path; deliberately outside the portable manifest. No helper, raw command/compiler stream, validation image or duplicate prior control payload is imported or claimed replayed.'})
        else:
            rows.append({**row, 'disposition': 'UNCHANGED_CURRENT_BYTES', 'resolved_path': name})
    save(C/'terminal/PREPARATION_PIN_RESOLUTION.json', {'entries': rows,
         'scope': 'All 123 preparation output identities remain exact dated evidence. This is resolution, never a rewrite of the original pinfile.'})
    (C/'terminal/README.md').write_text(
        '# Dated terminal evidence\n\nTERMINAL_STATUS.json at the kit root is current; earlier records are exact dated history.\n'
        'evidence/ contains only selected authored interfaces, including full reports and independent derivations.\n'
        'Their seals and pinfiles also identify outputs deliberately omitted under REVIEW_STAGE_SELECTION.json.\n'
        'before/ preserves the exact preterminal authored operative interfaces, not current commands or upload bindings.\n'
        'The old ZIP is durably local to the audit and absent from this payload. No third-party body, source text,\n'
        'rendered page, compiler/runtime cache, raw execution/compiler stream or old ZIP is newly redistributed.\n'
        'Whole01 and whole02 required ROOT adoption at their dated checkpoints; both were later adopted.\n'
        'The present administrative update still requires ROOT final integrity, unadopted.\n')
    print(json.dumps({'exact_interface_copies': len(copies), 'review_stage_rows': len(stages),
                      'preparation_pin_resolutions': len(rows)}))

if __name__ == '__main__':
    main()
