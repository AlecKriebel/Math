"""Bounded local terminal administration. Never compiles or alters proof inputs."""
import ast
import datetime
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
PR = int(AUDIT.name.split('_')[0][2:])
PUB = AUDIT / ('publication' if PR == 1034 else 'preprint')
REVIEW = AUDIT / 'reviews/package_02'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
ARCHIVE = PUB / ('source_audit_kit.zip' if PR == 1034 else 'pr1037_supportkit_v1.0.zip')
PIN_NAME = 'OUTPUT_PINS.json' if PR == 1034 else 'OUTPUT_PIN.json'
PROTECTED_NAMES = (['publication/research_note.tex', 'publication/research_note.pdf', 'publication/metadata.json', 'publication/zenodo_metadata_wrapper.json', 'publication/zenodo-deposit.json'] if PR == 1034 else ['preprint/paper/forest_transfer_catalan.tex', 'preprint/paper/forest_transfer_catalan.pdf', 'preprint/.zenodo.json', 'preprint/zenodo_metadata.json', 'preprint/zenodo-deposit.json'])
MUTABLE = (['RESEARCH_LOG.md', 'publication/README.md', 'publication/SUPPLEMENT.md', 'publication/build_package.py', 'publication/PACKAGE_ALLOWLIST.json', 'publication/PACKAGE_INPUT_PINS.json', 'publication/PACKAGE_MANIFEST.json', 'publication/CANDIDATE_INTEGRITY.json', 'publication/source_audit_kit.zip', 'publication/evidence/CURRENT_REVIEW_STATE.json', 'publication/evidence/MAP.json', 'publication/evidence/INDEX.md'] if PR == 1034 else ['RESEARCH_LOG.md', 'preprint/README.md', 'preprint/SUPPLEMENT.md', 'preprint/build_supportkit.py', 'preprint/CURRENT_REVIEW_STATE.json', 'preprint/REVIEW_HISTORY.json', 'preprint/EVIDENCE_INDEX.json', 'preprint/MANIFEST.json', 'preprint/ARCHIVE_PIN.json', 'preprint/pr1037_supportkit_v1.0.zip'])

