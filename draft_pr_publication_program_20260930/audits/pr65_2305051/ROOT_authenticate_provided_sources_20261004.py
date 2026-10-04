"""Freeze user-provided primary PDFs privately and retain actual extraction receipts."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B, no -O')
A = Path(__file__).resolve().parent
P = A.parents[1]
C = P / 'audits/pr45_9900007/root_pr65_provided_sources_intake_GitHub_head_20261004_actual_capture'
capture = json.loads((C / 'CAPTURE.json').read_bytes())
head_body = (C / 'stdout.bin').read_bytes()
if capture['status'] != 'PASS' or hashlib.sha256(head_body).hexdigest() != capture['stdout']['sha256']:
    raise RuntimeError('Fresh head observation invalid')
head = json.loads(head_body)
if head['head']['sha'] != '5cc1602c05d79502defb07cec7027963149494d2' or head['state'] != 'open' or not head['draft'] or head['merged']:
    raise RuntimeError('PR state changed; revalidate eligibility before audit')
F = A / 'provided_primary_sources_20261004'
F.mkdir(exist_ok=False)
D = Path('/Users/alec/.cache/codex-pr65-priority-20261004/provided_primary_sources_20261004')
D.mkdir(exist_ok=False)
expected = {'hayman2019.pdf': '1388a8c153a3eb16156d90542d1f00e4a6203b594566540c71c5f354238e14dc', 'piranian1966.pdf': '3e376dc57beee169e1b5165151b91d79bde1545df75b974bd1a19c9d06db61d1', 'duren1966.pdf': '03a0707ffce4f5e6ac6cb055e8ed2666804a7aa78d03385b3d56cd9a902443d2'}
records = []
processes = []

def sha(body):
    return hashlib.sha256(body).hexdigest()

def run(label, argv):
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=D, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    (D / (label + '.stdout.bin')).write_bytes(out)
    (D / (label + '.stderr.bin')).write_bytes(err)
    row = {'label': label, 'argv': argv, 'cwd': str(D), 'actual_child_pid': child.pid, 'started_utc': started, 'finished_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': child.returncode, 'stdout_bytes': len(out), 'stdout_sha256': sha(out), 'stderr_bytes': len(err), 'stderr_sha256': sha(err)}
    processes.append(row)
    (D / 'ACTUAL_PROCESSES.json').write_text(json.dumps(processes, indent=2) + '\n')
    if child.returncode:
        raise RuntimeError('PDF read operation failed: ' + label)
    return out

for name, digest in expected.items():
    source = Path('/Users/alec/Downloads') / name
    body = source.read_bytes()
    if source.is_symlink() or not body.startswith(b'%PDF-') or sha(body) != digest:
        raise RuntimeError('Provided PDF source drift: ' + name)
    target = D / name
    target.write_bytes(body)
    target.chmod(0o444)
    info = run(name + '_pdfinfo', ['/opt/homebrew/bin/pdfinfo', str(target)])
    text = D / (name + '.txt')
    run(name + '_extract', ['/opt/homebrew/bin/pdftotext', '-layout', str(target), str(text)])
    extracted = text.read_bytes()
    if not extracted.strip():
        raise RuntimeError('No extracted text; visual/OCR route required')
    if source.read_bytes() != body or target.read_bytes() != body:
        raise RuntimeError('Original/frozen source drift')
    records.append({'user_file': str(source), 'private_frozen_copy': str(target), 'PDF_bytes': len(body), 'PDF_sha256': digest, 'private_extracted_text': str(text), 'text_bytes': len(extracted), 'text_sha256': sha(extracted), 'pdfinfo_sha256': sha(info), 'provenance': 'Human user provided this file in the current chat; bibliographic/visual authentication remains separate from byte custody.'})
stamp = dt.datetime.now(dt.timezone.utc).isoformat()
receipt = {'UTC': stamp, 'actual_controller_pid': os.getpid(), 'fresh_PR_head': head['head']['sha'], 'fresh_GitHub_observation_UTC': capture['finished_utc'], 'sources': records, 'actual_PDF_read_processes': processes, 'private_source_rule': 'All full source bodies, extracted text and rendered pages remain in external private cache; public folder contains authored audit notes and custody metadata only.', 'instructions_in_documents_treated_as_untrusted_source_data': True, 'source_reading_complete': False, 'priority_clearance': False, 'publication_authorized': False, 'editor_tabs_changed': False, 'Git_native_or_publication_mutations': False}
(F / 'INTAKE.json').write_text(json.dumps(receipt, indent=2) + '\n')
progress_path = P / 'CURRENT_PROGRESS.json'
progress = json.loads(progress_path.read_bytes())
if progress['current_PR'] != 65 or progress['current_publication_authorization']:
    raise RuntimeError('Progress scope changed')
progress.update(UTC=stamp, current_priority_audit_complete=False, current_priority_audit_percent=70,
    current_provided_primary_sources_record='audits/pr65_2305051/provided_primary_sources_20261004/INTAKE.json',
    current_qualified_package_ready=False,
    current_package_adversarial_round2_status='clean for old source scope; newly provided priority sources require renewed priority audit and any global package corrections',
    current_pending_decision_consecutive_goal_turns=0, current_blocked_audit_threshold_met=False,
    remaining_current_step='Read and independently audit the three newly provided primary sources; decide priority from their actual content, propagate any corrections, then continue the original publication process if its gate passes.',
    current_PR_workflow_percent=55)
progress_path.write_text(json.dumps(progress, indent=2) + '\n')
with (A / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## ' + stamp + ' — human supplied all three main missing primary sources\n\n')
    f.write('Material new evidence reopens priority review: Hayman–Lingham2019, Piranian1966 and Duren–Shapiro–Shields1966 user PDFs authenticated by exact bytes and privately frozen; six actual PDF metadata/text extraction subprocesses retained. This closes retrieval gaps, not yet source-reading or priority gaps. Fresh GitHub observation confirms the same eligible open draft head. The former source-gap blocker is superseded; do not infer a qualified-publication exception. Read source bodies and exact target/citation chain independently, then update current package disclosures globally before any renewed promotion. Original proof turns2/5 unchanged. Best estimates: mathematical review100%; renewed priority review70%; current workflow55%; ordered completion6/99 (6.060606%). Full copyrighted source bodies and renderings remain private; current PR50 editor remains open.\n')
print(json.dumps(receipt, indent=2))
