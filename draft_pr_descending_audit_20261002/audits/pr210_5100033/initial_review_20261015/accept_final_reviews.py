"""Read-only evidence checks; writes only new root acceptance/probe-copy receipts."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib, json, zipfile, zlib, difflib

D=Path(__file__).resolve().parent
C=D.parent
B=C/'preprint'
P=C/'publication'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def save(p,x):
    with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
def seal(folder,expected):
    manifest=folder/'AUTHORED_MANIFEST.json'
    assert sha(manifest)==expected
    rows=load(manifest)['files']
    assert len({r['path'] for r in rows})==len(rows)
    for row in rows:
        p=folder/row['path']
        assert p.is_file() and not p.is_symlink()
        assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],str(p)
    return dict(manifest_sha256=sha(manifest),payloads=len(rows))

if __name__=='__main__':
    R=D/'whole_manuscript_adversary_03'
    sealed=seal(R,'2c2b5200baa6a43e4eec0fd8410ca11c959249b003562eedd1eecd2d9b0dbf50')
    authored=load(R/'FRESH_CONTROL_RESULTS.json')
    root=D/'root_reproduction/new_whole_manuscript_03'
    assert sha(root/'fresh_controls.py')==sha(R/'fresh_controls.py')
    replay=load(root/'FRESH_CONTROL_RESULTS.json')
    excluded=['utc_start','utc_end']
    a={k:v for k,v in authored.items() if k not in excluded}
    b={k:v for k,v in replay.items() if k not in excluded}
    assert canonical(a)==canonical(b)
    assert authored['exact_fixture']['zero_residuals']==80
    assert authored['finite_lattice']['primitive_pairs']==303
    assert authored['finite_lattice']['phase_cases']==10325
    assert authored['finite_lattice']['all_passed'] is True
    assert authored['universal_proof_from_finite_checks'] is False
    numeric=authored['numerical'];assert numeric['precision_digits']==115
    assert numeric['interval_certification'] is False and len(numeric['families'])==7
    for family in numeric['families']:
        assert family['phase_count']==3 and len(family['product_over_a4'])==3
        for value in family['max_normalized_errors'].values():
            d=Decimal(value);assert d.is_finite() and 0<=d<Decimal('1e-70')
        for row in family['complex_pole_rows']:
            assert row['row'] in [1,3]
            for key in ['residue_error','opposite_error','epsilon_squared_trace']:
                d=Decimal(row[key]);assert d.is_finite() and 0<=d<Decimal('1e-20')
        assert Decimal(family['wrong_cn_period_control'])==2
        span=Decimal(family['span'])
        assert span<Decimal('1e-70') if family['N']%2 else span>Decimal('1e-8')
    integrity=load(R/'PACKAGE_INTEGRITY_RECEIPT.json')
    for path,row in integrity['fixed_inputs'].items():
        p=B/path;assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    with zipfile.ZipFile(B/'k605a-source-verification.zip') as z:
        assert z.testzip() is None
        rows=integrity['zip_entries'];assert len(rows)==len(z.namelist())==181
        assert len(z.namelist())==len(set(z.namelist()))
        for row in rows:
            raw=z.read('k605a_outer_focal_pedal_product/'+row['path'])
            assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
            assert zlib.crc32(raw)==row['crc32']
            assert raw==(B/row['path']).read_bytes()
    sources=load(R/'SOURCE_AND_RELEASE_RECEIPT.json')
    for row in sources['sources']:
        p=Path(row['path']);assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    for row in sources['prior_whole_reviews_read_only_after_independent_freeze']:
        folder=D/row['family'];s=seal(folder,row['manifest_sha256'])
        assert s['payloads']==row['manifest_payloads'] and sha(folder/'REPORT.md')==row['report_sha256']
    qa=load(R/'VISUAL_QA_RECEIPT.json')
    for row in qa['pages']:
        p=Path(row['path']);assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
        assert row['actually_viewed_using_view_image'] is True and row['findings']==[]
    assert len(qa['pages'])==6 and qa['findings']==[]
    jobs=load(R/'PORTABLE_REPLAY_RECEIPT.json')['jobs']
    rootjobs=load(D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V4.json')['jobs']
    assert len(jobs)==len(rootjobs)==10
    assert {x['job']:x['scientific_canonical_sha256'] for x in jobs}=={x['job']:x['scientific_canonical_sha256'] for x in rootjobs}
    assert all(x['scientific_JSON_exact_equal'] is True for x in jobs)
    assert sum(x['raw_byte_equal'] is True for x in jobs)==8
    genuine=load(R/'GENUINE_PRIMARY_REPLAY_RECEIPT.json')['jobs']
    assert len(genuine)==1 and genuine[0]['attested_primary_hash_substitution_count']==0
    assert genuine[0]['scientific_JSON_exact_equal'] is True
    assert genuine[0]['scientific_canonical_sha256']==next(x['scientific_canonical_sha256'] for x in jobs if x['job']=='meromorphic_divisor')
    mutants=load(R/'HARNESS_MUTANT_RESULTS.json')
    assert mutants['count']==len(mutants['tests'])==28 and all(x['pass'] is True for x in mutants['tests'])
    final=load(R/'FINAL_INPUT_INTEGRITY.json')
    assert final['mandatory_findings']==final['optional_findings']==[]
    assert final['all_fixed_input_bytes_unchanged'] is True
    assert not (B/'FINAL_CLEARANCE.json').exists()
    save(D/'ROOT_REVIEW03_ACCEPTANCE.json',dict(
        utc=datetime.now(timezone.utc).isoformat(),case_completion_percent=85,
        whole_manuscript_reviews_completed=3,final_frozen_clean_reviews=1,
        reviewer_seal=sealed,report_sha256=sha(R/'REPORT.md'),
        full_report_and_programs_read=True,all_payloads_hash_verified=True,
        root_byte_identical_fresh_checker_reproduced=True,
        root_result_sha256=sha(root/'FRESH_CONTROL_RESULTS.json'),
        exact_scientific_comparison_exclusions=excluded,
        scientific_canonical_sha256=hashlib.sha256(canonical(a).encode()).hexdigest(),
        exact_fixture_zero_residuals=80,primitive_pairs=303,phase_cases=10325,
        fresh_families=7,fresh_phases=21,numerical_precision_digits=115,
        universal_proof_from_finite_checks=False,interval_certification=False,
        all_181_zip_crc_bytes_and_disk_pins_verified=True,
        all_16_current_source_hashes_verified=True,all_6_rendered_page_hashes_verified=True,
        ten_job_scientific_hashes_match_root_v4=True,genuine_three_primary_hash_substitutions=0,
        harness_mutants_passed=28,mandatory_findings=[],optional_findings=[],
        root_documentary_clarification='The reviewer source/release checker tested clearance absence at C and D rather than the actual B/FINAL_CLEARANCE.json path. Root directly checked the actual B path: absent before this acceptance. This corrects the limited checker-path observation; no scientific input, verdict, or reviewer payload is modified.',
        release_cleared_by_this_receipt=False))
    S=D/'release_helpers_adversary_03'
    seal(S,'a703e6b74255c85e7c0c7fab0bc210a4023620456f9ba5829893204b01f13f4a')
    O=D/'root_reproduction/release_helpers_review03_regression'
    O.mkdir()
    source=(S/'regression_workflow_probes.py').read_text()
    needle='D = OUT.parent\n';assert source.count(needle)==1
    adapted=source.replace(needle,'D = Path('+repr(str(D))+')\n')
    (O/'regression_workflow_probes.py').write_text(adapted)
    (O/'independent_transition_probes.py').write_bytes((S/'independent_transition_probes.py').read_bytes())
    save(O/'ROOT_ADAPTATION_RECEIPT.json',dict(
        utc=datetime.now(timezone.utc).isoformat(),purpose='Root rerun of all84 fully read supporting source03 controls in disposable local mocks; no genuine clearance or provider effects.',
        source_manifest_sha256=sha(S/'AUTHORED_MANIFEST.json'),
        unchanged_independent_program_sha256=sha(O/'independent_transition_probes.py'),
        original_regression_program_sha256=sha(S/'regression_workflow_probes.py'),
        adapted_regression_program_sha256=sha(O/'regression_workflow_probes.py'),
        exact_diff=''.join(difflib.unified_diff(source.splitlines(True),adapted.splitlines(True),fromfile='sealed_regression',tofile='root_layout_adaptation')),
        acceptance_guards_and_helper_bytes_unchanged=True))
    print('ROOT_REVIEW03_ACCEPTANCE written; all31 whole-review payloads and17 source-review payloads verified;84-control root replay copies prepared.')
