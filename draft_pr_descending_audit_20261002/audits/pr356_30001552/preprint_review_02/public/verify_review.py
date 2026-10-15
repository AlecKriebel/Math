"""Read-only reviewer02 inventories and retained evidence. Never runs mathematics."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import zipfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def record(path):
    require(path.is_file() and not path.is_symlink(), 'missing/linked file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mode': oct(path.stat().st_mode & 0o777)}


def load(path):
    return json.loads(path.read_text())


def files(root):
    found = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink: ' + str(p))
        if p.is_file():
            found.add(p.relative_to(root).as_posix())
    return found


def check_rows(root, rows):
    for n, pin in rows.items():
        relative = Path(n)
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe path')
        current = record(root / n)
        require(all(current[k] == v for k, v in pin.items()), 'pin mismatch: ' + n)


def evidence(root):
    src = load(root / 'source_first_gate.json')
    require(src['complete_contribution_read'] and src['all_four_pages_visually_inspected'], 'source read scope')
    require(not any(src['exposure_declaration'][k] for k in
                    ('candidate_tex_pdf', 'candidate_supplement', 'catalogue_metadata',
                     'prior_audits_or_controls', 'previous_fresh_reviewer_results')), 'source exposure')
    check_rows(root, {r['path']: {k: r[k] for k in ('bytes', 'sha256', 'mode')}
                      for r in src['artifacts']})
    freeze = load(root / 'analytic_freeze_gate.json')
    require(freeze['source_first_gate_sha256'] == record(root / 'source_first_gate.json')['sha256'], 'source/freeze bind')
    require(not freeze['zip_metadata_prior_audit_control_exposure'], 'analytic exposure')
    check_rows(root, {r['path']: {k: r[k] for k in ('bytes', 'sha256')} for r in freeze['pins']})
    require(datetime.fromisoformat(src['created_utc']) < datetime.fromisoformat(freeze['created_utc']), 'gate chronology')
    pkg = root / 'native_package/alternating-antimorphic-verification'
    z = zipfile.ZipFile(root / 'candidate/alternating-antimorphic-verification.zip')
    infos = z.infolist()
    require(len(infos) == 69 and len({i.filename for i in infos}) == 69, 'ZIP inventory')
    require(files(root / 'native_package') == {i.filename for i in infos}, 'extracted inventory')
    for info in infos:
        require((root / 'native_package' / info.filename).read_bytes() == z.read(info), 'ZIP member changed')
    for name in ('alternating-antimorphic-fine-wilf.tex', 'zenodo-deposit.json'):
        require((pkg / name).read_bytes() == (root / 'candidate' / name).read_bytes(), 'candidate/package identity')
    check_rows(pkg, load(pkg / 'MANIFEST.json')['files'])
    require(files(pkg) == set(load(pkg / 'MANIFEST.json')['files']) | {'MANIFEST.json'}, 'payload inventory')
    check_rows(pkg / 'submitted_problem', load(pkg / 'SOURCE_IDENTITY.json')['submitted_files'])
    pre = load(root / 'native_runs/preexecution.json')
    require(pre['assertions_enabled'] and pre['bytecode_disabled'], 'native execution convention')
    check_rows(root, pre['files'])
    compact = []
    for name in ('default', 'full', 'own'):
        before = load(root / 'native_runs' / (name + '.before.json'))
        after = load(root / 'native_runs' / (name + '.after.json'))
        require(before['files'] == pre['files'] == after['files_after'], 'native before/after inputs')
        require(before['preexecution_sha256'] == record(root / 'native_runs/preexecution.json')['sha256'], 'preexecution pin')
        require(before['argv'] == after['argv'] == pre['commands'][name], 'native command')
        require(datetime.fromisoformat(pre['utc']) <= datetime.fromisoformat(before['started_utc'])
                <= datetime.fromisoformat(after['finished_utc']), 'native timestamps')
        require(after['started_utc'] == before['started_utc'], 'native start time')
        require(after['exit_code'] == 0 and after['all_pre_pinned_bytes_unchanged'], 'native status')
        for channel in ('stdout', 'stderr'):
            path = root / 'native_runs' / (name + '.' + channel)
            require(all(record(path)[k] == v for k, v in after[channel].items()), 'whole native stream')
            require(path.read_bytes() == (root / 'expected_streams' / (name + '.' + channel)).read_bytes(), 'whole expected stream')
            require(after['whole_expected_' + channel + '_equal'], 'recorded stream equality')
        require((root / 'native_runs' / (name + '.stderr')).read_bytes() == b'', 'native stderr')
        require((root / 'public' / (name + '.stdout')).read_bytes() ==
                (root / 'native_runs' / (name + '.stdout')).read_bytes(), 'public/native stdout')
        compact.append({k: v for k, v in after.items() if k != 'files_after'})
    require([json.loads(s) for s in (root / 'native_capture_runner.stdout').read_text().splitlines()] == compact, 'whole runner stdout')
    require((root / 'native_capture_runner.stderr').read_bytes() == b'', 'runner stderr')
    require(load(root / 'public/execution_receipts.json')['runs'] == compact, 'public native metadata')
    require((root / 'own_controls.py').read_bytes() == (root / 'public/own_controls.py').read_bytes(), 'own public code')
    for name in ('source_only_baseline.md', 'independent_analytic_freeze.md'):
        require((root / name).read_bytes() == (root / 'public' / name).read_bytes(), 'public frozen prose')
    return {'source_artifacts': len(src['artifacts']), 'analytic_payloads': len(freeze['pins']),
            'zip_members': 69, 'native_runs': 3, 'preexecution_files': len(pre['files'])}


def external(root):
    rows = load(root / 'primary_source_pins.json')
    check_rows(Path('/'), {r['external_path'].lstrip('/'): {k: r[k] for k in ('bytes', 'sha256')} for r in rows})
    src = load(root / 'source_first_gate.json')
    original = Path(src['official_source_external_path'])
    require(record(original)['bytes'] == src['official_source_bytes'] and
            record(original)['sha256'] == src['official_source_sha256'], 'external original source')
    originals = load(root / 'original_candidate_fidelity.json')['original_files']
    for r in originals:
        require(all(record(Path(r['path']))[k] == r[k] for k in ('bytes', 'sha256')), 'external original candidate')
    parent = root.parent / 'preprint'
    for p in (root / 'candidate').iterdir():
        require(p.read_bytes() == (parent / p.name).read_bytes(), 'external released candidate4')
    pre = load(root / 'native_runs/preexecution.json')
    require(all(record(Path(pre['interpreter_path']))[k] == v for k, v in pre['interpreter'].items()), 'external interpreter')
    return len(rows) + 1 + len(originals) + 4 + 1


def main():
    require(__debug__, 'assertions must be enabled')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument('--mode', choices=('full', 'public'), default='full')
    ap.add_argument('--proposal', type=Path, help='Explicit unsealed review plan, before final manifests exist')
    ap.add_argument('--include-external-sources', action='store_true', help='Hash cached primary PDFs, original candidate files and interpreter; no acquisition')
    args = ap.parse_args()
    require(not (args.mode == 'public' and args.include_external_sources), 'external check requires full mode')
    root = args.root.resolve()
    final_names = {'PUBLIC_MANIFEST.json', 'PRIVATE_MANIFEST.json', 'CLOSURE_SEAL.json'}
    if args.proposal:
        proposal = load(args.proposal)
        rows = proposal['files']
        expected = set(rows) | {'closure_plan.json'}
        require(not (files(root) & final_names), 'proposal used after seal')
        state = 'UNSEALED_PROPOSAL'
        allowlist = set(proposal['terminal_capture_allowlist'])
    else:
        seal = load(root / 'CLOSURE_SEAL.json')
        require(seal['status'] == 'SEALED_ONCE', 'seal status')
        for name, digest in seal['manifest_sha256'].items():
            if args.mode == 'full' or name == 'PUBLIC_MANIFEST.json':
                require(record(root / name)['sha256'] == digest, 'manifest seal binding')
        public = load(root / 'PUBLIC_MANIFEST.json')['files']
        private = load(root / 'PRIVATE_MANIFEST.json')['files'] if args.mode == 'full' else {}
        rows = dict(private, **public)
        expected = set(rows) | final_names
        allowlist = set(seal['terminal_capture_allowlist'])
        if args.mode == 'full':
            require(record(root / 'closure_plan.json')['sha256'] == seal['closure_plan_sha256'], 'closure plan seal')
            plan = load(root / 'closure_plan.json')
            check_rows(root, {n: r for n, r in plan['files'].items() if n != 'research_log.md'})
            log = (root / 'research_log.md').read_bytes()
            appended = seal['research_log_append'].encode()
            require(log.endswith(appended), 'final log append')
            prefix = log[:-len(appended)]
            old_log = seal['research_log_before']
            require(len(prefix) == old_log['bytes'] and hashlib.sha256(prefix).hexdigest() == old_log['sha256'], 'old log preserved')
            require(old_log == plan['files']['research_log.md'] and record(root / 'research_log.md')['mode'] == old_log['mode'], 'old log mode/pin')
            require(record(root / 'source_first_gate.json')['sha256'] == seal['source_first_gate_sha256'], 'source seal bind')
            require(record(root / 'analytic_freeze_gate.json')['sha256'] == seal['analytic_freeze_gate_sha256'], 'analytic seal bind')
            check_rows(root / 'candidate', seal['candidate4'])
            check_rows(root, seal['terminal_capture_files'])
            before_rows = dict(plan['files'], **{'closure_plan.json': record(root / 'closure_plan.json')})
            before_sha = hashlib.sha256(json.dumps(before_rows, sort_keys=True).encode()).hexdigest()
            for mode in ('full', 'public'):
                cap = root / 'terminal_verifier'
                receipt = load(cap / (mode + '.receipt.json'))
                require(receipt['exit_code'] == 0 and receipt['namespace_payload_unchanged'], 'terminal native status')
                require(receipt['proposal_sha256'] == seal['closure_plan_sha256'], 'terminal plan pin')
                require(receipt['verifier_sha256'] == record(root / 'public/verify_review.py')['sha256'], 'terminal program pin')
                require(receipt['payload_before_sha256'] == before_sha, 'terminal entire preinventory pin')
                for channel in ('stdout', 'stderr'):
                    p = cap / (mode + '.' + channel)
                    require(all(record(p)[k] == v for k, v in receipt[channel].items()), 'terminal whole stream pin')
                    require(p.read_bytes() == (root / 'terminal_expected' / (mode + '.' + channel)).read_bytes(), 'terminal expected whole stream')
        state = 'SEALED_ONCE'
    if args.mode == 'full':
        require(files(root) - allowlist == expected, 'exact full inventory')
        check_rows(root, rows)
        detail = evidence(root)
    else:
        public_rows = {n: r for n, r in rows.items() if n.startswith('public/')}
        require(files(root / 'public') == {n.removeprefix('public/') for n in public_rows}, 'exact public inventory')
        check_rows(root, public_rows)
        detail = {'public_payload_files': len(public_rows)}
        receipts = load(root / 'public/execution_receipts.json')
        for row in receipts['runs']:
            pin = record(root / 'public' / (row['name'] + '.stdout'))
            require(all(pin[k] == v for k, v in row['stdout'].items()), 'public whole stream pin')
            require(row['exit_code'] == 0 and row['stderr']['bytes'] == 0, 'public recorded status')
        require(record(root / 'public/own_controls.py')['sha256'] == receipts['own_program_sha256'], 'public own code receipt')
    external_count = external(root) if args.include_external_sources else 0
    print(json.dumps({'status': 'PASS', 'mode': args.mode, 'state': state,
                      'saved_evidence': detail, 'external_bindings': external_count,
                      'filesystem_writes': False, 'mathematics_rerun': False,
                      'install_or_network': False,
                      'limitations': ['Inventory hashes do not certify global novelty, external human peer review, or independently authenticate past source acquisition.',
                                      'Public mode omits private source, candidate4/ZIP-member, preexecution/interpreter and stderr/input provenance bindings.',
                                      'Without --include-external-sources no current external source/candidate/interpreter body binding is asserted.']}, indent=2))


if __name__ == '__main__':
    main()
