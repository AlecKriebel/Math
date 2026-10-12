"""ROOT's actual final-package adjudication; no upload or native acceptance."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A = Path(__file__).absolute().parent
R = A.parents[2]
P = A / 'publication_package_v1'
OUTPUT = A / 'ROOT_FINAL_PREPRINT_PACKAGE_ADJUDICATION_20261003.json'

def pin(p):
    assert p.is_file() and not p.is_symlink()
    assert all(not q.is_symlink() for q in p.parents)
    b = p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(), bytes=len(b),
                sha256=hashlib.sha256(b).hexdigest(),
                full_mode=stat.S_IMODE(p.stat().st_mode))

def main():
    assert __debug__ and not OUTPUT.exists()
    os.umask(0o022)
    expected = {
        'integer_endpoint_discontinuity.tex': (19942, '818f5ebb96328c2cdf418b05ff34bc5bbec5943ef508c798c715dc1fca4a7114'),
        'integer_endpoint_discontinuity.pdf': (86446, 'f900d86763266c73a5886df7edd194d275a25c31d55755c00716860d2e46e4a9'),
        'integer-endpoint-discontinuity-verification-v1.zip': (22965, '354b396f6ad7b1fd2463ef34b243536f1c4f0819577b67f206f13bdd133e59d8'),
        'verify_integer_endpoint.py': (8644, '0a89bfe9750a3c6d8d195efe12091398517d3758d4a94725f12157b1365ddadc'),
        'expected_results.json': (22181, 'eb5446be0eaeb50205e0651d12333a34c36c4c921ede9d71dfcbcf69c256c91f'),
        'VERIFICATION_RECORD.json': (2316, 'fcf2f991a83663bde841337a936633989fa01fcc8148d1132081f95e7580d268'),
    }
    files = []
    for name, (size, digest) in expected.items():
        z = pin(P / name)
        assert (z['bytes'], z['sha256']) == (size, digest)
        files.append(z)
    captures = []
    actual = [
        ('root_pr57_final_pdf_export_actual_capture', 4654),
        ('root_pr57_final_pdf_render_actual_capture', 5157),
        ('root_pr57_final_pdf_export_v2_actual_capture', 12500),
        ('root_pr57_final_pdf_render_v2_actual_capture', 13265),
        ('root_pr57_portable_verification_actual_capture', 13374),
        ('root_pr57_verification_zip_actual_capture', 13605),
        ('root_pr57_zenodo_local_check_v2_actual_capture', 20441),
    ]
    for name, pid in actual:
        d = A.parent / 'pr45_9900007' / name
        assert {p.name for p in d.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        c = json.loads((d / 'CAPTURE.json').read_bytes())
        assert c['actual_execution'] is True and c['completed'] is True
        assert c['pid'] == pid and c['exit_code'] == 0 and c['status'] == 'PASS'
        assert c['operator_unchanged'] is True
        assert pin(d / 'prelaunch_operator.py')['sha256'] == c['operator_sha256'] == 'c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
        for k in ('stdout', 'stderr'):
            z = pin(d / (k + '.bin'))
            assert z['bytes'] == c[k]['bytes'] and z['sha256'] == c[k]['sha256']
        captures.append(dict(capture=pin(d / 'CAPTURE.json'), actual_pid=pid,
                             members=[pin(p) for p in sorted(d.iterdir())]))
    review = A / 'preprint_round2_wholepackage_adversary'
    verdict = json.loads((review / 'VERDICT.json').read_bytes())
    assert verdict['verdict'] == 'NO_ESSENTIAL_ISSUES_FOUND'
    assert all(verdict[k] == [] for k in verdict if k.startswith('actionable_'))
    for name, z in verdict['artifacts'].items():
        assert expected[name] == (z['bytes'], z['sha256'])
    result = dict(
        schema='pr57-ROOT-final-preprint-package-adjudication/v1',
        utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_ROOT_writer_pid=os.getpid(),
        actual_ROOT_writer=pin(Path(__file__)), exact_publication_files=files,
        zenodo_manifest=pin(P / 'zenodo-deposit.json'), actual_ROOT_captures=captures,
        final_round2_report=pin(review / 'REPORT.md'), final_round2_verdict=pin(review / 'VERDICT.json'),
        round1_ROOT_adjudication=pin(A / 'ROOT_PREPRINT_ROUND1_ADJUDICATION_20261003.json'),
        strongest_verified_claim='For every fixed finite integer r>=0, normalized uniformization on the plane and sphere is discontinuous from ordinary C^r metrics to C^(r+1) maps, witnessed by smooth complete strictly positive-curvature metrics.',
        exact_limits=['No RP2 or smooth/noninteger topology result; no abstract-homeomorphism obstruction.',
                      'Classical endpoint mechanisms credited; selected primary-source priority audit is bounded, not exhaustive.',
                      '374 finite exact cases diagnose conventions; the universal written proof supplies all-r validity.',
                      'Extensive AI use; unrefereed, without human peer review or formal proof certification.'],
        ROOT_full_final_editorial_diff_and_portable_checker_read=True,
        ROOT_all_six_final_PDF_pages_personally_inspected=True,
        independent_round2_all_six_pages_personally_inspected=True,
        final_source_editorial_reversals_recover_immutable_mathematics=True,
        mathematical_audit_percent=100, bounded_priority_audit_percent=100,
        manuscript_and_verification_package_percent=100, independent_final_review_percent=100,
        preprint_package_ready_for_ordered_publication=True,
        pending='Complete preceding PRs in ascending program order before actual Zenodo publication and DOI tracker update.',
        native_acceptance_completed=False, actual_external_upload_performed=False,
        DOI=None, tracker_row=None,
        dated_handoff_absences_superseded_by_actual_assembly_captures=True,
        preserved_failures=['Initial local-check outer directory creation failed ENOSPC before child; retry20441 is the actual success.',
                            'First seven-page export retained in source_history; small bibliography layout repair yields current six-page PDF.'],
        derived_preview_cleanup='Only ROOT-generated v1 seven PNGs and v2 six PNGs were removed after page inspection; exact PDFs, source, results, archives, render captures and independent final six PNGs remain. Removal evidence is retained in actual tool transcripts; no mathematical evidence was deleted.')
    body = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    with OUTPUT.open('xb') as f:
        f.write(body); f.flush(); os.fsync(f.fileno())
    OUTPUT.chmod(0o444)
    assert OUTPUT.read_bytes() == body
    print(json.dumps(dict(status='PASS_ROOT_FINAL_PREPRINT_PACKAGE_READY_UNPUBLISHED', record=pin(OUTPUT), actual_pid=os.getpid())))

if __name__ == '__main__':
    main()
