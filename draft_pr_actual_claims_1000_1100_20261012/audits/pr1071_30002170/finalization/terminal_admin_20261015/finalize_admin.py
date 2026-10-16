#!/usr/bin/env python3
"""One bounded administrative reconciliation; not a mathematical review."""
import hashlib, io, json, shutil, sys, zipfile
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path

D = Path(__file__).resolve().parent
A = D.parents[1]
P = A / 'NEWpreprint_v1_0'
REPO = A.parents[2]
ARCHIVE = 'PR1071_preprint_v1_0_support.zip'
UTC = datetime.now(timezone.utc).isoformat()

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def record(path, relative):
    b = path.read_bytes()
    return {'path': str(relative), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def check(path, row):
    need(path.is_file() and not path.is_symlink(), 'Absent/nonregular: ' + str(path))
    b = path.read_bytes()
    need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], 'Identity mismatch: ' + str(path))

def main():
    need(not (D / 'BASELINE_INPUT_PINS.json').exists(), 'One-shot mutation already started; inspect before rerunning.')
    baseline = [record(f, f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D)]
    write(D / 'BASELINE_INPUT_PINS.json', {'utc': UTC, 'scope': 'All immediate regular audit inputs outside this new effort; hash only, before any candidate mutation.', 'records': baseline})
    (D / '.gitignore').write_text('_scratch/\n__pycache__/\n')
    (D / 'RESEARCH_LOG.md').write_text('# PR1071 terminal administrative reconciliation\n\n' + UTC + ': immediate inputs frozen before mutation. Administrative completion estimate 10%. Mathematical and whole-review work is already root-adopted; this task does not confer root release approval.\n')
    changed_names = ['README.md', 'SUPPLEMENT.md', 'scripts/verify_package.py', 'INPUT_COPY_MAP.json', 'PACKAGE_MANIFEST.json', ARCHIVE, ARCHIVE + '.sha256', 'UPLOAD_BINDINGS.json']
    for name in changed_names:
        dest = D / 'before' / 'NEWpreprint_v1_0' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(P / name, dest)
        need(dest.read_bytes() == (P / name).read_bytes(), 'Before copy not exact')
    write(D / 'AUTHORIZED_EXISTING_CHANGES.json', {'utc': UTC, 'records': [{'path': 'NEWpreprint_v1_0/' + n, 'before_bytes_path_relative_to_audit': str((D / 'before' / 'NEWpreprint_v1_0' / n).relative_to(A)), 'reason': 'Terminal review status/custody reconciliation and necessary deterministic dependencies only.'} for n in changed_names]})
    protected_names = ['paper.tex', 'paper.pdf', 'metadata.json', 'metadata_wrapped.json', 'deposit.json', 'checks/original_finite_checks.py', 'checks/original_expected.json', 'scripts/package_paths.py', 'scripts/check.py', 'scripts/build_pdf.py', 'scripts/build_archive.py', 'CITATION.txt', 'STATUS.json', 'CURRENT_STATUS.json', 'REPAIR_NOTES.md']
    write(D / 'CORE_PROTECTED_IDENTITIES.json', {'records': [record(P / n, 'NEWpreprint_v1_0/' + n) for n in protected_names] + [record(A / 'publication/zenodo-deposit.json', 'publication/zenodo-deposit.json')]})
    root_adoption = read(A / 'ROOT_WHOLE_PACKAGE_REVIEW_02.json')
    need(root_adoption['status'] == 'ADOPT_ZERO_ACTIONABLE_COMPLETE_WHOLE02_PENDING_TERMINAL_ADMIN' and root_adoption['actionable_P0_P1_P2_P3'] == 0 and root_adoption['full_whole_reviews_completed'] == 2, 'Root adoption prerequisite missing')
    oldmap = read(P / 'INPUT_COPY_MAP.json')
    need(len(oldmap['copies']) == 83, 'Expected 83 exact historical copy records')
    copies = list(oldmap['copies'])
    added = []
    def copy(source_relative, target_relative, source_snapshot=None, meaning='Exact safe authored evidence; historical statements retain their dated meanings.'):
        src = A / (source_snapshot or source_relative)
        dest = P / target_relative
        need(not dest.exists(), 'New custody target already exists: ' + target_relative)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        row = {'original_path': source_relative, 'package_copy': target_relative, 'bytes': src.stat().st_size, 'sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'byte_exact': True, 'meaning': meaning}
        if source_snapshot:
            row['source_snapshot'] = source_snapshot
        copies.append(row)
        added.append(target_relative)
    # Preserve every changed authored historical interface, with no old ZIP copy in distribution.
    for name in changed_names:
        if name in (ARCHIVE, ARCHIVE + '.sha256'):
            continue
        copy('NEWpreprint_v1_0/' + name, 'history/whole02_candidate/' + name,
             str((D / 'before' / 'NEWpreprint_v1_0' / name).relative_to(A)),
             'Exact whole02-reviewed before bytes. The former pending status and interfaces are inactive historical stages.')
    whole = A / 'reviews/package_02'
    whole_rows = read(whole / 'OUTPUT_PINS.json')['files']
    excluded = []
    for row in whole_rows:
        check(whole / row['path'], row)
        if row['path'] == '.gitignore' or row['path'].endswith(('_compile.stdout.txt', '_compile.stderr.txt')):
            excluded.append({**record(whole / row['path'], 'reviews/package_02/' + row['path']), 'reason': 'Raw compiler stream' if 'compile.' in row['path'] else 'Private scratch-selection configuration; no scientific or custody claim requires redistribution.'})
        else:
            copy('reviews/package_02/' + row['path'], 'custody/reviews/package_02/' + row['path'])
    for name in ['OUTPUT_PINS.json', 'SEAL.json']:
        copy('reviews/package_02/' + name, 'custody/reviews/package_02/' + name)
    for name in ['ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'ROOT_REPAIR_REVIEW_01.json']:
        copy(name, 'custody/' + name)
    for name in ['REPAIR_REPORT.md', 'OUTPUT_PINS.json', 'SEAL.json']:
        copy('repairs/package01/' + name, 'custody/repairs/package01/' + name)
    # All files in whole02 are accounted for individually; no bodies or private copies were silently selected.
    accounted = {r['original_path'] for r in copies if r['original_path'].startswith('reviews/package_02/')} | {r['path'] for r in excluded}
    for f in sorted(whole.rglob('*')):
        if f.is_file() and not f.is_symlink() and str(f.relative_to(A)) not in accounted:
            excluded.append({**record(f, f.relative_to(A)), 'reason': 'Unselected private/generated review input; not needed for the selected authored evidence.'})
    write(P / 'WHOLE02_COPY_EXCLUSIONS.json', {'utc': UTC, 'scope': 'Every unselected regular whole02 file individually identified. Full primary publication bodies, extracts, pixels, raw compiler streams and private scratch are not redistributed. Empty render directories have no file bytes to pin.', 'records': excluded})
    write(P / 'INPUT_COPY_MAP.json', {**oldmap, 'scope': oldmap['scope'] + '; terminal whole02/root/repair evidence and exact before-byte authored interfaces appended without changing any of the original 83 rows.', 'copies': copies})
    status = {'utc': UTC, 'state': 'READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032', 'pr': 1071, 'head': 'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f', 'fresh_whole_package_reviews_completed': 2, 'minimum_fresh_reviews_required': 2, 'latest_review': 'custody/reviews/package_02/VERDICT.json', 'root_review_adoption': 'custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json', 'latest_actionable_P0_P1_P2_P3': 0, 'root_terminal_adoption_required': True, 'publication_ready': False, 'issues_resolved': False, 'published': False, 'services_held_after_pr': 1032, 'meaning': 'The two-review mathematical/package loop is complete with zero actionable findings in whole02. This terminal administrative candidate requires root integrity adoption before root may set release readiness. Publication and PR disposition remain held in ascending order after PR1032. STATUS.json, CURRENT_STATUS.json and every older report/seal retain their exact dated historical meanings; no earlier status was rewritten.'}
    write(P / 'TERMINAL_STATUS.json', status)
    (P / 'FINAL_ACCEPTANCE.md').write_text('# Terminal review accounting, pending root integrity adoption\n\n' + UTC + '\n\nTwo NEW complete whole-package adversarial reviews have been completed (minimum two). Whole01 found three P3 support-interface defects; bounded repair addressed them; the independent complete whole02 found zero actionable P0, P1, P2 or P3 issues. The root adopted that full whole02 evidence in custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json. The unchanged analytic paper and source/priority boundaries remain those reviewed there.\n\nTERMINAL_STATUS.json is the current workflow record. Its state is READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032, with root terminal integrity adoption still required. The administrative worker does not set publication_ready or issues_resolved true. STATUS.json is the original preparation stage; CURRENT_STATUS.json and REPAIR_NOTES.md are the dated bounded-repair stage. Their old pending fields are preserved exactly, not live instructions to redo completed review. The external root seal after adoption governs subsequent readiness; no DOI, submission, tracker update or PR action has occurred here.\n\nThe entire paper.tex, seven-page paper.pdf, all three native bibliographic metadata objects, original finite checker, current citation and static path policy are unchanged. The verifier only adds explicit terminal accounting checks; no mathematical or bibliographic meaning changes. Historical theorem and method priority, full novelty and worldwide current-open status remain UNKNOWN. Extensive AI assistance; unrefereed and not formally certified.\n\nThe original 83 copy records retain their exact values and order. Added safe authored whole02/root/repair evidence and exact before-byte interface history are source-equal copies. WHOLE02_COPY_EXCLUSIONS.json accounts individually for omitted whole02 files. Source bodies, extracted full texts, images, raw compiler streams, private runtimes and previous archives are not redistributed. No omitted historical program is claimed newly replayed. The current uploader manifest is external publication/zenodo-deposit.json; its unchanged native metadata object selects the unchanged paper.pdf and the same-named current support ZIP.\n')
    readme = (P / 'README.md').read_text()
    readme = readme.replace('STATUS.json retains the dated original preparation state. CURRENT_STATUS.json records the repaired package: one fresh whole review completed, three P3 findings repaired, and a NEW complete whole02 review required; publication_ready=false and issues_resolved=false. Ascending service operations are held at PR1032.', 'STATUS.json retains the original preparation state, and CURRENT_STATUS.json retains the dated bounded-repair stage. TERMINAL_STATUS.json now records two completed NEW whole reviews (minimum two), latest zero actionable P0–P3 findings, and the root adoption of whole02. The terminal administrative state is READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032, pending root integrity adoption; publication_ready=false and issues_resolved=false until that adoption. Ascending service operations remain held after PR1032.')
    readme = readme.replace('superseded by CURRENT_STATUS.json for current workflow status.', 'superseded first by the dated CURRENT_STATUS.json repair stage and now by TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md for current workflow accounting.')
    readme += '\n## Terminal review accounting\n\nTwo NEW complete whole reviews are complete; the latest found zero actionable issues after the whole01 repairs. See FINAL_ACCEPTANCE.md, TERMINAL_STATUS.json and the exact whole02/root evidence in custody/. Root terminal integrity adoption remains required; this package is unpublished and ordered services remain held after PR1032. The external native uploader input is publication/zenodo-deposit.json in the audit tree; its metadata equals the three unchanged reviewed bibliographic objects and it selects this paper.pdf and same-named current support ZIP. The included deposit.json is a historical metadata wrapper, not the uploader command input. No mathematical/bibliographic content changed in this terminal reconciliation.\n'
    (P / 'README.md').write_text(readme)
    supp = (P / 'SUPPLEMENT.md').read_text()
    supp = supp.replace('Preparation status is dated, with publication_ready=false and issues_resolved=false until at least two fresh whole-package reviews are completed and their findings handled.', 'The original preparation status is retained as a dated stage. At least two fresh whole-package reviews were required; both are now completed and the latest has zero actionable findings. Publication readiness and issues-resolved flags remain false pending root terminal integrity adoption.')
    supp = supp.replace('Bounded package repair (14 October 2026 UTC): CURRENT_STATUS.json records one completed fresh whole review and the requirement for a NEW whole02 review.', 'Dated bounded package repair (14 October 2026 UTC): the unchanged historical CURRENT_STATUS.json records the then-one completed fresh whole review and then-required whole02. That full review is now complete; TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md govern current workflow accounting.')
    supp += '\nTerminal administrative reconciliation (15 October 2026 UTC): two NEW complete whole-package reviews completed, latest zero actionable P0–P3 findings and root whole02 adoption preserved exactly in custody/. The terminal state is READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032, requiring root terminal integrity adoption; no external service or publication has occurred here. All prior statuses/seals remain byte-exact history. Added safe authored review evidence and exact whole02 interface history extend the original 83 copy records without changing their order or values. The current mathematical manuscript/PDF, native metadata, checker and citation remain unchanged.\n'
    (P / 'SUPPLEMENT.md').write_text(supp)
    verifier = (P / 'scripts/verify_package.py').read_text()
    anchor = "    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:\n"
    need(verifier.count(anchor) == 1, 'Verifier insertion interface drift')
    addition = """    terminal=json.loads(safe_path(root,'TERMINAL_STATUS.json').read_text())
    require(terminal['state']=='READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032' and terminal['fresh_whole_package_reviews_completed']==2 and terminal['minimum_fresh_reviews_required']==2, 'Terminal review accounting drift.')
    require(terminal['latest_actionable_P0_P1_P2_P3']==0 and terminal['root_terminal_adoption_required'] is True, 'Terminal findings or root adoption requirement drift.')
    require(terminal['publication_ready'] is False and terminal['issues_resolved'] is False and terminal['published'] is False and terminal['services_held_after_pr']==1032, 'Administrative record cannot confer release or bypass ordered service hold.')
    whole=json.loads(safe_path(root,'custody/reviews/package_02/VERDICT.json').read_text())
    require(whole['review_round']==2 and whole['kind']=='NEW_COMPLETE_WHOLE_PACKAGE_ADVERSARIAL_REVIEW' and whole['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':0} and whole['findings']==[], 'Latest complete review is not zero actionable.')
    require(whole['whole_reviews_completed']==2 and whole['minimum_whole_reviews_required']==2 and whole['root_terminal_adoption_required'] is True and whole['service_hold_pr']==1032, 'Latest review accounting/hold drift.')
    adoption=json.loads(safe_path(root,'custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json').read_text())
    require(adoption['status']=='ADOPT_ZERO_ACTIONABLE_COMPLETE_WHOLE02_PENDING_TERMINAL_ADMIN' and adoption['full_whole_reviews_completed']==2 and adoption['minimum_whole_reviews']==2 and adoption['actionable_P0_P1_P2_P3']==0, 'Root full whole02 adoption missing.')
    require(adoption['output_pins_sha256']==sha(safe_path(root,'custody/reviews/package_02/OUTPUT_PINS.json')), 'Root adoption does not bind selected whole02 output seal.')
"""
    verifier = verifier.replace(anchor, addition + anchor)
    (P / 'scripts/verify_package.py').write_text(verifier)
    # Membership only extends the already reviewed explicit allowlist.
    old_manifest = read(D / 'before/NEWpreprint_v1_0/PACKAGE_MANIFEST.json')
    names = {r['path'] for r in old_manifest['members']} | set(added) | {'TERMINAL_STATUS.json', 'FINAL_ACCEPTANCE.md', 'WHOLE02_COPY_EXCLUSIONS.json'}
    members = [record(P / name, name) for name in sorted(names)]
    write(P / 'PACKAGE_MANIFEST.json', {**old_manifest, 'policy': old_manifest['policy'] + '; terminal administrative review accounting and selected safe whole02/root/repair evidence added; all old stages preserved exactly.', 'members': members})
    names = sorted(names | {'PACKAGE_MANIFEST.json'})
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_STORED, allowZip64=False) as z:
        for name in names:
            info = zipfile.ZipInfo(name, (2026, 10, 14, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            z.writestr(info, (P / name).read_bytes())
    (P / ARCHIVE).write_bytes(buf.getvalue())
    archive_row = record(P / ARCHIVE, ARCHIVE)
    (P / (ARCHIVE + '.sha256')).write_text(archive_row['sha256'] + '  ' + ARCHIVE + '\n')
    binding = read(D / 'before/NEWpreprint_v1_0/UPLOAD_BINDINGS.json')
    # Only archive and manifest identities change; the original PDF and all bibliographic bytes do not.
    binding['archive'] = {'filename': ARCHIVE, 'bytes': archive_row['bytes'], 'sha256': archive_row['sha256']}
    binding['manifest_sha256'] = record(P / 'PACKAGE_MANIFEST.json', '')['sha256']
    write(P / 'UPLOAD_BINDINGS.json', binding)
    write(D / 'BUILD_SUMMARY.json', {'utc': UTC, 'old_copy_records': 83, 'new_copy_records': len(copies) - 83, 'all_copy_records': len(copies), 'archive': archive_row, 'archive_members': len(names), 'independent_checks_and_root_adoption_still_required': True, 'no_paper_or_metadata_changes': True, 'excluded_whole02_files': len(excluded)})
    with (D / 'RESEARCH_LOG.md').open('a') as f:
        f.write('\n' + datetime.now(timezone.utc).isoformat() + ': bounded terminal candidate built; all original 83 map rows preserved. Administrative completion estimate 45%; actual clean replay and exhaustive stage reconciliation pending.\n')
    print(json.dumps(read(D / 'BUILD_SUMMARY.json'), indent=2))

if __name__ == '__main__':
    main()
