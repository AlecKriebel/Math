#!/usr/bin/env python3
"""Fail-closed verifier for the sharp S_TC/W_TC JC boundary release."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'MANIFEST.sha256'
EXCLUDED={'MANIFEST.sha256','verification_output.txt','full_adversarial_verification_output.txt'}


def tracked_file(path):
    rel=path.relative_to(ROOT)
    return (
      path.is_file()
      and str(rel) not in EXCLUDED
      and '__pycache__' not in rel.parts
      and path.suffix!='.pyc'
      and not (rel.parts and rel.parts[0]=='review' and path.name.endswith('_output.txt'))
    )


def hash_file(path):
    h=sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def verify_manifest():
    expected={}
    for line in MANIFEST.read_text().splitlines():
        digest,relative=line.split('  ',1)
        assert relative not in expected
        expected[relative]=digest
    actual={str(path.relative_to(ROOT)):hash_file(path) for path in ROOT.rglob('*') if tracked_file(path)}
    assert set(actual)==set(expected),(sorted(set(actual)-set(expected)),sorted(set(expected)-set(actual)))
    assert actual==expected


def run(relative,needle,timeout=900,extra=()):
    print(f'[RUN] {relative}',flush=True)
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    process=subprocess.run(
      [sys.executable,str(ROOT/relative),*extra],cwd=ROOT,text=True,capture_output=True,
      timeout=timeout,env=env,
    )
    if process.returncode:
        print(process.stdout)
        print(process.stderr,file=sys.stderr)
        raise SystemExit(f'FAILED {relative}')
    assert needle in process.stdout,(relative,process.stdout[-2000:])
    print(f'[PASS] {relative}',flush=True)
    return process.stdout


def main():
    full_adversarial='--full-adversarial' in sys.argv[1:]
    unknown=[arg for arg in sys.argv[1:] if arg!='--full-adversarial']
    assert not unknown,unknown
    verify_manifest()

    # The two seven-port implementations are independent and can be replayed
    # concurrently.  The much larger cut review is hash-locked by default and
    # can be recomputed with --full-adversarial; its complete transcript and
    # certificate are already distributed in the manifest.
    jobs=(
      ('src/verify_seven_port_closure.py','"status": "PROVED"',900),
      ('review/review_seven_port_closure.py','"status": "VERIFIED"',900),
    )
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run,*job) for job in jobs]
        for future in futures:future.result()

    run('src/verify_frozen_nonroot_dependencies.py','"status": "VERIFIED"',300)
    run('src/verify_bounded_support_lift.py','"status": "PROVED"',300)
    run('src/verify_root_reduction.py','"status": "PROVED"',300)
    run('review/review_root_reduction.py','"status": "VERIFIED"',300)
    run('src/verify_frozen_cut_theorem.py','"status": "VERIFIED"',300)
    if full_adversarial:
        run('review/review_pointwise_cut.py','"status": "VERIFIED"',3600)
    else:
        cut_review=json.loads((ROOT/'certificates'/'pointwise_cut_adversarial_review.json').read_text())
        assert cut_review['status']=='VERIFIED'
        assert cut_review['distinct_factor_Bernstein_expansions_checked']==547
        assert cut_review['strict_wrong_split_minor_signs_checked']==421
        assert cut_review['two_active_endpoint_contradiction']=='VERIFIED'
        print('[PASS] hash-locked independent pointwise-cut adversarial replay',flush=True)
    run('src/verify_positive_gluing.py','"status": "PROVED"',300)
    run('src/verify_theta_sharpness.py','[PROVED] The inherited Theta pair',300)
    run('review/review_final_synthesis.py','"status": "VERIFIED"',300)
    run('src/build_sharp_boundary_certificate.py','"status": "PROVED"',300,('--check',))

    verify_manifest()

    theorem=json.loads((ROOT/'certificates'/'final_theorem.json').read_text())
    assert theorem['status']=='PROVED' and theorem['release_blockers']==[]
    assert all(theorem['assertions'].values())
    for dependency in theorem['dependencies'].values():
        assert hash_file(ROOT/dependency['path'])==dependency['sha256']

    seven=json.loads((ROOT/'certificates'/'seven_port_closure.json').read_text())
    assert seven['classification']['stochastic_disjointness']==192
    assert seven['classification']['lower_dimensional_or_one_sided_or_full_overlap']==0
    assert len(seven['completion_records'])==1686
    seven_review=json.loads((ROOT/'certificates'/'seven_port_adversarial_review.json').read_text())
    assert seven_review['universal_reduced_tensor_checks']=={'649':270,'705':216}

    final_review=json.loads((ROOT/'review'/'final_synthesis_review.json').read_text())
    assert final_review['status']=='VERIFIED' and not final_review['quarantined_dependency']
    report=(ROOT/'report'/'FINAL_SHARP_BOUNDARY_THEOREM.md').read_text()
    assert r'S_{\rm TC}\text{ is generically JC-identifiable modulo }T' in report
    assert r'W_{\rm TC}\text{ is not' in report
    assert 'UNRESOLVED' not in report and 'CONJECTURED' not in report and 'NUMERICALLY OBSERVED' not in report

    print(json.dumps({
      'status':'ALL EXACT CHECKS PASSED',
      'primary_theorem':'S_TC is generically JC-identifiable modulo T',
      'sharpness':'W_TC\\S_TC contains the all-n non-T Theta ambiguity',
      'seven_port_records_closed':192,
      'canonical_completed_targets_checked':1686,
      'universal_completion_tensor_checks':486,
      'pointwise_cut_Bernstein_factors_certified':547,
      'full_adversarial_replay':full_adversarial,
      'historical_gate_code_required':False,
      'quarantined_dependency':False,
    },indent=2,sort_keys=True))

if __name__=='__main__':main()
