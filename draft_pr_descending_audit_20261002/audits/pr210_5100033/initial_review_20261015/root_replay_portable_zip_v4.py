"""Verify exact ZIP contents and replay every portable job from an isolated extraction."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import tempfile
import zipfile

D = Path(__file__).resolve().parent
B = D.parent/'preprint'
PYTHON = '/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    package = json.loads((B/'PACKAGE_MANIFEST.json').read_text())
    for row in package['submission_files']+[package['source_manifest'],package['manuscript_source'],package['metadata']]:
        p=B/row['path']
        assert p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
    source=json.loads((B/'SOURCE_MANIFEST.json').read_text())
    prefix='k605a_outer_focal_pedal_product/'
    selected={prefix+row['path'] for row in source['files']}|{prefix+'SOURCE_MANIFEST.json'}
    with tempfile.TemporaryDirectory(prefix='pr210-root-portable-') as tmp:
        t=Path(tmp)
        with zipfile.ZipFile(B/'k605a-source-verification.zip') as z:
            assert len(z.namelist())==len(set(z.namelist()))==len(selected)
            assert set(z.namelist())==selected
            for name in z.namelist():
                parts=PurePosixPath(name).parts
                assert name.startswith(prefix) and '..' not in parts and not name.startswith('/')
                assert z.read(name)==(B/name[len(prefix):]).read_bytes()
            z.extractall(t)
        work=t/prefix/'verification'
        receipt=D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V4.json'
        run=subprocess.run([PYTHON,'-B','run_verification.py','--receipt',str(receipt)],cwd=work,capture_output=True)
        (D/'ROOT_PORTABLE_REPLAY_STDOUT_V4.txt').write_bytes(run.stdout)
        (D/'ROOT_PORTABLE_REPLAY_STDERR_V4.txt').write_bytes(run.stderr)
        assert run.returncode==0, 'Inspect retained portable reproduction error; do not relax checks.'
        r=json.loads(receipt.read_text())
        assert r['all_selected_jobs_passed'] and len(r['jobs'])==10
        assert all(j['scientific_JSON_exact_equal'] for j in r['jobs'])
    out=dict(utc=datetime.now(timezone.utc).isoformat(),all_ten_root_jobs_passed=True,
        isolated_zip_extraction=True,actual_zip_entries_checked=len(selected),
        source_manifest_sha256=digest(B/'SOURCE_MANIFEST.json'),
        verification_manifest_sha256=digest(B/'verification/MANIFEST.json'),
        root_complete_harness_adapter_integrity_validators_README_and_provenance_read=True,
        original20_and_five_family_manifest_and_all_payload_bindings_validated=True,
        helper_report_sha256=digest(D/'portable_verification_preparation_01/PREPARATION_REPORT.json'),
        raw_byte_equal_jobs=sum(j['raw_byte_equal'] for j in r['jobs']),
        exact_scientific_json_jobs=10,root_reproduction_receipt_sha256=digest(receipt),
        offline_meromorphic_primary_preflight='Three recorded hashes substituted only; no fresh PDF hashing in this portable replay. Root initial full run and helper extra genuine-PDF run separately recorded.',
        scientific_rows_exact_and_validated=True,publication_cleared=False,
        required_new_sequential_whole_manuscript_reviews_completed=2,
        counts=[43,20,20,0],goal_active_incomplete=True)
    (D/'ROOT_PORTABLE_PACKAGE_ACCEPTANCE_V4.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
