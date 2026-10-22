#!/usr/bin/env python3
"""One-shot bounded CASE-1071 support repair; no scientific content edits."""
import hashlib, json, shutil, sys, zipfile
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path

D = Path(__file__).resolve().parent
A = D.parents[1]
P = A / 'NEWpreprint_v1_0'
PROGRAM = A.parents[1]
ARCHIVE = 'PR1071_preprint_v1_0_support.zip'
CHANGED = ['README.md', 'SUPPLEMENT.md', 'scripts/package_paths.py',
           'scripts/verify_package.py', 'INPUT_COPY_MAP.json',
           'PACKAGE_MANIFEST.json', ARCHIVE, ARCHIVE + '.sha256',
           'UPLOAD_BINDINGS.json']

def now(): return datetime.now(timezone.utc).isoformat()
def need(ok, message):
    if not ok: raise RuntimeError(message)
def read(path): return json.loads(path.read_text())
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + '\n')
def pin(path, relative):
    b = path.read_bytes()
    return {'path': str(relative), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def log(message, percent):
    with (D / 'RESEARCH_LOG.md').open('a') as f:
        f.write('\n' + now() + ': ' + message + ' Bounded repair completion estimate ' + str(percent) + '%.\n')

def freeze():
    need(not (D / 'BASELINE_INPUT_PINS.json').exists(), 'Freeze already exists; inspect rather than overwrite.')
    rows = [pin(f, f.relative_to(A)) for f in sorted(A.rglob('*'))
            if f.is_file() and not f.is_symlink() and not f.is_relative_to(D)]
    write(D / 'BASELINE_INPUT_PINS.json', {'utc': now(), 'scope': 'Every pre-existing regular audit file outside this new effort; hash only before any mutation.', 'records': rows})
    (D / '.gitignore').write_text('_scratch/\n__pycache__/\n')
    (D / 'RESEARCH_LOG.md').write_text('# PR1071 physical case-alias support repair\n\n' + now() + ': Began bounded support-only repair. Exact target: physical samefile case aliases must not permit fresh outputs inside any frozen descendant. No mathematical, paper, citation, original checker or native metadata edit is authorized. Prior two whole reviews remain historical; new complete whole03 and root adoption are required. Readiness/issues-resolved/published false; services held after PR1032. Completion estimate 10%.\n')
    for name in CHANGED:
        dest = D / 'before' / 'NEWpreprint_v1_0' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(P / name, dest)
        need(dest.read_bytes() == (P / name).read_bytes(), 'Inexact before copy: ' + name)
    write(D / 'AUTHORIZED_EXISTING_CHANGES.json', {'utc': now(), 'records': [
        {'path': 'NEWpreprint_v1_0/' + name,
         'before_bytes_path_relative_to_audit': str((D / 'before' / 'NEWpreprint_v1_0' / name).relative_to(A)),
         'reason': 'Shared physical output ancestry guard, current support-hold accounting/custody, or necessary deterministic asset dependency.'}
        for name in CHANGED]})
    protected = ['paper.tex', 'paper.pdf', 'metadata.json', 'metadata_wrapped.json',
                 'deposit.json', 'CITATION.txt', 'checks/original_finite_checks.py',
                 'checks/original_expected.json', 'scripts/build_archive.py',
                 'scripts/build_pdf.py', 'scripts/check.py', 'STATUS.json',
                 'CURRENT_STATUS.json', 'TERMINAL_STATUS.json', 'FINAL_ACCEPTANCE.md',
                 'REPAIR_NOTES.md', 'FROZEN_INPUTS.json', 'INPUT_OUTPUT_PINS.json',
                 'FINAL_VERIFICATION.json', 'PREPARATION_REPORT.md']
    write(D / 'CORE_PROTECTED_IDENTITIES.json', {'records': [pin(P / name, 'NEWpreprint_v1_0/' + name) for name in protected] + [pin(A / name, name) for name in ['FINAL_SEAL.json', 'FINAL_INTEGRITY.json', 'publication/zenodo-deposit.json', 'publication/REPOSITORY_UPLOAD_INTERFACE.md', 'ROOT_WHOLE_PACKAGE_REVIEW_02.json']]})
    source_paths = ['ROOT_CASE_ALIAS_SCOPE_REVIEW.json', 'reviews/case_alias_scope_20261016/REPORT.md', 'reviews/case_alias_scope_20261016/OUTPUT_PINS.json', 'reviews/case_alias_scope_20261016/SEAL.json']
    write(D / 'PROGRAM_SOURCE_PINS.json', {'utc': now(), 'base': str(PROGRAM), 'scope': 'Read-only authored root/scope evidence; no unrelated package inspected.', 'records': [pin(PROGRAM / name, name) for name in source_paths]})
    write(D / 'PRIOR_ENOSPC_CONTEXT.json', {'utc': now(), 'scope': 'Existing failed-attempt context is preserved, never promoted to completed new checks.', 'prior_package_repair_failure': pin(A / 'repairs/package01/FAILED_ATTEMPT_01.json', 'repairs/package01/FAILED_ATTEMPT_01.json'), 'prior_package_repair_status': read(A / 'repairs/package01/FAILED_ATTEMPT_01.json'), 'scope_audit_context': 'The full scope REPORT records disk exhaustion, complete restoration of original command receipts and genuine final output creation. This is historical context; not a new repair execution.', 'current_attempt': 'No new controls have run at this checkpoint. Planned controls are not evidence.'})
    log('Hash-only baseline and exact before bytes saved for all nine permitted changes. All old seals and status files are protected as dated history.', 15)
    print(json.dumps({'baseline_files': len(rows), 'before_copies': len(CHANGED)}))

def mutate():
    need((D / 'BASELINE_INPUT_PINS.json').exists(), 'Freeze first')
    need(not (P / 'CASE_ALIAS_REPAIR_STATUS.json').exists(), 'Already mutated; inspect rather than repeat')
    for name in CHANGED:
        need((P / name).read_bytes() == (D / 'before' / 'NEWpreprint_v1_0' / name).read_bytes(), 'Changed before mutation: ' + name)
    stamp = now()
    source = (P / 'scripts/package_paths.py').read_text()
    start = source.index('def fresh_output(')
    source = source[:start] + '''def fresh_output(path, root=ROOT):
    """Return a preflighted absent file/directory; no mkdir or write occurs."""
    raw = Path(path)
    require('..' not in raw.parts, 'Parent traversal is not allowed in output paths.')
    target = Path(os.path.abspath(os.fspath(raw)))
    require(not target.exists() and not target.is_symlink(), 'Output must be new; existing files/directories, symlinks and hardlinks are rejected: ' + str(target))
    frozen = Path(root).resolve()
    require(not target.is_relative_to(frozen) and not target.resolve().is_relative_to(frozen), 'Output must be outside all frozen package descendants.')
    parent = target.parent
    # Inspect all existing ancestors even above absent intermediate directories.
    # samefile compares physical device/inode identity, including case aliases;
    # resolve() alone does not canonicalize case on a case-insensitive volume.
    for ancestor in (parent, *parent.parents):
        require(not ancestor.is_symlink(), 'Symlink output ancestor: ' + str(ancestor))
        if ancestor.exists():
            require(ancestor.is_dir(), 'Output ancestor is not a directory: ' + str(ancestor))
            require(not ancestor.samefile(frozen), 'Output must be outside all frozen package descendants.')
    require(parent.exists() and parent.is_dir(), 'Output parent must already exist: ' + str(parent))
    return target
'''
    (P / 'scripts/package_paths.py').write_text(source)
    # Prior current/terminal records are exact historical stages, still checked.
    verifier = (P / 'scripts/verify_package.py').read_text()
    anchor = "    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:\n"
    need(verifier.count(anchor) == 1, 'Verifier insertion anchor drift')
    addition = '''    repair=json.loads(safe_path(root,'CASE_ALIAS_REPAIR_STATUS.json').read_text())
    require(repair['state']=='PENDING_NEW_COMPLETE_WHOLE03_AFTER_CASE_ALIAS_REPAIR' and repair['pr']==1071 and repair['head']=='fc37aa5169a0fe6adae0a254c9ee6c1531a2911f', 'Current case-alias repair identity/state drift.')
    require(repair['fresh_whole_package_reviews_completed']==2 and repair['minimum_fresh_reviews_required']==2 and repair['new_complete_whole_review_required']==3 and repair['new_complete_whole_review_completed'] is False, 'New complete whole03 requirement/accounting drift.')
    require(repair['new_support_findings']=={'P0':0,'P1':0,'P2':0,'P3':1} and repair['bounded_repair_findings_fixed']==['CASE-1071'] and repair['prior_whole02_actionable_findings']==0, 'Dated review and new finding accounting drift.')
    require(repair['root_repair_adoption_required'] is True and repair['root_terminal_adoption_required'] is True, 'Current root adoption requirements drift.')
    require(repair['publication_ready'] is False and repair['issues_resolved'] is False and repair['published'] is False and repair['services_held_after_pr']==1032, 'Case-alias repair cannot confer readiness or bypass ordered hold.')
    require(repair['program_source_evidence']=='CASE_ALIAS_SOURCE_EVIDENCE.json', 'Missing new support finding provenance.')
    evidence=json.loads(safe_path(root,repair['program_source_evidence']).read_text())
    require(evidence['kind']=='SCOPED_AUTHORED_EXCERPTS_WITH_FULL_SOURCE_PINS' and evidence['finding']=='CASE-1071' and evidence['root_status']=='ROOT_ADOPT_THREE_NEW_UNPUBLISHED_SUPPORT_P3_FINDINGS_PENDING_BOUNDED_REPAIRS_AND_NEW_COMPLETE_WHOLE_REVIEWS', 'Case-alias evidence scope drift.')
'''
    (P / 'scripts/verify_package.py').write_text(verifier.replace(anchor, addition + anchor))
    root_evidence = read(PROGRAM / 'ROOT_CASE_ALIAS_SCOPE_REVIEW.json')
    report = (PROGRAM / 'reviews/case_alias_scope_20261016/REPORT.md').read_text()
    begin = report.index('### CASE-1071')
    end = report.index('### CASE-1085', begin)
    write(P / 'CASE_ALIAS_SOURCE_EVIDENCE.json', {'utc': stamp, 'kind': 'SCOPED_AUTHORED_EXCERPTS_WITH_FULL_SOURCE_PINS', 'finding': 'CASE-1071', 'scope': 'Only the exact CASE-1071 section and relevant root fields/actual PR1071 commands are excerpted; this is not a complete scope-audit copy or a new replay of old commands.', 'sources': read(D / 'PROGRAM_SOURCE_PINS.json')['records'], 'root_status': root_evidence['status'], 'root_utc': root_evidence['utc'], 'root_actual_pr1071_reproduction': [r for r in root_evidence['root_actual_reproduction'] if r['pr'] == 1071], 'root_mathematical_acceptance_unchanged': root_evidence['mathematical_acceptance_unchanged'], 'root_publication_ready_for_affected': root_evidence['publication_ready_for_affected'], 'root_services_held_after_pr': root_evidence['services_held_after_pr'], 'exact_report_section': report[begin:end], 'root_supersession': root_evidence['supersession']})
    status = {'utc': stamp, 'state': 'PENDING_NEW_COMPLETE_WHOLE03_AFTER_CASE_ALIAS_REPAIR', 'pr': 1071, 'head': 'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f', 'fresh_whole_package_reviews_completed': 2, 'minimum_fresh_reviews_required': 2, 'prior_whole02_actionable_findings': 0, 'new_support_findings': {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 1}, 'bounded_repair_findings_fixed': ['CASE-1071'], 'new_complete_whole_review_required': 3, 'new_complete_whole_review_completed': False, 'root_repair_adoption_required': True, 'root_terminal_adoption_required': True, 'publication_ready': False, 'issues_resolved': False, 'published': False, 'services_held_after_pr': 1032, 'program_source_evidence': 'CASE_ALIAS_SOURCE_EVIDENCE.json', 'meaning': 'Current bounded support repair of a new P3 after the two prior complete whole reviews. New complete whole03 and root adoption are required. All earlier statuses, verdicts, terminal/ROOT seals and findings retain exact dated historical meanings; the program support hold supersedes former readiness. No mathematical or bibliographic change or priority clearance is asserted.'}
    write(P / 'CASE_ALIAS_REPAIR_STATUS.json', status)
    (P / 'CASE_ALIAS_REPAIR_NOTES.md').write_text('# Current physical case-alias support repair\n\n' + stamp + '\n\nCASE-1071 is a new P3 output-location finding after two completed whole reviews (minimum two); historical whole02 had zero actionable findings. The shared fresh_output preflight now checks the physical identity of every existing output ancestor against the frozen root, including ancestors above absent intermediate directories and both case-spelling directions. It preserves absent destinations, existing real parents, lexical and resolved containment, no symlink ancestors, existing hardlink rejection and the new-empty-directory boundary for checker/compiler child files. Parent traversal components are rejected before normalization so a symlink cannot be hidden by lexical collapse. No case-folding heuristic is used. This remains a static local preflight without concurrent mutation guarantees.\n\nCASE_ALIAS_REPAIR_STATUS.json is the current workflow record: pending NEW complete whole03 and root repair/terminal adoption; publication_ready, issues_resolved and published false; ordered services held after PR1032. Earlier STATUS/CURRENT_STATUS/TERMINAL_STATUS/FINAL_ACCEPTANCE and external ROOT seals retain their exact historical bytes. The new program support hold supersedes former readiness. This bounded repair is not whole03 or publication approval.\n\nThe theorem, seven-page paper PDF/source, all native bibliographic metadata objects, original finite checker, citation and source credits remain unchanged. The all-H, all-T, all-n, both-grid, every-L2-estimator statement and its exclusions are those of the accepted paper. Brownian optimum and smooth rate are prior, Fourier/Gaussian antecedents are credited, full priority/novelty/open status UNKNOWN; no journal-error, firstness, human review or formal certification claim is added. No new actual paper compile, render or PDF marker is required or claimed here: unchanged whole02 already compiled both modes and viewed all seven pages.\n\nThe first 116 copy rows remain exact and ordered. New exact safe interface history and old root readiness/terminal evidence are appended; CASE_ALIAS_SOURCE_EVIDENCE.json is explicitly a scoped authored excerpt with full source pins. Every omitted prior ZIP/sidecar or unselected terminal/scope file is individually hash-accounted for. No third-party full source, extract, image, runtime or raw stream is added; no omitted historical program is claimed replayed. The external publication/zenodo-deposit.json stays native and byte-exact; included deposit.json remains a historical metadata wrapper.\n')
    oldmap = read(P / 'INPUT_COPY_MAP.json')
    need(len(oldmap['copies']) == 116, 'Expected original 116 map rows')
    copies = list(oldmap['copies']); added = []
    def copy(original, destination, snapshot=None):
        src = A / (snapshot or original); dst = P / destination
        need(not dst.exists(), 'New custody target exists: ' + destination)
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
        row = {'original_path': original, 'package_copy': destination, 'bytes': src.stat().st_size, 'sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'byte_exact': True, 'meaning': 'Exact authored historical bytes before CASE-1071 repair; earlier readiness/status claims retain their dated scope and are superseded by the current support hold.'}
        if snapshot: row['source_snapshot'] = snapshot
        copies.append(row); added.append(destination)
    for name in CHANGED:
        if name not in (ARCHIVE, ARCHIVE + '.sha256'):
            copy('NEWpreprint_v1_0/' + name, 'history/pre_case_alias01/' + name, str((D / 'before' / 'NEWpreprint_v1_0' / name).relative_to(A)))
    for name in ['FINAL_SEAL.json', 'FINAL_INTEGRITY.json']:
        copy(name, 'custody/pre_case_alias01/' + name)
    for name in ['REPORT.md', 'OUTPUT_PINS.json', 'SEAL.json']:
        copy('finalization/terminal_admin_20261015/' + name, 'custody/finalization/terminal_admin_20261015/' + name)
    exclusions = []
    selected = {r.get('source_snapshot', r['original_path']) for r in copies}
    for f in sorted((A / 'finalization/terminal_admin_20261015').rglob('*')):
        if f.is_file() and not f.is_symlink() and str(f.relative_to(A)) not in selected:
            exclusions.append({**pin(f, f.relative_to(A)), 'reason': 'Unselected exact terminal history: kept locally and hash-pinned; not redistributed or newly replayed.'})
    for name in [ARCHIVE, ARCHIVE + '.sha256']:
        f = D / 'before' / 'NEWpreprint_v1_0' / name
        exclusions.append({**pin(f, f.relative_to(A)), 'reason': 'Previous archive payload/sidecar retained exactly in local before custody; excluded from distribution.'})
    for r in read(D / 'PROGRAM_SOURCE_PINS.json')['records']:
        exclusions.append({**r, 'base': 'program_root', 'reason': 'Full authored program/scope source not redistributed; clearly scoped CASE-1071 excerpt and exact full-source pins are included.'})
    write(P / 'CASE_ALIAS_COPY_EXCLUSIONS.json', {'utc': stamp, 'scope': 'Every unselected terminal effort file, old archive/sidecar and selected full program/scope source is individually pinned. Existing whole01/whole02 exclusion ledgers remain unchanged. No third-party/source/raw/runtime bodies selected.', 'records': exclusions})
    write(P / 'INPUT_COPY_MAP.json', {**oldmap, 'scope': oldmap['scope'] + '; CASE-1071 exact pre-repair interface and dated terminal/root evidence appended after all original 116 unchanged ordered rows.', 'copies': copies})
    rm = (P / 'README.md').read_text()
    old = 'TERMINAL_STATUS.json now records two completed NEW whole reviews (minimum two), latest zero actionable P0–P3 findings, and the root adoption of whole02. The terminal administrative state is READY_FOR_SUBMISSION_UNPUBLISHED_HELD_AFTER_1032, pending root integrity adoption; publication_ready=false and issues_resolved=false until that adoption.'
    new = 'TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md preserve the dated two-review terminal stage and its historical whole02 zero-finding result. CASE_ALIAS_REPAIR_STATUS.json now governs current workflow: the new CASE-1071 P3 support defect is bounded-repaired, but a NEW complete whole03 review and root repair/terminal adoption are required. The program support hold supersedes former readiness; publication_ready=false, issues_resolved=false and published=false.'
    need(old in rm, 'README current-stage anchor drift'); rm = rm.replace(old, new)
    rm = rm.replace('Their parent must already exist and have no symlink ancestors.', 'Their parent must already exist and have no symlink ancestors. Physical existing-ancestor identity is checked against the frozen root, including case aliases and ancestors above absent intermediate directories. Parent-traversal (..) components are rejected before normalization.')
    rm = rm.replace('now by TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md for current workflow accounting.', 'then by the dated TERMINAL_STATUS.json/FINAL_ACCEPTANCE.md stage, and currently by CASE_ALIAS_REPAIR_STATUS.json for workflow accounting.')
    marker = '## Terminal review accounting\n'
    need(marker in rm, 'README terminal paragraph missing')
    rm = rm[:rm.index(marker)] + '## Current support hold and review accounting\n\nTwo prior NEW complete whole reviews are complete (minimum two); historical whole02 found zero actionable issues. A later program/root case-alias audit found the new CASE-1071 P3 support issue. This repair changes the shared output guard and accurate current accounting only. NEW complete whole03 and root repair/terminal adoption are required; this package remains unpublished with readiness/issues-resolved false and ordered services held after PR1032. Old terminal/ROOT seals remain exact dated history. See CASE_ALIAS_REPAIR_NOTES.md, CASE_ALIAS_REPAIR_STATUS.json and the explicitly scoped authored CASE_ALIAS_SOURCE_EVIDENCE.json.\n\nThe external native uploader input is publication/zenodo-deposit.json in the audit tree; its unchanged metadata equals the three unchanged reviewed bibliographic objects and it selects this unchanged paper.pdf and same-named repaired support ZIP. Included deposit.json remains a historical metadata wrapper. The first 116 exact copy-map rows remain unchanged and ordered; new before-byte authored history and individual omissions are recorded without old archive redistribution or claims of omitted historical replay. No mathematical/bibliographic content changed.\n'
    (P / 'README.md').write_text(rm)
    supp = (P / 'SUPPLEMENT.md').read_text()
    supp += '\nCurrent CASE-1071 support repair (' + stamp + '): the dated two-review terminal/ROOT readiness records are preserved as history. A new P3 physical case-alias output finding was then root-adopted; the bounded shared preflight repair now rejects physically internal case aliases in both spelling directions and above missing intermediate parents. It also rejects parent traversal before normalization. CASE_ALIAS_REPAIR_STATUS.json governs the current support hold: two prior complete whole reviews, minimum two, new complete whole03 plus root repair/terminal adoption required, readiness/issues-resolved/published false, services held after PR1032. No mathematical, paper/PDF, citation, native bibliographic object or original finite-checker change occurred. Exact before-byte history and individually pinned omissions preserve all prior custody, without a new compile/render/PDF marker or historical-program replay claim.\n'
    (P / 'SUPPLEMENT.md').write_text(supp)
    manifest = read(P / 'PACKAGE_MANIFEST.json')
    members = {r['path'] for r in manifest['members']}
    members.update(added + ['CASE_ALIAS_REPAIR_STATUS.json', 'CASE_ALIAS_REPAIR_NOTES.md', 'CASE_ALIAS_SOURCE_EVIDENCE.json', 'CASE_ALIAS_COPY_EXCLUSIONS.json'])
    manifest['policy'] += '; bounded CASE-1071 physical output-ancestry repair, separate current support hold, exact pre-repair history; all earlier 116 copy rows and dated verdicts/seals preserved.'
    manifest['members'] = [pin(P / name, name) for name in sorted(members)]
    write(P / 'PACKAGE_MANIFEST.json', manifest)
    # Necessary asset generation only; explicit names, no ambient glob selection.
    with zipfile.ZipFile(P / ARCHIVE, 'w', compression=zipfile.ZIP_STORED, allowZip64=False) as z:
        for name in sorted(members | {'PACKAGE_MANIFEST.json'}):
            i = zipfile.ZipInfo(name, date_time=(2026,10,14,0,0,0)); i.create_system=3; i.external_attr=0o100644<<16; i.compress_type=zipfile.ZIP_STORED
            z.writestr(i, (P / name).read_bytes())
    archive = pin(P / ARCHIVE, ARCHIVE)
    (P / (ARCHIVE + '.sha256')).write_text(archive['sha256'] + '  ' + ARCHIVE + '\n')
    binding = read(P / 'UPLOAD_BINDINGS.json')
    binding['archive']['bytes'] = archive['bytes']; binding['archive']['sha256'] = archive['sha256']
    binding['manifest_sha256'] = pin(P / 'PACKAGE_MANIFEST.json', '')['sha256']
    # No bibliographic/native-manifest or unrelated descriptive binding edit.
    write(P / 'UPLOAD_BINDINGS.json', binding)
    write(D / 'BUILD_SUMMARY.json', {'utc': now(), 'archive': archive, 'archive_members': len(members)+1, 'copy_rows': len(copies), 'original_116_rows_unchanged_ordered': copies[:116] == oldmap['copies'], 'added_exact_copies': added, 'individual_exclusions': len(exclusions)})
    log('Shared physical-ancestor guard and separate current support-hold record implemented. Rebuilt explicit deterministic archive/bindings. No controls are claimed yet.', 45)
    print(json.dumps(read(D / 'BUILD_SUMMARY.json'), indent=2))

if __name__ == '__main__':
    {'freeze': freeze, 'mutate': mutate}[sys.argv[1]]()
