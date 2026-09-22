"""Preserve and independently rehash a completed review extraction's evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import shutil

REVIEW = Path(__file__).resolve().parent
PROJECT = REVIEW.parent
EXTRACTION = REVIEW / 'extracted/qubit-povm-pvm-v2.0.0'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipts = list((EXTRACTION / 'reproduction_runs').glob('*/receipt.json'))
    assert len(receipts) == 1, 'Expected one fresh reproduction'
    outer = json.loads(receipts[0].read_text())
    assert outer['status'] == 'passed'
    kernel = outer['lean_receipt']['kernel_report']
    run = EXTRACTION / 'bell_lean' / outer['lean_receipt']['pointer']['directory']
    assert kernel == json.loads((run / 'kernel_report.json').read_text())
    assert sha(run / 'kernel_report.json') == outer['lean_receipt']['sha256']
    assert kernel['status'] == 'passed' and kernel['last_stage'] == 'complete'
    assert kernel['run_id'] == run.name
    assert kernel['formal_statement_contracts_passed']
    assert kernel['all_project_source_kernel_checked']
    assert outer['shipment_manifest_sha256'] == sha(EXTRACTION / 'SHA256SUMS.txt')
    for row in outer['commands']:
        assert row['exit_code'] == 0
        assert sha(EXTRACTION / row['log']) == row['log_sha256']
    for row in kernel['commands']:
        assert sha(EXTRACTION / 'bell_lean' / row['log']) == row['log_sha256']
        if row['exit_code']:
            assert Path(row['log']).name.endswith('-smoke-invalid.log')
    for rel, expected in kernel['source_snapshot'].items():
        assert sha(EXTRACTION / 'bell_lean' / rel) == expected
        assert sha(PROJECT / 'bell_lean' / rel) == expected
    audit = json.loads((run / 'axiom_audit.json').read_text())
    assert audit['run_id'] == run.name and audit['dependency_audit_passed']
    builds = [r for r in kernel['commands']
              if len(r['argv']) == 3 and r['argv'][:2] == ['lake', 'build']
              and r['argv'][2].startswith('Bell.')]
    contracts = json.loads((run / 'statement_audit.json').read_text())
    examples = sum(sum(1 for line in (EXTRACTION / 'bell_lean' / rel).read_text().splitlines()
                       if line.strip().startswith('example'))
                   for rel in contracts['all_contract_sources'])
    assert len(builds) == 68 and examples == 78
    assert len(audit['declarations']) == 826
    assert len(kernel['source_snapshot']) == 104
    destination = REVIEW / 'evidence/fresh_reproduction'
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(receipts[0].parent, destination / 'outer')
    (destination / 'lean').mkdir()
    for path in run.iterdir():
        if path.is_file():
            shutil.copy2(path, destination / 'lean' / path.name)
    summary = {
        'status': 'passed', 'checked_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'run_id': run.name, 'started_utc': outer['started_utc'],
        'ended_utc': outer['ended_utc'], 'production_modules': len(builds),
        'contract_examples': examples, 'public_axiom_reports': len(audit['declarations']),
        'protected_inputs_unchanged': len(kernel['source_snapshot']),
        'command_logs_rehashed': len(kernel['commands']),
        'shipment_files_checked': outer['shipment_files_checked'],
        'zip_sha256': sha(PROJECT / 'version2_completion_20260921/output/qubit-povm-pvm-v2.0.0.zip'),
        'outer_receipt_sha256': sha(receipts[0]),
        'kernel_report_sha256': sha(run / 'kernel_report.json'),
        'trust': 'Pinned compiler/runtime and provisioned compiled dependencies trusted; '
                 'all project modules rebuilt, Mathlib not independently rebuilt.'
    }
    (REVIEW / 'fresh_reproduction_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
