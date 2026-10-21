#!/usr/bin/env python3
"""Validate and inventory this source-preparation snapshot; no service calls.

After a deliberate paper edit, --refresh-paper-binding updates its hash only.
Run run_checks.py again before resealing: old verification receipts are rejected.
This seal never certifies an unseen PDF/archive or whole-package review.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HISTORICAL_SHA = '2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393'


def require(value, message):
    if not value:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-paper-binding', action='store_true')
    args = parser.parse_args()
    binding_path = ROOT/'PROOF_BINDING.json'
    binding = json.loads(binding_path.read_text())
    require(digest(ROOT/binding['historical_proof_relative_path']) == HISTORICAL_SHA,
            'exact audited historical proof must be preserved')
    paper_sha = digest(ROOT/binding['paper_relative_path'])
    if args.refresh_paper_binding:
        binding['paper_sha256'] = paper_sha
        binding_path.write_text(json.dumps(binding, indent=2)+'\n')
        print(json.dumps({'paper_binding_refreshed':True, 'paper_sha256':paper_sha,
                          'next_step':'Run run_checks.py with a new retained receipt before sealing.'}))
        return
    require(binding['paper_sha256'] == paper_sha, 'current paper must match portable binding')
    require(binding['current_verifier_sha256'] == digest(ROOT/'verify_exact.py')
            and binding['current_runner_sha256'] == digest(ROOT/'run_checks.py'),
            'V2 source binding must identify the current verifier and runner')
    actual = json.loads((ROOT/'verification_results/actual_run_receipt.json').read_text())
    require(actual['all_pass'] and actual['intentional_controls_rejected'] == 12,
            'successful actual controls required')
    require(len(actual['verification_reports']) == 2, 'normal and optimized receipts required')
    require(all(r['paper_sha256'] == paper_sha
                and r['historical_proof_sha256'] == HISTORICAL_SHA
                and r['verifier_sha256'] == digest(ROOT/'verify_exact.py')
                for r in actual['verification_reports']), 'receipts must bind current note and verifier')
    require(actual['runner_sha256'] == digest(ROOT/'run_checks.py'), 'runner receipt must bind current runner')
    require(all(r['actual_exit'] == r['expected_exit'] for r in actual['actual_subprocesses']),
            'actual exits must match expected results')
    correction = json.loads((ROOT/'CORRECTION_LEDGER.json').read_text())
    require(correction['finding']['id'] == 'F01' and correction['source_repair_completed']
            and correction['current_verifier_sha256'] == digest(ROOT/'verify_exact.py'),
            'current correction ledger must bind the repaired F01 verifier')
    require(correction['actual_run_receipt_sha256']
            == digest(ROOT/'verification_results/actual_run_receipt.json'),
            'correction ledger must bind the actual current verification')
    meta = json.loads((ROOT/'intended_zenodo_metadata.json').read_text())['metadata']
    plan = json.loads((ROOT/'zenodo-deposit.json').read_text())
    require(plan['metadata'] == meta, 'metadata objects must be exactly identical')
    require(meta['publication_type'] == 'preprint' and meta['upload_type'] == 'publication',
            'narrow preprint deposit type')
    require(meta['creators'] == [{'name':'Kriebel, Alec','affiliation':'Independent researcher',
                                 'orcid':'0009-0001-9320-500X'}], 'author identity must be exact')
    excluded = {'SOURCE_PREPARATION_MANIFEST.json','SHA256SUMS','SEAL.json'}
    files = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in excluded:
            continue
        # This preparation inventory excludes any later PDF/archive/build file.
        if path.suffix not in ('.py','.tex','.md','.json','.txt'):
            continue
        require('private' not in path.parts and '.secrets' not in path.parts,
                'private custody or credentials cannot enter support')
        files.append({'relative_path':relative,'bytes':path.stat().st_size,'sha256':digest(path)})
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest = {'schema':'pr108-source-preparation-manifest/v1','UTC':utc,
                'actual_operator_PID':os.getpid(),'PR':108,'problem_id':30003996,
                'original_head':'3526d46bf143b08e5055ffa7728c6278e9f958ea',
                'review_hash':'9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d',
                'dataset_revision':'37e53eabe540fb458758e198be61634bd02ee008',
                'imported_prior_report':{},'source_folder':'publication_package_v2',
                'author_orcid':'https://orcid.org/0009-0001-9320-500X',
                'effective_proof_sha256':HISTORICAL_SHA,'paper_sha256':paper_sha,
                'original_effort':'2/5 from incoming QUEUE and prose; original structured ledger absent',
                'new_central_proof_search_turns':0,'source_preparation_completion_estimate_percent':100,
                'whole_package_review_completed':False,'publication_ready':False,
                'whole_package_R1_completed':True,'whole_package_R2_completed':False,
                'R1_F01_source_repair_completed':True,
                'correction_ledger_sha256':digest(ROOT/'CORRECTION_LEDGER.json'),
                'planned_upload_files':plan['files'],'planned_uploads_included_in_source_seal':False,
                'third_party_source_bodies_included':False,'files':files,
                'payload_total_bytes':sum(f['bytes'] for f in files),
                'scope':'Stable authored text/source preparation only; no unseen PDF or archive certification.'}
    manifest_path = ROOT/'SOURCE_PREPARATION_MANIFEST.json'
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    sums = [f['sha256']+'  '+f['relative_path'] for f in files]
    sums.append(digest(manifest_path)+'  SOURCE_PREPARATION_MANIFEST.json')
    (ROOT/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    seal = {'schema':'pr108-source-preparation-seal/v1','UTC':utc,'actual_operator_PID':os.getpid(),
            'source_preparation_completion_estimate_percent':100,'whole_package_review_completed':False,
            'publication_ready':False,'manifest_relative_path':'SOURCE_PREPARATION_MANIFEST.json',
            'manifest_bytes':manifest_path.stat().st_size,'manifest_sha256':digest(manifest_path),
            'checksums_relative_path':'SHA256SUMS','checksums_bytes':(ROOT/'SHA256SUMS').stat().st_size,
            'checksums_sha256':digest(ROOT/'SHA256SUMS'),'payload_files':len(files),
            'payload_bytes':manifest['payload_total_bytes'],
            'limitations':'R1 F01 repaired in V2; unchanged PDF passed R1. Outer V2 archive assembly and new fresh whole-package R2 remain for parent.'}
    (ROOT/'SEAL.json').write_text(json.dumps(seal, indent=2)+'\n')
    print(json.dumps(seal))


if __name__ == '__main__':
    main()