def require(ok, why):
    if not ok:
        raise RuntimeError(why)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rec(p, root=AUDIT):
    return {'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}

def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def edit(p, old, new):
    data = p.read_text()
    require(data.count(old) == 1, 'administrative anchor differs: ' + str(p))
    p.write_text(data.replace(old, new))

def copy(p, q):
    q.parent.mkdir(parents=True, exist_ok=True)
    require(not q.exists(), 'refusing to overwrite frozen copy: ' + str(q))
    q.write_bytes(p.read_bytes())
    require(p.read_bytes() == q.read_bytes(), 'copy differs')

def inventory():
    return [rec(p) for p in sorted(AUDIT.rglob('*')) if p.is_file() and 'finalization' not in p.relative_to(AUDIT).parts]

def stage_gate():
    root = json.loads((AUDIT / 'ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text())
    verdict = json.loads((REVIEW / 'VERDICT.json').read_text())
    require(root['root_entire_report_and_verdict_read'] and root['mathematics_accepted_unchanged'], 'root has not adopted entire exact review')
    require(root['status'] == 'ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL', 'wrong root stage')
    counts = verdict['severity_counts'] if PR == 1034 else verdict['issue_counts']
    require(set(counts) == {'P0', 'P1', 'P2', 'P3'} and all(v == 0 for v in counts.values()), 'terminal actionable findings')
    require(verdict.get('findings', verdict.get('issues')) == [], 'terminal findings')
    require(sha(REVIEW / 'REPORT.md') == root['report_sha256'] and sha(REVIEW / 'VERDICT.json') == root['verdict_sha256'] and sha(REVIEW / PIN_NAME) == root['output_pins_sha256'], 'root reviewed seal differs')
    expected = verdict['candidate']['archive']['sha256'] if PR == 1034 else verdict['candidate_zip_sha256']
    require(sha(ARCHIVE) == expected, 'reviewed archive changed before finalization')
    rows = json.loads((REVIEW / PIN_NAME).read_text())['files']
    for r in rows:
        p = REVIEW / r['path']
        require(p.stat().st_size == r['bytes'] and sha(p) == r['sha256'], 'sealed review output changed: ' + r['path'])
    require(len(rows) == (31 if PR == 1034 else 67), 'terminal output count')
    return root, verdict, rows

def freeze():
    require(not (HERE / 'INPUT_PINS.json').exists(), 'already frozen; use verification script')
    root, verdict, rows = stage_gate()
    before = inventory()
    save(HERE / 'INPUT_PINS.json', {'utc': NOW, 'schema': 'strict-all-existing-audit-inputs-v1', 'scope': 'Every pre-existing regular audit file outside this new finalization effort, including excluded private/source/environment/scratch custody. Hash metadata is not a distribution promise.', 'files': before, 'self_excluded': True})
    save(HERE / 'FROZEN_BASELINE.json', {'utc': NOW, 'pr': PR, 'reviewed_archive': rec(ARCHIVE), 'protected_math_metadata': [rec(AUDIT / x) for x in PROTECTED_NAMES], 'allowed_existing_mutations': MUTABLE, 'review_outputs': [rec(REVIEW / r['path']) for r in rows] + [rec(REVIEW / PIN_NAME)], 'root_adoption': rec(AUDIT / 'ROOT_WHOLE_PACKAGE_REVIEW_02.json'), 'fresh_whole_package_reviews': 2, 'services_hold': 'ascending cursor PR1032', 'root_final_adoption_required': True})
    for name in MUTABLE:
        copy(AUDIT / name, HERE / 'frozen_before' / name)
    history = PUB / ('evidence/history/before_terminal_admin_20261014' if PR == 1034 else 'history/before_terminal_admin_20261014')
    history_rows = []
    for name in MUTABLE:
        p = AUDIT / name
        if p == ARCHIVE or name == 'RESEARCH_LOG.md':
            continue
        relative = p.relative_to(PUB)
        q = history / relative
        copy(p, q)
        history_rows.append({'source_before_path': name, 'frozen_copy_path': q.relative_to(AUDIT).as_posix(), **{k:v for k,v in rec(q).items() if k != 'path'}})
    save(history / 'HISTORY.json', {'utc': NOW, 'stage': 'Reviewed repaired candidate BEFORE terminal readiness administration; all pending labels retain this exact input-stage meaning.', 'files': history_rows, 'reviewed_archive': rec(ARCHIVE), 'reviewed_archive_copy': str((HERE / 'frozen_before' / ARCHIVE.relative_to(AUDIT)).relative_to(AUDIT)), 'duplicate_archive_distributed': False, 'private_bodies_and_proof_source_not_duplicated': True})
    (HERE / 'RESEARCH_LOG.md').write_text(f'# Terminal administration log for PR{PR}\n\n{NOW}: 15% of bounded terminal administration. Exact accepted zero-finding review and every sealed output rehashed. All pre-existing audit bytes frozen by INPUT_PINS; pending receipts copied before mutation. No mathematical change or external action.\n')
    return root, verdict, rows, before

def terminal_copies(rows):
    target = PUB / ('evidence/package_02' if PR == 1034 else 'evidence/whole_20261014/package_02')
    copies, exclusions = [], []
    rows = rows + [rec(REVIEW / PIN_NAME, REVIEW)]
    for r in rows:
        relative = PurePosixPath(r['path'])
        require(not relative.is_absolute() and '..' not in relative.parts and len(relative.parts) == 1, 'unexpected terminal output path')
        p = REVIEW / r['path']
        require(rec(p, REVIEW) == r, 'terminal output pin mismatch')
        if p.suffix.lower() not in {'.md', '.json', '.py'}:
            reason = ('Strict existing PR1034 payload suffix policy excludes this authored text diff; original diff remains sealed locally.' if PR == 1034 and p.suffix == '.txt' else 'Extraction of manuscript text is omitted; the unchanged paper PDF/TeX are already included.' if p.name in {'candidate_pdf.txt','recompiled_pdf.txt'} else 'Control file or raw process stdout/stderr is omitted from public payload; authored JSON receipts/results retain the exact historical execution and failure scope. Original sealed output and hash remain local.')
            exclusions.append({**r, 'source_path': p.relative_to(AUDIT).as_posix(), 'distribution': 'OMITTED', 'reason': reason})
            continue
        q = target / p.name
        copy(p, q)
        copies.append({'package_path': q.relative_to(PUB).as_posix(), 'audit_package_path': q.relative_to(AUDIT).as_posix(), 'source_path': p.relative_to(AUDIT).as_posix(), 'bytes': r['bytes'], 'sha256': r['sha256'], 'stage': 'Unchanged authored terminal whole review02; hash references keep original input-stage meaning.'})
    rootcopy = PUB / 'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json'
    copy(AUDIT / 'ROOT_WHOLE_PACKAGE_REVIEW_02.json', rootcopy)
    rr = rec(rootcopy)
    copies.append({'package_path': rootcopy.relative_to(PUB).as_posix(), 'audit_package_path': rr['path'], 'source_path': 'ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'bytes': rr['bytes'], 'sha256': rr['sha256'], 'stage': 'Unchanged root full-report/verdict acceptance, pending terminal administration at its own dated stage.'})
    map_path = PUB / 'evidence/TERMINAL_REVIEW_02_COPY_MAP.json'
    save(map_path, {'utc': NOW, 'pr': PR, 'files': copies, 'omitted_outputs': exclusions, 'sealed_output_manifest_copied_unchanged': True, 'pin_references_to_private_or_omitted_inputs_are_not_distribution_promises': True, 'third_party_bodies_raw_render_extraction_environment_duplicate_archives_excluded': True})
    save(PUB / 'evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json', {'utc': NOW, 'pr': PR, 'policy': 'Only unchanged authored md/json/py terminal outputs and root receipt are copied. Every pinned omitted terminal output has its own reason. Original seal/input/custody manifests retain hashes of private outputs without redistributing bodies.', 'omitted_terminal_outputs': exclusions, 'unlisted_private_review_trees': ['reviews/package_02/private_raw','reviews/package_02/rawprivate','reviews/package_02/visual','reviews/package_02/render','reviews/package_02/clean_compile','reviews/package_02/clean_extraction','reviews/package_02/.venv'], 'unlisted_private_trees_policy': 'Not copied. Their exact source/custody pins remain in unchanged terminal manifests. No full third-party bodies, extracted full text, renders, environment, compiler products or duplicate ZIPs are included.'})
    return copies, exclusions

def acceptance(root, verdict):
    path = PUB / 'evidence/FINAL_ACCEPTANCE.json'
    save(path, {'utc': NOW, 'pr': PR, 'scope': verdict.get('scope'), 'fresh_whole_package_reviews': 2, 'terminal_review_status': verdict['status'], 'actionable_issue_counts': {'P0':0,'P1':0,'P2':0,'P3':0}, 'actionable_issues': [], 'root_entire_terminal_report_verdict_adopted': True, 'root_terminal_review_receipt': 'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'terminal_copy_map': 'evidence/TERMINAL_REVIEW_02_COPY_MAP.json', 'protected_mathematical_source_PDF_metadata': [rec(AUDIT / x) for x in PROTECTED_NAMES], 'publication_ready': True, 'published': False, 'publication_order_hold': 'BLOCKED FROM SERVICES: preceding PR1032 priority disposition / ascending cursor1032', 'root_final_administrative_verification_pending': True, 'postreview_changes': 'Unchanged authored terminal review records/root adoption and administrative state/history/navigation/build stage only.', 'novelty_or_worldwide_priority_established': False, 'extensive_AI_use': True, 'human_peer_review': False, 'formal_certificate': False, 'services_or_external_contact_performed': False})

def administer_1034(root, verdict, copies):
    state_path = PUB / 'evidence/CURRENT_REVIEW_STATE.json'
    state = json.loads(state_path.read_text())
    state.update({'utc': NOW, 'state':'FINAL_ZERO_ACTIONABLE_TERMINAL_ADMINISTRATION', 'required_review': None, 'review_assigned':True, 'review_verdict':'evidence/package_02/VERDICT.json', 'publication_ready':True, 'published':False, 'root_review_required':False, 'fresh_whole_package_reviews':2, 'all_actionable_issues_resolved':True, 'actionable_issue_counts':{'P0':0,'P1':0,'P2':0,'P3':0}, 'repair_state':'VERIFIED_BY_NEWWHOLE02_ZERO_ACTIONABLE', 'root_terminal_adoption':'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'final_acceptance':'evidence/FINAL_ACCEPTANCE.json', 'publication_order_hold':'BLOCKED_FROM_SERVICES_PRECEDING_PR1032_PRIORITY_CURSOR', 'root_final_administrative_verification_pending':True})
    save(state_path, state)
    stage = json.loads((PUB / 'evidence/MAP.json').read_text())
    stage['utc'] = NOW
    stage['historical_stages'].append({'name':'repaired_application_note_pending_NEWwhole02', 'records':'publication/evidence/history/before_terminal_admin_20261014', 'reviewed_archive_sha256': verdict['candidate']['archive']['sha256'], 'meaning':'Frozen exact pending candidate independently cleared by NEWwhole02; its original receipts retain pending-stage wording.'})
    stage['historical_stages'].append({'name':'NEWwhole02', 'records':'publication/evidence/package_02', 'root_adoption':'publication/evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'meaning':'Second fresh exact whole-candidate review, unchanged report/verdict/output seal; zero actionable P0-P3.'})
    stage['current_stage'].update({'name':'final_zero_actionable_terminal_administration','publication_ready':True,'published':False,'terminal_acceptance':'publication/evidence/FINAL_ACCEPTANCE.json','publication_order_hold':'preceding PR1032 priority cursor; services blocked','root_final_administrative_verification_pending':True})
    save(PUB / 'evidence/MAP.json', stage)
    edit(PUB / 'README.md', 'This is a prepared, unrefereed application-note candidate. The accompanying kit records the review history through 13 October 2026 and the current preparation state in `evidence/CURRENT_REVIEW_STATE.json`. Publication readiness remains false after the two repairs requested by whole-package review NEWwhole01; fresh exact-candidate review NEWwhole02 and root adoption are required. Mathematical acceptance and adoption of credited application framing are earlier, separate stages.', 'This is an unrefereed application note. Two fresh whole-package reviews are complete; NEWwhole02 verified the repaired exact candidate with zero actionable P0–P3 findings, and the root adopted its complete report and verdict. Terminal administration dated 14 October 2026 records `publication_ready=true` and `published=false` in `evidence/CURRENT_REVIEW_STATE.json`. The unchanged terminal records and root receipt are mapped in `evidence/TERMINAL_REVIEW_02_COPY_MAP.json`; `evidence/FINAL_ACCEPTANCE.json` records the readiness boundary. Root verification of this final administrative append remains pending. Publication services are blocked by the preceding PR1032 priority cursor.')
    edit(PUB / 'SUPPLEMENT.md', 'do not supersede the paper’s current credited framing or pending whole-package review.', 'do not supersede the paper’s current credited framing or the separately recorded terminal whole-package clearance.')
    source = (PUB / 'SUPPLEMENT.md').read_text()
    source = source[:source.index('## Current gate')] + '## Current terminal administration\n\nAs of 14 October 2026, two fresh whole-package reviews are complete. NEWwhole02 independently verified the complete repaired candidate and all thirteen PDF pages with zero actionable P0–P3 findings; the root adopted the entire report and verdict. `evidence/FINAL_ACCEPTANCE.json`, the unchanged `evidence/package_02/REPORT.md` and `VERDICT.json`, and `evidence/TERMINAL_REVIEW_02_COPY_MAP.json` record that stage. Current readiness is true and published is false. Root verification of the administrative append is pending, and publication services remain blocked by the preceding PR1032 priority cursor.\n\n`evidence/history/before_terminal_admin_20261014/` preserves the reviewed pending receipts before this append. All earlier wording and pins retain their exact dated input meanings. Only unchanged authored terminal records, the root receipt, and administrative state/history/navigation/build controls were appended or changed. The reviewed paper source, PDF, metadata and all existing proof/checker records remain byte-identical. Private-source pins in the copied seals do not promise inclusion of private bodies; the terminal exclusion ledger explains each omitted output.\n'
    (PUB / 'SUPPLEMENT.md').write_text(source)
    edit(PUB / 'evidence/INDEX.md', 'Current state is `publication/evidence/CURRENT_REVIEW_STATE.json`: **PENDING NEWwhole02; not publication-ready**.', 'That repaired pending state is preserved in `publication/evidence/history/before_terminal_admin_20261014/`. Current state is `publication/evidence/CURRENT_REVIEW_STATE.json`: **zero actionable terminal review accepted; publication-ready, unpublished, service-held at PR1032**.')
    with (PUB / 'evidence/INDEX.md').open('a') as out:
        out.write('\n8. **Terminal whole review02 and administrative append, 14 October 2026**: `publication/evidence/package_02/REPORT.md` and `VERDICT.json` are unchanged copies; its complete `OUTPUT_PINS.json` is preserved even where output types are excluded. `publication/evidence/TERMINAL_REVIEW_02_COPY_MAP.json` pins each copy and explains every omitted sealed output. `publication/evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json` is the unchanged root adoption. `publication/evidence/FINAL_ACCEPTANCE.json` records readiness, the service hold and pending final root administrative verification. Existing proof, PDF, metadata, checkers and old reviews remain unchanged.\n')
    builder = PUB / 'build_package.py'
    edit(builder, 'require(state["publication_ready"] is False and state["required_review"] == "NEWwhole02",\n            "this preparation builder binds the repaired pending NEWwhole02 candidate only")\n    require(state["state"] == "PENDING_NEW_WHOLE_PACKAGE_REVIEW", "wrong stage")', '''require(state["publication_ready"] is True and state["required_review"] is None,
            "terminal ready stage requires accepted zero-actionable NEWwhole02")
    require(state["state"] == "FINAL_ZERO_ACTIONABLE_TERMINAL_ADMINISTRATION" and
            state["published"] is False and state["fresh_whole_package_reviews"] == 2,
            "wrong terminal administration stage")
    terminal = json.loads(files["publication/evidence/package_02/VERDICT.json"])
    adoption = json.loads(files["publication/evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json"])
    acceptance = json.loads(files["publication/evidence/FINAL_ACCEPTANCE.json"])
    require(terminal["status"] == "PASS_EXACT_SCOPED_MATHEMATICS_SOURCE_PREPRINT_PACKAGE" and
            terminal["findings"] == [] and terminal["severity_counts"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
            "terminal review not zero actionable")
    require(adoption["root_entire_report_and_verdict_read"] and adoption["mathematics_accepted_unchanged"] and
            adoption["status"] == "ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL",
            "root has not accepted terminal exact-candidate review")
    for name, field in (("REPORT.md", "report_sha256"), ("VERDICT.json", "verdict_sha256"),
                        ("OUTPUT_PINS.json", "output_pins_sha256")):
        require(hashlib.sha256(files["publication/evidence/package_02/" + name]).hexdigest() == adoption[field],
                "root accepted terminal record hash differs")
    require(acceptance["fresh_whole_package_reviews"] == 2 and acceptance["publication_ready"] is True and
            acceptance["published"] is False and acceptance["actionable_issues"] == [],
            "terminal acceptance stage differs")
    for row in acceptance["protected_mathematical_source_PDF_metadata"]:
        require(record(row["path"], files[row["path"]]) == row, "protected reviewed payload changed")''')
    edit(builder, '"stage": "repaired_application_note_pending_NEWwhole02",\n        "publication_ready": False,', '"stage": "final_zero_actionable_terminal_administration",\n        "publication_ready": True,\n        "published": False,\n        "publication_order_hold": "preceding PR1032 priority cursor; services blocked",')
    edit(builder, '"publication_ready": False,\n        "required_review": "NEWwhole02",', '"publication_ready": True,\n        "published": False,\n        "required_review": None,\n        "root_final_administrative_verification_pending": True,\n        "publication_order_hold": "preceding PR1032 priority cursor; services blocked",')
    allow_path = PUB / 'PACKAGE_ALLOWLIST.json'
    allow = json.loads(allow_path.read_text())
    added = [p.relative_to(AUDIT).as_posix() for p in PUB.rglob('*') if p.is_file() and ('before_terminal_admin_20261014' in p.parts or 'package_02' in p.parts or p.name in {'ROOT_WHOLE_PACKAGE_REVIEW_02.json','TERMINAL_REVIEW_02_COPY_MAP.json','TERMINAL_SOURCE_EXCLUSION_LEDGER.json','FINAL_ACCEPTANCE.json'})]
    allow['files'] = sorted(set(allow['files'] + added))
    allow['terminal_append'] = 'Only unchanged safe authored NEWwhole02/root records, historical pending administration receipts, and administrative acceptance/navigation. Existing suffix/hash/original/metadata controls are retained.'
    save(allow_path, allow)
    pin = json.loads((PUB / 'PACKAGE_INPUT_PINS.json').read_text())
    pin['files'] = [rec(AUDIT / n) for n in allow['files']]
    pin['terminal_admin_utc'] = NOW
    pin['stage'] = 'final_zero_actionable_terminal_administration'
    save(PUB / 'PACKAGE_INPUT_PINS.json', pin)

def administer_1037(root, verdict, copies):
    state_path = PUB / 'CURRENT_REVIEW_STATE.json'
    state = json.loads(state_path.read_text())
    state.update({'utc':NOW,'new_paper_and_package_review':'PASS_ZERO_ACTIONABLE_P0_P3_NEW_WHOLE_02','fresh_whole_review_assigned_by_preparer':False,'publication_ready':True,'published':False,'all_issues_resolved':True,'fresh_whole_package_reviews':2,'whole_review_02':{'record':'evidence/whole_20261014/package_02/VERDICT.json','status':verdict['status'],'issue_counts':verdict['issue_counts']},'root_terminal_adoption':'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json','final_acceptance':'evidence/FINAL_ACCEPTANCE.json','repair_01':'P3 release wording repair independently verified by NEWwhole02','publication_order_hold':'BLOCKED_FROM_SERVICES_PRECEDING_PR1032_PRIORITY_CURSOR','root_final_administrative_verification_pending':True,'submission_approved':False})
    save(state_path,state)
    hist_path = PUB / 'REVIEW_HISTORY.json'
    hist = json.loads(hist_path.read_text())
    hist['utc'] = NOW
    hist['stages'].append({'stage':'repaired_candidate_pending_whole02','records':'history/before_terminal_admin_20261014','reviewed_archive_sha256':verdict['candidate_zip_sha256'],'scope':'Frozen exact pending administration receipts before terminal append; original pending wording remains historical.'})
    hist['stages'].append({'stage':'whole_review_20261014_02','records':'evidence/whole_20261014/package_02','verdict':verdict['status'],'issue_counts':verdict['issue_counts'],'output_seal':'evidence/whole_20261014/package_02/OUTPUT_PIN.json','root_adoption':'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json','copy_map':'evidence/TERMINAL_REVIEW_02_COPY_MAP.json','scope':'Unchanged second fresh complete review; zero actionable findings; private/pinned omitted outputs remain omitted with individual reasons.'})
    hist['stages'].append({'stage':'terminal_administration_20261014','acceptance':'evidence/FINAL_ACCEPTANCE.json','publication_ready':True,'published':False,'root_final_administrative_verification_pending':True,'service_hold':'preceding PR1032 priority cursor'})
    hist['next_review'] = 'Terminal exact-candidate NEWwhole02 accepted; root final administrative verification pending; publication_ready=true, published=false; services blocked at preceding PR1032.'
    save(hist_path,hist)
    idx_path=PUB/'EVIDENCE_INDEX.json'
    idx=json.loads(idx_path.read_text());idx['utc']=NOW
    for c in copies:
        idx['entries'].append({k:c[k] for k in ('package_path','source_path','bytes','sha256','stage')})
    idx['terminal_omission_ledger']='evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json'
    save(idx_path,idx)
    with (PUB/'README.md').open('a') as out:
        out.write('\nTerminal administration, 14 October 2026: two fresh whole-package reviews are complete. The unchanged second report and verdict in `evidence/whole_20261014/package_02/` found zero actionable P0–P3 issues, and the root adopted the entire exact review. `evidence/FINAL_ACCEPTANCE.json` and `CURRENT_REVIEW_STATE.json` record publication readiness true and published false. Root final administrative verification is pending; publication services remain blocked by the preceding PR1032 priority cursor. `evidence/TERMINAL_REVIEW_02_COPY_MAP.json` pins every unchanged terminal copy and individually explains omitted sealed outputs. Reviewed paper source/PDF, all three metadata forms, original and existing copied evidence/checkers remain unchanged. Prior pending receipts are frozen in `history/before_terminal_admin_20261014/`.\n\nRun `python -B build_supportkit.py` from the clean extracted package root to regenerate the ZIP byte-for-byte. The builder requires the accepted zero-actionable terminal verdict, its exact root-adopted report/verdict/output seal and unchanged protected paper/metadata. Historical transfer comparator commands use ordinary Python; its assertion side effects make optimized `-O` replay unsupported. No optimized validity is claimed for that historical comparator.\n')
    with (PUB/'SUPPLEMENT.md').open('a') as out:
        out.write('\n## Terminal whole review and execution boundary\n\nThe second fresh complete review in `evidence/whole_20261014/package_02/REPORT.md` and `VERDICT.json` passed with zero actionable P0–P3 issues. The root adopted its whole report and exact output seal. The 14 October terminal acceptance is administrative: unchanged authored terminal copies and state/history/navigation were appended; the reviewed source/PDF/metadata and prior proofs/checkers/outputs remain byte-identical. Current readiness is true, published is false, root final administrative verification remains pending, and services are blocked by preceding PR1032. The copied seals preserve hashes for private/omitted inputs; `evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json` gives individual omission reasons.\n\nThe historical graph comparator uses an assertion with union side effects, so optimized Python removes necessary operations. Reproduction of that comparator is supported only by the documented ordinary Python commands. Review02 optimized evidence applies to its newly explicit checks and side-effect-free exterior operations, with the historical comparator excluded. This limitation is preserved; terminal administration does not change checker code or certify the unsupported optimized mode.\n')
    builder=PUB/'build_supportkit.py'
    edit(builder,"files=sorted((p for p in ROOT.rglob('*') if included(p)),key=lambda p:p.relative_to(ROOT).as_posix())",'''def require(ok, message):
    if not ok: raise RuntimeError(message)
state=json.loads((ROOT/'CURRENT_REVIEW_STATE.json').read_text())
terminal=json.loads((ROOT/'evidence/whole_20261014/package_02/VERDICT.json').read_text())
adoption=json.loads((ROOT/'evidence/root/ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text())
acceptance=json.loads((ROOT/'evidence/FINAL_ACCEPTANCE.json').read_text())
require(state['publication_ready'] is True and state['published'] is False and
        state['all_issues_resolved'] is True and state['fresh_whole_package_reviews']==2,
        'accepted terminal ready administration required')
require(terminal['status']=='PASS_ZERO_ACTIONABLE_P0_P3' and terminal['issues']==[] and
        terminal['issue_counts']=={'P0':0,'P1':0,'P2':0,'P3':0}, 'terminal actionable review findings')
require(adoption['root_entire_report_and_verdict_read'] and adoption['mathematics_accepted_unchanged'] and
        adoption['status']=='ADOPT_ZERO_ACTIONABLE_FINDINGS_PENDING_TERMINAL_ADMIN_SEAL',
        'root terminal exact-candidate acceptance required')
for name,field in (('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('OUTPUT_PIN.json','output_pins_sha256')):
    require(digest((ROOT/'evidence/whole_20261014/package_02'/name).read_bytes())==adoption[field],
            'root-adopted terminal review hash differs')
require(acceptance['fresh_whole_package_reviews']==2 and acceptance['publication_ready'] is True and
        acceptance['published'] is False and acceptance['actionable_issues']==[], 'terminal acceptance differs')
for row in acceptance['protected_mathematical_source_PDF_metadata']:
    p=ROOT/Path(row['path']).relative_to('preprint')
    if p.name=='zenodo-deposit.json' and not p.exists():
        continue  # Explicitly external sidecar; absent from a clean extracted kit.
    require(p.stat().st_size==row['bytes'] and digest(p.read_bytes())==row['sha256'],
            'protected reviewed paper/metadata differs')
metadata=json.loads((ROOT/'.zenodo.json').read_text())
require(json.loads((ROOT/'zenodo_metadata.json').read_text())=={'metadata':metadata}, 'metadata wrapper differs')
deposit=ROOT/'zenodo-deposit.json'
if deposit.exists():
    require(json.loads(deposit.read_text())=={'metadata':metadata,'files':[{'path':'paper/forest_transfer_catalan.pdf'},{'path':'pr1037_supportkit_v1.0.zip'}]}, 'external deposit metadata/file selection differs')
files=sorted((p for p in ROOT.rglob('*') if included(p)),key=lambda p:p.relative_to(ROOT).as_posix())''')
    edit(builder,"'review_state':'PENDING_NEW_WHOLE_02; publication_ready=false; all_issues_resolved=false; no publication approval'", "'review_state':'ACCEPTED_ZERO_ACTIONABLE_NEW_WHOLE_02; publication_ready=true; all_issues_resolved=true; published=false; root final administration verification pending; services blocked by preceding PR1032'")

def verify_final(before, copies):
    baseline = {r['path']:r for r in before}
    for name,r in baseline.items():
        if name not in MUTABLE:
            require(rec(AUDIT/name)==r,'protected pre-existing audit bytes changed: '+name)
    for c in copies:
        require((PUB/c['package_path']).read_bytes()==(AUDIT/c['source_path']).read_bytes(),'terminal copied bytes differ')
    if PR==1037:
        oldidx=json.loads((HERE/'frozen_before/preprint/EVIDENCE_INDEX.json').read_text())
        for r in oldidx['entries']:
            p=PUB/r['package_path'];q=AUDIT/r['source_path']
            require(p.read_bytes()==q.read_bytes() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'historical authored evidence copy differs')
    with zipfile.ZipFile(ARCHIVE) as z:
        names=z.namelist();require(names==sorted(set(names)) and len(names)==len({n.casefold() for n in names}),'zip order or duplicate')
        require(z.testzip() is None,'zip CRC')
        for info in z.infolist():
            n=info.filename;parts=PurePosixPath(n)
            require(n.isascii() and not parts.is_absolute() and '..' not in parts.parts and '\\' not in n and info.external_attr>>16==0o100644,'unsafe ZIP path/mode')
            p=(AUDIT if PR==1034 else PUB)/n
            require(z.read(n)==p.read_bytes(),'zip current file differs: '+n)
            require(not any(x.lower() in {'raw','rawprivate','private_raw','render','visual','.venv','clean_compile','clean_extraction','__pycache__','tmp'} for x in parts.parts),'private ZIP path')
            require(not n.endswith(('.zip','.png','.pyc')),'duplicate/private output ZIP member')
            if n.endswith(('.stderr','.stdout')):
                with zipfile.ZipFile(HERE/'frozen_before'/ARCHIVE.relative_to(AUDIT)) as oldzip:
                    require(n in oldzip.namelist() and z.read(n)==oldzip.read(n),
                            'new process stream cannot be appended to public ZIP')
            if p.suffix != '.pdf':
                text=p.read_text()
                if p.suffix=='.json':json.loads(text)
                if p.suffix=='.py':ast.parse(text)
        raw=io.BytesIO()
        with zipfile.ZipFile(raw,'w',compression=zipfile.ZIP_STORED if PR==1034 else zipfile.ZIP_DEFLATED,compresslevel=None if PR==1034 else 9) as independent:
            for n in names:
                info=zipfile.ZipInfo(n,(2026,10,13,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
                info.compress_type=zipfile.ZIP_STORED if PR==1034 else zipfile.ZIP_DEFLATED
                independent.writestr(info,((AUDIT if PR==1034 else PUB)/n).read_bytes(),compress_type=info.compress_type,compresslevel=None if PR==1034 else 9)
        require(raw.getvalue()==ARCHIVE.read_bytes(),'independent archive regeneration differs')
        extraction=HERE/'clean_extraction';extraction.mkdir()
        z.extractall(extraction)
    runroot=extraction/'publication' if PR==1034 else extraction
    builder='build_package.py' if PR==1034 else 'build_supportkit.py'
    command=[sys.executable,'-B',builder]
    result=subprocess.run(command,cwd=runroot,capture_output=True,text=True)
    (HERE/'CLEAN_BUILD.stdout').write_text(result.stdout);(HERE/'CLEAN_BUILD.stderr').write_text(result.stderr)
    require(result.returncode==0,'clean extracted documented builder fails: '+result.stderr)
    require((runroot/ARCHIVE.name).read_bytes()==ARCHIVE.read_bytes(),'clean extracted archive differs')
    manifest_name='PACKAGE_MANIFEST.json' if PR==1034 else 'MANIFEST.json'
    manifest=json.loads((PUB/manifest_name).read_text())
    for r in manifest['files']:
        require(rec((AUDIT if PR==1034 else PUB)/r['path'],AUDIT if PR==1034 else PUB)==r,'final manifest payload differs')
    linkcount=0
    for name in ['README.md','SUPPLEMENT.md']+(['evidence/INDEX.md'] if PR==1034 else []):
        p=PUB/name
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if not link.startswith(('https:','http:','#')):
                require((p.parent/link.split('#')[0]).exists(),'broken administrative link');linkcount+=1
    save(HERE/'FINAL_INTEGRITY.json',{'utc':NOW,'pr':PR,'status':'PASS_ADMINISTRATION_PENDING_PARENT_ADOPTION','archive':rec(ARCHIVE),'archive_members':len(names),'manifest_payloads':len(manifest['files']),'all_zip_CRC_safe_paths_modes_member_bytes':True,'independent_in_memory_regeneration_byte_exact':True,'documented_clean_extracted_builder':{'command':command,'cwd':runroot.relative_to(HERE).as_posix(),'exit_code':result.returncode,'byte_exact_archive':True},'protected_preexisting_files_checked':len(baseline)-len(MUTABLE),'all_historical_copies_unchanged':True,'terminal_unchanged_copies':len(copies),'modified_admin_links_verified':linkcount,'protected_source_PDF_metadata':[rec(AUDIT/x) for x in PROTECTED_NAMES],'metadata_and_deposit_bytes_unchanged':True,'compiler_run':False,'root_final_administrative_adoption_pending':True})
    save(HERE/'FINAL_SEAL.json',{'utc':NOW,'pr':PR,'status':'PROPOSED_FINAL_SEAL_PENDING_PARENT_ROOT_ADOPTION','publication_ready':True,'published':False,'fresh_whole_package_reviews':2,'actionable_issues':[],'mathematical_payload':[rec(AUDIT/x) for x in PROTECTED_NAMES],'archive':rec(ARCHIVE),'archive_members':len(names),'final_integrity':rec(HERE/'FINAL_INTEGRITY.json'),'postreview_changes':'Unchanged safe authored terminal review/root records and administrative acceptance/history/navigation/build stage only.','publication_order_hold':'BLOCKED FROM SERVICES BY PRECEDING PR1032 PRIORITY CURSOR','root_final_administrative_adoption_required':True})
    return len(names),len(manifest['files'])

def main():
    require(PR in {1034,1037},'bounded PR identity')
    if (HERE/'INPUT_PINS.json').exists():
        require(not (HERE/'OUTPUT_PINS.json').exists(),'completed terminal administration is sealed')
        before=json.loads((HERE/'INPUT_PINS.json').read_text())['files']
        mapping=json.loads((PUB/'evidence/TERMINAL_REVIEW_02_COPY_MAP.json').read_text())
        copies,exclusions=mapping['files'],mapping['omitted_outputs']
        with (HERE/'RESEARCH_LOG.md').open('a') as out:
            out.write(f'\n{datetime.datetime.now(datetime.timezone.utc).isoformat()}: 70%. First final integrity pass stopped because its process-stream guard wrongly rejected unchanged historical authored stdout/stderr already present in the reviewed PR1037 ZIP. Corrected this local administrative verifier to permit only exact old ZIP stream bytes; newly appended process streams remain excluded. No paper/checker/source-review byte changed.\n')
    else:
        root,verdict,rows,before=freeze()
        copies,exclusions=terminal_copies(rows)
        acceptance(root,verdict)
        if PR==1034:administer_1034(root,verdict,copies)
        else:administer_1037(root,verdict,copies)
    with (HERE/'RESEARCH_LOG.md').open('a') as out:
        out.write(f'\n{datetime.datetime.now(datetime.timezone.utc).isoformat()}: 65% of bounded terminal administration. Unchanged safe terminal records/root receipt copied and individually mapped exclusions written; pending history preserved; explicit zero-terminal-review builder gate installed. Reviewed paper/metadata and old checkers untouched.\n')
    builder=PUB/('build_package.py' if PR==1034 else 'build_supportkit.py')
    result=subprocess.run([sys.executable,'-B',str(builder)],capture_output=True,text=True)
    (HERE/'BUILD.stdout').write_text(result.stdout);(HERE/'BUILD.stderr').write_text(result.stderr)
    require(result.returncode==0,'terminal builder fails: '+result.stderr)
    members,payloads=verify_final(before,copies)
    timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (AUDIT/'RESEARCH_LOG.md').open('a') as out:
        out.write(f'\n{timestamp}: terminal administration checkpoint; 95% of local finalization (parent final verification/adoption remains). Two fresh exact whole reviews complete with zero actionable P0–P3. Unchanged terminal authored records/root receipt copied; historical pending receipts preserved; protected paper/PDF/metadata/originals/checkers/reviews unchanged. ZIP {sha(ARCHIVE)}, {members} entries / {payloads} manifest payloads, every CRC/member and independent plus clean extracted regeneration byte-exact. Ready=true, published=false, services BLOCKED by preceding PR1032 cursor. No compiler, Git/index/branch, remote/service or external-contact action. See finalization/terminal_admin_20261014/FINALIZATION_REPORT.md and proposed external FINAL_SEAL.json; parent root adoption pending.\n')
    with (HERE/'RESEARCH_LOG.md').open('a') as out:
        out.write(f'\n{timestamp}: 95% of local terminal finalization. All pre-existing nonwhitelisted bytes, historical copies, terminal copies, manifest payloads and ZIP members checked; independent reconstruction and documented clean extracted builder are byte-identical. Parent must inspect every modified admin/code file and protected math/metadata before adopting the proposed seal. Services held at PR1032.\n')
    after=inventory();before_map={r['path']:r for r in before};after_map={r['path']:r for r in after}
    changed=[{'path':n,'before':before_map[n],'after':after_map[n],'class':'administration or deterministic generated package only'} for n in sorted(before_map) if before_map[n]!=after_map[n]]
    require({r['path'] for r in changed}<=set(MUTABLE),'unwhitelisted mutation')
    added=[r for r in after if r['path'] not in before_map]
    require(all(r['path'].startswith(('publication/evidence/','preprint/evidence/','preprint/history/')) for r in added),'unexpected public append')
    save(HERE/'CHANGE_INVENTORY.json',{'utc':timestamp,'allowed_existing_mutations':MUTABLE,'changed_existing_files':changed,'added_audit_payload_files':added,'unchanged_existing_file_count':len(before)-len(changed),'new_finalization_artifacts_scope':'this folder only; not distributed; frozen ZIP/clean extraction outputs intentionally local','protected_paper_metadata':[rec(AUDIT/x) for x in PROTECTED_NAMES],'math_or_original_checker_or_source_report_changes':False})
    (HERE/'FINALIZATION_REPORT.md').write_text(f'''# PR{PR} terminal administrative finalization

Local administration passes, pending parent root verification and adoption. Two fresh whole-package reviews were already complete. The terminal exact-candidate review has zero actionable P0–P3 findings and its complete report/verdict/output seal were root-adopted before this work. This effort makes no new mathematical or source-review finding.

The final archive is `{ARCHIVE.relative_to(AUDIT)}`: SHA-256 `{sha(ARCHIVE)}`, {ARCHIVE.stat().st_size} bytes, {members} members and {payloads} manifest-hashed payloads. Readiness is true; published is false. **Publication services remain BLOCKED by preceding PR1032 priority cursor.** Parent final administrative verification/adoption is still required. The proposed `FINAL_SEAL.json` and `FINAL_INTEGRITY.json` live outside the distributed ZIP.

`INPUT_PINS.json` freezes every pre-existing regular audit file outside this new effort, including private/source/render/environment evidence. `FROZEN_BASELINE.json` defines the original archive, mathematical/PDF/metadata protection and mutation whitelist. Every existing nonwhitelisted byte was rehashed unchanged. `frozen_before/` preserves all prior mutable administrative records and the exact reviewed archive before mutation. Distributed `history/before_terminal_admin_20261014/` (under publication/evidence for PR1034) preserves old pending receipts/history without a duplicate ZIP. Historical pending flags, prior verdicts, source reports, omitted-input pin meanings and checkers remain exact.

{len(copies)} unchanged safe authored terminal/root records were copied; {len(exclusions)} sealed terminal outputs were individually omitted. The copied output manifest itself is unchanged and still lists omitted outputs honestly. The copy map and source exclusion ledger in the final evidence tree explain each omission. Private third-party bodies, full extracts, source images, renders, environments, process streams and duplicate archives remain excluded. Authored JSON source/custody pins may refer to excluded private bodies; inclusion of a pin record never promises inclusion of its referents.

The only permitted changes were unchanged terminal copies, readiness/acceptance/history/index/README/supplement administration, minimal explicit zero-terminal-review builder gates and regenerated allowlist/input pins/manifests/ZIP/integrity. `CHANGE_INVENTORY.json` gives every existing before/after hash and every appended file. The paper, TeX/PDF, bare/wrapped/deposit metadata, submitted originals, all previous proofs/checkers/copied outputs and source review records were not modified. Selected deposit PDF/ZIP filenames remain exact.

Every final manifest row and every ZIP CRC/name/mode/payload was checked against current disk bytes. A separate in-memory reconstruction reproduced all archive bytes. A fresh clean extraction executed the documented ordinary Python builder successfully and reproduced the identical archive. Metadata equality and protected byte checks passed. No compiler was run for the unchanged PDF. Administrative navigation links resolve. Terminal review source records were not rerun or reinterpreted as a new proof review.

PR1037 historical assertion-dependent graph comparator optimized execution remains unsupported; its documented normal Python commands and review02 optimized scope are unchanged. The finite optimized checks of review02 explicitly excluded that comparator; terminal readiness makes no optimized-comparator claim.

No Git/index/branch/remote, PR, release, tracker, Zenodo or other service action was performed. No individual was contacted and no outreach was prepared. Best-guess local finalization completion is 95%, with parent verification/adoption the remaining 5%; this is not a novelty or mathematical-discovery percentage.
''')
    outputs=[rec(p,HERE) for p in sorted(HERE.rglob('*')) if p.is_file() and not any(x in {'clean_extraction','frozen_before'} for x in p.relative_to(HERE).parts) and p.name!='OUTPUT_PINS.json']
    save(HERE/'OUTPUT_PINS.json',{'utc':timestamp,'self_excluded':True,'local_frozen_history_clean_extraction_separately_input_pinned_or_archive_verified':True,'files':outputs,'final_audit_payload_files':after,'strict_changed_file_inventory':'CHANGE_INVENTORY.json','no_late_writes_after_output_seal':True,'parent_root_adoption_pending':True})
    print(json.dumps({'pr':PR,'archive':rec(ARCHIVE),'members':members,'payloads':payloads,'terminal_copies':len(copies),'omissions':len(exclusions),'changed_existing':len(changed),'added':len(added),'status':'PASS_PENDING_PARENT_ROOT_ADOPTION'}))

if __name__=='__main__':main()
